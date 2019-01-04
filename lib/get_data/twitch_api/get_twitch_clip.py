

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
        while True:
            time.sleep(0.2)
            params = {
                'broadcaster_id': streamer_id,
                'after': cursor
                }
            # api 요청
            res = requests.get(url, headers=headers, params=params)
            if res:
                data_ = res.json()
                total_clips.extend(data_['data'])

                if data_['pagination']:
                    cursor = data_['pagination']['cursor']
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
