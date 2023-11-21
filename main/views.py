from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import yfinance as yf
import concurrent.futures
import decimal
import requests
from urllib.request import urlopen 
from datetime import date
from dateutil.relativedelta import relativedelta

from .models import rsi_strategy_model
# from .models import two_percent_strategy_model
# from .models import hammer_strategy_model
from .models import sma44_strategy_model
from .models import listedNseCompanies
from .models import traded_stock_model
# from .models import sma44_strategy_v2_model
import sys

python_code_path = "C://Users//Jenil Shah//Desktop//StockGrow//Stock_Filter//pythoncode"
sys.path.insert(1,python_code_path)

import niftychart

import strategy_testing

import ipo

import stockinnews

import sector_indices


# Request limiter
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
# class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
#     pass


     



def Home(request):
    chart,details= niftychart.get_nifty_chart()
    gain_tree_map,loss_tree_map = sector_indices.get_sectorial_indices()
    return render(request, 'Home.html',{
        "title" : 'Home',
        'chart' : chart,
        'open' : details['day_open'],
        'close' : details['day_close'],
        'high' : details['day_high'],
        'low' : details['day_low'],
        'gainTreemap': gain_tree_map,
        'lossTreemap': loss_tree_map,
    })


def VirtualTrade(request,stock):   
    if(request.method == "POST"):
        if(request.POST['stock_action'] == "BUY"):
            stock_symbol = request.POST["stock_symbol"]
            quantity = request.POST['quantity']
            price = decimal.Decimal(request.POST['price'])
            target = decimal.Decimal(request.POST['target'])
            stoploss = decimal.Decimal(request.POST['stoploss'])
            print(target)
            instance = traded_stock_model(
                symbol =stock_symbol,
                quantity = quantity,
                price = price,
                target = target,
                stoploss = stoploss
            )
            instance.save()

        # if(request.POST['stock_action'] == "BUY"):


    if(stock == 'all'):
        nse_stocks = listedNseCompanies.objects.all().values()
    else:
        nse_stocks = listedNseCompanies.objects.filter(stock_name__contains = stock)
    
    return render(request,'VirtualTrade.html',{
        "title" : "VirtualTrade",
        'stocks' : nse_stocks,
    })

def fetch_portfolio_stock_data(dictionary):
    ticker = yf.Ticker(dictionary['symbol'] + ".NS")
    historical_data = ticker.history(period="1d")
    price = round(historical_data['Close'].iloc[-1], 2)
    dictionary['ltp'] = price
    dictionary['invested_amt'] = round(price * int(dictionary['quantity']),2)
    return dictionary

def Portfolio(request):
    portfolio_stocks_data = traded_stock_model.objects.all().values()
    
    # Use ThreadPoolExecutor for parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers= 4) as executor:
        portfolio_stocks_data = list(executor.map(fetch_portfolio_stock_data, portfolio_stocks_data))
    
    return render(request, 'Portfolio.html', {
        "title": "Portfolio",
        "portfolio_stocks": portfolio_stocks_data,
    })


def Strategy_Testing(request,pk,stock):
    strategy = pk
    stock=stock
    if(strategy == "rsi_14"):
        table ,size= strategy_testing.rsi_14(stock)
        return render(request,'StrategyTesting.html',{
            "title" : 'Strategy Testing',
            "table" : table,
            "number_of_stocks" : size,
            'strategy': 'rsi_14'
        })
    elif(strategy == "2percent"):
        table, size= strategy_testing.two_percent(stock)
        return render(request,'StrategyTesting.html',{
            "title" : 'Strategy Testing',
            "table" : table,
            "number_of_stocks" : size,
            "strategy" : "2percent"
        })
    # elif(strategy == "hammer"):
    #     table, size= strategy_testing.hammerCandle()
    #     return render(request,'StrategyTesting.html',{
    #         "title" : 'Strategy Testing',
    #         "table" : table,
    #         "number_of_stocks" : size
    #     })
    elif(strategy == "sma_44" ):
        table, size= strategy_testing.sma44support(stock)
        return render(request,'StrategyTesting.html',{
            "title" : 'Strategy Testing',
            "table" : table,
            "number_of_stocks" : size,
            'strategy': "sma_44"
        })
    elif(strategy  == "sma_44_v2"):
        table,size = strategy_testing.sma44supportVersion(stock)
        return render(request,"StrategyTesting.html",{
            'title': 'Strategy Testing',
            "table": table,
            "number_of_stocks": size,
        })
    elif(strategy == 'main' and stock == 'none'):
        return render(request,'StrategyTesting.html',{"title" : 'Strategy Testing'})

def SIN(request):
    table ,size = stockinnews.get_stock_in_news()
    return render(request,'SIN.html',{
        "title" : 'Stocks In News',
        "table" : table,
        "number_of_stocks" : size
    })

def IPO(request):
    table = ipo.get_ipo_details()
    return render(request,'IPO.html',{
        "title" : 'IPO',
        "table" : table
    })

def About(request):
    return render(request,'About.html',{"title" : 'About'})


def Data(request):
    return render(request, 'processData.html')



def ProcessData(request):

    def calc_rsi(data):
        data['Change'] = data['Close'].diff()
        gain = data['Change'].apply(lambda x: x if x > 0 else 0)
        loss = data['Change'].apply(lambda x: abs(x) if x < 0 else 0)
        avg_gain = gain.ewm(com=13,min_periods=14).mean()
        avg_loss = loss.ewm(com=13, min_periods=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.values


    def rsi_strategy(data):
        rsi_data = calc_rsi(data)
        if rsi_data[-1] >= 35 and rsi_data[-2] < 35:
            return True

    # def two_percent_strategy(data):
    #     return (
    #         (data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1] * 100 >= 2
    #     )
    

    # def sma44_strategy_v(data):
    #     today_open = data['Open'].iloc[-1]
    #     today_close = data['Close'].iloc[-1]
    #     today_high = data['High'].iloc[-1]
    #     today_low = data['Low'].iloc[-1]
    #     prev_close = data['Close'].iloc[-2]
    #     prev_open = data['Open'].iloc[-1]
    #     prev_high = data['High'].iloc[-2]
    #     prev_low = data['Low'].iloc[-1]

    #     prev_candle_mid = (prev_close - prev_close)/2
    #     moving_average_44 = data['Close'].rolling(window=44).mean()

    #     if (today_close > today_open) and (today_low == today_open) and (today_open < moving_average_44.iloc[-1] < today_close):
    #         return True
    #     elif (prev_close > prev_open) and (today_close > today_open) and (prev_low * 0.995 < moving_average_44.iloc[-2] < prev_open * 1.008) and ( today_open >= prev_candle_mid  and today_close >= prev_close ):
    #         return True




    # def hammer_strategy(data):
    #     red_lower_wick = data['Close'].iloc[-1] - data['Low'].iloc[-1]
    #     red_upper_wick = data['High'].iloc[-1] - data['Open'].iloc[-1]
    #     green_upper_wick = data['High'].iloc[-1] - data['Close'].iloc[-1]
    #     green_lower_wick = data['Close'].iloc[-1] - data['Low'].iloc[-1]
    #     body = abs(data['Close'].iloc[-1] - data['Open'].iloc[-1])
    #     if data['Close'].iloc[-1] < data['Open'].iloc[-1]:
    #         return red_lower_wick >= 2 * body and red_upper_wick / data['Open'].iloc[-1] <= 0.005
    #     elif data['Close'].iloc[-1] > data['Open'].iloc[-1]:
    #         return green_lower_wick >= 2 * body and green_upper_wick / data['Close'].iloc[-1] <= 0.005
    #     return False



    def sma44_strategy(data):
        rsi_data = calc_rsi(data)
        moving_average_44 = data['Close'].rolling(window=44).mean()
        data['rsi'],data['sma_44'] = rsi_data , moving_average_44.values
        data.reset_index(inplace = True)

        for i in range(0,len(data)):
            today_open = data['Open'].iloc[-1]
            today_close = data['Close'].iloc[-1]
            today_high = data['High'].iloc[-1]
            today_low = data['Low'].iloc[-1]
            prev_close = data['Close'].iloc[-2]
            prev_open = data['Open'].iloc[-2]
            prev_high = data['High'].iloc[-2]
            prev_low = data['Low'].iloc[-2]
            prev_candle_mid = (prev_close - prev_open)/2
            if (today_close > today_open) and (today_low == today_open) and (today_open < data['sma_44'].iloc[-1] < today_close) and data['rsi'].iloc[-1] > 55:
                    # sma_stocks.append(stock_symbol)
                    return True
            elif (prev_close > prev_open) and (today_close > today_open) and (prev_low * 0.995 < data['sma_44'].iloc[-2] < prev_open * 1.008) and ( today_open >= prev_candle_mid  and today_close >= prev_close ) and data['rsi'].iloc[-1] > 55:
                    # sma_stocks.append(stock_symbol)
                    return True
            elif (today_close > today_open) and (today_low * 0.995 < data['sma_44'].iloc[i] < today_close * 1.008) and ((((today_close - today_open)/today_open)*100) >=2) and data['rsi'].iloc[-1] > 55 :
                    # sma_stocks.append(stock_symbol)
                    return True
            else:
                continue



    # with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    #     for strategy in strategies:
    #         strategy_results = list(executor.map(lambda symbol: process_stock(symbol, strategy), stock_symbols))
    #         results[strategy.__name__] = strategy_results
    #         results[strategy.__name__] = [r for r in results[strategy.__name__]  if r is not None]
    #         results[strategy.__name__].sort(key=lambda x: x['price'])
    # Store results in the database (you can optimize this part as needed)

    # <<<< Modified main >>>>>>
    nse_stocks = pd.read_csv(r'C:\Users\Jenil Shah\Desktop\StockGrow\Stock_Filter\pythoncode\nse_final.csv')
    stock_symbols = nse_stocks['Symbol'].to_numpy()

    
    strategies = [rsi_strategy,sma44_strategy]

    results = {strategy.__name__: [] for strategy in strategies}

    
    for symbol in stock_symbols:
        try:
            # ticker = yf.Ticker(symbol + ".NS")
            # data = ticker.history(period = '1y')
            
            end_date = date.today()
            start_date = end_date - relativedelta(years=1)

            data = yf.download(symbol+'.NS', start = str(start_date), end = str(end_date), interval = "1wk")
            # data.drop(columns=['Stock Splits','Dividends'], axis = 0, inplace = True)
            for strategy in strategies:
                if strategy(data):
                    print("done")
                    results[strategy.__name__].append({
                            'symbol': symbol,
                            # 'name': ticker.info['shortname'],
                            'name': "temp",
                            'price': data['Close'].iloc[-1],
                        })
                else:
                    continue
                results[strategy.__name__] = [r for r in results[strategy.__name__]  if r is not None]
                results[strategy.__name__].sort(key=lambda x: x['price'])
            # time.sleep(2.7)
        except Exception as e:
            print(f' Error fetxhing {symbol} : {e}')
            # time.sleep(2.5)



    for strategy in results.keys():
        if strategy == 'rsi_strategy':
            temp_data = rsi_strategy_model.objects.all()
            if temp_data.exists():
                temp_data.delete()
                for i in results[strategy]:
                    instance = rsi_strategy_model(
                        symbol = i['symbol'],
                        stock_name = i['name'],
                        price = i['price'],
                    )
                    instance.save()
            else:
                for i in results[strategy]:
                    instance = rsi_strategy_model(
                        symbol = i['symbol'],
                        stock_name = i['name'],
                        price = i['price'],
                    )
                    instance.save()


        # if strategy == 'two_percent_strategy':
        #     temp_data = two_percent_strategy_model.objects.all()
        #     if temp_data.exists():
        #         temp_data.delete()
        #         for i in results[strategy]:
        #             instance = two_percent_strategy_model(
        #                 symbol = i['symbol'],
        #                 stock_name = i['name'],
        #                 price = i['price'],
        #             )
        #             instance.save()
        #     else:
        #         for i in results[strategy]:
        #             instance = two_percent_strategy_model(
        #                 symbol = i['symbol'],
        #                 stock_name = i['name'],
        #                 price = i['price'],
        #             )
        #             instance.save()


        # if strategy == 'hammer_strategy':
        #     temp_data = hammer_strategy_model.objects.all()
        #     if temp_data.exists():
        #         temp_data.delete()
        #         for i in results[strategy]:
        #             instance = hammer_strategy_model(
        #                 symbol = i['symbol'],
        #                 stock_name = i['name'],
        #                 price = i['price'],
        #             )
        #             instance.save()
        #     else:
        #         for i in results[strategy]:
        #             instance = hammer_strategy_model(
        #                 symbol = i['symbol'],
        #                 stock_name = i['name'],
        #                 price = i['price'],
        #             )
        #             instance.save()


        if strategy == 'sma44_strategy':
            temp_data = sma44_strategy_model.objects.all()
            if temp_data.exists():
                temp_data.delete()
                for i in results[strategy]:
                    instance = sma44_strategy_model(
                        symbol = i['symbol'],
                        stock_name = i['name'],
                        price = i['price'],
                    )
                    instance.save()
            else:
                for i in results[strategy]:
                    instance = sma44_strategy_model(
                        symbol = i['symbol'],
                        stock_name = i['name'],
                        price = i['price'],
                    )
                    instance.save()


        
        # if strategy == 'sma44_strategy_v':
        #     temp_data = sma44_strategy_v2_model.objects.all()
        #     if temp_data.exists():
        #         temp_data.delete()
        #         for i in results[strategy]:
        #             instance = sma44_strategy_v2_model(
        #                 symbol = i['symbol'],
        #                 stock_name = i['name'],
        #                 price = i['price'],
        #             )
        #             instance.save()
        #     else:
        #         for i in results[strategy]:
        #             instance = sma44_strategy_v2_model(
        #                 symbol = i['symbol'],
        #                 stock_name = i['name'],
        #                 price = i['price'],
        #             )
        #             instance.save()
            
    return HttpResponse("Data is processed successfully")



def UploadData(request):

    nse_stocks = pd.read_csv(r'C:\Users\Jenil Shah\Desktop\StockGrow\Stock_Filter\pythoncode\nse_final.csv')
    if listedNseCompanies.objects.all().exists():
        listedNseCompanies.objects.all().delete()
    for i in range(len(nse_stocks)):
        instance = listedNseCompanies(
            symbol = nse_stocks['Symbol'].iloc[i],
            stock_name = nse_stocks['Company Name'].iloc[i]
        )
        instance.save()
    return HttpResponse('DONE')