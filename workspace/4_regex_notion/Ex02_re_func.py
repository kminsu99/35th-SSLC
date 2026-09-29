# 2. re 모듈 주요 함수 — search · match · findall · compile
import re

# 2-1. re.search() — 문자열 어디든 첫 지점 반환
# import re

# log_line = "192.168.0.1 - - [05/Apr/2026] GET /etc/passwd 403"

# match = re.search(r"/etc/passwd", log_line)
# if match:
#     print(f"[위험] 민감 파일 접근 시도 감지: {match.group()}")


#-------------------------------------------
# 2-2. re.match() — 문자열의 시작부터 일치하는지 확인
# import re

# log_line = "[ERROR] Unauthorized access attempt from 192.168.0.1"

# pattern = r"\[ERROR\]"
# pattern = r"[ERROR]"
# m = re.match(pattern, log_line)

# if m:
#     print(f"보안 위협 로그입니다: {m.group()}")
# else:
#     print("ERROR로 시작하는 로그가 아닙니다")

#-------------------------------------------
# 2-3. re.findall() — 일치하는 모든 부분을 리스트로 반환
# import re

# text = "요청1 처리결과: 200, 요청2 처리결과: 404, 요청3 처리결과: 500"

# codes = re.findall(r"\d{3}", text)
# # codes = re.search(r"\d{3}", text)
# print(f"추출된 상태 코드 목록: {codes}")


#-----------------------------------------------
# 2-4. re.compile() — 대용량 로그 반복 검사를 위한 사전 컴파일

# import re

# ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

# logs = ["1.1.1.1 GET ...", "invalid line", "2.2.2.2 POST ..."]

# for line in logs:
#     if ip_pattern.search(line):
#         print(f"IP 발견: {line}")

# **문제 1**  — 
# 로그 문자열 `"[INFO] Service started"`이 `"[ERROR]"`로 시작하는지 
# `re.match()`로 확인하는 코드를 작성해 봅시다. 
# (시작하지 않으므로 `None`이 반환되는지 확인해보세요.)
log_str = "[INFO] Service started"
print(re.match(r"\[ERROR\]", log_str))

# **문제 2** — 
# `text = "요청1: 200, 요청2: 404, 요청3: 500"`에서 
# `re.findall()`로 3자리 상태 코드를 모두 추출하는 코드를 작성해 봅시다.
text = "요청1: 200, 요청2: 404, 요청3: 500"
print(re.findall(r"\d{3}", text))

# **문제 3**  — 
# 수만 줄짜리 로그 파일을 한 줄씩 검사하며 IP 패턴을 찾아야 할 때, 
# 매번 `re.search(r"패턴", line)`처럼 패턴을 문자열로 직접 넘기는 방식과 
# `re.compile()`로 미리 컴파일해둔 `pattern.search(line)`을 호출하는 방식 
# 중 어느 쪽이 더 유리한지, 그리고 왜 그러한지 설명해 봅시다.

"""
캐시는 파이썬 내부적으로 search도함. comile만 캐시하는게 아님

compile장점은 가독성, 재사용성
패턴을 한번 만들어두고 다른곳에서 바로 재사용가능
패턴이 복잡할경우 패턴을 변수로 관리하는게 나을듯
#휴먼폴트
"""