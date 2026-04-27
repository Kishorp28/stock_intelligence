import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator, SMAIndicator
from ta.volatility import BollingerBands
from textblob import TextBlob

def calculate_technical_indicators(df):
    """
    Calculate RSI, MACD, EMA, SMA, Bollinger Bands using the 'ta' library.
    Expects df to have 'Close' column.
    """
    if df.empty or 'Close' not in df.columns:
        return df

    # RSI
    df['rsi_14'] = RSIIndicator(close=df['Close'], window=14).rsi()
    
    # MACD
    macd = MACD(close=df['Close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    
    # Moving Averages
    df['ema_20'] = EMAIndicator(close=df['Close'], window=20).ema_indicator()
    df['sma_50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
    
    # Bollinger Bands
    bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['bollinger_upper'] = bb.bollinger_hband()
    df['bollinger_lower'] = bb.bollinger_lband()
    
    return df

def analyze_sentiment(news_list):
    """
    Calculate sentiment scores for a list of news articles using TextBlob.
    Returns average sentiment from -1.0 to +1.0.
    """
    if not news_list:
        return 0.0
        
    total_polarity = 0.0
    for article in news_list:
        text = f"{article.get('headline', '')} {article.get('description', '')}"
        analysis = TextBlob(text)
        total_polarity += analysis.sentiment.polarity
        
    return total_polarity / len(news_list)

def create_target_labels(df, future_window=30):
    """
    Create label for Next 30-Day returns.
    > 10% -> 2 (Buy/Strong Buy)
    0-10% -> 1 (Hold)
    < 0% -> 0 (Sell/Strong Sell)
    """
    if df.empty or 'Close' not in df.columns:
        return df
        
    # Calculate future return pct
    df['future_close'] = df['Close'].shift(-future_window)
    df['future_return_pct'] = ((df['future_close'] - df['Close']) / df['Close']) * 100
    
    def generate_label(ret):
        if pd.isna(ret):
            return np.nan
        if ret > 10.0:
            return 2 # Buy
        elif ret >= 0.0:
            return 1 # Hold
        else:
            return 0 # Sell
            
    df['label'] = df['future_return_pct'].apply(generate_label)
    return df
