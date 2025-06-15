# read .env file
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) 
#------------------------------------------------------------

import streamlit as st
from langchain_openai import ChatOpenAI

# LangChain 라이브러리를 사용하여 자연어 처리를 수행하는 간단한 웹 애플리케이션을 만드는 Python 스크립트입니다.

# 사용자 입력에 대한 응답을 반환하는 함수입니다.
def load_answer(question):
    llm = ChatOpenAI(model="gpt-4.1-nano")
    answer = llm.invoke(question)
    return answer

# 앱 UI가 시작되는 부분입니다.
st.set_page_config(page_title="LangChain Demo")
st.header("LangChain Demo")

# 사용자 입력을 받는 함수입니다.
def get_text():
    input_text = st.text_input("사용자: ", key="input", on_change=on_submit)
    return input_text

# Submit 동작을 처리하는 콜백 함수입니다.
def on_submit():
    st.session_state.submit = True

# 상태 변수를 초기화합니다.
if "submit" not in st.session_state:
    st.session_state.submit = False

user_input = get_text()
response = load_answer(user_input)

submit = st.button('응답 생성')  

# Enter 키나 버튼 클릭으로 submit 상태 설정
if submit or st.session_state.submit:
    st.subheader("응답:")
    st.write(response.content)
