import torch
from transformers import BertTokenizer, BertModel
from opensearchpy import OpenSearch
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()

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

# 사용자의 질문에 대한 검색 쿼리
user_question = "OpenTelemetry 설치 방법은?"
query = {
    "match": {
        "metadata.content": user_question
    }
}

# OpenSearch에 쿼리 전송
response = client.search(
    body={"query": query},
    index=os.getenv('OPENSEARCH_INDEX')
)

# 검색 결과 출력
hits = response["hits"]["hits"]
for hit in hits:
    metadata = hit['_source']['metadata']
    title = metadata['title']
    url = metadata['url']
    content = metadata['content']
    product = metadata['product']
    header = metadata['header']
    print("Title:", title)
    print("URL:", url)
    print("Content:", content)
    print("Product:", product)
    print("Header:", header)
    print()
