````md
# 📈 Intelligent Stock Recommendation & Prediction Engine

A production-ready full-stack AI platform for intelligent stock recommendation, prediction, and portfolio decision support.

This system is built as a real-world fintech product—not just a basic stock price prediction project. It combines Machine Learning, Financial Analysis, Technical Indicators, News Sentiment Analysis, and Personalized Investment Preferences to recommend suitable stocks with Buy / Hold / Sell decisions.

The architecture is fully decoupled and deployed in production using:

- **Frontend:** React + Vite (Hosted on Vercel)
- **Backend:** FastAPI + Uvicorn (Hosted on Render)
- **Database:** MySQL
- **Containerization:** Docker + Docker Compose
- **ML Engine:** Random Forest + XGBoost + Technical Analysis Pipeline

---

# 🚀 Live Production Deployment

## Frontend (Vercel)

https://stock-intelligence-ten.vercel.app/

## Backend (Render)

https://stock-intelligence-pnbe.onrender.com

## API Documentation (Swagger UI)

https://stock-intelligence-pnbe.onrender.com/docs

---

# 🎯 Problem Statement

Investors often struggle to choose the right stocks because:

- Too much financial data exists
- Manual analysis is difficult
- Investment goals differ for every investor
- Short-term and long-term strategies are different
- News and sentiment significantly affect stock movement

This system solves that problem by delivering personalized stock recommendations instead of generic stock predictions.

---

# 🚀 Core Features

## Personalized Stock Recommendation Engine

The system asks users for:

- Investment Type (Short-term / Long-term)
- Risk Level (Low / Medium / High)
- Investment Amount
- Preferred Sector
- Expected Return %
- Dividend Preference
- Market Cap Preference

Based on these preferences, the platform recommends suitable stocks.

---

## Machine Learning Prediction Engine

Uses:

- Random Forest Classifier
- XGBoost Classifier

to generate:

- Strong Buy
- Buy
- Hold
- Sell
- Strong Sell

recommendation labels based on 30-day forward return probability.

---

## Technical Analysis Engine

Generates advanced indicators such as:

- RSI (14)
- MACD
- EMA (20)
- SMA (50 / 200)
- Bollinger Bands
- Volatility Score
- Momentum Score

These are used as model features for recommendation prediction.

---

## Real-Time News Sentiment Analysis

Uses:

- NewsAPI
- TextBlob
- VADER Sentiment

to calculate sentiment polarity scores (-1.0 to +1.0) from recent company news headlines.

This improves recommendation quality significantly.

---

## Historical Backtesting Simulator

Compares:

- AI Recommended Portfolio

vs

- Nifty Benchmark Performance

using historical rolling-window simulation over previous market periods.

This validates recommendation performance.

---

## Interactive Frontend Dashboard

Built using:

- React + Vite
- Plotly Charts
- Responsive UI
- Production-safe API integration

Dashboard shows:

- Recommended Stocks
- Buy / Sell Signals
- Confidence Score
- Predicted Return
- Sentiment Score
- Portfolio Allocation
- Interactive Charts

---

# 📂 Project Architecture

```text
stock_intelligence/
│
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── config/
│   │
│   ├── ml_engine/
│   │   ├── data_collector.py
│   │   ├── preprocessor.py
│   │   ├── model_trainer.py
│   │   ├── recommender.py
│   │   └── sentiment_engine.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── database_schema.sql
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .gitignore
├── Project_Report.md
├── README.md
└── requirements.txt
````

---

# ⚙️ Tech Stack

## Frontend

* React + Vite
* JavaScript
* Plotly.js
* CSS
* Axios

## Backend

* FastAPI
* Uvicorn
* Python

## Machine Learning

* Pandas
* NumPy
* Scikit-learn
* XGBoost
* TA Library
* TextBlob
* VADER

## Database

* MySQL

## Deployment

* Vercel
* Render
* Docker
* Docker Compose

---

# 🗄️ Database Tables

Main MySQL tables:

* users
* user_preferences
* stocks_master
* stock_prices
* financial_ratios
* technical_indicators
* news_sentiment
* predictions
* recommendations
* portfolio_history

These tables store both raw market data and generated recommendations.

---

# ⚙️ Local Development Setup

## Step 1 — Clone Repository

```bash
git clone <your-repository-url>
cd stock_intelligence
```

---

## Step 2 — Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3 — Run Data Pipeline

This fetches:

* historical stock prices
* financial ratios
* technical indicators
* sentiment data

```bash
python run_pipeline.py
```

---

## Step 4 — Start Backend Server

```bash
python -m uvicorn main:app --reload
```

Backend runs on:

http://localhost:8000

Swagger docs:

http://localhost:8000/docs

---

## Step 5 — Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

http://localhost:5173

---

# 🐳 Docker Deployment (Recommended)

Production-ready containerized deployment:

```bash
docker-compose up --build
```

This launches:

* Frontend
* Backend
* Database

using a single command.

---

# 🌐 Production Deployment

## Backend Deployment (Render)

Hosted using:

### Render Web Service

Production backend URL:

https://stock-intelligence-pnbe.onrender.com

Features:

* Auto Deploy from GitHub
* Environment Variable Support
* FastAPI Production Hosting
* Swagger Documentation
* Health Check Monitoring

---

## Frontend Deployment (Vercel)

Hosted using:

### Vercel Static Deployment

Production frontend URL:

https://stock-intelligence-ten.vercel.app/

Features:

* GitHub Auto Deploy
* Vite Native Support
* Fast CDN Delivery
* Production Build Optimization

---

# 🔐 Important Production Configuration

## Backend CORS Setup

FastAPI CORS configured specifically for:

```python
allow_origins = [
    "https://stock-intelligence-ten.vercel.app"
]
```

No wildcard CORS used.

Production-safe configuration only.

---

## Frontend Environment Variable

Create:

frontend/.env

Add:

```env
VITE_API_URL=https://stock-intelligence-pnbe.onrender.com
```

Used in React as:

```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

No localhost dependency in production.

---

# 📊 Example Recommendation Output

## User Input

* Long-term Investment
* Medium Risk
* ₹1,00,000 Investment
* IT Sector
* Dividend Required
* Large Cap

## System Output

### Recommended Stocks

1. TCS → Strong Buy
2. Infosys → Buy
3. HCL Tech → Hold

### Suggested Allocation

* TCS → 40%
* Infosys → 35%
* HCL → 25%

### Predicted Return

12–18%

### Confidence Score

87%

---

# 🧠 ML Label Logic

Recommendation labels are generated using future 30-day return:

| Return % | Label |
| -------- | ----- |
| > 10%    | Buy   |
| 0–10%    | Hold  |
| < 0%     | Sell  |

This becomes the target variable for training ML models.

---

# 🚀 Future Improvements

Possible upgrades:

* LSTM Deep Learning Prediction
* Live NSE/BSE API Integration
* User Authentication
* Portfolio Tracking
* Watchlist Feature
* Notification Alerts
* AI Chat-based Financial Assistant
* AWS Production Deployment
* Redis + Celery Background Jobs

---

# 💼 Resume-Ready Project Title

## Intelligent Stock Recommendation and Prediction System Using Machine Learning and Financial Analysis

This is much stronger than:

"Stock Price Prediction Project"

because it solves a real investment decision problem.

---

# Final Result

Users can:

* Open frontend from Vercel
* Submit investment preferences
* Trigger backend API on Render
* Get stock recommendations
* View prediction results
* Use the system fully online

without localhost or manual backend startup.

This makes the project industry-level and placement-ready.

```
```
