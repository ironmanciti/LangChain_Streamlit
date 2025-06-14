import streamlit as st
import pandas as pd

# 이 스크립트는 Streamlit을 사용하여 데이터프레임, 테이블, JSON, 코드 등을 화면에 표시하는 예제입니다.

# CSV 파일을 읽어와 데이터프레임으로 저장합니다.
df = pd.read_csv("data/iris.csv")

# 데이터프레임을 동적으로 표시합니다.
st.dataframe(df)

# 각 열에서 최대값을 강조하여 표시합니다.
st.dataframe(df.style.highlight_max(axis=0))

# 데이터프레임의 표시 영역 크기를 지정합니다. (너비: 300, 높이: 100)
st.dataframe(df, 300, 100)

# 데이터프레임의 상위 5개 행을 표시합니다.
st.write(df.head())

# 데이터프레임을 정적 테이블로 표시합니다.
st.table(df)

# JSON 데이터를 표시합니다.
st.json({"data": "This is Json"})

# Python 코드를 문자열로 작성합니다.
mycode = """
    def main():
        st.write("Hello streamlit !)
    
    main()
"""

# Python 코드를 코드 블록으로 표시합니다.
st.code(mycode, language="python")
