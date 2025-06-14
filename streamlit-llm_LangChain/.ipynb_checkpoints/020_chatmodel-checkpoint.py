# .env 파일 읽기
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

# LLM 모델 초기화
llm = ChatOpenAI(model="gpt-4o-mini")

# Streamlit 페이지 설정
st.set_page_config(page_title="LangGraph Chatbot")
st.header("LangGraph 기반 대화형 챗봇")

# LangGraph 워크플로우 정의
workflow = StateGraph(state_schema=MessagesState)

# 모델 호출 함수 정의
def call_model(state: MessagesState):
    """
    LLM 모델을 호출하고 응답을 반환합니다.
    """
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    return {"messages": state["messages"]}

# 그래프 노드 및 엣지 설정
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# 메모리 체크포인트
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 대화 이력 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="당신은 유용한 도우미입니다.")]

# 사용자 입력 처리 함수
def get_text():
    """
    사용자 입력을 받는 함수입니다.
    """
    return st.text_input("You: ", key="input", placeholder="질문을 입력하세요...")

# 사용자 입력 및 응답 처리
user_input = get_text()
submit = st.button('Generate')

# 대화 루프 (사용자 입력이 있을 때마다 반복 실행)
if user_input or submit:
    if user_input:
        # 새로운 사용자 입력을 세션 메시지에 추가
        st.session_state.messages.append(HumanMessage(content=user_input))
    
        # LangGraph 앱 호출
        output = app.invoke({"messages": st.session_state.messages}, config={"configurable": {"thread_id": "chat1"}})
        
        # 최신 메시지 가져오기
        response = output["messages"][-1].content
        
        # 응답을 세션 상태에 추가
        st.session_state.messages.append(AIMessage(content=response))
        
        # UI에 대화 표시
        st.subheader("Answer:")
        st.write(response)

# 대화 히스토리 표시
st.subheader("Chat History")
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.markdown(f"**You:** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.markdown(f"**Bot:** {msg.content}")
