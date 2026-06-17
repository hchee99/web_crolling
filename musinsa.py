import requests
from bs4 import beautifulSoup

from selenium import webdriver
from selenium .webdriver.common.by import By
from selenium.webdriber.chrome.options import Options

import time
import pandas as pd
from tqdm import tqdm

#브라우저의 옵션(크롬 브라우저 옵션)
#동적으로 selenium을 기반으로 작업할 때 아래와 같은 규칙 적용~
option = Options()
option.add_argument('--no-sandbox') #샌드박스 비활성화(보안 꺼)
option.add_argument('--disable-dev-shm-usage') #공유메모리 꺼
option.add_argument('--disable-gpu') #gpu사용하지마
option.add_argument('--enable-unsafe-swiftshader')#gpu쓰지 않을때 대용

driver = webdriver.Chrome(options = option)
base_url = 'https://www.musinsa.com/categories/item/001'

driver.get(base_url)