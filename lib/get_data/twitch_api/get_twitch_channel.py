def start(list_streamer_id):
    """
    twitch_channel 테이블의 데이터를 반환하는 함수
    * input
     - list_streamer_id : streamer_id 의 리스트 (twitch_stream 테이블의 group_by(streamer_id))
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
    i = 1
    for streamer_id in list_streamer_id:
        url = 'https://api.twitch.tv/kraken/channels/%s' % streamer_id
        
        res = requests.get(url, headers=headers)
        if res:
            data_ = res.json()

            data_dict = {
                "streamer_id": data_['_id'],
                "streamer_name": data_['display_name'],
                "logo": data_['logo'],
                "homepage": data_['url'],
            }
            inform.append(data_dict)
            print("채널 데이터 %s/%s 로드완료" % (i, len(list_streamer_id)))
            i += 1

    return inform