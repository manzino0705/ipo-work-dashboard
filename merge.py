from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import datetime


def get_merge():
    chrome_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 헤드리스 모드로 실행
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get("https://kind.krx.co.kr/common/stockschedule.do?method=StockScheduleMain&index=7")
    time.sleep(5)

    table = driver.find_element(By.XPATH, "//*[@id='contents']/article/table")
    df = pd.read_html(table.get_attribute('outerHTML'))[0]
    datas = df.values.tolist()

    driver.quit()

    result = [] 
    today = datetime.date.today()


    for data in datas:
        m_number = data[0].split('-')[1]
        if int(m_number) < int(today.month) : continue # 이번달 내용만 가져옴 
        # 월 
        months = { '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May',
                   '06': 'Jun', '07': 'Jul',  '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec' }
        
        month = months[m_number]

        # 요일 
        day = data[0].split('-')[2]
        # if int(day) < int(today) : continue  # 오늘 이후 일정만 가져옴 

        # 분할/합병 - 회사명 
        merge = data[2]
        com = data[1] # 회사명

        # 분할설정회사 
        m_com = data[3]

        result.append([month,day,merge+'-'+com, merge+'설정회사: '+m_com])

    return result 
        
# result = get_merge()
# print(result)
# 분할일, 회사명, 구분, 분할설정회사(합병상대회사), 주총예정일