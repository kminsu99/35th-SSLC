#35기_파이썬_PBL_BASIC02_강민수
"""
방화벽 구간 패킷 손실률(Packet Loss Rate) 점검, 회선 이상 여부 보고
모니터링 로그, 정상적 숫자 외 측정실패(None), 장비 통신 오류 문자열(Timeout, Error) 같은 
비정상 값이 섞여 들어옴, 이 값으로 연산하면 오류
따라서 이상 입력값 필터링, 특정 위험수치 감지->즉시 대응(중단)

요구사항
1. 데이터 처리 : 제공된 [raw_logs]순회, 패킷로스율 분석
2. 예외 상황 대응 : 숫자로 변환할 수 없는값(문자열, None etc)등은 예외처리->에러메시지 출력 후 다음 로그
3. 비상 중단 : 로그 중 손실률 99%이상 -> 대규모 DDos공격 징후로 간주 즉시 반복문 탈출(break)
4. 비지니스 로직(아래 순서로 우선판정)
'''
95% 이상 : [CRITICAL] 즉시 회선 차단 및 우회 경로 전환 MSG 출력
70% 이상 : [WARNING] 네트워크 관리자 호출 및 회선 점검 MSG 출력
0% : [CEHCK] 트래픽 없음 - 회선 다운 의심 MSG 출력
'''
5. 공통 마감 : 성공/실패 여부와 상관 없이 각 점검 건마다 구분선 출력(finally use)
6. 결과 요약 : 전체 점검이 끝난 뒤, List Comprehension사용 [WARNING] 이상(70% 이상)으로 판정된 손실률 값만 모은 리스트 별도 출력

"""

#데이터 준비
import random

line_names = [f"LINE-{i:02d}" for i in range(1,13)]
raw_logs = [random.randint(1,100) for _ in range(10)] + [0, "Timeout", None, 99, "Error"]
random.shuffle(raw_logs)

#1. 데이터 처리 : 제공된 [raw_logs]순회, 패킷로스율 분석
print("--- 실시간 네트워크 트래픽 점검 시작 ---")
for log in raw_logs:
    #에러 가드 설치
    #2. 예외 상황 대응 : 숫자로 변환할 수 없는값(문자열, None etc)등은 예외처리->에러메시지 출력 후 다음 로그
    try:
        log = float(log)
        #조건 우선순위 설정
        # 3. 비상 중단 : 로그 중 손실률 99%이상 -> 대규모 DDos공격 징후로 간주 즉시 반복문 탈출(break)
        if log >= 99:
            print(f"[EMERGENCY] {log:.1f} 감지! 대규모 DDos 공격 의심으로 전체 점검 중단!")
            break
        # 4. 비지니스 로직(아래 순서로 우선판정)
        # 95% 이상 : [CRITICAL] 즉시 회선 차단 및 우회 경로 전환 MSG 출력
        elif log >= 95:
            print(f"[CRITICAL] 패킷 손실률 {log:.1f}%: 즉시 회선 차단 및 우회 경로 전환")
        # 70% 이상 : [WARNING] 네트워크 관리자 호출 및 회선 점검 MSG 출력
        elif log >= 70:
            print(f"[WARNING] 패킷 손실률 {log:.1f}%: 네트워크 관리자 호출 및 회선 점검 필요")
        # 0% : [CEHCK] 트래픽 없음 - 회선 다운 의심 MSG 출력
        elif log == 0:
            print(f"[CEHCK] 패킷 손실률 {log:.1f}%: 트래픽 없음 (회선 다운 의심)")
        else:
            print(f"[NORMAL] 패킷 손실률 {log:.1f}%: 회선 정상")
    #예외 핸들링
    except:
        print(f"[DATA ERROR]읽을 수 없는 로그 형식입니다. (입력값: {log})")
        continue
    #공통 마감 출력
    #5. 공통 마감 : 성공/실패 여부와 상관 없이 각 점검 건마다 구분선 출력(finally use)
    finally:
        print("-" * 15, " 점검 완료 ", "-" * 15)

#요약 출력
#6. 결과 요약 : 전체 점검이 끝난 뒤, List Comprehension사용 [WARNING] 이상(70% 이상)으로 판정된 손실률 값만 모은 리스트 별도 출력
print("[요약] 위험(WARNING 이상) 손실률 목록: ", end="")
#type(log) == float or << log는 float형 실수가 저장되있지않음, int형만 있음 따라서 불요
warning_list = [float(log) for log in raw_logs if (type(log)==int) and float(log) >= 70.0]
print(warning_list)
