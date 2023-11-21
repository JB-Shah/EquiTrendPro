import pandas as pd
import yfinance as yf
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def get_nifty_chart():
    ticker = yf.Ticker("^NSEI")
    historical_data = ticker.history(period = "1d",interval='2m')
    date = historical_data.index.to_numpy()
    close_prices = historical_data['Close'].to_numpy()
    # fig = px.line(
    #     x = date,
    #     y = close_prices,
    # )
    # # --- Updating Layout ---
    # fig.update_traces(line_color='#2b3674')
    fig = go.Figure(data=[go.Candlestick(x=date,
                open=historical_data['Open'],
                high=historical_data['High'],
                low=historical_data['Low'],
                close=historical_data['Close'])])
    # fig.update_xaxes(visible=False)
    # fig.update_yaxes(visible=False)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_yaxes(autorange=True)
    fig.update_layout(annotations=[], overwrite=True,plot_bgcolor="white",xaxis_title = None,yaxis_title = None)

    # --- Chart --
    chart = fig.to_html(config = {"displayModeBar" : False})
    
    day_open = round(historical_data['Open'].iloc[0],2)
    day_close = round(historical_data['Close'].iloc[-1],2)
    day_high = round(historical_data['High'].max(),2)
    day_low = round(historical_data['Low'].min(),2)

    nifty_details = {
        'day_open' : day_open,
        'day_close' : day_close,
        'day_high' : day_high,
        'day_low' : day_low
    }
    return chart,nifty_details