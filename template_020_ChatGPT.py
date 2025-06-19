#---------------------------------------------------------
# langgraph를 이용한 Chatbot 구현
#---------------------------------------------------------
# .env 파일에서 환경 변수를 읽어옵니다.
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

# streamlit_chat 라이브러리
from streamlit_chat import message

# LLM 초기화 - 올바른 모델명으로 수정
llm = ChatOpenAI(model='gpt-4o-mini')

from langchain_tavily import TavilySearch

# ---------------------------------------------------------------------------------
# 페이지 설정
# ---------------------------------------------------------------------------------
# 웹 애플리케이션의 페이지 제목과 아이콘을 설정
st.set_page_config(page_title='나만의 ChatGpt', page_icon=":robot_face:")


# 페이지 제목을 중앙에 정렬하여 표시
# - unsafe_allow_html=True: HTML을 직접 사용할 수 있도록 허용
st.markdown("<h1 style='text-align: center;'>우리 즐겁게 대화 해요 </h1>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------------
# 사이드바 버튼 설정
# ---------------------------------------------------------------------------------
st.sidebar.title("😎")
refresh_button = st.sidebar.button("대화 내용 초기화")  # 변수명 오타 수정
summaries_button = st.sidebar.button("대화 내용 요약")

# ---------------------------------------------------------------------------------
# LangGraph 앱과 MemorySaver 초기화 (최초 1회만)
# ---------------------------------------------------------------------------------
if "app" not in st.session_state:
    memory = MemorySaver()
    # TavilySearch 툴 인스턴스를 생성 (최대 결과 2개로 제한)
    tool = TavilySearch(max_results=2)

    # 사용할 툴들을 리스트로 구성 (여러 개의 도구가 필요한 경우를 대비해 리스트 형태로 작성)
    tools = [tool]

    agent_executor = create_react_agent(llm, tools, checkpointer=memory)

    # 5) LangGraph 앱 컴파일
    st.session_state.app = agent_executor

    # 6) 대화 이력을 저장할 메시지 리스트 초기화
    st.session_state.messages = [
        SystemMessage(content="당신은 나의 유용한 비서 입니다. 한국어로 답하세요.")
    ]

# ---------------------------------------------------------------------------------
# 사이드바 버튼 동작 정의
# ---------------------------------------------------------------------------------
# 1) "대화 내용 초기화" 버튼: 대화 기록 리셋
if refresh_button:  # 변수명 수정
    st.session_state.messages = [
        SystemMessage(content="당신은 나의 유용한 비서 입니다. 한국어로 답하세요.")  # 내용 일치시킴
    ]

# 2) "대화 내용 요약" 버튼: LLM에게 요약을 요청해 결과를 사이드바에 표시
if summaries_button:
    conversation_text = []
    for msg in st.session_state.messages:
        if isinstance(msg, SystemMessage):
            role = "System"
        elif isinstance(msg, HumanMessage):
            role = "User"
        elif isinstance(msg, AIMessage):
            role = "AI"
        else:
            role = "unknown"
        conversation_text.append(f"{role}: {msg.content}")

    joined_conversation = "\n".join(conversation_text)

    prompt_content = f"""
        {joined_conversation}
        ----
        요약:
    """

    summary_response = llm.invoke([HumanMessage(content=prompt_content)])
    summary_text = summary_response.content

    st.sidebar.write("** 대화 내용 요약 **")
    st.sidebar.write(summary_text)

# ---------------------------------------------------------------------------------
# 메인 영역: 입력 폼 및 모델 호출
# clear_on_submit=True : 폼이 제출될 때 입력 필드 자동 초기화
# ---------------------------------------------------------------------------------
with st.form(key="my_form", clear_on_submit=True):
    user_input = st.text_area("질문을 하세요:", key="input", height=100)
    submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append(HumanMessage(content=user_input))
        config = {"configurable": {"thread_id": "abc123"}}
        # AI 응답 생성 - 올바른 형식으로 수정
        output = st.session_state.app.invoke(
            {'messages': [HumanMessage(content=user_input)]}, config
        )
        
        # AI 응답을 메시지 리스트에 추가
        response = output['messages'][-1].content
        st.session_state.messages.append(AIMessage(content=response))

# ---------------------------------------------------------------------------------
# 대화 내역 표시
# ---------------------------------------------------------------------------------
st.subheader("대화 내역")
for idx, msg in enumerate(st.session_state.messages):
    if isinstance(msg, HumanMessage):
        message(msg.content, is_user=True, key=str(idx) + "_user")
    elif isinstance(msg, AIMessage):
        message(msg.content, is_user=False, key=str(idx) + "_ai")








