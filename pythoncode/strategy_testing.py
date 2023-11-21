import pandas as pd
import yfinance as yf
import concurrent.futures
import plotly.graph_objects as go

from main.models import rsi_strategy_model
# from main.models import two_percent_strategy_model
from main.models import sma44_strategy_model
# from main.models import sma44_strategy_v2_model

def generateTable(results):
    table_data = {
        'Sr.NO': list(range(1, len(results) + 1)),
        'Symbol': [f'<a href="https://in.tradingview.com/chart/XAEVDngh/?symbol={r.symbol}">{r.symbol}</a>' for r in results],
        'Stock': [r.stock_name for r in results],
        'Price': [r.price for r in results],
    }
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=[f'<b>{key}</b>' for key in table_data.keys()],
                    line_color='#2b3674',
                    fill_color='#2b3674',
                    font=dict(color='white', size=20),
                    align='left'),
        cells=dict(values=list(table_data.values()),
                   line_color='#2b3674',
                   fill_color='white',
                   font=dict(color='#2b3674', size=20),
                   align='left',
                   height=30,
                   ),
        columnwidth = [1,3,6,1.25],)
    ])
    
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0.25,
            pad=0
        ),
        paper_bgcolor="white",
        height=583.013,
        width=1217.88,
    )
    
    table = fig.to_html(config={"displayModeBar": False})
    return table ,len(results)



# def sma44supportVersion(stock):
    if(stock == 'all'):
        results = sma44_strategy_v2_model.objects.all()
        table ,size = generateTable(results)
        return table ,size 
    else:
        results = sma44_strategy_v2_model.objects.filter(stock_name__contains = stock)
        table ,size = generateTable(results)
        return table ,size 


def rsi_14(stock):
    if(stock == 'all'):
        results = rsi_strategy_model.objects.all()
        # results = [r for r in results if r is not None]  # Remove None values
        # results.sort(key=lambda x: x['price'])  # Sort by price
        
        table ,size = generateTable(results)
        return table ,size 
    else:
        results = rsi_strategy_model.objects.filter(stock_name__contains = stock)
        table ,size = generateTable(results)
        return table ,size 


# def two_percent(stock):
    if(stock == 'all'):
        results = two_percent_strategy_model.objects.all()
        table ,size = generateTable(results)
        return table ,size 
    else:
        results = two_percent_strategy_model.objects.filter(stock_name__contains = stock)
        table ,size = generateTable(results)
        return table ,size 





def sma44support(stock):
    if(stock == 'all'):
        results = sma44_strategy_model.objects.all()
        table ,size = generateTable(results)
        return table ,size 
    else:
        results = sma44_strategy_model.objects.filter(stock_name__contains = stock)
        table ,size = generateTable(results)
        return table ,size 


