import streamlit as st
import requests

# API 엔드포인트
API_URL = 'http://127.0.0.1:5000/chat'

# Streamlit 애플리케이션 설정
st.title('Chat with ChatGPT')

# 사용자 입력 받기
user_question = st.text_input('Enter your question here:')

# Send 버튼 클릭 시 동작
if st.button('Send'):
    # API로 사용자의 질문 전송
    response = requests.post(API_URL, json={'question': user_question})

    # API 응답 확인
    if response.status_code == 200:
        data = response.json()
        summary = data['summary']
        urls = data['urls']
        
        # 요약된 답변 출력
        st.text('Summary:')
        st.write(summary)
        
        # 관련 URL 출력
        st.text('Related URLs:')
        for url in urls:
            st.write(url)
    else:
        st.error('Error communicating with the server')
