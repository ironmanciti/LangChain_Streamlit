# read local .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 
#------------------------------------------------------------
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 응답을 반환하는 함수
def getLLMResponse(form_input, email_sender, email_recipient, email_style):
    llm = ChatOpenAI(temperature=.9, model="gpt-4o-mini")
    
    #PROMPT 구축을 위한 템플릿
    template = """
    {style} 스타일로 작성된 이메일을 작성하고, 주제는 다음을 포함합니다: {email_topic}.\n\n발신자: {sender}\n수신자: {recipient}
    \n\n이메일 내용:
    
    """
    
    #final PROMPT 생성
    prompt = PromptTemplate.from_template(template)
  
    #LLM을 이용한 response 생성
    response = llm.invoke(
        prompt.format(email_topic=form_input, sender=email_sender, 
                      recipient=email_recipient, style=email_style)
        )

    return response

st.set_page_config(page_title="이메일 생성기",
                    page_icon='📧',
                    layout='centered',
                    initial_sidebar_state='collapsed')

st.header("이메일 생성기 📧")

form_input = st.text_area('이메일 내용을 입력하세요.', height=275)

#사용자 입력을 받기 위한 UI 열 생성
# 3개의 column을 10:10:5 비율로 생성
col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    email_sender = st.text_input('보내는 사람')
with col2:
    email_recipient = st.text_input('받는 사람')
with col3: 
    # 드롭다운 생성 
    email_style = st.selectbox('작성 스타일',
            ('공식 문서', '감사하는 마음', '불만족 감정', '중립적'),
            index=0)

submit = st.button("이메일 생성")

if submit:
    response = getLLMResponse(form_input, email_sender, email_recipient, email_style)
    st.write(response.content)
