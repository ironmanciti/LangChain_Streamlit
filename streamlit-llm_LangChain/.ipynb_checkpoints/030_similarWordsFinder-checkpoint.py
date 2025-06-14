import os
import openai
import sys
sys.path.append('./')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']
#------------------------------------------------------------

import streamlit as st

#임베딩은 부동 소수점 숫자의 벡터입니다. 두 벡터 사이의 거리는 관련성을 측정합니다.
from langchain.embeddings import OpenAIEmbeddings

#FAISS는 Facebook AI Research에서 개발한 오픈소스 라이브러리로, 특히 고차원 벡터를 사용한 대규모 데이터 세트의 효율적인 유사성 검색 및 클러스터링을 위해 개발되었습니다.
#최근접 이웃 검색 및 추천 시스템과 같은 작업에 최적화된 인덱싱 구조와 알고리즘을 제공합니다.

from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader

st.set_page_config(page_title="Educate Kids")
st.header("다음 단어 중 하나를 고르시면 비슷한 단어를 알려드리겠습니다.")

#OpenAIEmbeddings 객체 초기화
embeddings = OpenAIEmbeddings()

# CSVLoader 객체 초기화
loader = CSVLoader(file_path='myData.csv', csv_args={
    'delimiter': ',',
    'quotechar': '"',
    'fieldnames': ['Words']
})

data = loader.load()

import pandas as pd
df = pd.read_csv('myData.csv')
st.write(df)

db = FAISS.from_documents(data, embeddings)

#사용자로부터 입력을 받아 변수에 저장하는 함수
def get_text():
    input_text = st.text_input("You: ")
    return input_text

user_input=get_text()
submit = st.button('비슷한 단어 고르기')  

if submit:
    docs = db.similarity_search(user_input)
    print(docs)
    st.subheader("Top Matches:")
    st.text("1st " + docs[0].page_content)
    st.text("2nd " + docs[1].page_content)

