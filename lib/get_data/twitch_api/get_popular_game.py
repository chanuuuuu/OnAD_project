"""
1분단위 실행

트위치 api 이용하여
'./data/popular_games' 폴더에
'popular_games_오늘날짜_시간' 으로 저장

* 저장되는 데이터 :
    게임이름, 그 게임을 보는 시청자 수
"""

import requests
from datetime import datetime 
import os

# api 파라미터 설정
url = 'https://api.twitch.tv/kraken/games/top'
headers = {'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
params = {'limit': 100 }
cursor = None
params['after'] = cursor

data_list = []
# api 요청
res = requests.get(url, headers=headers, params=params )
if res:
    data_ = res.json()

    # 게임 인기 순위
    game_ranking = [games['game']['localized_name'] for games in data_['top']]
    # 인기도
    popularity = [games['game']['popularity'] for games in data_['top']]

    # 스트리머 이름, 제목, 시청자수 저장
    popular_games = list(zip(game_ranking, popularity))


    # 저장될 폴더 만들기
    data_folder = "C:\\Users\\idec\\Google 드라이브\\onad\\data"
    popular_games_folder = "C:\\Users\\idec\\Google 드라이브\\onad\\data\\popular_games"

    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
        
    if not os.path.exists(os.getcwd() + popular_games_folder):
        os.mkdir(os.getcwd() + popular_games_folder)


    with open(popular_games_folder + '\\popular_games_%s.txt' % datetime.now().strftime("%Y-%m-%d_%H%M"), 'a', encoding='utf-8') as fp:
        for data in popular_games:
            fp.write(str(data[0]) + " " + str(data[1]) + '\n')

else:
    with open(popular_games_folder + '\\popular_games_%s.txt' % datetime.now().strftime("%Y-%m-%d_%H%M"), 'a', encoding='utf-8') as fp:
        fp.write("에러")

print("완료")
