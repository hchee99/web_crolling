#인터넷 요청 -> requests
import requests
#정적 웹페이지 크롤링 -> bs
from bs4 import BeautifulSoup
#동적 웹페이지 크롤링
from selelnium import webdriver

#시간 라이브러리
import time
#진행률을 표시하는 라이브러리 +for문
from tqdm import tqdm

#크롤링한 내용을 엑셀 파일로 저장하기 위해서
#xlsx -> openpy1(파이썬으로 엑셀 컨트롤)
#csv -> pandas를 사용
import pandas as pd


url = 'https://www.cheongwon.go.kr/portal/petition/open/view?'

response = requests.get(url)
print(response)