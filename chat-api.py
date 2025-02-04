from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from opensearchpy import OpenSearch
from dotenv import load_dotenv
import os

# Flask 애플리케이션 생성
chatapi2 = Flask(__name__)
CORS(chatapi2)  # CORS 활성화

# OpenAI API 키 설정
OpenAIclient = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# OpenSearch 클라이언트 설정
client = OpenSearch(
    hosts=[{'host': os.getenv('OPENSEARCH_HOST'), 'port': int(os.getenv('OPENSEARCH_PORT'))}],
    http_auth=(os.getenv('OPENSEARCH_USER'), os.getenv('OPENSEARCH_PASSWORD')),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# 프롬프트 파일 읽기
with open('prompt.txt', 'r') as file:
    base_prompt = file.read()

# API 엔드포인트 설정
@chatapi2.route('/chat', methods=['POST'])
def chat():
    # 사용자의 질문 받기
    user_question = request.json['question']

    # OpenSearch에 쿼리 전송하여 검색 결과 가져오기
    query = {
        "match": {
            "metadata.content": user_question
        }
    }

    response = client.search(
        body={"query": query},
        index=os.getenv('OPENSEARCH_INDEX')
    )

    # 검색 결과 처리
    hits = response["hits"]["hits"]
    urls = []
    summary_input = f"{base_prompt}\nQuestion: {user_question}\nSearch Results:\n"

    for hit in hits:
        metadata = hit['_source']['metadata']
        summary_input += metadata['title'] + ": " + metadata['content'] + "\n"

        urls.append(metadata['url'] + " | " + metadata['title'] + " | " + metadata['product'])

    # OpenAI를 사용하여 검색 결과 요약
    summary_response = OpenAIclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": summary_input}],
        temperature=0.3,
        max_tokens=400
    )

    # 요약된 답변 출력
    summary = summary_response.choices[0].message.content.strip()

    # 결과 반환
    return jsonify({"summary": summary, "urls": urls})

# 서버 실행
if __name__ == '__main__':
    chatapi2.run(debug=True, port=5002)
