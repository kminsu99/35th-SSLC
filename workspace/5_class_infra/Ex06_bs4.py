import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_security_news():

    # 현재 보안뉴스 메인 페이지
    url = "https://www.boannews.com/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        # ==================================
        # 1. 웹페이지 요청
        # ==================================
        response = requests.get(
            url,
            # headers=headers,
            timeout=10
        )

        response.raise_for_status()

        print("✅ 연결 성공")
        print("상태 코드:", response.status_code)


        # ==================================
        # 2. HTML 파싱
        # ==================================
        soup = BeautifulSoup(   response.text,  "html.parser"  )


        # ==================================
        # 3. 모든 링크 확인
        # ==================================
        links = soup.find_all("a")

        print("\n" + "=" * 60)
        print("🛡️ 최신 보안 뉴스")
        print("=" * 60)


        count = 0
        seen_titles = set()

        #--------------------------------------------
        # 여기
        


        if count == 0:
            print("❌ 뉴스 기사를 찾지 못했습니다.")


    except requests.exceptions.RequestException as e:
        print("❌ 웹사이트 연결 오류")
        print(e)


if __name__ == "__main__":
    get_security_news()