import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_security_news():

    # 현재 보안뉴스 메인 페이지
    url = "https://www.boannews.com/"

    #정상적인 브라우저 접근인지 헤더로 확인하는 사이트도 있음
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
        for a in links:
            title = a.get_text()
            href = a.get('href')

            # 링크가 없으면 제외
            if not href: continue

            # 링크가 보안뉴스 외부 링크 제외
            if "boannews" not in href: continue

            seen_titles.add(title)
            count += 1
            print(f"\n {count}. {title}")
            print(f"🔗 {href}")
            if count == 10: break
        if count == 0:
            print("❌ 뉴스 기사를 찾지 못했습니다.")

    except requests.exceptions.RequestException as e:
        print("❌ 웹사이트 연결 오류")
        print(e)
def get_security_news_return_str():
    url = "https://www.boannews.com/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(
            url,
            # headers=headers,
            timeout=10
        )
        response.raise_for_status()
        soup = BeautifulSoup(   response.text,  "html.parser"  )
        links = soup.find_all("a")
        count = 0
        seen_titles = set()
        str_data = ""
        for a in links:
            title = a.get_text()
            href = a.get('href')
            if not href: continue
            if "boannews" not in href: continue
            seen_titles.add(title)
            count += 1
            if count == 10: break
            #출력을 문자열로 저장, <br>이 html 줄바꿈
            str_data += (f"{count}. {title}<br>🔗 {href}<br>")
        if count == 0:
            print("❌ 뉴스 기사를 찾지 못했습니다.")
        else:
            return str_data #문자열 리턴
    except requests.exceptions.RequestException as e:
        print("❌ 웹사이트 연결 오류")
        print(e)

if __name__ == "__main__":
    get_security_news()