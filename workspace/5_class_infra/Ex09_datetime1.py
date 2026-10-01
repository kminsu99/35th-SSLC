# from datetime import datetime

# # 1. 현재 시각 가져오기
# now = datetime.now()
# print(f"현재 시간: {now}")

# # 2. strftime: 객체 -> 문자열 (String From Time)
# # 형식 지정자: %Y(년), %m(월), %d(일), %H(시), %M(분), %S(초)
# #Y[4] y[2]
# file_data = now.strftime("%Y-%m-%d")
# print(file_data)

# file_time = now.strftime("%y%m%d_%H%M%S")
# print(file_time)

# # 실무 활용: 날짜가 포함된 보안 리포트 파일명 생성

# filename = f"Security_report_{file_time}.txt"
# print(f"{filename} 생성하였습니다.")

# ---------------------------------------
from datetime import datetime, timedelta

today = datetime.now()
# 과거/미래 계산 — 최근 7일치 로그만 남기고 삭제할 때 등에 활용
after_two_days = today + timedelta(days=2)
print(f"이틀 후 : {after_two_days}")

#일주일전
print(f"일주일 전 : {today + timedelta(days=-7)}")
#지금시간에서 3시간 후
print(f"3시간 후 : {today + timedelta(hours=3)}")

# 인증서 만료일까지 남은 일수 계산
cart_expire = datetime(2026,12,31)
d_day = cart_expire - today
print(f"SSL 인증서 만료까지 {d_day.days}일 남았습니다.")
#===================================
# [ 참고 ] 현재 세계 표준시(UTC)를 가져오기
from datetime import timezone
today = datetime.now(timezone.utc)
print(f"표준 시간 : {today}")
