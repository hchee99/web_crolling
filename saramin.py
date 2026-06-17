import requests
from bs4 import BeautifulSoup

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

# import time
import pandas as pd
import re
# from tqdm import tqdm

#'헤더' -> 브라우저가 서버에 무언가 요청할때 
# 나 이런 브라우저에요 라는 내용
base_url ='https://www.saramin.co.kr/zf_user/search'
headers = {
    #요청하는 브라우저의 종류
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    #요청하는 언어의 종류
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}
#리퀘스트를 보냄
#headers : 웹페이지에 정보를 요청하는 브라우저에 대한 내용
#params : 웹페이지에 이런 정보를 요청합니다 '검색어, 검색조건'
#timeout : 웹페이로부터 회신이 올 때 까지 기다리는 시간 최대치
response = requests.get(base_url, headers=headers,
                        params = {'searchword':"AI"},
                        timeout = 10)

#만약 response가 <200>이라면 -> 정상
soup = BeautifulSoup(response.text,'html.parser')
# print(response.text)

# 검색 결과
rows = []

# find : 전통적인 선택 방식
# select : 현대적인 선택 방식
# soup.select(구분자) : '구분자"가 들어가는 모든 내용을 select(선택)
# soup.find_all('div', class = 'item_recruit')
for item in soup.select('div.item_recruit'):

    #1. 회사명
    #select_one(구분자) : 구분자 이름을 갖는 딱 하나만 가져와
    corp_name = item.select_one('div.area_corp')

    #2. 채용 정보
    job_area = item.select_one('div.area_job')

    #3. 공고 제목
    #<div>로 시작하지 않음 .job_tit/div가 아니어도 괜찮아!
    #job_tit이라는 녀석을 찾아서 one 한개만 가져와!
    job_title = job_area.select_one('.job_tit')

    #4. 조건
    conditions = job_area.select_one('.job_condition')
    location = ''
    condition1 = ''

    if conditions :
        span = conditions.select('span')

        if len(span) > 0:
            location = span[0].get_text(strip = True)

        if len(span) >1:
            condition1 = span[1].get_text(strip = True)
        
    #5. 직무 분야
    job_sector = job_area.select_one('.job_sector')
    job_sector = (job_sector.get_text(strip = True) if job_sector else "")

    rows.append({
        '공고 이름' : job_title,
        '회사 위치' : location,
        '조건 1' : condition1,
        '조건 2' : job_sector,
        '회사 이름' : corp_name
    })


df = pd.DataFrame(rows)
print(df)