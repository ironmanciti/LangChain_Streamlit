# .env 파일에서 환경 변수를 읽어오기
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  

import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import CSVLoader
import pandas as pd

# Streamlit 페이지 설정
st.set_page_config(page_title="Educate Kids", page_icon=":robot_face:")

# 웹 페이지 헤더
st.header("영어 단어 하나를 입력하시면 비슷한 단어들을 골라 드리겠습니다.")

# OpenAIEmbeddings 객체 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# CSV 파일 로드 및 벡터 저장소 구축
@st.cache_resource
def load_vector_store():
    # CSV 파일 데이터 로드
    loader = CSVLoader(
        file_path='similar_words.csv',
        csv_args={
            'delimiter': ',',  # CSV 파일의 구분자 설정
            'quotechar': '"',  # CSV 파일의 텍스트 묶음 기호 설정
            'fieldnames': ['Words']  # CSV 필드 이름 설정
        }
    )
    data = loader.load()
    
    # InMemoryVectorStore 벡터 스토어 생성
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(data)
    return vector_store

vector_store = load_vector_store()

# CSV 데이터 미리보기
@st.cache_data
def load_dataframe():
    df = pd.read_csv('similar_words.csv')
    return df

df = load_dataframe()

# 데이터프레임을 Streamlit에 표시 (3줄만 표시되도록 설정)
st.dataframe(df.head(3), height=150)  

# 사용자 입력 받기
def get_text():
    return st.text_input("사용자: ")

user_input = get_text()

# 버튼 클릭 이벤트 설정
submit = st.button('비슷한 단어 고르기')

# 버튼이 눌리고 입력값이 존재하는 경우 실행
if submit and user_input:
    # 사용자 입력을 사용해 유사도 검색 수행
    docs = vector_store.similarity_search(user_input, k=5)
    
    # 검색 결과 출력
    st.subheader("Top 5 Matches:")
    
    # 최대 5개의 검색 결과를 순서대로 출력
    for i, doc in enumerate(docs, start=1):
        st.text(f"{i}st Match: {doc.page_content}")
