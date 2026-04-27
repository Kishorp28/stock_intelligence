import pandas as pd

def get_recommendations(user_prefs, predicted_stocks_df):
    """
    Filter the ML predicted stocks based on user preferences.
    """
    if predicted_stocks_df.empty:
        return pd.DataFrame()
        
    filtered = predicted_stocks_df.copy()
    
    # Ensure necessary columns are cleanly mapped if running independently
    required_cols = ['symbol', 'company_name', 'sector', 'industry', 'market_cap', 'dividend_yield', 'recommendation', 'confidence']
    for col in required_cols:
        if col not in filtered.columns:
            filtered[col] = 'Unknown' if col != 'dividend_yield' and col != 'confidence' else 0.0
    
    # 1. Base ML Recommendation constraint
    # Exclude 'Sell'. 'Buy' (>10%) and 'Hold' (0-10%) are acceptable for recommendations.
    filtered = filtered[filtered['recommendation'].isin(['Buy', 'Hold'])]
    
    # 2. Sector Preference
    preferred_sector = user_prefs.get('preferred_sector', 'All')
    if preferred_sector and preferred_sector != 'All':
        filtered = filtered[filtered['sector'].str.contains(preferred_sector, case=False, na=False)]
        
    # Helper to categorize market cap
    def get_market_cap_category(val):
        try:
            val = float(val)
            if val > 200000000000:
                return 'Large'
            elif val > 50000000000:
                return 'Mid'
            else:
                return 'Small'
        except:
            return 'Unknown'
            
    filtered['market_cap_category'] = filtered['market_cap'].apply(get_market_cap_category)

    # 3. Market Cap Preference
    market_cap_pref = user_prefs.get('market_cap_preference', 'Any')
    if market_cap_pref and market_cap_pref != 'Any':
        filtered = filtered[filtered['market_cap_category'] == market_cap_pref]
        
    # 4. Dividend Preference
    needs_dividend = user_prefs.get('dividend_preference', False)
    if needs_dividend:
        try:
            # Safely cast to float
            filtered['dividend_yield'] = pd.to_numeric(filtered['dividend_yield'], errors='coerce').fillna(0)
            filtered = filtered[filtered['dividend_yield'] > 0.0] # Any dividend paying stock
        except:
            pass
            
    # 5. Risk Level Heuristics
    risk_level = user_prefs.get('risk_level', 'Medium')
    if risk_level == 'Low':
        # Low risk -> strongly prefer Large Cap
        if market_cap_pref == 'Any':
            filtered = filtered[filtered['market_cap_category'] == 'Large']
            
    # Sort strictly by ML model confidence to ensure best placement first
    if 'confidence' in filtered.columns:
        filtered = filtered.sort_values(by='confidence', ascending=False)
        
    return filtered
