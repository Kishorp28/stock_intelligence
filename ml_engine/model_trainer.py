import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Technical and Financial features to train the models on
FEATURES = [
    'rsi_14', 'macd', 'macd_signal', 'ema_20', 'sma_50', 
    'bollinger_upper', 'bollinger_lower', 'pe_ratio', 
    'eps', 'roe', 'debt_to_equity', 'dividend_yield'
]

def train_models(df):
    """
    Train Random Forest and XGBoost models on the preprocessed dataset.
    Target variable: 'label' (0: Sell, 1: Hold, 2: Buy)
    """
    print("Preparing data for training...")
    
    # Needs historical snapshot where we had both features and the future label computed
    train_df = df.copy()
    train_df[FEATURES] = train_df[FEATURES].fillna(0)
    train_df = train_df.dropna(subset=['label'])
    
    if train_df.empty:
        print("Not enough complete data to train models.")
        return None, None
        
    X = train_df[FEATURES]
    y = train_df['label']
    
    if len(X) < 100:
        print("Warning: Small dataset may lead to overfitting.")
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    print("Random Forest Accuracy:", accuracy_score(y_test, rf_preds))
    print("RF classification report:\n", classification_report(y_test, rf_preds))
    
    print("Training XGBoost Classifier...")
    # XGBoost requires labels starting from 0 (which we have: 0, 1, 2)
    xgb_model = XGBClassifier(n_estimators=100, random_state=42, eval_metric='mlogloss')
    xgb_model.fit(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)
    print("XGBoost Accuracy:", accuracy_score(y_test, xgb_preds))
    
    # Save models
    rf_path = os.path.join(MODEL_DIR, 'rf_model.joblib')
    xgb_path = os.path.join(MODEL_DIR, 'xgb_model.joblib')
    
    joblib.dump(rf_model, rf_path)
    joblib.dump(xgb_model, xgb_path)
    print(f"Models successfully saved to {MODEL_DIR}")
    
    return rf_model, xgb_model

def predict_stocks(df, model_type='rf'):
    """
    Predict Buy/Hold/Sell labels for latest stock data.
    """
    model_path = os.path.join(MODEL_DIR, f'{model_type}_model.joblib')
    if not os.path.exists(model_path):
        print(f"Model {model_type} not found at {model_path}. Please train first.")
        return df
        
    model = joblib.load(model_path)
    
    # For prediction we just need features, no 'label' (future window unknown yet)
    predict_df = df.copy()
    predict_df[FEATURES] = predict_df[FEATURES].fillna(0)
    if predict_df.empty:
        return predict_df
        
    predictions = model.predict(predict_df[FEATURES])
    predict_probs = model.predict_proba(predict_df[FEATURES])
    
    predict_df['prediction'] = predictions
    predict_df['confidence'] = predict_probs.max(axis=1) # Get the highest probability
    
    # Map predictions to human readable labels (handling float predictions)
    label_map = {0: 'Sell', 1: 'Hold', 2: 'Buy', 0.0: 'Sell', 1.0: 'Hold', 2.0: 'Buy'}
    predict_df['recommendation'] = predict_df['prediction'].map(label_map)
    
    return predict_df
