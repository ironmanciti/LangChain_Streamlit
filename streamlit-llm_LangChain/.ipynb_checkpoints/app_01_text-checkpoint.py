# 이 스크립트는 Streamlit을 사용하여 다양한 UI 컴포넌트를 화면에 표시하는 예제입니다.
import streamlit as st  # Streamlit 라이브러리 가져오기

def main():
    #--- Text Display -----------------
    # 페이지 제목을 설정합니다.
    st.title("이것은 title입니다.")  
    
    # 페이지에 헤더를 추가합니다.
    st.header("이것은 header 입니다.")  
    
    # 페이지에 서브헤더를 추가합니다.
    st.subheader("이것은 subheader 입니다.")  
    
    # 간단한 텍스트를 출력합니다.
    st.text("Hello World Streamlit")  
    
    # 변수 값을 포함한 텍스트를 출력합니다.
    name = "김길동"  # 이름 변수 설정
    st.text("{}님, 안녕하세요. 반갑습니다.".format(name))  
    
    # 마크다운을 사용하여 LaTeX 수식을 출력합니다.
    st.markdown("이것은 $\\frac{1}{x}$입니다.")  
    
    #--- Bootstrap 형식의 Color Text Display -------
    # 성공 메시지를 출력합니다.
    st.success("실행 성공")  
    
    # 경고 메시지를 출력합니다.
    st.warning("위험합니다.")  
    
    # 참고 메시지를 출력합니다.
    st.info("참고하세요.")  
    
    # 에러 메시지를 출력합니다.
    st.error("에러입니다.")  
    
    #--- st.write : 만능 function -------
    # 수식 연산 결과를 텍스트로 출력합니다.
    st.text(2+3)  
    
    # 수식 연산 결과를 write를 사용해 출력합니다.
    st.write(2+3)  
    
    # 마크다운을 사용하여 서브 타이틀을 출력합니다.
    st.markdown("## 이것은 title입니다.")  
    
    # write를 사용하여 서브 타이틀을 출력합니다.
    st.write("## 이것은 title입니다.")  
    
    # LaTeX 수식을 write를 사용하여 출력합니다.
    st.write("이것은 $\\frac{1}{x}$입니다.")  
    
    # Streamlit 객체의 모든 속성 및 메서드를 출력합니다.
    st.write(dir(st))  
    
    # st.write 메서드의 도움말을 출력합니다.
    st.help(st.write)  

# 메인 함수 실행
if __name__ == "__main__":  
    main()
