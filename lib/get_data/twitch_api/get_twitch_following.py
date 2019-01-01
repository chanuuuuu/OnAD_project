

def start(streamer_id):
    """
    twitch_following 테이블의 데이터를 반환하는 함수
    * output
     - result : 리스트, data_dict들의 모음
    """
    # api 요청
    import requests

    # stream api 파라미터 설정
    url = 'https://api.twitch.tv/helix/users/follows'
    headers = {'Client-ID' : 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

    total_clips = []
    cursor = None
    while True:
        params = {
            'to_id': streamer_id,
            'after': cursor,
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
    inform = []
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
        inform.append(data_dict)
            
    return inform
