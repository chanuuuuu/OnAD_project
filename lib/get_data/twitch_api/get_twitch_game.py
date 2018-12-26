
def start():
    """
    twitch_game 테이블의 데이터를 반환하는 함수
    * output
     - result : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests

    # stream api 파라미터 설정
    url = 'https://api.twitch.tv/kraken/games/top'
    headers = {'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

    cursor = None

    while True:
        # 파라미터 설정
        # first : 긁어오는 개수 100이 최대
        # after : 다음 긁어올 커서의 위치
        params = {'limit': 100, 'after': cursor}

        # api 요청
        res = requests.get(url, headers=headers, params=params)
        if res:
            data_ = res.json()
            # 게임 인기 순위
            print(data_)
            break