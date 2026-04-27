from django.db import models
from django.contrib.auth.models import User

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_type = models.CharField(max_length=50) # Short-term / Long-term
    risk_level = models.CharField(max_length=50) # Low / Medium / High
    investment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    preferred_sector = models.CharField(max_length=100)
    expected_return = models.DecimalField(max_digits=5, decimal_places=2)
    dividend_preference = models.BooleanField(default=False)
    market_cap_preference = models.CharField(max_length=50) # Large / Mid / Small cap
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_preferences'

class StockMaster(models.Model):
    MARKET_CAP_CHOICES = [
        ('Large', 'Large'),
        ('Mid', 'Mid'),
        ('Small', 'Small'),
    ]
    symbol = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=150)
    sector = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    market_cap = models.CharField(max_length=10, choices=MARKET_CAP_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stocks_master'

class StockPrice(models.Model):
    stock = models.ForeignKey(StockMaster, on_delete=models.CASCADE)
    trade_date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    high_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    low_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    close_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    volume = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'stock_prices'
        unique_together = ('stock', 'trade_date')

class FinancialRatio(models.Model):
    stock = models.ForeignKey(StockMaster, on_delete=models.CASCADE)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    eps = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    roe = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    debt_to_equity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dividend_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'financial_ratios'

class TechnicalIndicator(models.Model):
    stock = models.ForeignKey(StockMaster, on_delete=models.CASCADE)
    trade_date = models.DateField()
    rsi_14 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    macd = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    macd_signal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ema_20 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sma_50 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bollinger_upper = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bollinger_lower = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'technical_indicators'
        unique_together = ('stock', 'trade_date')

class NewsSentiment(models.Model):
    stock = models.ForeignKey(StockMaster, on_delete=models.CASCADE)
    news_date = models.DateField()
    headline = models.TextField()
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=4, null=True)

    class Meta:
        db_table = 'news_sentiment'

class Prediction(models.Model):
    stock = models.ForeignKey(StockMaster, on_delete=models.CASCADE)
    prediction_date = models.DateField()
    predicted_return_30d = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    recommendation_label = models.CharField(max_length=20) # Strong Buy, Buy, Hold, Sell, Strong Sell
    model_version = models.CharField(max_length=50)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        db_table = 'predictions'

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(StockMaster, on_delete=models.CASCADE)
    recommendation_date = models.DateField()
    reasoning = models.TextField()

    class Meta:
        db_table = 'recommendations'
