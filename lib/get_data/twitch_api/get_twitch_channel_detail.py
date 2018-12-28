
def start(list_streamer_id):
    """
    twitch_game_detail 테이블의 데이터를 반환하는 함수
    * output
        - result : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests

    # stream api 파라미터 설정
    headers = {
            'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko',
            'Accept': 'application/vnd.twitchtv.v5+json'
            }

    inform = []
    for streamer_id in list_streamer_id:
        url = 'https://api.twitch.tv/kraken/channels/%s' % streamer_id
        
        res = requests.get(url, headers=headers)
        data_ = res.json()

        data_dict = {
            "streamer_id": data_['_id'],
            "follower": data_['followers'],
            "viewer": data_['views'],
        }
        inform.append(data_dict)
    return inform