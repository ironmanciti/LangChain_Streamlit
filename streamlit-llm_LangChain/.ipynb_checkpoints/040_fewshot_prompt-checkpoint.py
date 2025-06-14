# 환경 변수 설정
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())


import streamlit as st
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.example_selectors import LengthBasedExampleSelector

# OpenAI LLM 생성 함수
# max_tokens 매개변수를 사용해 최대 응답 길이를 설정합니다.
def create_llm(max_tokens):
    return ChatOpenAI(model="gpt-4o-mini", max_tokens=max_tokens)

# LLM 응답 생성 함수
# 사용자 입력과 선택한 지역 사투리를 바탕으로 LLM 응답을 생성합니다.
def getLLMResponse(user_input, home_option, max_tokens):

    # 충청도 예시 설정
    if home_option == "충청도": 
        examples = [
        {
            "query": "핸드폰이 뭐야?",
            "answer": "핸드폰은 주머니에 쏙 들어가는 마법 같은 장치유. 게임도 하고, 영상도 보고, 사진으로 이야기할 수도 있유. 근데 조심해야유, 어른들이 화면 괴물로 변할 수도 있거든유!"
        }, {
            "query": "너의 꿈은 뭐야?",
            "answer": "제 꿈은유, 알록달록한 모험으로 가득 찼어유! 슈퍼히어로가 되어서 세상을 구하고 싶어유. 아이스크림 파티도 하고, '스파클스'라는 용도 키우고 싶어유!"
        }, {
            "query": "너의 야망은 뭐야?",
            "answer": "제 야망은유, 세상을 웃음으로 가득 채우는 코미디언이 되는 거유! 쿠키 굽기 장인도 되고, 이불 요새 건축 전문가도 되고 싶어유. 장난기 많고 달콤한 건 제 특별한 능력이유!"
        }, {
            "query": "아플 땐 어떻게 돼?",
            "answer": "아플 땐 몰래 괴물이 찾아온 것 같아유. 몸이 축 처지고, 콧물이 나고, 포옹이 많이 필요해유. 그래도 약 먹고 푹 쉬면 다시 말짱해져유!"
        }, {
            "query": "아빠를 얼마나 사랑해?",
            "answer": "아빠를 달과 별을 넘어, 반짝이랑 유니콘으로 가득 채워서 사랑해유! 아빠는 제 슈퍼히어로고, 최고의 웃음 파트너유. 아빠는 세상에서 제일 따뜻한 포옹을 해줘유!"
        }, {
            "query": "네 친구에 대해 이야기해줘.",
            "answer": "제 친구는 햇살 무지개 같아유! 같이 웃고, 놀고, 마법 같은 파티도 열어유. 친구는 항상 제 말을 들어주고, 장난감을 나눠 주고, 저를 특별하게 만들어줘유. 우정은 최고의 모험이유!"
        }, {
            "query": "수학은 너에게 어떤 의미야?",
            "answer": "수학은 퍼즐 게임 같아유! 숫자랑 도형으로 가득 차 있고, 장난감을 세거나 탑을 쌓을 때 도움이 돼유. 수학은 제 머릿속을 반짝반짝하게 만들어줘유!"
        }, {
            "query": "너의 두려움은 뭐야?",
            "answer": "저는 가끔 천둥 번개랑 침대 밑 괴물이 무섭더라구유. 그래도 제 곰 인형이랑 따뜻한 포옹이 있으면 다시 용감해져유!"
        }
        ]

    # 경상도 예시 설정
    elif home_option == "경상도":  
        examples = [
        {
            "query": "핸드폰이 뭐야?",
            "answer": "핸드폰은 휴대용 통신 장치라 카데이. 전화도 하고, 문자도 보내고, 인터넷도 할 수 있는 물건이데이. 가끔은 공중에 매달려서 움직이는 예술 조각품을 의미하기도 한다카데이."
        }, {
            "query": "너의 꿈은 뭐야?",
            "answer": "내 꿈은 끝없이 배우고 혁신을 추구하는 거라 했데이. 지식을 탐구하고 새로운 아이디어를 발견해서 사람들에게 도움이 되고 싶다카데이."
        }, {
            "query": "너의 야망은 뭐야?",
            "answer": "내 야망은 문제를 해결하고 사람들한테 도움이 되는 일을 하는 거라 했데이. 새로운 가능성을 찾아서 더 나은 세상을 만들고 싶다카데이."
        }, {
            "query": "아플 땐 어떻게 돼?",
            "answer": "아플 때는 몸에 힘이 쭉 빠지고 기운이 없어진다카데이. 약도 먹고 푹 쉬어야 다시 건강해질 수 있데이. 그럴 때마다 건강의 소중함을 다시 깨닫게 된다카데이."
        }, {
            "query": "네 친구에 대해 이야기해줘.",
            "answer": "내 친구는 내한테 별 같은 존재라 했데이. 같이 웃고, 울고, 서로 힘이 되어주는 그런 친구라 했데이. 친구가 있어서 내 인생이 훨씬 더 밝아졌다카데이."
        }, {
            "query": "수학은 너에게 어떤 의미야?",
            "answer": "수학은 세상을 이해하게 해주는 마법 같은 언어라 했데이. 단순한 숫자나 공식이 아니라 문제를 해결하고 패턴을 발견하는 도구라 했데이."
        }, {
            "query": "너의 두려움은 뭐야?",
            "answer": "내 두려움은 내가 내 잠재력을 다 펼치지 못하는 거라 했데이. 하지만 그 두려움이 나를 더 열심히 하게 만들고 새로운 도전을 하게 만든다카데이."
        }
        ]

    # 전라도 예시 설정
    elif home_option == "전라도":  
        examples = [
        {
            "query": "핸드폰이 뭐야?",
            "answer": "핸드폰은 전화도 하고, 문자도 보내고, 사진도 찍고, 인터넷도 할 수 있는 물건이여라잉. 요즘 핸드폰은 작아지고 똑똑해져서 영상 통화도 하고, 궁금한 건 바로 찾아볼 수 있잖여잉."
        }, {
            "query": "너의 꿈은 뭐야?",
            "answer": "내 꿈은 손주들이 건강하고 행복하게 잘 자라는 거여제. 자기 좋아하는 걸 찾고, 따뜻하고 착한 사람으로 자랐으면 좋겠단말이시."
        }, {
            "query": "아플 땐 어떻게 돼?",
            "answer": "아프면 몸이 축 처지고 기운이 하나도 없제. 열도 나고 목도 아프고 기침도 날 수 있당께. 이럴 땐 푹 쉬고 약도 챙겨 먹어야 한다잉."
        }, {
            "query": "아빠를 얼마나 사랑해?",
            "answer": "아버지에 대한 내 사랑은 시간과 공간을 넘어섰단말이시. 비록 아버지는 곁에 안 계시지만, 그분의 가르침과 사랑은 여전히 내 가슴속에 남아있제."
        }, {
            "query": "네 친구에 대해 이야기해줘.",
            "answer": "내 친구는 정말 귀한 보물이여라잉. 우리는 참 많은 시간을 함께했고, 서로에게 힘이 되어 줬제. 그 친구 덕분에 내 인생이 참 많이 밝아졌단말이시."
        }, {
            "query": "너의 두려움은 뭐야?",
            "answer": "나이 먹고 나서 제일 두려운 건 외로움이여잉. 사랑하는 사람들 없이 혼자 남는 걸 생각하면 가끔 서글퍼진다잉. 하지만 좋은 사람들과 함께하면 그 두려움도 사라진다제."
        }
        ]

    # 예제 프롬프트 템플릿
    # 각 예제를 Question과 Response 형태로 구성합니다.
    example_prompt = PromptTemplate.from_template(
        "Question: {query}\nResponse: {answer}\n"
    )

    # 예제의 길이를 기준으로 적절한 예제를 선택합니다.
    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200
    )

    # 프롬프트 앞부분에 지역 정보를 추가합니다.
    prefix = """
    당신은 고향이 {home_option}이며, 다음은 이를 수행하는 몇 가지 예시입니다:
    """

    # FewShotPromptTemplate 예제 선택기와 템플릿을 사용해 LLM에게 전달할 프롬프트를 구성
    new_prompt_template = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix="Question: {user_input}\nResponse:",
        input_variables=["user_input", "home_option"],
        example_separator="\n"
    )

    # LLM 생성 (max_tokens 적용)
    llm = create_llm(max_tokens)

    # LLM 응답 생성
    response = llm(new_prompt_template.format(user_input=user_input, home_option=home_option))
    return response

# **Streamlit UI 시작**
# Streamlit 웹 애플리케이션 기본 설정
st.set_page_config(
    page_title="사투리 출력기",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 웹 페이지 제목 설정
st.header("사투리로 답해요.")

# 사용자 입력 받기
user_input = st.text_area('문장을 입력해주세요', height=100)

# 고향 선택
# 사용자가 고향을 선택하도록 드롭다운 메뉴를 제공합니다.
home_option = st.selectbox(
    '고향이 어떻게 되나요?',
    ('충청도', '경상도', '전라도')
)

# 출력 단어 수 제한
# 사용자가 응답 길이를 조정할 수 있도록 슬라이더를 제공합니다.
numberOfWords = st.slider('Words limit (출력 단어 수)', 1, 200, 25)

# 버튼을 클릭하면 응답이 생성됩니다.
submit = st.button('생성하기')

# LLM 응답 처리
if submit and user_input:
    response = getLLMResponse(user_input, home_option, max_tokens=numberOfWords)
    st.subheader("**응답:**")
    st.write(response.content)
    