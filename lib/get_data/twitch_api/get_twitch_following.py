
def start(streamer_list):
    """
    twitch_following 테이블의 데이터를 반환하는 함수
    * output
     - result : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests
    import time

    # stream api 파라미터 설정
    url = 'https://api.twitch.tv/helix/users/follows'
    headers = {'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

    total_followers = []
    for i, streamer_id in enumerate(streamer_list):
        cursor = None
        while True:
            params = {
                'first': 100,
                'to_id': streamer_id,
                'after': cursor,
                }

            time.sleep(0.5)
            # api 요청
            res = requests.get(url, headers=headers, params=params)
            if res:
                data_ = res.json()
                total_followers.extend(data_['data'])

                if data_['pagination']:
                    cursor = data_['pagination']['cursor']
                else: break

        # 받아온 데이터 [{...}, {...}]형태로 만들기
            inform = [{
                'user_id': follower['from_id'],
                'following_streamer': follower['to_id'],
                'streamer_name': follower['to_name'],
                'followed_at': follower['followed_at']
            } for follower in total_followers ]
            
    return inform
