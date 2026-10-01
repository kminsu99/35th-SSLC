from ftplib import FTP
from pathlib import Path


def backup_log():
    HOST = "127.0.0.1" #local ip
    # HOST = "192.168.10.41" # 짝꿍 아이피 가능
    PORT = 2121

    # 로컬 파일 위치를 변수로 관리
    BASE_DIR = Path(__file__).parent
    DOWNLOAD_FOLDER = BASE_DIR / "download"
    # DOWNLOAD_FOLDER = "download"
    SOURCE_FILE = "security_report.txt"

    # 서버에 저장된 파일명
    backup_file = "daily_report_backup.txt"

    # 폴더 + 파일명 결합
    local_file = Path(DOWNLOAD_FOLDER) / SOURCE_FILE

    # 1. 서버 접속 및 로그인
    with FTP() as ftp:
        ###
        ftp.connect(HOST, PORT)
        ftp.login("anonymous", "anonymous")
        print("--- FTP 서버 접속 완료 ---")

        ### 2. 파일 다운로드 실습 (Server -> Local)
        with open(local_file, "wb") as f:
            ftp.retrbinary(f"RETR {backup_file}", f.write)
        print("보안 리포트 다운로드 성공!")


if __name__ == "__main__":
    backup_log()