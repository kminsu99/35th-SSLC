# — 로그인 실패 임계치 판정

# failed_login_count = int( input('로그인 실패 횟수를 입력하세요-> '))

# if failed_login_count >= 8:
#     print(f"[경고] 실패 횟수 {failed_login_count}회 - 계정 잠금 정책 발동 대상입니다")

# — 인증서 만료 임박 판정

# cert_days_left = int( input('인증서 만료 남은 일을 입력하세요-> '))

# if cert_days_left <= 7:
#     print(f"[경고] TLS 인증서가 {cert_days_left}일 후 만료됩니다. 즉시 갱신하세요")
# else:
#     print(f"[정상] 인증서 만료까지 {cert_days_left}일 남았습니다")





# — CVSS 점수 기반 심각도 등급 분류
    # |        점수 | 위험도 |
    # | ---------: | ---  |
    # |        0.0 | 없음  |
    # |  0.1 ~ 3.9 | 낮음  |
    # |  4.0 ~ 6.9 | 중간  |
    # |  7.0 ~ 8.9 | 높음  |
    # | 9.0 ~ 10.0 | 치명적 |


# cvss_score = 5.1

# if cvss_score >= 9.0:
#     severity = "CRITICAL"
# elif cvss_score >= 7.0:
#     severity = "HIGH"
# elif cvss_score >= 4.0:
#     severity = "MEDIUM"
# else:
#     severity = "LOW"

# print(f"CVSS {cvss_score} -> 등급: {severity}")




# 불리언으로 처리되는 조건
# failed_login = True
# failed_login = False
# failed_login = 3
# failed_login = 0
# failed_login = -1

# if failed_login:
#     print(f"로그인 실패 {failed_login}회 - 계정 확인 필요")
# else:
#     print("로그인 실패 없음 - 정상")

# word = 'korea'
# print(word.find('k'))
# if word.find('k') != -1:
#     print(f'k는 {word}에 포함')
# print(word.find('b'))
# if word.find('b') != -1:
#     print(f'b는 {word}에 포함')


#============================================
# [ 연습문제 ]
'''
[ 문제 1 ] 
    변수 failed_count = 15가 있습니다. 
    값이 10 이상이면 "계정 잠금 필요", 아니면 "정상"을 출력하는 코드를 작성해 봅시다.

'''
failed_count = 15
if failed_count >= 10:
    print('계정 잠금 필요')
else:
    print('정상')


'''
[ 문제 2 ] 
    patched = False, cvss_score = 9.2 두 변수가 있습니다. 
     패치가 안 되어 있으면서 CVSS가 9.0 이상이면 "즉시 패치 필요", 
     패치는 안 됐지만 CVSS가 9.0 미만이면 "패치 예정", 
     이미 패치되어 있으면 "조치 완료"를 출력하는 if-elif-else를 작성해 봅시다.
'''
patched = False
cvss_score = 9.2
if(patched == True):
    print('조치 완료')
else:
    if(cvss_score >=9):
        print("즉시 패치 필요")
    else:
        print("패치 예정")


'''
[문제 3  ]
  open_port = 6379, approved_ports = {22, 80, 443} (허용 포트 Set)가 있습니다.
   open_port가 approved_ports에 포함되어 있지 않으면 
   "비인가 포트 감지: 6379"를 출력하는 코드를 in 연산자로 작성해 봅시다.
'''
open_port = 6379
approved_ports = {22, 80, 443}

if(open_port not in approved_ports):
    print(f"비인가 포트 감지: {open_port}")