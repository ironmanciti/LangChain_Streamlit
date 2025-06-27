from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from send_email import send_email
from pydantic import BaseModel, Field

class EmailOutput(BaseModel):
    to: str = Field(description="수신자의 이메일 주소")
    subject: str = Field(description="이메일 제목 줄")
    body: str = Field(description="이메일 본문")

# ------------------- LLM 응답 생성 함수 ---------------------
def getLLMResponse(form_input, email_sender, email_recipient, email_style):
    model_with_structure = ChatOpenAI(model="gpt-4.1-nano").with_structured_output(EmailOutput)

    template = """
    "{style}" 스타일로 작성된 이메일을 생성하세요.

    보내는 사람: {sender}
    받는 사람: {to}
    이메일 주제: {subject}
    """

    prompt = PromptTemplate.from_template(template)

    formatted_prompt = prompt.format(
        style=email_style,
        subject=form_input,
        sender=email_sender,
        to=email_recipient
    )

    response = model_with_structure.invoke(formatted_prompt)
    return response  # 구조화된 출력값 (dict 형태)

# ------------------- Streamlit UI ---------------------
st.set_page_config(page_title="이메일 생성기", page_icon='📧', layout='centered', initial_sidebar_state='collapsed')

st.header("이메일 생성기 📧")

form_input = st.text_area('이메일 내용을 입력하세요.', height=275)

col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    email_sender = st.text_input('보내는 사람')
with col2:
    email_recipient = st.text_input('받는 사람')
with col3:
    email_style = st.selectbox('작성 스타일', ('공식 문서', '감사하는 마음', '불만족 감정', '중립적'), index=0)

submit = st.button("이메일 생성")

if submit:
    structured_output = getLLMResponse(form_input, email_sender, email_recipient, email_style)

    # 실제 이메일 전송
    result = send_email(
        structured_output.to,
        structured_output.subject,
        structured_output.body
    )
    st.success(f"이메일 전송 결과:\n{result}")
    st.subheader("📨 생성된 이메일 내용")
    st.write(f"**제목:** {structured_output.subject}")
    st.write(f"**내용:**\n{structured_output.body}")


