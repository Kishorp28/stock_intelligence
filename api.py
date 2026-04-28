from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import math
import os

from ml_engine.model_trainer import predict_stocks
from ml_engine.recommender import get_recommendations
from ml_engine.data_collector import fetch_company_news
from ml_engine.preprocessor import analyze_sentiment

app = FastAPI(title="Intelligent Stock Recommendation API")

# Allow CORS strictly for Vercel production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stock-intelligence-ten.vercel.app",
        "https://stock-intelligence-eh7t.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Stock Recommendation API Running"}

DATA_FILE = "latest_stock_data.csv"

class UserPreferences(BaseModel):
    investment_type: str = "Long-term (1+ Years)"
    risk_level: str = "Medium"
    investment_amount: float = 100000.0
    preferred_sector: str = "All"
    expected_return: float = 15.0
    dividend_preference: bool = False
    market_cap_preference: str = "Any"

def clean_df_for_json(df):
    """Clean NaN and Inf values to standard format so they can be JSON serialized."""
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0).replace([np.inf, -np.inf], 0)
        else:
            df[col] = df[col].fillna("Unknown")
    return df

@app.get("/api/market-data")
def get_market_data():
    """Return an overview of the loaded global universe data."""
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="Data pipeline has not been executed yet.")
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        raise HTTPException(status_code=404, detail="No data available.")
        
    df = clean_df_for_json(df)
    
    # Return fundamental distributions for the charts
    records = df[['symbol', 'company_name', 'sector', 'industry', 'market_cap', 'rsi_14', 'macd', 'Close']].to_dict(orient="records")
    return {"status": "success", "total_records": len(df), "data": records}

@app.post("/api/recommend")
def recommend_stocks(prefs: UserPreferences):
    """Run model inference and match with user constraints."""
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="Data pipeline has not been executed yet.")
        
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        raise HTTPException(status_code=404, detail="No data available.")
        
    # Base predictive payload
    predicted_df = predict_stocks(df, model_type='rf')
    
    constraints = {
        'preferred_sector': prefs.preferred_sector,
        'market_cap_preference': prefs.market_cap_preference,
        'dividend_preference': prefs.dividend_preference,
        'risk_level': prefs.risk_level
    }
    
    # Filter with rules
    recs_df = get_recommendations(constraints, predicted_df)
    recs_df = clean_df_for_json(recs_df)
    
    if recs_df.empty:
        # Fallback empty logic
        fallback_df = get_recommendations({'preferred_sector': 'All', 'market_cap_preference': 'Any', 'dividend_preference': False, 'risk_level': 'Medium'}, predicted_df)
        fallback_df = clean_df_for_json(fallback_df)
        return {
            "status": "partial",
            "message": "No stocks match your exact criteria. Showing algorithm baselines.",
            "recommendations": fallback_df.to_dict(orient="records") if not fallback_df.empty else []
        }
        
    return {
        "status": "success",
        "message": f"Found {len(recs_df)} high-conviction matches.",
        "recommendations": recs_df.to_dict(orient="records")
    }

import yfinance as yf
@app.get("/api/history/{symbol}")
def get_stock_history(symbol: str):
    try:
        hist = yf.download(symbol, period="3mo", progress=False)
        if isinstance(hist.columns, pd.MultiIndex):
            hist = hist.xs(symbol, axis=1, level=1)
        if hist.empty:
            raise HTTPException(status_code=404, detail="No historical data found.")
        hist['SMA20'] = hist['Close'].rolling(window=20).mean()
        hist = hist.fillna(0)
        return {
            "dates": hist.index.strftime('%Y-%m-%d').tolist(),
            "open": hist['Open'].tolist(),
            "high": hist['High'].tolist(),
            "low": hist['Low'].tolist(),
            "close": hist['Close'].tolist(),
            "sma20": hist['SMA20'].tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news/{symbol}")
def get_stock_news(symbol: str):
    df = pd.read_csv(DATA_FILE)
    company_row = df[df['symbol'] == symbol]
    company_name = symbol.replace('.NS', '') if company_row.empty else str(company_row['company_name'].iloc[0])
    
    articles = fetch_company_news(company_name)
    if not articles:
        articles = fetch_company_news(symbol.replace('.NS', ''))
        
    sentiment = analyze_sentiment(articles) if articles else 0.0
    return {
        "status": "success",
        "symbol": symbol,
        "articles": articles,
        "sentiment_score": sentiment,
        "sentiment_label": "Bullish" if sentiment > 0.1 else ("Bearish" if sentiment < -0.1 else "Neutral")
    }

class BacktestPayload(BaseModel):
    symbols: list[str]
    initial_capital: float = 100000.0

@app.post("/api/backtest")
def run_portfolio_backtest(payload: BacktestPayload):
    try:
        if not payload.symbols:
            raise HTTPException(status_code=400, detail="No symbols provided")
            
        all_symbols = payload.symbols + ['^NSEI']
        data = yf.download(all_symbols, period="6mo", progress=False)['Close']
        if isinstance(data, pd.Series):
            data = data.to_frame(name=all_symbols[0])
            
        data = data.ffill().fillna(0)
        returns = data.pct_change().fillna(0)
        
        bench_str = '^NSEI' if '^NSEI' in returns.columns else returns.columns[-1]
        bench_growth = (1 + returns[bench_str]).cumprod() * payload.initial_capital
        
        valid_symbols = [s for s in payload.symbols if s in returns.columns]
        if valid_symbols:
            port_returns = returns[valid_symbols].mean(axis=1)
        else:
            port_returns = returns[bench_str] * 0
            
        port_growth = (1 + port_returns).cumprod() * payload.initial_capital
        dates = data.index.strftime('%Y-%m-%d').tolist()
        
        return {
            "status": "success",
            "dates": dates,
            "portfolio_value": port_growth.tolist(),
            "benchmark_value": bench_growth.tolist(),
            "total_return_pct": float(((port_growth.iloc[-1] - payload.initial_capital) / payload.initial_capital) * 100) if len(port_growth) > 0 else 0,
            "benchmark_return_pct": float(((bench_growth.iloc[-1] - payload.initial_capital) / payload.initial_capital) * 100) if len(bench_growth) > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
