import requests
import json

url = 'http://127.0.0.1:5000/supabase'
data = {'question': '트랜잭션 추적을 위한 자바에이전트 옵션은?'}

response = requests.post(url, json=data)

print(response.json())