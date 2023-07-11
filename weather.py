import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_weather():
    # 날씨 예보 페이지 URL
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=영등포구+날씨+"

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    
    result = [] 
    
    # 현재 날씨 정보가 포함된 요소 찾기 
    now_weather = soup.select('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today')
 
    now_day = str(datetime.now()).split(' ')[0] # 오늘의 요일
    now_day = datetime.strptime(now_day, '%Y-%m-%d')
    
    dateDict = {0: 'MONDAY', 1:'TUESDAY', 2:'WEDNESDAY', 3:'THURSDAY', 4:'FRIDAY', 5:'SATURDAY', 6:'SUNDAY'}
    now_day = dateDict[now_day.weekday()]

    now_figure = now_weather[0].find("span", class_="blind").text
    now_tem = now_weather[0].find("strong").text[-5:-1]
    now_time = str(datetime.now()).split(' ')[1][:8]
    
    # 일주일 동안의 날씨 정보가 포함된 요소 찾기
    weather_elements = soup.select('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.content_area > div.inner > div > div.list_box._weekly_weather > ul > li ')
    
    # 일주일 동안의 날씨 정보 크롤링 
    for element in weather_elements:
        day = element.find("span", class_="date").text.strip()[:-1] # 날짜
        figure = element.find("span", class_= "blind").text
        low = element.find("span", class_= "lowest").text[4:6] # 최저기온
        high = element.find("span", class_= "highest").text[4:6] # 최고기온
        icon = 'icon'+str(weather_elements.index(element)+1)
        
        result.append([day,figure,low,high,icon])
        
        if len(result) > 6 :
            break 
    
    # 오늘 날씨 정보 추가 
    now_element=[now_day, now_figure,now_tem,now_time] # 날짜, 날씨, 기온, 시간 
    result.append(now_element)
    
    # html 반영을 위한 코드처리 
    for r in result : 
        if r[1] == '맑음' : r[1]='CLEAR_DAY'
        elif '구름' in r[1] and '맑음' in r[1] : r[1] ='PARTLY_CLOUDY_DAY' 
        elif r[1] == '구름많음' : r[1]='CLOUDY'
        elif '안개' in r[1] : r[1]='FOG'
        elif r[1] == '흐림' : r[1]='CLOUDY'
        elif '비' in r[1] : r[1]='RAIN'
        elif '바람' in r[1] : r[1] ='WIND'
        elif '눈' in r[1] : r[1]='SNOW'
        else : r[1] = 'CLEAR_DAY'
        
        r[1] = 'Skycons.'+r[1]

    # print(result)
    return result 

# result = get_weather()
