## WhaTap Docs Chatbot

아래 내용은 테스트 후 내용을 더 보출할 예정입니다.

* [데이터베이스 구성 안 참조](https://www.notion.so/whatap/WhaTap-Docs-e89922a56c3540ea96f88e5fa97f11ed)

* [스크랩을 위한 저장소](https://github.com/whatap/docs-ai-scrap.git)

### .env 파일 작성

`.env` 파일을 작성하세요.관련 정보는 @<kj.im@whatap.io>로 문의주세요.

```
OPENSEARCH_HOST=
OPENSEARCH_PORT=
OPENSEARCH_USER=
OPENSEARCH_PASSWORD=
OPENSEARCH_INDEX=
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
```

### Python 환경 설정

```
poetry install
```

### API 실행하기

#### OpenSearch 데이터베이스용 API

1. chat-api.py를 실행하세요.

2. app.py에서 `API_BASE_URL` 항목을 `http://127.0.0.1:5000/chat`으로 변경하세요.

3. app.py를 다음 명령어로 실행하세요.

```
streamlit run app.py
```

#### Supabase 데이터베이스용 API

1. chat-api.py를 실행하세요.

2. app.py에서 `API_BASE_URL` 항목을 `http://127.0.0.1:5000/supabase`로 변경하세요.

3. app.py를 다음 명령어로 실행하세요.

```
streamlit run app.py
```

### 테스트 결과

OpenSearch 보다 Supabase의 데이터베이스가 더 나은 결과를 도출합니다. 여러가지 질문을 해보고 테스트해보시기 바랍니다.

[테스트 결과 샘플](https://www.notion.so/whatap/b0a85a0283364ec6b6de311697bcc74a)

Supabase는 오픈 소스입니다.
