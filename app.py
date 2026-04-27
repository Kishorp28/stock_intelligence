import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import yfinance as yf
from datetime import datetime

# Import local modules
from ml_engine.model_trainer import predict_stocks
from ml_engine.recommender import get_recommendations

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Intelligent Stock AI", layout="wide", page_icon="🏦", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 6px; height: 3em; background-color: #0b5ed7; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #0a58ca; }
    .metric-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #eef2f5;}
    .metric-title { font-size: 16px; color: #6c757d; font-weight: bold; text-transform: uppercase;}
    .metric-val { font-size: 28px; font-weight: 800; color: #212529; margin-top: 5px;}
    .recommendation-buy { color: #198754; font-weight: bold; font-size: 14px;}
    .company-header { color: #0b5ed7; margin-top: 0; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col1, col2 = st.columns([0.6, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
with col2:
    st.title("Intelligent Stock Recommendation Engine")
    st.markdown("*A professional placement-ready application utilizing scalable ensemble Machine Learning to map technical and fundamental signals perfectly onto individual investment portfolios.*")

st.markdown("---")

# --- SIDEBAR: PREFERENCES ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1000/1000189.png", width=60)
st.sidebar.title("Portfolio Setup")
st.sidebar.markdown("Define your investment strategy bounds.")

inv_type = st.sidebar.selectbox("⏱️ Investment Horizon", ["Short-term (< 6 months)", "Long-term (1+ Years)"])
risk_level = st.sidebar.select_slider("⚖️ Risk Appetite", options=["Low", "Medium", "High"], value="Medium")
inv_amount = st.sidebar.number_input("💵 Capital Allocation (₹)", min_value=1000, value=100000, step=10000, format="%d")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("**Market Constraints**")
sectors_available = ["All", "Technology", "Financial Services", "Consumer Defensive", "Healthcare", "Industrials", "Energy"]
preferred_sector = st.sidebar.selectbox("🏢 Preferred Sector", sectors_available)

market_cap_pref = st.sidebar.selectbox("📊 Market Cap Focus", ["Any", "Large", "Mid", "Small"])
dividend_pref = st.sidebar.checkbox("💰 Require Dividend Yield?", value=False)
expected_return = st.sidebar.slider("💹 Minimum Target ROI (%)", min_value=1, max_value=50, value=15)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.sidebar.button("Generate Recommendations 🚀")

# --- DATA LAYER ---
DATA_FILE = "latest_stock_data.csv"

@st.cache_data(ttl=3600)
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()

df = load_data()

# --- TABS ---
tab_dashboard, tab_market, tab_ai = st.tabs(["🎯 Portfolio AI Matches", "📈 Market Universe", "🧠 ML Engine Architecture"])

with tab_market:
    st.header("Global Data Snapshot")
    if df.empty:
        st.warning("⚠️ No backend data found. Please run the data pipeline (`python run_pipeline.py`) to scrape Yahoo Finance.")
    else:
        st.write(f"**Loaded Universe:** {len(df)} Equities Evaluated Live")
        st.dataframe(df[['symbol', 'sector', 'industry', 'market_cap', 'Close', 'rsi_14', 'macd']].head(50), use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Sector Distribution")
            fig_pie = px.pie(df, names='sector', hole=0.3, color_discrete_sequence=px.colors.sequential.Teal)
            st.plotly_chart(fig_pie)
        with c2:
            st.subheader("RSI Momentum Spread")
            fig_hist = px.histogram(df, x='rsi_14', nbins=20, labels={'rsi_14':'RSI (14 Day)'})
            fig_hist.add_vline(x=30, line_dash="dash", line_color="green", annotation_text="Oversold")
            fig_hist.add_vline(x=70, line_dash="dash", line_color="red", annotation_text="Overbought")
            st.plotly_chart(fig_hist)

with tab_ai:
    st.header("Machine Learning Analytics")
    st.write("This engine uses dual-classification logic via **Random Forest** and **XGBoost** pipelines. Each stock's features are automatically engineered (SMA, EMA, RSI, Bollinger Bands, P/E, EPS) into a combined multidimensional vector.")
    
    st.markdown("""
    #### ⚙️ Feature Pipeline
    - **Technical Indicators (TA):** `RSI_14`, `MACD`, `MACD_SIGNAL`, `EMA_20`, `SMA_50`, `Bollinger_Bands(Upper/Lower)`
    - **Fundamentals:** `P/E Ratio`, `EPS`, `ROE`, `Debt/Equity`, `Dividend Yield`
    
    #### 🎯 Target Variable
    The model autonomously translates the Forward-30-Day returns into discrete predictive signals during training:
    - **Buy (+):** `> 10.0% expected categorical return`
    - **Hold (0):** `0.0% to 10.0% expected categorical return`
    - **Sell (-):** `< 0.0% expected return probability`
    """)

with tab_dashboard:
    if analyze_btn:
        with st.spinner("🤖 Processing predictive topology and intersecting with user heuristics..."):
            if df.empty:
                st.error("Data pipeline has not been executed. Cannot serve predictions.")
            else:
                predicted_df = predict_stocks(df, model_type='rf')
                
                prefs = {
                    'preferred_sector': preferred_sector,
                    'market_cap_preference': market_cap_pref,
                    'dividend_preference': dividend_pref,
                    'risk_level': risk_level
                }
                
                recs_df = get_recommendations(prefs, predicted_df)
                
                if recs_df.empty:
                    st.error("No equities meet your rigid parameters currently. **Suggestions:**")
                    st.info("1. Switch Sector from '{}' to 'All'\n2. Switch Market Cap from '{}' to 'Any'\n3. Toggle Dividend Preference.".format(preferred_sector, market_cap_pref))
                    
                    st.markdown("#### 💡 Next Best Alternatives (System Defaults)")
                    fallback_df = get_recommendations({'preferred_sector': 'All', 'market_cap_preference': 'Any', 'dividend_preference': False, 'risk_level': 'Medium'}, predicted_df)
                    if not fallback_df.empty:
                        st.dataframe(fallback_df[['symbol', 'company_name', 'recommendation', 'confidence']].head(5))
                    
                else:
                    st.success(f"Execution Complete: {len(recs_df)} high-conviction ML matches found.")
                    st.markdown(f"### 💼 Formulated Portfolio (₹{inv_amount:,.2f})")
                    
                    allocation_per_stock = inv_amount / len(recs_df)
                    
                    # Top line metrics rendering Custom UI
                    metric_cols = st.columns(min(len(recs_df), 4))
                    for idx, row in recs_df.head(4).iterrows():
                        col = metric_cols[idx % len(metric_cols)]
                        with col:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">{row['symbol']}</div>
                                <div class="metric-val">₹{allocation_per_stock:,.0f}</div>
                                <div class="recommendation-buy">AI Conviction: {row.get('confidence', 0)*100:.1f}%</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("---")
                    
                    for idx, row in recs_df.iterrows():
                        symbol = row['symbol']
                        company_name = row.get('company_name', symbol)
                        if pd.isna(company_name): company_name = symbol
                        
                        confidence_score = row.get('confidence', 0)
                        
                        with st.expander(f"📌 {company_name} ({symbol}) - Match Score: {confidence_score*100:.1f}%", expanded=(idx==0)):
                            desc_col, chart_col = st.columns([1, 2.5])
                            
                            with desc_col:
                                st.markdown(f"<h4 class='company-header'>{company_name} Overview</h4>", unsafe_allow_html=True)
                                
                                st.write(f"**Industry:** {row.get('sector', 'N/A')}")
                                
                                cap_str = row.get('market_cap_category', 'Unknown')
                                st.write(f"**Market Capitalization:** {cap_str} Cap")
                                
                                pe_val = row.get('pe_ratio', 0)
                                st.write(f"**P/E Ratio:** {round(pe_val, 2) if pd.notna(pe_val) else 'N/A'}")
                                
                                dy = row.get('dividend_yield', 0)
                                if pd.notna(dy) and isinstance(dy, float) and dy > 0:
                                    st.write(f"**Dividend Yield:** {dy*100:.2f}%")
                                else:
                                    st.write(f"**Dividend Yield:** None")
                                    
                                rsi = row.get('rsi_14', 50)
                                st.write(f"**Momentum (RSI-14):** {round(rsi, 2)}")
                                
                                st.markdown("##### ✔️ Algorithmic Thesis")
                                if row['recommendation'] == 'Buy':
                                    st.write("- **Quantitative Edge:** Model recognizes multi-variate pattern indicating >10% forward momentum in 30 days.")
                                else:
                                    st.write("- **Stability Check:** Asset flagged as 'Hold' indicating strong downside protection. Ideal for risk mitigation.")
                                
                                if rsi < 30:
                                    st.caption("📈 **Oversold:** Technical RSI below 30 signals high asymmetry for entry.")
                                elif rsi > 70:
                                    st.caption("📉 **Overbought:** RSI elevated. Consider scaling in incrementally for safety.")
                            
                            with chart_col:
                                try:
                                    hist = yf.download(symbol, period="3mo", progress=False)
                                    if isinstance(hist.columns, pd.MultiIndex):
                                        hist = hist.xs(symbol, axis=1, level=1)
                                        
                                    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                                open=hist['Open'],
                                                high=hist['High'],
                                                low=hist['Low'],
                                                close=hist['Close'],
                                                name="Price")])
                                                
                                    hist['SMA20'] = hist['Close'].rolling(window=20).mean()
                                    fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA20'], mode='lines', name='SMA 20', line=dict(color='#0b5ed7', width=2)))

                                    fig.update_layout(
                                        title=f"90-Day Trajectory: {symbol}",
                                        xaxis_rangeslider_visible=False,
                                        margin=dict(l=0, r=0, t=30, b=0),
                                        height=330,
                                        plot_bgcolor='#f7f9fc',
                                        paper_bgcolor='white',
                                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                                except Exception as e:
                                    st.error("Live charting momentarily unavailable.")
    else:
        st.info("👈 **Configure your portfolio parameters in the setup menu and execute the Engine.**")
