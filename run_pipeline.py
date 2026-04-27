import pandas as pd
from ml_engine.data_collector import fetch_historical_prices, fetch_financial_ratios, NIFTY_SYMBOLS
from ml_engine.preprocessor import calculate_technical_indicators, create_target_labels
from ml_engine.model_trainer import train_models

def main():
    print("="*60)
    print("=== Intelligent Stock Recommendation Data Pipeline ===")
    print("="*60)
    
    print("\n[1/3] Fetching Market Data & Fundamentals...")
    prices_df = fetch_historical_prices(NIFTY_SYMBOLS, period='2y')
    ratios_df = fetch_financial_ratios(NIFTY_SYMBOLS)
    
    print("\n[2/3] Performing Feature Engineering...")
    processed_dfs = []
    
    if not prices_df.empty:
        # Group by symbol and calculate indicators to prevent bleed between stocks
        for symbol, group in prices_df.groupby('symbol'):
            group_ti = calculate_technical_indicators(group.copy())
            group_labeled = create_target_labels(group_ti, future_window=30)
            processed_dfs.append(group_labeled)
            
        full_df = pd.concat(processed_dfs)
        
        # Merge technical indicators data with foundational ratios
        full_df = pd.merge(full_df, ratios_df, on='symbol', how='left')
        
        print(f"Engineered {len(full_df)} total datapoints across {len(NIFTY_SYMBOLS)} stocks.")
        
        print("\n[3/3] Training Machine Learning Models...")
        train_models(full_df)
        
        # Important: For the Streamlit dashboard, we only need the most recent row per stock 
        # to run live inference against
        latest_data = full_df.groupby('symbol').last().reset_index()
        latest_data.to_csv('latest_stock_data.csv', index=False)
        print("\n✅ Setup Complete! Live data snapshot saved to 'latest_stock_data.csv'.")
        print("🚀 You may now run `streamlit run app.py` to start the frontend dashboard.")
    else:
        print("❌ Data collection failed! Pipeline aborted. Check your internet connection or yfinance limits.")

if __name__ == '__main__':
    main()
