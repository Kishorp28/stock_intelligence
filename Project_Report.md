# Comprehensive Project Report
## Intelligent Stock Recommendation and Prediction System Using Machine Learning

---

### 1. Project Abstract & Objective
The objective of this project was to construct a professional, placement-grade algorithmic stock recommendation engine. Unlike traditional basic price predictors, this system evaluates real-world user configurations (Risk Appetite, Capital, Expected Return, Sector Preference) combined with rigorous Machine Learning probability maps to identify high-conviction equities in the Indian Market (NIFTY 100). The architecture was deliberately decoupled into a modern structural paradigm featuring a Python backend and a React Single-Page Application (SPA) frontend.

---

### 2. System Architecture
The application utilizes a completely uncoupled paradigm for independent scaling and robustness:
1. **Data Engineering Layer:** Autonomous Python scripting (`yfinance`, `NewsData.io`) for quantitative ingestion.
2. **Machine Learning Model Registry:** A specialized Decision Tree / Random Forest predictive classifier trained on statistical feature engineering.
3. **Backend Middleware Server:** A highly concurrent `FastAPI` REST proxy serving algorithmic logic across generic JSON endpoints on the `Uvicorn` asynchronous server.
4. **Frontend Client Interface:** A lightning-fast Single-Page Application (SPA) built natively using `Vite + React.js`, equipped with `react-plotly.js` data charting and custom vanilla CSS aesthetics.

---

### 3. Data Collection & Preprocessing
Data purity is essential for quantitative tracking.
- **Historical Ingestion:** Automated pipelines extract 2-year multi-interval historical closing metrics and fundamental corporate ratios (P/E, ROE, EPS, Dividend Yield, Debt/Equity) natively using the `yfinance` programmatic module.
- **Natural Language Sentiment:** The system autonomously fetches the latest live financial news for targeted corporate entities using external global NEWS Rest APIs and calculates a polarity score (-1.0 to 1.0) mathematically using `TextBlob`.
- **Deriving Technical Indicators:** We utilized the `ta` processing suite to engineer dense multivariate technical vectors essential for momentum trading:
  - Relative Strength Index (RSI-14)
  - Moving Average Convergence Divergence (MACD)
  - Exponential / Simple Moving Averages (EMA-20 / SMA-50)
  - Bollinger Band Deviation Widths

---

### 4. Machine Learning Algorithmic Engine
The intelligence of the platform operates on deterministic threshold classifications evaluated through predictive Decision Trees.
- **Label Generation Pipeline:** The model determines localized ground-truth mapping based strictly on 30-day forward growth criteria. An equity registering a strict >10% future growth is labeled "Buy (2)", while assets projecting defensive stability (>0%) map to "Hold (1)", and negative correlations map to "Sell (0)".
- **Model Topology:** A rigorous `RandomForestClassifier` (100 estimators, depth limited to 10 nodes to prevent historical overfitting) was trained using Scikit-Learn.
- **Runtime Inference Engine:** Upon user request, the engine analyzes global feature datasets instantly, replacing arbitrary missing properties (`NaN`) elegantly without crashing, outputting standardized JSON recommendation distributions mapping the calculated algorithmic confidence interval (e.g. 75% quantitative conviction margin).

---

### 5. Backend REST Capabilities (FastAPI)
By pivoting away from embedded architectures (like Streamlit or pure Django), we developed strict corporate-standard APIs enabling multi-platform cross-compatibility:
- `/api/recommend`: Ingests user JSON parameters (capital, risk, etc.), cross-evaluates against the active Random Forest memory state, and executes strict sub-filtering routines to yield custom placement strategies.
- `/api/news/{symbol}`: Dynamic endpoint generating real-time algorithmic polarity assessments of corporate activities.
- `/api/backtest`: The mathematical backbone enabling robust historical validations. Automatically calculates standardized Nifty-benchmark equity performance yield curves over a configurable 6-month historical sliding window.

---

### 6. React Frontend Application (GUI)
The structural User Interface was coded flawlessly mirroring modern financial investment platforms (like Zerodha or Robinhood):
- Natively constructed utilizing `React Hooks` (useState, useEffect, mapping logic).
- Interactive navigation operates solely through efficient document object (DOM) replacement without requiring massive CSS reframing.
- **Dynamic Visualization:** Directly maps computational confidence levels and historic trading intervals via complex SVG constructions and robust `react-plotly.js` library candlestick rendering engines seamlessly embedded in an expandable grid.
- **Theme Standardization:** Hardcoded pristine white aesthetics employing ultra-premium variables avoiding standardized external layout frameworks like Bootstrap to showcase core web-development competency.

---

### 7. Key Operational Modules
For final showcase demonstrations, the platform contains specifically isolated environments mirroring real-world trading components:
1. **Investor Portfolio Recommender:** Fusing computational mathematics with hardline human risk-preferences to yield highly contextual results securely.
2. **Global Market Analysis Heatmap:** Tracking fundamental metric health checks and sector asset allocations across the generalized NIFTY 100 grouping.
3. **Historical Portfolio Backtesting Simulator:** Constructing mathematically accurate performance differentials proving the accuracy of internal Random Forest distributions over specific benchmark benchmarks unconditionally.
4. **Live Corporate Sentiment Tracking:** Live API mapping rendering text analysis instantly without caching delays.

---

### 8. Conclusion
The Intelligent Stock Prediction mapping has evolved strictly beyond arbitrary predictions into a thoroughly functional Full-Stack data science ecosystem. From executing intensive big-dataset ingestion and applying real-world classifier topologies to successfully launching and transmitting findings to a beautiful responsive React Dashboard across strict REST guidelines, the project unequivocally demonstrates proficiency traversing advanced multi-cloud technologies simultaneously.
