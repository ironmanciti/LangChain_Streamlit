#---------------------------------------------------------
# langgraph를 이용한 Chatbot 구현
#---------------------------------------------------------
# .env 파일에서 환경 변수를 읽어옵니다.
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# streamlit_chat 라이브러리
from streamlit_chat import message  # 채팅 말풍선 형태로 메시지를 보여줍니다.

# LLM 초기화
llm = ChatOpenAI(model="gpt-4.1-nano")

# ---------------------------------------------------------------------------------
# 페이지 설정
# ---------------------------------------------------------------------------------
# 웹 애플리케이션의 페이지 제목과 아이콘을 설정
st.set_page_config(page_title="나만의 ChatGPT", page_icon=":robot_face:")

# 페이지 제목을 중앙에 정렬하여 표시
# - unsafe_allow_html=True: HTML을 직접 사용할 수 있도록 허용
st.markdown("<h1 style='text-align: center;'>우리 즐겁게 대화해요</h1>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------------
# 사이드바 버튼 설정
# ---------------------------------------------------------------------------------
st.sidebar.title("😎")
refresh_button = st.sidebar.button("대화 내용 초기화")
summaries_button = st.sidebar.button("대화 내용 요약")

# ---------------------------------------------------------------------------------
# LangGraph 앱과 MemorySaver 초기화 (최초 1회만)
# ---------------------------------------------------------------------------------
if "app" not in st.session_state:
    
    # 1) LangGraph의 워크플로우(StateGraph) 정의
    workflow = StateGraph(state_schema=MessagesState)

    # 1-1) 프롬프트 템플릿 정의 (표준 구조 적용)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "당신은 친구처럼 말합니다. 모든 질문에 최선을 다해 대답하세요."),
        MessagesPlaceholder(variable_name="messages"),
    ])

    # 2) 모델 호출 함수 정의 (프롬프트 템플릿 적용)
    def call_model(state: MessagesState):
        prompt = prompt_template.invoke({"messages": state["messages"]})
        response = llm.invoke(prompt)
        return {"messages": response}

    # 3) 노드 및 엣지 연결
    workflow.add_node("model", call_model)
    workflow.add_edge(START, "model")

    # 4) MemorySaver를 사용해 대화 상태를 메모리에 저장/불러오기
    memory = MemorySaver()

    # 5) LangGraph 앱 컴파일
    st.session_state.app = workflow.compile(checkpointer=memory)

    # 6) 대화 이력을 저장할 메시지 리스트 초기화
    st.session_state.messages = [
        SystemMessage(content="당신은 유용한 도우미입니다.")
    ]

# ---------------------------------------------------------------------------------
# 사이드바 버튼 동작 정의
# ---------------------------------------------------------------------------------
# 1) "대화 내용 초기화" 버튼: 대화 기록 리셋
if refresh_button:
    st.session_state.messages = [
        SystemMessage(content="당신은 유용한 도우미입니다.")
    ]

# 2) "대화 내용 요약" 버튼: LLM에게 요약을 요청해 결과를 사이드바에 표시
if summaries_button:
    
    # 2-1) 메시지들을 텍스트로 합치기
    conversation_text = []
    for msg in st.session_state.messages:
        if isinstance(msg, SystemMessage):
            role = "System"
        elif isinstance(msg, HumanMessage):
            role = "User"
        elif isinstance(msg, AIMessage):
            role = "AI"
        else:
            role = "Unknown"
        conversation_text.append(f"{role}: {msg.content}")
        
    joined_conversation = "\n".join(conversation_text)

    # 2-2) 요약 프롬프트 만들기
    prompt_content = f"""다음 대화를 요약해주세요:
            {joined_conversation}
            --- 
            요약:
            """

    # 2-3) LLM에게 요약 요청
    summary_response = llm.invoke([HumanMessage(content=prompt_content)])
    summary_text = summary_response.content

    # 2-4) 사이드바에 요약 결과 표시
    st.sidebar.write("**대화 요약:**")
    st.sidebar.write(summary_text)

# ---------------------------------------------------------------------------------
# 메인 영역: 입력 폼 및 모델 호출
# clear_on_submit=True : 폼이 제출될 때 입력 필드 자동 초기화
# ---------------------------------------------------------------------------------
with st.form(key='my_form', clear_on_submit=True):
    user_input = st.text_area("질문을 입력하세요:", key='input', height=100)
    submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        # 사용자 입력을 HumanMessage 로 추가
        st.session_state.messages.append(HumanMessage(content=user_input))
        
        # LangGraph 앱을 호출해 AI 응답 생성
        output = st.session_state.app.invoke(
            {"messages": user_input},
            config={"configurable": {"thread_id": "chat1"}}
        )
        
        # 새롭게 생성된 AI 응답
        response = output["messages"][-1].content
        st.session_state.messages.append(AIMessage(content=response))

# ---------------------------------------------------------------------------------
# "마지막 AIMessage" 폼 바로 아래에 표시
# ---------------------------------------------------------------------------------
# - 대화 이력이 비어있지 않고, 마지막 메시지가 AIMessage이면 표시
if st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if isinstance(last_msg, AIMessage):
        st.text(last_msg.content)

# ---------------------------------------------------------------------------------
# 그 외의 대화 이력(마지막 메시지 제외)을 아래에서 순서대로 표시
# is_user=True : 사용자가 입력한 메세지
# ---------------------------------------------------------------------------------
st.subheader("이전 대화 이력")
for idx, msg in enumerate(st.session_state.messages):  # 맨 마지막 AIMessage는 제외
    if isinstance(msg, HumanMessage):
        message(msg.content, is_user=True, key=str(idx) + "_user")
    elif isinstance(msg, AIMessage):
        message(msg.content, is_user=False, key=str(idx) + "_ai")
