# Create your models here.
from django.db import models

class rsi_strategy_model(models.Model): 
    symbol = models.CharField(max_length = 221)
    stock_name = models.CharField(max_length = 221)
    price =  models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return self.symbol

# class two_percent_strategy_model(models.Model):

#     symbol = models.CharField(max_length = 221)
#     stock_name = models.CharField(max_length = 221)
#     price = models.DecimalField(max_digits=12, decimal_places=2)

#     def __str__(self):
#         return self.symbol

# class hammer_strategy_model(models.Model):

#     symbol = models.CharField(max_length = 221)
#     stock_name = models.CharField(max_length = 221)
#     price = models.DecimalField(max_digits=12, decimal_places=2)

#     def __str__(self):
#         return self.symbol

class sma44_strategy_model(models.Model):

    symbol = models.CharField(max_length = 221)
    stock_name = models.CharField(max_length = 221)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.symbol


class listedNseCompanies(models.Model):

    symbol = models.CharField(max_length = 221)
    stock_name = models.CharField(max_length = 221)

    def __str__(self):
        return self.symbol


class traded_stock_model(models.Model):

    symbol = models.CharField(max_length = 221)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    target = models.DecimalField(max_digits=12, decimal_places=2)
    stoploss = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.symbol


# class sma44_strategy_v2_model(models.Model):

#     symbol = models.CharField(max_length = 221)
#     stock_name = models.CharField(max_length = 221)
#     price = models.DecimalField(max_digits=12, decimal_places=2)

#     def __str__(self):
#         return self.symbol