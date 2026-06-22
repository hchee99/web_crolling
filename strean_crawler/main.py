import streamlit as st
import pandas as pd
from crawling import crawling_saramin, crawling_work24, download_to_csv

st.set_page_config(page_title="채용공고 자동 크롤링 서비스", layout='wide')

st.title("채용 공고 조회 서비스")
st.write("""이 서비스는 사람인과 고용24 페이지에 검색어를 입력하여 
         자동으로 공고를 크롤링하도록 만든 서비스입니다.
         크롤링된 내용은 하단의 표에서 확인 가능하며, 
         csv파일로 다운로드받아 엑셀로 열어보실 수 있습니다.
         """)

site_select = st.radio("크롤링할 사이트 선택", ['사람인', '고용24'], horizontal=True)

with st.expander("상세 검색 조건", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        search_text = st.text_input("검색어를 입력", placeholder='예 : 파이썬, 인공지능')
        except_text = st.text_input('제외할 검색어', placeholder='예 : 야간 근무, 출장')
        max_pages = st.number_input('크롤링 페이지 수', min_value=1, max_value=30)

    with col2:
        if site_select == '사람인':
            loc_options = {
                "전체": None, "서울": "101000", "경기": "102000", "인천": "108000",
                "부산": "106000", "대구": "104000", "광주": "103000", "대전": "105000"
            }
        
            selected_location = st.multiselect('지역을 선택하세요.', list(loc_options.keys()), default=['전체'])
            locations = [loc_options[x] for x in selected_location if loc_options[x]]

            cat_options = {
                "전체": None, "IT개발·데이터": "2", "경영·사무": "3",
                "마케팅·홍보": "4", "디자인": "9", "영업": "5"
            }

            selected_category = st.multiselect("직무를 선택하세요.", list(cat_options.keys()), default=["IT개발·데이터"])
            category = [cat_options[x] for x in selected_category if cat_options[x]]

            career_option = {'전체':'0', '신입':'1', '경력':'2', '신입/경력':'3'}
            selected_career = st.selectbox('경력을 선택하세요', list(career_option.keys()))
            career = career_option[selected_career]

            edu_option = {'전체':'0', '고졸':'1', '대졸(2,3년)':'2', '대졸(4년)':'3', '석사':'4', '박사':'5'}
            selected_edu = st.selectbox('학력을 선택하세요', list(edu_option.keys()))
            edu = edu_option[selected_edu]

        else:
            region = st.text_input('지역 코드를 입력하세요', value='11000', help='지역 코드 알 수 없는 관계로 서울로 제한')
            occupation = st.text_input('직종 코드를 입력하세요', value='024', help='직종 코드 제한')
            
            career_options = {"전체": "A", "신입": "N", "경력": "E", "관계없음": "Z"}
            edu_options = {"전체": "noEdu", "중졸이하": "01,02", "고졸": "03", 
                           "대졸(2~3년)": "04", "대졸(4년)": "05", "석사": "06", 
                           "박사": "07", "학력무관": "00"}
            
            career_sel = st.selectbox('경력을 선택하세요', list(career_options.keys()))
            career = career_options[career_sel]
            edu_sel = st.selectbox('학력을 선택하세요', list(edu_options.keys()))
            edu = edu_options[edu_sel]

crawling_clicked = st.button("크롤링 시작", use_container_width=True, type='primary')

if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()

if crawling_clicked :
    if not search_text:
        st.warning('검색어를 입력해주세요!')
    else:
        with st.spinner(f"{site_select}에서 {search_text} 검색 결과 가져오는 중..."):
            if  site_select == '사람인' :
                df = crawling_saramin(search_text=search_text, except_text=except_text,
                                      region=locations, category=category,
                                      career=career, education=edu, max_pages=max_pages)
            else :
                df = crawling_work24(search_text=search_text, except_text=except_text,
                                     region=region, category=occupation,
                                     career=career, education=edu, max_pages=max_pages)

            st.session_state['df'] = df        

df = st.session_state['df']

if not df.empty:
    st.subheader('검색 결과')
    st.dataframe(df, use_container_width=True, hide_index=True)
     
    csv_data = download_to_csv(df)

    st.download_button(label='CSV 결과 다운로드',
                       data=csv_data,
                       file_name=f'crawling_results_{site_select}.csv',
                       mime='text/csv')