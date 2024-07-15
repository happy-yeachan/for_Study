import streamlit as st
import pandas as pd

# Excel 파일 로드
file_path = "정처기실기_1-5장.xlsx"

# 파일이 존재하는지 확인하고 오류 처리
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error(f"파일을 찾을 수 없습니다: {file_path}")
    st.stop()  # 파일이 없으면 앱 실행 중지
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.stop()  # 다른 오류 발생 시 앱 실행 중지

# '문제'와 '답' 열이 존재하는지 확인
if '문제' not in df.columns or '답' not in df.columns:
    st.error("Excel 파일에는 '문제'와 '답' 열이 필요합니다.")
    st.stop()

# 세션 상태 변수 초기화
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ''
if 'result' not in st.session_state:
    st.session_state.result = ''

# 정답 확인 함수
def check_answer():
    index = st.session_state.current_question
    correct_answer = df['답'][index].strip()
    user_answer = st.session_state.user_answer.strip()
    if user_answer == correct_answer:
        st.session_state.result = "정답입니다!"
    else:
        st.session_state.result = "틀렸습니다."

# 다음 문제로 이동 함수
def next_question():
    if st.session_state.current_question < len(df) - 1:
        st.session_state.current_question += 1
        st.session_state.user_answer = ''
        st.session_state.result = ''
        st.experimental_rerun()  # 현재 페이지를 다시 로드하여 상태 업데이트

# 현재 문제와 입력 필드 표시
st.title("소프트웨어 생명주기 문제 풀기")

index = st.session_state.current_question
st.write(f"문제 {index+1}: {df['문제'][index]}")
st.text_input("답", key="user_answer", value=st.session_state.user_answer)

# 정답 확인 버튼
if st.button("정답확인하기"):
    check_answer()

# 결과 표시 및 다음 문제로 이동 버튼
if st.session_state.result:
    st.write(st.session_state.result)
    if st.session_state.result == "정답입니다!":
        if st.button("다음 문제로"):
            next_question()
