import streamlit as st
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import CSVLoader
import pandas as pd

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
@st.cache_resource
def load_vector_store():
    loader = CSVLoader(
        file_path=csv_path,
        csv_args={
            'delimiter': ',',
            'quotechar': '"',
            'fieldnames': ['Words']
        }
    )
    data = loader.load()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(data)
    return vector_store

vector_store = load_vector_store()

# 데이터프레임 미리보기
@st.cache_data
def load_dataframe():
    df = pd.read_csv(csv_path)
    return df

df = load_dataframe()
st.dataframe(df.head(5), height=150)

# 검색 방식 선택
search_type = st.selectbox(
    "검색 방식 선택",
    ["similarity_search", "similarity_search_with_score", "similarity_search_by_vector"],
    format_func=lambda x: {
        "similarity_search": "유사도 검색 (문자열 쿼리)",
        "similarity_search_with_score": "유사도+점수 반환",
        "similarity_search_by_vector": "벡터 직접 검색"
    }[x]
)

user_query = st.text_input("검색할 단어/문장 입력:")
submit = st.button("검색 실행")

if submit and user_query:
    if search_type == "similarity_search":
        docs = vector_store.similarity_search(user_query, k=5)
        st.subheader("Top 5 유사 단어:")
        for i, doc in enumerate(docs, 1):
            st.write(f"{i}. {doc.page_content}")
    elif search_type == "similarity_search_with_score":
        results = vector_store.similarity_search_with_score(user_query, k=5)
        st.subheader("Top 5 유사 단어 및 점수:")
        for i, (doc, score) in enumerate(results, 1):
            st.write(f"{i}. {doc.page_content} (유사도: {score:.3f})")
    elif search_type == "similarity_search_by_vector":
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        query_vec = embeddings.embed_query(user_query)
        docs = vector_store.similarity_search_by_vector(query_vec, k=5)
        st.subheader("Top 5 (벡터 직접 검색):")
        for i, doc in enumerate(docs, 1):
            st.write(f"{i}. {doc.page_content}")

