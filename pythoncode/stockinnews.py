# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import re
# import plotly.graph_objects as go
# import numpy as np
# # MoneyControl Web Scraping

# def get_mc_buzz():
#     anchor_tags_list = []
#     href_list = []
#     buzz_stocks_section_list = []
#     buzz_stocks_list = []
#     url = "https://www.moneycontrol.com/news/business/stock"
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#     news_list = soup.find_all("li", {'class': 'clearfix'})


#     for news_section in news_list:
#         anchor_tags = news_section.find('a')
#         anchor_tags_list.append(anchor_tags)

#     for anchor_tag in anchor_tags_list:
#         href = anchor_tag['href']
#         href_list.append(href)


#     for href_link in href_list:
#         if re.search("^https://www.moneycontrol.com/news/photos/business/stocks/buzzing-stocks",href_link):
#             response = requests.get(href_link)
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#             buzz_sections = soup.find_all('span')


#             for buzz_section in buzz_sections:
#                 buzz_stocks_section = buzz_section.find_all('strong')
#                 buzz_stocks_section_list.append(buzz_stocks_section)
#             for each_buzz_stock_section in buzz_stocks_section_list:
#                 for i in each_buzz_stock_section: 
#                     buzz_stocks_list.append(i.text)

#     return buzz_stocks_list

# def get_stock_in_news():
#     # Web Scraping
#     anchor_tags_list = []
#     href_list = []
#     stock_left_sections_list = []
#     stock_anchor_tags_list = []
#     stock_href_list = []
#     stock_names = []
#     url = "https://www.moneycontrol.com/news/business/stock"
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#     news_list = soup.find_all("li", {'class': 'clearfix'})


#     for news_section in news_list:
#         anchor_tags = news_section.find('a')
#         anchor_tags_list.append(anchor_tags)

#     for anchor_tag in anchor_tags_list:
#         href = anchor_tag['href']
#         href_list.append(href)


#     for href_link in href_list:
#         response = requests.get(href_link)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
        
#         stock_left_sections = soup.find_all('div', {'class': 'page_left_wrapper'})
#         stock_left_sections_list.append(stock_left_sections)
        
#     for each_left_section in stock_left_sections_list:
#         for anchor_tag in each_left_section:
#             stock_anchor_tags = anchor_tag.find_all('a')
#             stock_anchor_tags_list.append(stock_anchor_tags)
#     # stock_anchor_tags_list

#     for each_stock_anchor_tag in stock_anchor_tags_list:
#         for href in each_stock_anchor_tag:
#             if(re.search("^https://www.moneycontrol.com/india/stockpricequote/", href['href'])):
#                 stock_href_list.append(href)
#     for stock_name in stock_href_list:
#         stock_names.append(stock_name.text)
    
#     stock_names = list(set(stock_names))
#     #  Buzzing Stocks
#     buzz_stocks = get_mc_buzz()



#     # Adjusting null values 
#     table_length = max(len(stock_names), len(buzz_stocks))

#     if len(stock_names) < table_length:
#         for i in range( table_length - len(stock_names)):
#             stock_names.append("")

#     if len(buzz_stocks) < table_length:
#         for i in range( table_length - len(buzz_stocks)):
#             buzz_stocks.append("")
    
#     # DataFrame
#     stock_in_news = pd.DataFrame(list(zip(stock_names,buzz_stocks)),columns = ['Stock Name','Buzz Stocks'])
#     # Plotly
#     fig = go.Figure(data=[go.Table(
#         header=dict(values=list(stock_in_news.columns),
#                     line_color='#2b3674',
#                     fill_color='#2b3674',
#                     font=dict(color='white', size=20),
#                     align='center'),
#         cells=dict(values= stock_in_news.transpose().values.tolist(),
#                    line_color='#2b3674',
#                    fill_color='white',
#                    font=dict(color='#2b3674', size=20),
#                    align='center',
#                    height=30,
#                    ))
#     ])
    
#     fig.update_layout(
#         autosize=False,
#         margin=dict(
#             l=0,
#             r=0,
#             b=0,
#             t=0.25,
#             pad=0
#         ),
#         paper_bgcolor="white",
#         height=583.013,
#         width=1217.88,
#     )
    
#     table = fig.to_html(config={"displayModeBar": False})
 
#     return table , len(stock_names)


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import plotly.graph_objects as go
import numpy as np
import concurrent.futures

def get_mc_buzz():
    def fetch_page(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return ""

    anchor_tags_list = []
    href_list = []
    buzz_stocks_section_list = []
    buzz_stocks_list = []
    url = "https://www.moneycontrol.com/news/business/stock"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    news_list = soup.find_all("li", {'class': 'clearfix'})

    for news_section in news_list:
        anchor_tags = news_section.find('a')
        anchor_tags_list.append(anchor_tags)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        href_list = list(executor.map(lambda tag: tag['href'], anchor_tags_list))

    for href_link in href_list:
        if re.search("^https://www.moneycontrol.com/news/photos/business/stocks/buzzing-stocks", href_link):
            response_text = fetch_page(href_link)
            if response_text:
                soup = BeautifulSoup(response_text, 'html.parser')
                buzz_sections = soup.find_all('span')
                for buzz_section in buzz_sections:
                    buzz_stocks_section = buzz_section.find_all('strong')
                    buzz_stocks_section_list.append(buzz_stocks_section)
                for each_buzz_stock_section in buzz_stocks_section_list:
                    for i in each_buzz_stock_section:
                        buzz_stocks_list.append(i.text)

    return buzz_stocks_list

def get_stock_in_news():
    def fetch_page(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return ""

    anchor_tags_list = []
    href_list = []
    stock_left_sections_list = []
    stock_anchor_tags_list = []
    stock_href_list = []
    stock_names = []
    url = "https://www.moneycontrol.com/news/business/stock"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    news_list = soup.find_all("li", {'class': 'clearfix'})

    for news_section in news_list:
        anchor_tags = news_section.find('a')
        anchor_tags_list.append(anchor_tags)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        href_list = list(executor.map(lambda tag: tag['href'], anchor_tags_list))

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        response_texts = list(executor.map(fetch_page, href_list))

    for response_text in response_texts:
        if response_text:
            soup = BeautifulSoup(response_text, 'html.parser')
            stock_left_sections = soup.find_all('div', {'class': 'page_left_wrapper'})
            stock_left_sections_list.append(stock_left_sections)

    for each_left_section in stock_left_sections_list:
        for anchor_tag in each_left_section:
            stock_anchor_tags = anchor_tag.find_all('a')
            stock_anchor_tags_list.append(stock_anchor_tags)

    for each_stock_anchor_tag in stock_anchor_tags_list:
        for href in each_stock_anchor_tag:
            if(re.search("^https://www.moneycontrol.com/india/stockpricequote/", href['href'])):
                stock_href_list.append(href)

    for stock_name in stock_href_list:
        stock_names.append(stock_name.text)

    stock_names = list(set(stock_names))

    buzz_stocks = get_mc_buzz()

    table_length = max(len(stock_names), len(buzz_stocks))

    if len(stock_names) < table_length:
        stock_names.extend([""] * (table_length - len(stock_names)))

    if len(buzz_stocks) < table_length:
        buzz_stocks.extend([""] * (table_length - len(buzz_stocks)))

    stock_in_news = pd.DataFrame(list(zip(stock_names, buzz_stocks)), columns=['Stock Name', 'Buzz Stocks'])

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(stock_in_news.columns),
                    line_color='#2b3674',
                    fill_color='#2b3674',
                    font=dict(color='white', size=20),
                    align='center'),
        cells=dict(values=stock_in_news.transpose().values.tolist(),
                   line_color='#2b3674',
                   fill_color='white',
                   font=dict(color='#2b3674', size=20),
                   align='center',
                   height=30,
                   ))
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

    return table, len(stock_names)
