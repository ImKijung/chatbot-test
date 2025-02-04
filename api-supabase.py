from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import json

import os
from supabase import create_client

# Flask 애플리케이션 생성
chatapi = Flask(__name__)
CORS(chatapi)  # CORS 활성화

# OpenAI API 키 설정
OpenAIclient = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Supabase 클라이언트 설정
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
client = create_client(supabase_url, supabase_key)

# 프롬프트 파일 읽기
with open('prompt.txt', 'r', encoding='UTF8') as file:
    base_prompt = file.read()

# API 엔드포인트 설정
@chatapi.route('/supabase', methods=['POST'])
def chat():
    # 사용자의 질문 받기
    user_question = request.json['question']

    # 사용자 질문의 벡터 임베딩 생성
    embedding_response = OpenAIclient.embeddings.create(
      input=user_question,
      model="text-embedding-ada-002"
    )
    query_embedding = embedding_response.data[0].embedding

    # Supabase에서 벡터 검색 실행
    response = client.rpc('match_whatap_docs', {
        'query_embedding': query_embedding,
        'similarity_threshold': 0.8,  # 유사성 임계값 설정
        'match_count': 10  # 반환할 최대 문서 수 설정
    }).execute()


    # 검색 결과 처리
    hits = response.data
    urls = []
    summary_input = f"Question: {user_question}\nSearch Results:\n"

    for hit in hits:
      metadata = json.loads(hit['metadata'])
      summary_input += f"{metadata['title']}: {metadata['content']}\n"
      urls.append(f"{metadata['url']} | {metadata['title']} > {metadata['header']} | {metadata['product']}")

    # OpenAI를 사용하여 검색 결과 요약
    summary_response = OpenAIclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "system", "content": summary_input}
        ],
        temperature=0.3,
        max_tokens=400
    )

    # 요약된 답변 출력
    summary = summary_response.choices[0].message.content.strip()

    # 결과 반환
    return jsonify({"summary": summary, "urls": urls})

# 서버 실행
if __name__ == '__main__':
    chatapi.run(debug=True, port=5003)
