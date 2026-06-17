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
print(response.text)

