import torch
from transformers import BertTokenizer, BertModel
from opensearchpy import OpenSearch
from dotenv import load_dotenv
from openai import OpenAI
import os

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
OpenAIclient = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# BERT 모델 및 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# OpenSearch 클라이언트 설정
client = OpenSearch(
    hosts=[{'host': os.getenv('OPENSEARCH_HOST'), 'port': int(os.getenv('OPENSEARCH_PORT'))}],
    http_auth=(os.getenv('OPENSEARCH_USER'), os.getenv('OPENSEARCH_PASSWORD')),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# 사용자의 질문 받기
user_question = input("질문을 입력하세요: ")

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
summary_input = f"Question: {user_question}\nSearch Results:\n"

for hit in hits:
    metadata = hit['_source']['metadata']
    summary_input += metadata['title'] + ": " + metadata['content'] + "\n"
    urls.append(metadata['url'] + " | " + metadata['title'] + " | " + metadata['product'])

# 프롬프트 파일 생성
prompt_filename = 'prompt.txt'

# 프롬프트 파일 읽기
with open(prompt_filename, 'r') as file:
    prompt = file.read()

# OpenAI를 사용하여 검색 결과 요약
summary_response = OpenAIclient.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": prompt}],
    temperature=0.3,
    max_tokens=150
)

# 요약된 답변 출력
summary = summary_response.choices[0].message.content.strip()
print("요약된 답변:", summary)

# 관련 URL 경로 출력
print("관련 URL 경로:")
for url in urls:
    print(url)
