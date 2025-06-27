# .env 파일에서 환경 변수를 읽어오기
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import CSVLoader
import pandas as pd

# Streamlit 페이지 설정
st.set_page_config(page_title="시맨틱 검색 심화 연습", page_icon=":mag:")
st.title("시맨틱 검색 엔진 실습")

st.markdown("""
#### 이 앱은 LangChain의 시맨틱 검색 개념(문서 분할, 임베딩, 벡터스토어, 다양한 검색 방식 등)을 실습할 수 있도록 설계되었습니다.

- **실습**: 입력 쿼리로 유사 단어 검색, 다양한 검색 방식 비교
""")

# ------------------- 실습: 벡터스토어 구축 및 검색 -------------------
st.header("1. 시맨틱 검색 실습")

# CSV 파일 경로
csv_path = 'similar_words.csv'

# CSV 데이터 로드 및 벡터스토어 구축
def load_vector_store():
    # return vector_store
    pass

# 데이터프레임 미리보기
def load_dataframe():
    pass

# 벡터스토어 불러오기

# 데이터프레임 불러오기 및 미리보기


# 검색 방식 선택


# 사용자 입력 받기
