import streamlit as st
import requests

response = False

API_BASE_URL = "http://127.0.0.1:5003/supabase"
# API_BASE_URL = "http://127.0.0.1:5002/chat"

def request_chat_api(user_message: str) -> dict:
    url = API_BASE_URL
    try:
        resp = requests.post(
            url,
            json={"question": user_message},
        )
        resp.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Check if response contains JSON content
        content_type = resp.headers.get('content-type')
        if content_type and 'application/json' in content_type:
            return resp.json()
        else:
            return {"error": "Server did not return JSON content"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error: {e}"}

st.header("WhaTap Docs Q&A Chatbot")

st.markdown("""---""")

question_input = st.text_input("Enter question")
question = question_input.replace("톰캣", "Tomcat").replace("로그", "Log").replace("자바", "Java").replace("파이썬", "Python").replace("피에이치피", "PHP").replace("닷넷", ".NET").replace("서버", "Server").replace("쿠버네티스", "Kubernetes").replace("데이터베이스", "Database").replace("오라클", "Oracle").replace("포스트그레", "PostgreSQL").replace("NPM", "Network Performance Monitoring").replace("브라우저", "Browser").replace("티베로", "Tibero").replace("엠에스", "MS").replace("아마존", "Amazon").replace("클라우드", "Cloud").replace("오픈텔레메트리", "OpenTelemetry").replace("슬랙", "Slack")

rerun_button = st.button("Rerun")

st.markdown("""---""")

if question_input:
    response = request_chat_api(question)
else:
    pass

if rerun_button:
    response = request_chat_api(question)
else:
    pass

if response:
    st.write("Response:")
    summary = response["summary"]
    urls = response["urls"]
    # 요약된 답변 출력
    st.text("Summary:")
    st.write(summary)
    
    # 관련 URL 출력
    st.text("Related URLs:")
    for url in urls:
        st.write(url)
else:
    pass


with st.sidebar:
    st.title("Usage Stats:")
    st.markdown("""---""")
