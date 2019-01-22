
def start(api_key, streamer_ids, started_at, ended_at):
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
    headers = {'Client-ID' : api_key}

    total_clips = []  # 총 데이터를 담는 그릇
    for i, streamer_id in enumerate(streamer_ids):
        print(streamer_id)
        cursor = None  # 커서 초기화
        params = {
            'started_at': started_at, # 최초 한번 이후 수정
            'ended_at': ended_at,
            'broadcaster_id': streamer_id,
            'first': 100,
            'after': cursor
            }
        # api 요청
        res = requests.get(url, headers=headers, params=params)
        if res:
            data = res.json()['data']
            total_clips.extend(data)

            # 조회수 500 이상인 경우만
            total_clips = [clip for clip in total_clips if clip['view_count'] > 100]

        # 받아온 데이터 [{...}, {...}]형태로 만들기
        inform = []  # dict 데이터를 담는 그릇
        for clip in total_clips:
            data_dict = {
                'streamer_name': clip['broadcaster_name'],
                'streamer_id': clip['broadcaster_id'],
                'clip_id': clip['id'],
                'user_id': clip['creator_id'],
                'created_at': clip['created_at'],
                'title': clip['title'],
                'url': clip['url'],
                'viewer_count': clip['view_count'],
                'thumbnail': clip['thumbnail_url'],
            }
            # 최종 반환 데이터에 추가
            inform.append(data_dict)
        print("스트리머 %s/%s 완료" % (i + 1, len(streamer_ids)))
    
    return inform
