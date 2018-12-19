"""
1분단위 실행

트위치 api 이용하여
지금 스트리밍중인 스트리머 리스트 가져와
'./data/live_stream' 폴더에
'live_stream_오늘날짜_시간' 으로 저장

* 저장되는 데이터 :
    스트리머 이름, 스트리머 id, 지금 시청자 수
"""


import json
import pandas as pd
import requests
from datetime import datetime 
import re
import os

# api 파라미터 설정
url = 'https://api.twitch.tv/helix/streams'
headers = {'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
params = {'first': 100 , 'language':'ko', 'after': None }
cursor = None
data_list = []
params['after'] = cursor

# api 요청
res = requests.get(url, headers=headers, params=params )
if res:
    data_ = res.json()
    streamers = res.json()['data']

    # 저장될 폴더 만들기
    data_folder = "C:\\Users\\idec\\Google 드라이브\\onad\\data"
    live_stream_folder = "C:\\Users\\idec\\Google 드라이브\\onad\\data\\twitch_live_stream_list"

    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
        
    if not os.path.exists(live_stream_folder):
        os.mkdir(live_stream_folder)

    # 스트리머 이름, 제목, 시청자수 저장
    for streamer in streamers:
        name  = streamer['user_name']
        viewer = streamer['viewer_count']
        title = streamer['title']
        url = streamer['thumbnail_url']
        p = re.compile('(live_user_)(?P<user_id>[\w]+)(-)')
        m = p.search(url)

        with open(live_stream_folder + '\\live_stream_%s.txt' % datetime.now().strftime("%Y-%m-%d_%H%M"), 'a', encoding='utf-8') as fp:
            fp.write(name + " " + m.group('user_id') + " " + str(viewer))
            fp.write('\n')

else:
    with open(live_stream_folder + '\\live_stream_%s.txt' % datetime.now().strftime("%Y-%m-%d_%H%M"), 'a', encoding='utf-8') as fp:
        fp.write('에러')

print("완료")
