import feedparser
import time
import requests

# 보안 뉴스 RSS 주소
# 전체기사: https://www.boannews.com/rss/allArticle.xml
# 인기기사: https://www.boannews.com/rss/clickTop.xml
# 사건·사고: https://www.boannews.com/rss/S1N2.xml
# 공공·정책: https://www.boannews.com/rss/S1N3.xml
# 비즈니스: https://www.boannews.com/rss/S1N4.xml
rss_url = "https://www.boannews.com/rss/clickTop.xml"

feed = feedparser.parse(rss_url)
# print(feed)

news_list = feed.entries[:10]
print(news_list[0])
print("-" * 40)

for news in news_list:
    print(f"제목 : {news.title}")
    print(f"🔗링크 : {news.link}")
    #뉴스일을 0000년 00월 00일 00시 00분
    t = time.strptime(str(news.published), "%Y-%m-%d %H:%M:%S")
    print(f'게시일: {t.tm_year}년 {t.tm_mon}월 {t.tm_mday}일 {t.tm_hour}시 {t.tm_min}분')
    
    from datetime import datetime
    dt = datetime.strptime(news.published, "%Y-%m-%d %H:%M:%S")
    print(f'날짜: {dt.strftime("%Y년 %m월 %d일 %H시 %M분")}')





