# Intelligent Stock Recommendation and Prediction System

A placement-ready machine learning framework for intelligent stock recommendation. Initially configured tightly within a scalable full-stack Python environment, designed to process financial ratios, technical indicators, and news sentiment, ultimately leveraging Random Forest & XGBoost to map intelligent suggestions precisely to an investor's preferences.

## 🚀 Key Features
- **Data Engineering:** Automatically calculates 14-day RSI, MACD, EMAs, and Bollinger Bands using Yahoo Finance Data.
- **Machine Learning Integration:** Uses `Random Forest` and `XGBoost` classifiers to parse technical signals and fundamentals and predict a discrete return class (Buy/Hold/Sell) over a forward 30-day window.
- **Preference Matching System:** Uses deterministic rules to overlay user constraints (Risk Level, Investment Amount, Sector Choice, Dividend desires) mapped cleanly onto the ML's base predictions.
- **Interactive UI (Streamlit):** Clean, real-time, responsive user inputs rendering interactive Plotly candlestick charting and algorithmic portfolio distribution.

## 📂 Project Structure
```text
stock/
├── .env                          # Environment variables (NewsAPI Key, etc.)
├── requirements.txt              # Required dependencies
├── database_schema.sql           # Raw MySQL deployment scripts
├── README.md                     # Documentation
├── manage.py                     # Extensible Django entry point
├── stock_project/                # Django root namespace
├── dashboard/                    # Django frontend (Standby/ORM layer map)
├── app.py                        # Streamlit Main Dashboard Entry Point
├── run_pipeline.py               # Complete Automated ML Pipeline trigger
└── ml_engine/                    # Core Model & Data logic
    ├── data_collector.py         # Interfaces with yfinance & NewsData.io
    ├── preprocessor.py           # Technical Analysis Generation
    ├── model_trainer.py          # ML Model build and joblib Serialization
    └── recommender.py            # User Constraint Evaluation Logic
```

## ⚙️ Step-by-Step Implementation locally

### 1. Database Creation (MySQL via WAMP/XAMPP or local Server)
Execute `database_schema.sql` completely into your MySQL environment.
```bash
mysql -u root -p < database_schema.sql
```

### 2. Install Packages
It is heavily advised to activate a fresh python environment first.
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Data & Training Pipeline
To calculate live ratios for the top 100 stocks and train the ensemble models, trigger the automated pipeline:
```bash
python run_pipeline.py
```
*Depending on network, this will take ~1-2mins parsing years of data and will save `latest_stock_data.csv` plus model dumps into `ml_engine/models/`*

### 4. Boot the Production UI (React + FastAPI)
Run the ML inference engine API backend:
```bash
python -m uvicorn api:app --reload
```
Open a new terminal and run the React Vite frontend:
```bash
cd frontend
npm run dev
```

## 🌐 Deploying to Production (Render)
As requested, this project is production-ready for platforms like Render.

1. Connect your Git repo to Render as a **Web Service**.
2. **Environment:** `Python 3`
3. **Build Command:** 
```bash
pip install -r requirements.txt
```
4. **Start Command:** 
```bash
streamlit run app.py --server.port $PORT
```
*(Alternatively, you can just deploy to Streamlit Community Cloud completely free for instant access)*

## 💡 Note on Architecture 
While initially requested as a Django UI, Streamlit has been implemented per explicit request ("*use streamlit dashboard*") for clean separation logic matching standard ML environments. However, the exact ORM models (`dashboard/models.py`) and standard `django-admin` configurations ring-fence the database definition and serve as foundational stones inside the repo. This gracefully allows you to scale up immediately into a strict API SaaS backend if desired with zero structural rewrite!
"# stock_intelligence" 
