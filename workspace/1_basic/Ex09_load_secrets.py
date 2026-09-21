import os
from dotenv import load_dotenv

load_dotenv()

vt_key = os.getenv("VT_API_KEY")
target_host = os.getenv("AUDIT_TARGET_HOST")

print(f"이번 감사 대상 호스트: {target_host}")
print(f"스캐너 키 로드 확인: {vt_key[:4]}****")

# 만일 없는 환경 변수를 불러오면?
# vt_key_none = os.getenv("VT_KEY")
# print(vt_key_none)
# print(f"스캐너 키 로드 확인: {vt_key_none[:4]}****")

#getenv 찾을때 없는걸찾으면 
vt_key_none = os.getenv("VT_KEY", 'test-0000-0000-key')
print(vt_key_none)
print(f"스캐너 키 로드 확인: {vt_key_none[:4]}****")

vt_key_none = os.getenv("VT_API_KEY", 'test-0000-0000-key')
print(vt_key_none)
print(f"스캐너 키 로드 확인: {vt_key_none[:4]}****")