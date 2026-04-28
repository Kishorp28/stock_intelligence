# 📈 Intelligent Stock Recommendation & Prediction Engine

A highly advanced, placement-ready Data Science framework designed for intelligent stock recommendation and algorithmic backtesting. 
Originally prototyped on monolithic architectures, the system has been entirely upgraded into a scalable, decoupled **Full-Stack environment** featuring a **FastAPI Machine Learning Server** and a lightning-fast **React (Vite) Single-Page Application (SPA)**.

## 🚀 Key Features
- **Machine Learning Classifiers:** Utilizes high-frequency `Random Forest` and `XGBoost` decision trees trained on complex technical vectors (RSI-14, MACD, EMA-20, Bollinger Bands) to calculate multivariate probability thresholds correlating to 30-day forward growth momentum.
- **Real-Time NLP Sentiment:** Autonomous Natural Language Processing using `TextBlob` and global news APIs to calculate polarity assessments (-1.0 to 1.0) of real-time corporate media headlines.
- **Historical Backtesting Simulator:** Calculates mathematical performance yield differentials simulating AI-derived portfolios against benchmark Nifty indices purely using historical daily closures over a rolling 6-month sliding window.
- **Interactive UI (React + Vite):** A decoupled, pristine Vanilla CSS graphical interface rendering dynamic interactive `react-plotly.js` candlestick charting grids and seamless state management.

---

## 📂 Project Architecture
```text
stock_intelligence/
├── docker-compose.yml            # Universal Production Orchestrator
├── Dockerfile                    # FastAPI & ML Backend Container
├── .gitignore                    # Security and Node modules exclusion
├── Project_Report.md             # Comprehensive Placement Academic Report
├── database_schema.sql           # Raw MySQL deployment matrices
├── run_pipeline.py               # Autonomous Dataset Pipeline trigger
├── api.py                        # Uvicorn FastAPI REST Middleware Layer
├── ml_engine/                    # Core Model & Data logic
│   ├── data_collector.py         # Interfaces with yfinance & News APIs
│   ├── preprocessor.py           # Technical Analysis & NLP Generation
│   ├── model_trainer.py          # ML Model building and serialization
│   └── recommender.py            # User Constraint Evaluation Logic
└── frontend/                     # React Vite Workspace
    ├── Dockerfile                # Multi-stage Nginx UI Container
    ├── package.json              # Javascript dependencies
    └── src/
        ├── App.jsx               # Main React Dashboard Component
        └── index.css             # Vanilla CSS Custom Aesthetics
```

---

## ⚙️ How to Deploy (Docker - Recommended)
The fastest and most professional way to launch the system is using the pre-configured containerized environment.

1. Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
2. Open a terminal in the root directory and construct the production ecosystems:
```bash
docker-compose up --build
```
3. Once compiled, access your application natively at `http://localhost:5173`.

*(Note: Docker aggressively caches the heavy C++ ML dependencies. The very first run will take 3-5 minutes, but subsequent boots will take < 3 seconds).*

---

## ⚙️ How to Deploy (Manual Local Setup)
If you prefer running the systems physically on your hardware without Docker:

### 1. Data Processing Pipeline
Activate your Python environment and generate the latest market weights:
```bash
pip install -r requirements.txt
python run_pipeline.py
```

### 2. Boot the ML Backend
Start the high-concurrency FastAPI middleware:
```bash
python -m uvicorn api:app --reload
```

### 3. Boot the React Client
Open a secondary terminal, navigate to the UI module, and start the Vite web-server:
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Deploying to the Cloud
This project is configured natively for completely free cloud scaling!
- **FastAPI Backend:** Host automatically using [Railway.app](https://railway.app) (It will autonomously read the root `requirements.txt`).
- **React Frontend:** Host automatically using [Vercel](https://vercel.com) (Just point Vercel directly to your `/frontend` directory). 
*(Note: Be sure to update your `axios` fetch URLs in `App.jsx` from localhost to point to your live Railway backend link!)*
