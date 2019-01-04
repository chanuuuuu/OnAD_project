def start(list_streamer_id):
    """
    twitch_channel과 twitch_channel_detail  테이블의 데이터를 반환하는 함수
    * input
     - list_streamer_id : streamer_id 의 리스트 (twitch_stream 테이블의 group_by(streamer_id))
    * output
     - inform : 리스트, data_dict들의 모음
     - detail_inform : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests
    import time
    # stream api 파라미터 설정
    headers = {
            'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko',
            'Accept': 'application/vnd.twitchtv.v5+json'
            }

    inform = []  # 채널 데이터
    detail_inform = []  # 채널 세부 데이터
    for i, streamer_id in enumerate(list_streamer_id):
        url = 'https://api.twitch.tv/kraken/channels/%s' % streamer_id
        time.sleep(0.5)
        res = requests.get(url, headers=headers)
        print(res)
        if res:
            data_ = res.json()

            data_dict = {
                "streamer_id": data_['_id'],
                "streamer_name": data_['display_name'],
                "logo": data_['logo'],
                "homepage": data_['url'],
            }

            inform.append(data_dict)

            detail_data_dict = {
                "streamer_id": data_['_id'],
                "follower": data_['followers'],
                "viewer": data_['views'],
            }
            print(detail_data_dict)
            detail_inform.append(detail_data_dict)

            print("채널 데이터 %s/%s 로드완료" % (i + 1, len(list_streamer_id)))

    return inform, detail_inform