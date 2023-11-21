from django.contrib import admin

from .models import rsi_strategy_model
# from .models import two_percent_strategy_model
# from .models import hammer_strategy_model
from .models import sma44_strategy_model
# from .models import sma44_strategy_v2_model
from .models import listedNseCompanies
from .models import traded_stock_model


# Register your models here.
admin.site.register(rsi_strategy_model)
# admin.site.register(two_percent_strategy_model)
# admin.site.register(hammer_strategy_model)
admin.site.register(sma44_strategy_model)
admin.site.register(listedNseCompanies)
admin.site.register(traded_stock_model)
# admin.site.register(sma44_strategy_v2_model)
