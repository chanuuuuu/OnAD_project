
def start():
    """
    twitch_stream 테이블의 데이터를 반환하는 함수
    twitch_stream_detail 테이블의 데이터를 반환하는 함수

    * output
       (twitch_stream_data, twitch_stream_detail_data)
     - twitch_stream_data : 리스트, data_dict들의 모음
     - twitch_stream_detail_data : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests

    # stream api 파라미터 설정
    url = 'https://api.twitch.tv/helix/streams'
    headers = {'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

    cursor = None
    streamers = list()

    while True:
        # 파라미터 설정
        # first : 긁어오는 개수 100이 최대
        # after : 다음 긁어올 커서의 위치
        params = {'first': 100 , 'language':'ko', 'after': cursor }

        # api 요청
        res = requests.get(url, headers=headers, params=params)
        if res:
            print("로드함")
            data_ = res.json()
            streamers.extend(data_['data'])
            
            if data_['pagination']:
                cursor = data_['pagination']['cursor']
            else: break

    # 10 명이하의 시청자를 가진 스트리머는 제외 (필요치 않을 듯)
    streamings = [stream for stream in streamers if stream['viewer_count'] > 10]

    # 개별 data_dict 를 리스트안에 넣어 반환하기 위해
    twitch_stream_data = []
    twitch_stream_detail_data = []

    for streaming in streamings:
        stream_id = streaming['id']
        streamer_id = streaming['user_id']
        streamer_name = streaming['user_name']
        broad_date = streaming['started_at']
        title = streaming['title']
        viewer = streaming['viewer_count']
        game_id = streaming['game_id']

        twitch_stream_data_dict = {
            'stream_id': stream_id,
            'streamer_id': streamer_id,
            'streamer_name': streamer_name,
            'broad_date': broad_date,
        }
        twitch_stream_data.append(twitch_stream_data_dict)

        twitch_stream_detail_data_dict = {
            'stream_id': stream_id,
            'viewer': viewer,
            'title': title,
            'game_id': game_id,
        }
        twitch_stream_detail_data.append(twitch_stream_detail_data_dict)
    
    return twitch_stream_data, twitch_stream_detail_data
