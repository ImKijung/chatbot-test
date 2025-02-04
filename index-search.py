import torch
from transformers import BertTokenizer, BertModel
from opensearchpy import OpenSearch
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()

# OpenSearch 클라이언트 설정
client = OpenSearch(
    hosts=[{'host': os.getenv('OPENSEARCH_HOST'), 'port': int(os.getenv('OPENSEARCH_PORT'))}],
    http_auth=(os.getenv('OPENSEARCH_USER'), os.getenv('OPENSEARCH_PASSWORD')),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

index_name=os.getenv('OPENSEARCH_INDEX')

# 검색 쿼리 설정 (size=1로 설정하여 첫 번째 문서만 가져옴)
query = {
    "size": 1,
    "query": {
        "match_all": {}
    }
}

# 검색 실행
response = client.search(index=index_name, body=query)

# 첫 번째 문서의 데이터 출력
hits = response['hits']['hits']
if hits:
    first_document = hits[0]
    print("첫 번째 문서의 전체 데이터:", first_document['_source'])
else:
    print("인덱스에 데이터가 없습니다.")

# 마지막 문서의 데이터 출력
# hits = response['hits']['hits']
# if hits:
#     last_document = hits[0]
#     print("마지막 문서의 전체 데이터:", last_document['_source'])
# else:
#     print("인덱스에 데이터가 없습니다.")