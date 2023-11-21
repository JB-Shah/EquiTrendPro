import yfinance as yf
import pandas as pd
import plotly.express as px
import concurrent.futures

def get_sectorial_indices():
    gaining_sector = []
    losing_sector = []

    sectorial_indices = [
        ("^NSEBANK", "Nifty Bank"),
        ("^CNXAUTO", "Nifty Auto"),
        ("NIFTY_FIN_SERVICE.NS", "Nifty Financial Services"),
        ("^CNXFMCG", "Nifty FMCG"),
        ("^CNXIT", "Nifty IT"),
        ("^CNXMETAL", "Nifty Metal"),
        ("^CNXPSUBANK", "Nifty PSU Bank"),
        ("^CNXMEDIA", "Nifty Media"),
        ("^CNXPHARMA","Nifty Pharma"),
        ("HDFCPVTBAN.NS","Nifty Pvt Bank"),
        ("^CNXREALTY","Nifty Realty"),
        ("NIFTY_HEALTHCARE.NS","Nifty HealthCare"),
        ("NIFTY_OIL_AND_GAS.NS","Nifty Oil & Gas"),
    ]

    def fetch_sector_data(sector_symbol, sector):
        ticker = yf.Ticker(sector_symbol)
        data = ticker.history(period="1d")
        calc_growth = round(((data["Close"].values[0] - data["Open"].values[0]) / data["Open"].values[0]) * 100, 2)
        if calc_growth > 0 or calc_growth < 0:
            return (sector, calc_growth)
        # elif calc_growth < 0:
        #     return (sector, abs(calc_growth))
        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        sector_data = list(executor.map(lambda x: fetch_sector_data(x[0], x[1]), sectorial_indices))
    
    sector_data = [data for data in sector_data if data is not None]
    data_gain = [data for data in sector_data if data[1] > 0 ]
    data_loss = [(data[0],abs(data[1])) for data in sector_data if data[1] < 0]
    print(data_loss)
    gain_df = pd.DataFrame(data_gain, columns=["Sector", "Growth Area"])
    loss_df = pd.DataFrame(data_loss, columns=["Sector", "Growth Area"])

    fig_gain = px.treemap(gain_df, path=['Sector'], values='Growth Area', hover_name='Growth Area')
    fig_loss = px.treemap(loss_df, path=['Sector'], values='Growth Area', hover_name='Growth Area')

    for fig in [fig_gain, fig_loss]:
        fig.update_layout(
            autosize=False,
            margin=dict(l=0, r=0, b=0, t=0, pad=0),
            height=400.013,
            width=400.94,
            treemapcolorway=['green'] if fig == fig_gain else ['red'],
        )

    gain_treemap = fig_gain.to_html(config={"displayModeBar": False})
    loss_treemap = fig_loss.to_html(config={"displayModeBar": False})
    
    return gain_treemap, loss_treemap



# import yfinance as yf
# import pandas as pd
# import plotly.express as px

# def get_sectorial_indices():
#     gaining_sector = []
#     losing_sector = []

#     sectorial_indices = [
#         ("^NSEBANK", "Nifty Bank"),
#         ("^CNXAUTO", "Nifty Auto"),
#         ("NIFTY_FIN_SERVICE.NS", "Nifty Financial Services"),
#         ("^CNXFMCG", "Nifty FMCG"),
#         ("^CNXIT", "Nifty IT"),
#         ("^CNXMETAL", "Nifty Metal"),
#         ("^CNXPSUBANK", "Nifty PSU Bank"),
#         ("^CNXMEDIA", "Nifty Media"),
#         ("^CNXPHARMA","Nifty Pharma"),
#         ("HDFCPVTBAN.NS","Nifty Pvt Bank"),
#         ("^CNXREALTY","Nifty Realty"),
#         ("NIFTY_HEALTHCARE.NS","Nifty HealthCare"),
#         ("NIFTY_OIL_AND_GAS.NS","Nifty Oil & Gas"),
#     ]

#     for sector_symbol, sector in sectorial_indices:
#         ticker = yf.Ticker(sector_symbol)
#         data = ticker.history(period="1d")
#         calc_growth = round(((data["Close"].values[0] - data["Open"].values[0]) / data["Open"].values[0]) * 100, 2)
#         if calc_growth > 0:
#             gaining_sector.append((sector, calc_growth))
#         elif calc_growth < 0:
#             losing_sector.append((sector, abs(calc_growth)))

    
#     gain_df = pd.DataFrame(gaining_sector, columns=["Sector", "Growth Area"])
#     loss_df = pd.DataFrame(losing_sector, columns=["Sector", "Growth Area"])

#     fig_gain = px.treemap(gain_df, path=['Sector'], values='Growth Area', hover_name='Growth Area')
#     fig_loss = px.treemap(loss_df, path=['Sector'], values='Growth Area', hover_name='Growth Area')

#     for fig in [fig_gain, fig_loss]:
#         fig.update_layout(
#             autosize=False,
#             margin=dict(l=0, r=0, b=0, t=0, pad=0),
#             height=400.013,
#             width=400.94,
#             treemapcolorway=['green'] if fig == fig_gain else ['red'],
#         )

#     gain_treemap = fig_gain.to_html(config={"displayModeBar": False})
#     loss_treemap = fig_loss.to_html(config={"displayModeBar": False})
    
#     return gain_treemap, loss_treemap
