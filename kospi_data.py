import requests
from bs4 import BeautifulSoup

import pandas as pd 
from pandas.tseries.offsets import BDay
from datetime import datetime


# KOSPI , KOSDAQ 현재 시세 가져오기 

def get_now_stock_data(target):
    url = f'https://finance.naver.com/sise/sise_index.nhn?code={target}'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    price = soup.select_one('#now_value').text  # 현재 지수 
    
    change_element = soup.select_one('#change_value_and_rate').text.split(' ')
    
    change = change_element[0] # 변동값 
    change_rate = change_element[1][:-2] # 변동률 
    change_yn='상승' # 상승하락 여부 
    if '-' in change_rate: change_yn = '하락'
    
    # 상승이면 위삼각형 + 초록색, 하락이면 아래삼각형 + 빨간색 
    
    if change_yn == '상승':
        color = 'green'
        icon = 'fa fa-sort-asc'
    else : 
        color = 'red'
        icon = 'fa fa-sort-desc'

    pre_date = str(datetime.today()-BDay(1)).split(' ')[0].replace('-','.')[2:] # 변동 기준일 
        
    return [price, change, change_rate, color, icon, pre_date ]

def get_kospi_kosdaq_data():
    kospi = get_now_stock_data('KOSPI')
    kosdaq = get_now_stock_data('KOSDAQ')

    return [kospi,kosdaq]



# 미국, 일본 환율, 유가 금 시세 가져오기 
# 미국 : usd, 일본 : jpy 

def get_exchange_rate():
    url = 'https://finance.naver.com/marketindex/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    result = [] 

    urls=['#exchangeList > li.on > a.head.usd > div > ', '#exchangeList > li > a.head.jpy > div > ']# 미국, 일본 
    urls.append('#oilGoldList > li.on > a.head.wti > div > ') # 유가 
    urls.append('#oilGoldList > li > a.head.gasoline > div > ') # 휘발유

    for url in urls:
        exchange_rate = soup.select_one(url+'span.value').text
        exchange_change = soup.select_one(url+'span.change').text
        exchange_yn = soup.select_one(url+'span.blind').text 

        # 상승이면 위삼각형 + 초록색, 하락이면 아래삼각형 + 빨간색 
        if exchange_yn == '상승':
            color = 'green'
            icon = 'fa fa-sort-asc'
        else : 
            exchange_change = '-' + exchange_change
            color = 'red'
            icon = 'fa fa-sort-desc'

        result.append([ exchange_rate, exchange_change, color, icon ])
    

    exchange_basic = soup.select_one('#exchangeList > li.on > div > span.time').text # 환율 기준 시간 
    result.append(exchange_basic.split(' ')[1])

    # print(result)

    return result 