import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_date(day):
    
    # 오늘 날짜 정보 추가 
    now = datetime.strptime(day, '%Y.%m.%d')
                                           
    month_names = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December']
    
    month_name = month_names[now.month-1]
    day = now.day 
    
    return month_name, str(day)[-2:]


def get_news():

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('http://www.paxnet.co.kr/news/ipo',headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    lis = soup.select('#contents > div.cont-area > div.board-thumbnail > ul > li')

    result = [] 
    
    # 뉴스 크롤링 
    for li in lis:
        day = li.find("dl", class_="text")

        if day == None : continue

        text = day.text.split('\n')
        
        title = text[1]
        body = text[2]+'...'
        url = 'http://www.paxnet.co.kr' + day.select_one('a')['href']
        url = url.replace('¤', '&curren')
        company = text[-4] + ' ' + text[-3][-5:]
        
        date = text[-3].split(' ')[0]
        month, day = get_date(date)
        
        result.append([title,body, url,company,month,day]) 

    return result 