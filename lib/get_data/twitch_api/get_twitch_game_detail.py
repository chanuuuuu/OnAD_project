

def start():
    """
    twitch_game_detail 테이블의 데이터를 반환하는 함수
    * output
     - result : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests

    # stream api 파라미터 설정
    url = 'https://api.twitch.tv/kraken/games/top'
    headers = {'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

    total_games = []
    for _ in range(10):
        params = {'limit': 100}
        # api 요청
        res = requests.get(url, headers=headers, params=params)
        if res:
            data_ = res.json()
            total_games.extend(data_['top'])
            if '_links' not in data_:
                break
            else:
                if 'next' in data_['_links']:
                    url = data_['_links']['next']

    inform = [{"game_id": data['game']['_id'],
            "all_viewer": data['viewers'],
            "stream_this_game": data['channels']} for data in total_games]
            
    return inform
