
from datetime import date ,datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def get_ipo_details():
    # Intializin URL
    url = "https://www.moneycontrol.com/ipo/ipo-snapshot/issues-open.html"
    # Getting Response
    response = requests.get(url)
    
    # Checking Response Stauts
    if response.status_code != 200:
        print("Failed to fetch the webpage")
        return None

    # Parsing HTML code
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting required data
    ipo_data = []
    ipo_table = soup.find('table', {'class': 'tablesorter'})

    if ipo_table:
        rows = ipo_table.find_all('tr')
        headers = [header.text.strip() for header in rows[0].find_all('th')]
        for row in rows[1:]:
            columns = row.find_all('td')
            company_name = columns[0].a
            ipo_link = "https://www.moneycontrol.com" + company_name['href']
            company_name = f'<a href="{ipo_link}">{company_name.text.strip()}</a>'
            
            ipo_data.append({
                'Company Name': company_name,
                'Open Date': columns[6].text.strip().replace('-'," ") ,
                'Close Date':columns[7].text.strip().replace('-'," ") ,
                'Offer Price': columns[4].text.strip(),
                'Lot Size': columns[5].text.strip(),
            })
    # Sorting data
    ipo_data.sort(key=lambda x: x['Open Date'], reverse = True) 

    # Dictionary to DataFrame
    ipo_df = pd.DataFrame(ipo_data)
    



    # Ploty Table
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(ipo_df.columns),
                    line_color='#2b3674',
                    fill_color='#2b3674',
                    font=dict(color='white', size=20),
                    align='left'),
        cells=dict(values=ipo_df.transpose().values.tolist(),
                   line_color='#2b3674',
                   fill_color= 'white',
                   font=dict(color='#2b3674', size=20),
                   align='left',
                   height=30))
    ])

    fig.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, b=0, t=0.25, pad=0),
        paper_bgcolor="white",
        height=583.013,
        width=1217.88,
    )

    table = fig.to_html(config={"displayModeBar": False})
    return table