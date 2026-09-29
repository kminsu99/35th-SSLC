# 1. 정규표현식 문법 기초 
import re

# # 1-1. 문자, 숫자 매치

# import re
# log_line = "203.0.113.55 - admin [05/Apr/2026:14:20:01] GET /etc/passwd HTTP/1.1 403 531"
# # \d : 숫자 하나, \w : 문자/숫자 매치 하나, \s : 공백 문자, . : 줄바꿈 제외 문자 1개
# # 여기
# has_digit = re.search(r"\d", log_line)
# print(has_digit)
# print("-"*30)
# first_word = re.search(r"\w+", log_line)
# print(first_word)
# print("-"*30)

# print(f"숫자 포함 여부: {bool(has_digit)}")
# print(f"첫 번째 문자 매치: {first_word.group()}")



# 1-2. 반복 횟수 지정 (길이 조절)
# import re

# status_line = "GET /index.html HTTP/1.1 200 1024"

# # \d{3} : 숫자가 정확히 3자리 (HTTP 상태 코드 자릿수)
# match = re.search(r"\d{3}", status_line)
# if match:
#     print(f"상태 코드 후보: {match.group()}")

# # https? : s가 0번 또는 1번 나올 수 있음 (http/https 둘 다 허용)
# internal_url = "http://api.internal.company.com/v1/alerts"
# internal_url = "https://api.internal.company.com/v1/alerts"
# internal_url = "ftp://api.internal.company.com/v1/alerts"

# # 여기
# if re.search(r"https?://", internal_url):
#     print("정상적인 http url 입니다")



# 1-3. 위치 · 범위 · 그룹 · OR 연산자
# import re

# auth_log = "Failed password for root from 211.23.45.10 port 54321 ssh2"

# # ( | ) : 여러 값 중 하나라도 일치하면 매칭 (OR)
# if re.search(r"(admin|root)", auth_log):
#     print("[경고] 관리자급 계정을 대상으로 한 로그인 시도 감지")

# # ^ : 문자열의 시작, $ : 문자열의 끝
# release_tag = "2026-04-05-hotfix"
# if re.match(r"^2026-", release_tag):
#     print("2026년도 릴리스 태그입니다")

# # [ ] 문자 집합, - 범위, [^] 부정(그 문자들이 아닌 것)
# password_candidate = "P@ssw0rd!"
# password_candidate = "가"
# if re.search(r"[^\sa-zA-Z0-9ㄱ-힣]", password_candidate):
#     print("특수문자가 포함되어 비밀번호 정책을 만족합니다")


# import re

# log_line = "ERROR: Login failed from 192.168.1.100"

# # search() #문자열 어디에서든 찾기
# result = re.search(r"Login", log_line)
# print(result.group())   # Login

# # match() #문자열 처음부터 찾기
# result = re.match(r"Login", log_line)
# print(result)            # None

# import re

# log_line = "2026-09-16 ERROR Login failed"

# print(re.search(r"^2026", log_line))
# print(re.match(r"^2026", log_line))
# print(re.search(r"ca*t", "ct")) #o
# print(re.search(r"ca*t", "cat")) #o
# print(re.search(r"ca*t", "caat")) #o
# print(re.search(r"ca+t", "ct")) #x
# print(re.search(r"ca+t", "cat")) #o
# print(re.search(r"ca+t", "caat")) #o
# print(re.search(r"ca{2,}t", "caaaaaaat"))
# print(re.search(r"ca{,5}t", "caaaaat"))
# print(re.search(r"ca?t", "ct"))
# print(re.search(r"ca?t", "cat"))
# print(re.search(r"ca?t", "caaat"))

### 연습문제 — 정규표현식 기초

# **문제 1** — 
# `\d{4}-\d{2}-\d{2}` 패턴이 어떤 형식의 문자열을 검증하는지 설명하고, 
# `"2026-04-05"`라는 문자열이 이 형식을 정확히 만족하는지 
# `re.match()`로 확인하는 코드를 작성해 봅시다.

#문자4개 - 문자2개 - 문자2개 패턴
#ex) aaaa-aa-aa
print(re.match(r"\d{4}-\d{2}-\d{2}", "2026-04-05"))


# **문제 2** — 
# `log_line = "Failed login for admin from 10.0.0.5"`에서 
# `admin` 또는 `root` 계정이 포함되어 있는지 `re.search()`와 `(admin|root)` 그룹으로 확인하고, 
# 발견되면 경고 메시지를 출력하는 코드를 작성해 봅시다.
log_line = "Failed login for admin from 10.0.0.5"
if re.search(r"(admin|root)", log_line):
    print("WARNING : admin, root access")


# **문제 3**  — 
# IPv4 주소를 매칭하기 위한 네 가지 후보 중 가장 정확한 것을 고르고 그 이유를 설명해 봅시다: 
# `\d.\d.\d.\d` / `\d+\.\d+\.\d+\.\d+` / `\w+\.\w+\.\w+\.\w+` / `[0-9]{1,3}[.][0-9]{1,3}`

#\d+\.\d+\.\d+\.\d+
#123.123.123.123 식만족