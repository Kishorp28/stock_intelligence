from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserPreference)
admin.site.register(StockMaster)
admin.site.register(StockPrice)
admin.site.register(FinancialRatio)
admin.site.register(TechnicalIndicator)
admin.site.register(NewsSentiment)
admin.site.register(Prediction)
admin.site.register(Recommendation)
