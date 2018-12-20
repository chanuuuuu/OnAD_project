"""
1.activities : 특정 채널이나 사용자가 유튜브에서 실행한 모든 작업 정보가 포함됨 (* 필수파라미터: (3)=channelId)
1) part=snippet: 동영상 업로드, 채널의 즐겨찾기
"""






import requests, json
from bs4 import BeautifulSoup 

api_key = "AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak"
param = "22"

target_url = "https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=KR&hl=ko-kr&pageToken=&key={}".format(api_key)

session = requests.Session ()
headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }

# 우선 동영상 페이지에 requests를 실행 html 소스를 손에 넣어 live_chat_replay의 선두 url을 입수
html = requests.get (target_url)
soup = BeautifulSoup (html.text, "html.parser" )

test = eval(soup.text.replace("false","False").replace("true","True"))