from django.urls import path 
from . import views
urlpatterns = [
    path('',views.Home),
    path('Home',views.Home),
    path('Strategy_Testing/<str:pk>/search^<str:stock>',views.Strategy_Testing,name='strategy_testing'),
    # path('Strategy_Testing/main/none',views.Strategy_Testing),
    path('SIN',views.SIN),
    path('IPO',views.IPO),
    path('About',views.About),
    path('Data',views.Data),
    path('Data/processData',views.ProcessData),
    path('portfolio',views.Portfolio,name="portfolio"),
    path('virtual_trade/<str:stock>',views.VirtualTrade),
    # path('<str:page>/<str:strategy>/<str:stock>',views.searchStocks,name = "search_complete"),
    path('Data/uploadData',views.UploadData),
]