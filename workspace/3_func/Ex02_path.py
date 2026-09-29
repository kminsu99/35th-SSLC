# 2-1. 경로 
# os 방식: 문자열 더하기나 join 함수 사용
# import os
# os_path = os.path.join("security_logs", "2026", "weekly_report.txt")
# print(f"OS 경로: {os_path}")

# # pathlib 방식: / 기호로 직관적 연결
# from pathlib import Path
# pure_path = Path("security_logs") / "2026" / "weekly_report.txt"
# print(f"Pathlib 경로: {pure_path}")

'''
절대경로 : 시작점부터 시작하는 경로

상대경로 : 기준점부터 시작하는 경로
'''

# 2-2. 디렉터리 생성 및 존재 확인 — 감사 로그 저장소 준비
# os 방식
# import os

# if not os.path.exists("security_logs1/daily"):
#     os.makedirs("security_logs1/daily")
#     with open("security_logs1/daily/audit.log", "w", encoding="utf-8") as f:
#         f.write("audit start, 작업시작")
#     file_name = os.path.basename("security_logs1/daily/audit.log")
#     print(file_name)

# pathlib 방식
# from pathlib import Path

# if not Path("security_logs2/daily").exists():
#     Path("security_logs2/daily").mkdir(parents=True, exist_ok=True)
#     Path("security_logs2/daily/audit.log").touch()
#     file_name = Path("security_logs2/daily/audit.log").name
#     print(file_name)


# 2-3. 파일 목록 검색(Wildcard) — 오늘 생성된 로그만 찾기

# os 방식 (glob 모듈 따로 필요)
# import glob
# log_files_os = glob.glob("3_func/*.py")
# print(log_files_os)

"""
 . : 현재dir
 .. : 부모dir
"""

# pathlib 방식 (자체 지원)
# from pathlib import Path

# log_files_path = list(Path(".").glob("l*.log"))

# for file in log_files_path:
#     print(f"발견된 로그: {file.name}, 크기: {file.stat().st_size} bytes")

"""
### 문제 2-A. pathlib로 폴더·파일 생성 및 확인

os 모듈은 사용하지 않고, pathlib만 사용해 아래 순서대로 동작하는 코드를 작성하세요.

1. reports/2026/09 폴더를 생성한다 (이미 존재해도 오류 없이)
2. 해당 폴더 안에 scan_result.txt 파일을 생성하고 "Scan completed: 3 hosts checked" 내용을 저장한다
3. 파일이 존재하는지 확인 후, 존재하면 "✅ 파일 확인: <파일명>" 형태로 출력한다
4. 파일 크기(bytes)도 함께 출력한다
"""
# [ 도전 문제 2-A ]
from pathlib import Path
reports_path = "reports/2026/09"
Path(reports_path).mkdir(parents=True, exist_ok=True)
source = Path(reports_path) / "scan_result.txt"
Path(source).touch()
Path(source).write_text("Scan completed: 3 hosts checked", encoding="utf-8")
if Path(source).exists():
    print("✅ 파일 확인: <파일명>")
    print(f"파일 크기: {Path(source).stat().st_size} bytes")
"""
기대 출력:
    ✅ 파일 확인: scan_result.txt
    파일 크기: 35 bytes

💡 힌트: 파일 크기는 Path 객체의 .stat().st_size 속성으로 구합니다.
"""


# 2-4. 파일 이동/복사/이름 변경 — 점검 완료 로그 아카이빙
# from pathlib import Path
# import shutil

# # [1] 준비 작업
# source = Path("latest_scan.log")
# if not source.exists():
#     source.write_text("포트 스캔 결과 Port Scan Result: 3306 OPEN", encoding="utf-8")

# archive_dir = Path("archive")
# destination1 = archive_dir / "copy_scan.log"   # 경로 결합

# [2] 복사 및 이동 로직
# if source.exists():
#     archive_dir.mkdir(exist_ok=True)

#     # 복사 (원본 유지) — 감사팀 제출용 사본
#     # shutil.copy(source, destination1)
    
#     # 이동 (원본 삭제) — 처리 완료된 로그를 아카이브로 이동
#     # shutil.move(source, archive_dir)

#     # 폴더 내 파일 목록 출력 (glob 사용)
#     # file_list = archive_dir.glob("*.log")
#     # print(f"현재 log 파일 목록 : {list(file_list)}")

#     # 이름 변경 (rename) — 날짜별 스캔 이력 구분
#     # new_path = archive_dir / "2026-09-28_scan.log"
#     # # destination1.rename(new_path)
#     # shutil.move(destination1, new_path)

#     # 최종 전체 목록 확인
    
#     # final_list = list(archive_dir.iterdir())
#     # final_list = list(Path('.').iterdir())
#     # print(f"최종 아카이브 : {final_list}")



# #연습
# from pathlib import Path
# import shutil

# # 상황:
# # 서버에서 생성된 보안 로그(security.log)를 백업 폴더에 복사하고,
# # 원본 로그는 처리 완료 폴더로 이동하려고 합니다.


# # 1. 준비 작업
# # 현재 폴더에 "security.log" 파일이 있는지 확인하세요.
# # 파일이 없다면 아래 내용을 가진 파일을 생성하세요.
# #
# # "Suspicious Login Detected"
# src = Path("security.log")
# if not src.exists():
#     src.touch()


# # 2. 폴더 및 경로 준비
# # "backup" 폴더와 "processed" 폴더를 사용할 예정입니다.
# #
# # backup 폴더 안에 "security_backup.log"라는 경로를 만드세요.
# backup_dir = Path("backup/")
# backup_file = backup_dir / "security_backup.log"
# Path(backup_dir).mkdir(parents=True, exist_ok=True)
# Path(backup_file).touch()

# # 3. 파일 복사
# # security.log 파일을 backup/security_backup.log로 복사하세요.
# #
# # 원본 security.log 파일은 유지되어야 합니다.
# shutil.copy(src, Path(backup_file))


# # 4. 파일 이동
# # 원본 security.log 파일을 processed 폴더로 이동하세요.
# #
# # 이동 후 현재 폴더에는 security.log가 없어야 합니다.
# processed_dir = Path("processed/")
# processed_dir.mkdir(parents=True, exist_ok=True)
# shutil.move(src, "processed")

# # 5. 로그 파일 검색
# # backup 폴더에서 확장자가 ".log"인 파일 목록을 glob()을 사용하여 출력하세요.
# print(list(backup_dir.glob("*.log")))

# # 6. 파일 이름 변경
# # backup/security_backup.log 파일이 존재한다면
# # "backup_2026.log"로 이름을 변경하세요.
# # if Path(backup_file).exists():
# #     Path(backup_file).rename("backup/backup_2026.log")

# # 7. 최종 확인
# # backup 폴더의 모든 파일 목록을 출력하세요.
# # processed 폴더의 모든 파일 목록도 출력하세요.
# print(list(backup_dir.glob("*")))
# print(list(processed_dir.glob("*")))