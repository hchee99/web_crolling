#라이브러리 임포트
#크롤링 : 인터넷에 있는 정보를 긁어옴!
import requests                #인터넷 주소(url)에 html 파일을 요청
from bs4 import BeautifulSoup  #그렇게 해서 얻어온 html파일을 예쁘게 '파싱'(필요정보추출)
import pandas as pd
import re                      #정규표현식(re), 문자열 정제
import re
from io import StringIO

#buffer(임시 데이터) 상태인 df을 encode한 후
#결과를 반환해주는 코드
#지금은 내 컴퓨터(로컬)이지만, 배포 후 '클라우드'에 존재
#클라우드에서 임시 파일인 buffer를 나의 컴퓨터로 다운로드 가능한 상태로 변경
def download_to_csv(df):
    buffer = StringIO()
    df.to_csv(buffer,index = False)
    return buffer.getvalue().encode('utf-8-sig')

#검색어, 제외할검색어, 지역, 직무, 경력, 학력, 페이지 수
#매개변수에 입력될 자료형 '미리 안내'
#디폴트 값 

#url, header, paramerters => requests.get(주소) 주소로 요청
#soup 객체로 파싱, 가지고 있다가 select(), select_one() 으로 필요한 파트 추출
#처음에 초기화해놓은 rows에 append해서 최종적인 모양 만듦
def crawling_saramin(search_text:str, 
                     except_text:str = "",
                     region:list = None, 
                     category:list = None,
                     career:str = "",
                     education:str = "",
                     max_pages:int = 1):
    
    #결과로 반환할 데이터 프레임의 '열 이름'과 '행' 리스트
    columns = ['이름', '위치', '조건1', '조건2', '회사이름', '링크']
    rows = []

    #requests로 일단 '검색할 페이지'에 요청!
    url = "https://www.saramin.co.kr/zf_user/search"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    }

    #1페이지부터 ~ max_pages+1 까지 크롤링 할수있게 반복문
    #page => 한 페이지 검색 결과
    for page in range(1, max_pages+1):

        #파라미터 정제 -> 여기서 파라미터는 '검색 조건'
        #'키'는 웹사이트 지정한 '키'
        parameters = {'searchword':search_text,
                    'except_read':except_text,
                    'comp_page':page}
        #직무
        if category :
            parameters['cat_mcd'] = category
        #위치
        if region:
            parameters['loc_mcd'] = region
        #경력
        if career:
            parameters['career_cd'] = career
        #학력
        if education:
            parameters['edu_cd'] = education

        try : 
            response = requests.get(url=url,
                        headers=headers,
                        params=parameters,         #조건에 대한 정보
                        timeout=15)        #html반환해줄때까지 대기시간

            #크롤링 결과를 response로 받고,
            #response안에 있는 text파일을 'html.parser'로 파싱
            #객체 soup를 생성
            soup = BeautifulSoup(response.text, 'html.parser')
            
            #내가 필요한 결과의 '구분자'전달, 추출
            #soup.select(구분자) : '구분자'를 보유한 모든 내용
            #soup.select_one(구분자) : '구분자'를 보유한 내용 딱 하나
            items = soup.select('div.item_recruit')
            for item in items:
                #직무정보(job_area), 회사정보(corp_area) 가져옴
                job_area = item.select_one('div.area_job')
                corp_area = item.select_one('div.area_corp')

                #직무정보가 없다!
                if not job_area :
                    #한 칸의 정보가 없을 때에는 '이번에만 넘어가자' 
                    continue 

                #직무, 회사정보 get
                job_title = job_area.select_one('.job_tit').get_text(strip=True)
                condition_area = job_area.select_one('.job_condition')
                spans = condition_area.select('span') 

                print(spans)
                location = spans[0].get_text(strip=True)
                condition1 = spans[1].get_text(strip=True)

                #condition2 = spans[-1].get_text(strip=True) 
                job_sector = item.select_one('div.job_sector')
                condition2 = job_sector.get_text(strip=True)

                #회사정보
                print(corp_area)
                cor_name = corp_area.select_one('strong').get_text(strip=True)

                #링크
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
    #print(df)
    return df

def crawling_work24(search_text:str, 
                     except_text:str = "",
                     region:list = None, 
                     category:list = None,
                     career:str = "",
                     education:str = "",
                     max_pages:int = 1):
    
    #1.request 
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

    response = requests.get(url, 
                            headers=headers,
                            params = parameters,
                            timeout=15)
    #2.soup 파싱
    soup = BeautifulSoup(response.text, 
                         'html.parser')

    #3.이름, 위치, 조건1, 조건2, 회사이름, 링크 soup파싱에서 추출 
    items = soup.select('div.box_table_group.gap_box08.column')
    items_2 = soup.select('td.link.pd24')

    #a -> items(왼쪽 박스)
    #b -> items_2(오른쪽 박스)

    rows = []
    for a, b in zip(items, items_2):
        #이름, 위치, 조건1(연봉), 조건2(근무시간), 회사이름, 링크
        cells = a.select('div.cell')   
        name = cells[1].get_text(strip=True)
        corp_name = cells[0].get_text(strip=True) 

        #select() : get_text가 가능
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
        print(location)

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
    #print(df)
    return df
        
#if __name__ == '__main__':
    #crawling_saramin("빅데이터")
    #crawling_work24('AI')