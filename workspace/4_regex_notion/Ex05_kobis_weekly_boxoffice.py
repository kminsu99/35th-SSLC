import os
import requests
from dotenv import load_dotenv

# .env 파일의 환경변수 불러오기
load_dotenv()

# 영화진흥위원회(KOBIS) 주간 박스오피스 API

MOVIE_API_KEY = os.getenv("MOVIE_API_KEY")
MOVIE_BASE_URL = os.getenv("MOVIE_BASE_URL")

if not MOVIE_API_KEY:
    # 예외 발생
    raise ValueError(".env 파일에 MOVIE_API_KEY가 없습니다.")


url = MOVIE_BASE_URL + "/searchWeeklyBoxOfficeList.json"
params = {
    "key" : MOVIE_API_KEY,
    "targetDt" : 20260927, #YYYYMMDD
    "weekGb" : 0, #0주간/1주말/2주중
}
request_json = f"{MOVIE_BASE_URL}/searchWeeklyBoxOfficeList.json"
response =  requests.get(f"{request_json}"
             , params=params
             , timeout=5)
print(response)

response.raise_for_status()

# print(f"상태 코드 : {response.status_code}")
# print(f"최종 요청 url : {response.url}")
# print(f"데이터 형식: {response.headers.get('Content-Type')}")

data = response.json()
# print(data)
box_office = data.get('boxOfficeResult', {}).get('weeklyBoxOfficeList', [])
# print(lambda movie.get('movieNm'): movie.get('rank')<10, ranking)
for movie in box_office:
    print(
        f"{movie.get('rank', ''):>3} 위   "
        f"제목 : {movie['movieNm']:<5}   "
        f"/ 개봉일 : {movie['openDt']}   "
        f"/ 관람수 : {movie.get('audiAcc')} 명"
    )