CREATE DATABASE IF NOT EXISTS stock_project;
USE stock_project;

CREATE TABLE user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    investment_type VARCHAR(50), -- Short-term / Long-term
    risk_level VARCHAR(50), -- Low / Medium / High
    investment_amount DECIMAL(15, 2),
    preferred_sector VARCHAR(100), -- IT, Banking, etc.
    expected_return DECIMAL(5, 2),
    dividend_preference BOOLEAN,
    market_cap_preference VARCHAR(50), -- Large / Mid / Small cap
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- FOREIGN KEY (user_id) REFERENCES auth_user(id) -- Django auth table will handle this relation
);

CREATE TABLE stocks_master (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(150),
    sector VARCHAR(100),
    industry VARCHAR(100),
    market_cap ENUM('Large', 'Mid', 'Small'),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10, 2),
    high_price DECIMAL(10, 2),
    low_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    volume BIGINT,
    UNIQUE KEY unique_stock_date (stock_id, trade_date),
    FOREIGN KEY (stock_id) REFERENCES stocks_master(id) ON DELETE CASCADE
);

CREATE TABLE financial_ratios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    pe_ratio DECIMAL(10, 2),
    eps DECIMAL(10, 2),
    roe DECIMAL(10, 2),
    debt_to_equity DECIMAL(10, 2),
    dividend_yield DECIMAL(10, 2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stocks_master(id) ON DELETE CASCADE
);

CREATE TABLE technical_indicators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    trade_date DATE NOT NULL,
    rsi_14 DECIMAL(10, 2),
    macd DECIMAL(10, 2),
    macd_signal DECIMAL(10, 2),
    ema_20 DECIMAL(10, 2),
    sma_50 DECIMAL(10, 2),
    bollinger_upper DECIMAL(10, 2),
    bollinger_lower DECIMAL(10, 2),
    UNIQUE KEY unique_stock_date_tech (stock_id, trade_date),
    FOREIGN KEY (stock_id) REFERENCES stocks_master(id) ON DELETE CASCADE
);

CREATE TABLE news_sentiment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    news_date DATE NOT NULL,
    headline TEXT,
    sentiment_score DECIMAL(5, 4), -- Range: -1.0 to 1.0 (TextBlob/VADER)
    FOREIGN KEY (stock_id) REFERENCES stocks_master(id) ON DELETE CASCADE
);

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    prediction_date DATE NOT NULL,
    predicted_return_30d DECIMAL(10, 2),
    recommendation_label ENUM('Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell'),
    model_version VARCHAR(50),
    confidence_score DECIMAL(5, 2),
    FOREIGN KEY (stock_id) REFERENCES stocks_master(id) ON DELETE CASCADE
);

CREATE TABLE recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_id INT NOT NULL,
    recommendation_date DATE NOT NULL,
    reasoning TEXT,
    -- FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (stock_id) REFERENCES stocks_master(id) ON DELETE CASCADE
);
