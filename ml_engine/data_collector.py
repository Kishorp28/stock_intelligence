import yfinance as yf
import pandas as pd
import requests
import os

# Load env variables if available (fallback to default string for simplicity)
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'pub_471136f82e1a4781aa90994743f7eaa8')

# A representative subset of Nifty 100 for demonstration. Can be expanded to all 100 later.
NIFTY_SYMBOLS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 
    'HINDUNILVR.NS', 'SBIN.NS', 'ITC.NS', 'ASIANPAINT.NS', 'BAJFINANCE.NS', 
    'L&T.NS', 'HCLTECH.NS', 'MARUTI.NS', 'SUNPHARMA.NS', 'TATAMOTORS.NS', 
    'TATASTEEL.NS', 'WIPRO.NS', 'ONGC.NS', 'NTPC.NS', 'HDFCLIFE.NS'
]

def fetch_historical_prices(symbols, period='2y'):
    """
    Fetch historical prices from Yahoo finance for given symbols.
    """
    print(f"Fetching historical prices for {len(symbols)} symbols...")
    data = yf.download(symbols, period=period, group_by='ticker')
    all_data = []

    for symbol in symbols:
        try:
            # Handle multi-index columns dynamically
            if len(symbols) > 1:
                df = data[symbol].dropna().copy()
            else:
                df = data.dropna().copy()
                
            df['symbol'] = symbol
            all_data.append(df)
        except Exception as e:
            print(f"Error fetching prices for {symbol}: {e}")
            
    if all_data:
        final_df = pd.concat(all_data)
        final_df.reset_index(inplace=True)
        return final_df
    return pd.DataFrame()

def fetch_financial_ratios(symbols):
    """
    Fetch fundamental financial ratios using yfinance info property.
    """
    print(f"Fetching financial ratios for {len(symbols)} symbols...")
    ratios_list = []
    
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            ratios = {
                'symbol': symbol,
                'pe_ratio': info.get('trailingPE', None),
                'eps': info.get('trailingEps', None),
                'roe': info.get('returnOnEquity', None),
                'debt_to_equity': info.get('debtToEquity', None),
                'dividend_yield': info.get('dividendYield', None),
                'market_cap': info.get('marketCap', None),
                'company_name': info.get('longName', symbol),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
            }
            ratios_list.append(ratios)
        except Exception as e:
            print(f"Error fetching ratios for {symbol}: {e}")
            
    return pd.DataFrame(ratios_list)

def fetch_company_news(company_name):
    """
    Fetch latest news for a specific company using NewsData.io
    """
    query = company_name.replace('.NS', '')
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={query}&language=en"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        articles = []
        if data.get('status') == 'success':
            for article in data.get('results', []):
                articles.append({
                    'headline': article.get('title'),
                    'description': article.get('description'),
                    'content': article.get('content'),
                    'news_date': article.get('pubDate'),
                })
        return articles
    except Exception as e:
        print(f"Error fetching news for {query}: {e}")
        return []

if __name__ == '__main__':
    prices = fetch_historical_prices(NIFTY_SYMBOLS[:2], period="1mo")
    print("Prices head:", prices.head())
    
    ratios = fetch_financial_ratios(NIFTY_SYMBOLS[:2])
    print("Ratios DataFrame:\n", ratios)
    
    news = fetch_company_news(NIFTY_SYMBOLS[0])
    print(f"News articles found for {NIFTY_SYMBOLS[0]}: {len(news)}")
