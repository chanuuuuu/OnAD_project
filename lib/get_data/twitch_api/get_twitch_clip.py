

def start(streamer_ids):
    """
    twitch_clip 테이블의 데이터를 반환하는 함수
    * output
     - result : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests
    import time
    # stream api 파라미터 설정
    url = 'https://api.twitch.tv/helix/clips'
    headers = {'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

    total_clips = []  # 총 데이터를 담는 그릇
    time.sleep(1)
    for i, streamer_id in enumerate(streamer_ids):
        cursor = None  # 커서 초기화
        for _ in range(10):
            # 클립 조회수 50 이상인 것들만 가져올 것이기 때문에 더 많은 요청은 낭비임
            # top100 을 넘어서기도 전에 조회수는 50이하로 내려감.
            time.sleep(0.2)
            params = {
                'broadcaster_id': streamer_id,
                'started_at': '2018-12-05T00:00:01Z', # 최초 한번 이후 수정
                'ended_at': '2019-01-08T23:59:59Z',
                'first': 100,
                'after': cursor
                }
            # api 요청
            res = requests.get(url, headers=headers, params=params)
            if res:
                data = res.json()['data']
                total_clips.extend(data)
                if 'cursor' in res.json()['pagination']:
                    cursor = res.json()['pagination']['cursor']
                else: break

        # 받아온 데이터 [{...}, {...}]형태로 만들기
        inform = []  # dict 데이터를 담는 그릇
        for clip in total_clips:
            data_dict = {
                'streamer_id': streamer_id,
                'clip_id': clip['id'],
                'user_id': clip['creator_id'],
                'created_at': clip['created_at'],
                'title': clip['title'],
                'url': clip['url'],
                'viewer_count': clip['view_count'],
                'thumbnail': clip['thumbnail_url'],
            }
        # 최종 반환 데이터에 추가
        inform.extend(data_dict)
        print("스트리머 %s/%s 완료" % (i + 1, len(streamer_ids)))
    
    return inform
