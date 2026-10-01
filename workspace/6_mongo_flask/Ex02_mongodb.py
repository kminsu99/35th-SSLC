# #=================================
# # 0. 연결 확인
# # pip install pymongo
# from pymongo import MongoClient

# try:
#     # MongoDB의 기본 포트 - 27017
#     client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
#     print(client.server_info().get('version'))
#     print("MongoDB 엔진 가동 확인 완료!")
# except Exception as e:
#     print("연결 실패: 서버가 꺼져 있거나 설치가 잘못됨.", e)
# exit()
# #====================================
# 1. CRUD 확인
from pymongo import MongoClient
from datetime import datetime
"""
서버종류(프로토콜):서버아이피주소:포트번호
http://127.8.9.7:80
http://www.daum.net:80
mongodb://127.0.0.1:27017
"""

client = MongoClient('mongodb://localhost:27017/') # 로컬 PC에서 실행 중인 MongoDB에 연결
db = client['security_db']  # security_db라는 데이터베이스를 선택
col = db['vulnerabilities'] # vulnerabilities라는 컬렉션을 선택

# [1] 입력하기 Insert
# vuln_doc = {
#     "cve_id": "CVE-2026-1234",
#     "title": "OpenSSL 원격 코드 실행 취약점",
#     "severity": "Critical",
#     "affected_hosts": ["WEB-01", "WEB-02"],
#     "collected_at": datetime.now()
# }
# vuln_doc = {
#     "cve_id": "Bastion-2026-1234",
#     "title": "서버 실행 취약점",
#     "severity": "Critical",
#     "affected_hosts": ["WEB-01", "Bastion-02", "Bastion-03", "Bastion-04"],
#     "collected_at": datetime.now()
# }

# result = col.insert_one(vuln_doc)
# print(f"저장된 ID : {result.inserted_id}")
# exit()

# [2] 검색하기  Select
# data = col.find_one()
# # print(f"찾는 데이타: {data}")
# print(f"찾는 데이타: {data.get('title', '없음')}")
# print(f"찾는 데이타: {data.get('title2', '없음')}")

# data = col.find_one({"severity": "Critical"})
# print(f"찾는 데이타: {data.get('title', '없음')}")

# [3] 수정하기 Update
# data = col.find_one({"severity": "Critical"})
# col.update_one(
#     {"cve_id" : data.get('cve_id', '')}, #filter
#     {"$set": {"status" : "Patched"}} #update
# )
# print(f"{data.get('cve_id', '')}, status update")

# [4] 삭제하기 Delete
# data = col.find_one({"severity": "Critical"})
# col.delete_one(
#     {"cve_id" : data.get('cve_id', '')}, #filter
# )
# print(f"{data.get('cve_id', '')}, deleted")



### 📝 연습문제 — MongoDB CRUD
'''
**문제 1** — 
`{"ip": "203.0.113.55", "action": "blocked"}` 
문서 한 건을 저장하는 코드를 작성해 봅시다.
'''
# from pymongo import MongoClient
# from datetime import datetime

# client = MongoClient('mongodb://localhost:27017/') # 로컬 PC에서 실행 중인 MongoDB에 연결
# db = client['security_db']  # security_db라는 데이터베이스를 선택
# col = db['vulnerabilities'] # vulnerabilities라는 컬렉션을 선택

# vuln_doc = {
#     "ip": "203.0.113.55",
#     "action": "blocked"
# }

# result = col.insert_one(vuln_doc)
# print(f"저장된 ID : {result.inserted_id}")

'''
**문제 2** — severity가 Critical인 모든 문서를 조회해 
title만 반복 출력하는 코드를 작성해 봅시다.
'''
# from pymongo import MongoClient
# from datetime import datetime

# client = MongoClient('mongodb://localhost:27017/') # 로컬 PC에서 실행 중인 MongoDB에 연결
# db = client['security_db']  # security_db라는 데이터베이스를 선택
# col = db['vulnerabilities'] # vulnerabilities라는 컬렉션을 선택

# data_list = col.find({"severity": "Critical"})
# for data in data_list:
#     print(f"찾는 데이타: {data.get('title', '없음')}")