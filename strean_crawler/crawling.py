import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from io import StringIO

def download_to_csv(df):
    buffer = StringIO()
    df.to_csv(buffer,index = False)
    return buffer.getvalue().encode('utf-8-sig')

def crawling_saramin(search_text:str, except_text:str = "", region:list = None, 
                     category:list = None, career:str = "", education:str = "", max_pages:int = 1):
    
    columns = ['이름', '위치', '조건1', '조건2', '회사이름', '링크']
    rows = []

    url = "https://www.saramin.co.kr/zf_user/search"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    }

    for page in range(1, max_pages+1):
        parameters = {'searchword':search_text,
                      'except_read':except_text,
                      'comp_page':page}
        if category :
            parameters['cat_mcd'] = category
        if region:
            parameters['loc_mcd'] = region
        if career:
            parameters['career_cd'] = career
        if education:
            parameters['edu_cd'] = education

        try : 
            response = requests.get(url=url, headers=headers, params=parameters, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('div.item_recruit')
            
            for item in items:
                job_area = item.select_one('div.area_job')
                corp_area = item.select_one('div.area_corp')

                if not job_area :
                    continue 

                job_title = job_area.select_one('.job_tit').get_text(strip=True)
                condition_area = job_area.select_one('.job_condition')
                spans = condition_area.select('span') 

                location = spans[0].get_text(strip=True)
                condition1 = spans[1].get_text(strip=True)

                job_sector = item.select_one('div.job_sector')
                condition2 = job_sector.get_text(strip=True) if job_sector else ""

                cor_name = corp_area.select_one('strong').get_text(strip=True) if corp_area else ""

                link = job_area.select_one('.job_tit').select_one('.data_layer[href]')
                real_link = 'https://www.saramin.co.kr' + link.get('href')

                rows.append({
                    '이름':job_title,
                    '위치':location,
                    '조건1':condition1,
                    '조건2':condition2,
                    '회사이름':cor_name,
                    '링크':real_link
                })

        except Exception as e:
            print(f'에러 발생 {e}')
            break

    df = pd.DataFrame(rows)
    return df

def crawling_work24(search_text:str, except_text:str = "", region:list = None, 
                    category:list = None, career:str = "", education:str = "", max_pages:int = 1):
    
    url = 'https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do'     
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    parameters = {'srcKeyword':search_text,
                  'notSrcKeyword':except_text,
                  'pageIndex':max_pages,
                  'resultCnt':10,
                  'CodeDepth1Info':region,
                  'occupation':"024",
                  'careerTypes':"",
                  'academicGbnoEdu':""}

    response = requests.get(url, headers=headers, params=parameters, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.select('div.box_table_group.gap_box08.column')
    items_2 = soup.select('td.link.pd24')

    rows = []
    for a, b in zip(items, items_2):
        cells = a.select('div.cell')   
        name = cells[1].get_text(strip=True)
        corp_name = cells[0].get_text(strip=True) 

        money = b.select_one('span.item.b1_sb').get_text(strip=True)
        money = re.sub(r'\s+', '', money)

        if b.select_one('ul.emp_info_dtl').has_attr('li'):
            t = ''
            work_time = b.select_one('ul.emp_info_dtl').select_one('li.time')
            if len(work_time) > 1:
                for i in range(len(work_time)):
                    t += work_time.select('span')[i].text
            elif len(work_time) == 1:
                t = work_time.select_one('span').text
            else:
                t = ''
            work_time = t
        else:
            work_time = "모름"

        link = cells[1].select_one('a').get('href')
        real_link = 'https://www.work24.go.kr' + link

        location = b.select_one('ul.emp_info_dtl').select_one('li.site').get_text(strip=True)
        location = re.sub(r'\s+', '', location)

        rows.append(
            {
            '이름':name,
            '위치':location,
            '연봉':money,
            '근무시간':work_time,
            '회사이름':corp_name,
            '링크':real_link
            }
        )
    
    df = pd.DataFrame(rows)
    return df