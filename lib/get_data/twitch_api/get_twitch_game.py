
def start(api_key, ):
    """
    twitch_game 테이블의 데이터를 반환하는 함수
    * output
     - result : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests
    # stream api 파라미터 설정
    url = 'https://api.twitch.tv/helix/games/top'
    headers = {'Client-ID' : api_key}

    cursor = None
    data = []
    while True:
        params = {'first': 100, 'after': cursor}
        # api 요청
        res = requests.get(url, headers=headers, params=params)
        if res:
            data_ = res.json()
            data.extend(data_['data'])
            if data_['pagination']:
                cursor = data_['pagination']['cursor']
            else : break

    total_games = [ {"game_id": i['id'], "game_name": i['name'], "thumbnail": i['box_art_url']} for i in data]

    return total_games