
def start(api_key, channel_list):
    '''
    채널세부정보 딕셔너리들이 모인 리스트로 반환하는 함수
    *input
        - channel_list(list) : 채널고유ID 목록
    *output
        - [{채널정보}, {}, ...]
    '''
    # 각 채널 하나하나의 데이터를 받아오는 함수
    def get_channel_detail(api_key, channel_id, is_user=None):
        '''
        각 채널의 세부정보를 반환하는 함수
        * input
        channel_id : 채널 고유 ID
        is_user : 채널명이 user/유튜버이름 인지의 flag 값
            user인 경우 "user" 또는 True 입력
        api_key : API key 값
        
        * output
            정보 묶음(list)
                [channel_id, 구독자수, 채널조회수, 모든 영상 수]
        '''
        import requests
        from bs4 import BeautifulSoup

        if is_user: # user 라면(셀럽의 경우 user/youtuber-id 형식의 채널명을 가짐)
            # 채널 고유 id를 가져오기 위한 api 호출
            target_url = '''https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={}&key={}'''.format(channel_id, api_key) 
            html = requests.get (target_url)
            soup = BeautifulSoup (html.text, "html.parser" )
            api_dict = eval(soup.text.replace("false", "False").replace("true", "True"))
            channel_id = api_dict['items'][0]["id"]  # 기존의 channel_id와 같은 형식의 channel_id

        param = "statistics"
        channel_detail_info = {
            'channel_id': "",
            'subscribe_cnt': "",
            'hit_cnt': "",
            'total_video_cnt': "",
        }

        target_url ='''https://www.googleapis.com/youtube/v3/channels?part={}&id={}&key={}'''.format(param, channel_id, api_key) 
        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )
        api_dict = eval(soup.text.replace("false", "False").replace("true", "True"))
        if api_dict['items']:
            if api_dict['items'][0]:
                channel_detail_info['channel_id'] = api_dict['items'][0]['id']  # 채널 고유ID
                channel_detail_info['subscribe_cnt'] = api_dict["items"][0][param]['subscriberCount']  # 채널구독자수
                channel_detail_info['hit_cnt'] = api_dict["items"][0][param]['viewCount']  # 채널조회수
                channel_detail_info['total_video_cnt'] = api_dict["items"][0][param]['videoCount']  # 채널에 올린 동영상 수
        
        return channel_detail_info

    # 채널 리스트 모두를 돌며 위의 함수 실행
    for channel_id in channel_list:
        if "/user" in channel_id:
            # user 채널이라면
            channel_detail_info = [get_channel_detail(api_key, channel_id.replace("/user", ""), is_user=True)
                                    for channel_id in channel_list]
            # 채널 기본 정보 리스트를 반환
            return channel_detail_info
        else:
            channel_detail_info = [get_channel_detail(api_key, channel_id) for channel_id in channel_list]
            # 채널 기본 정보를 반환
            return channel_detail_info
    
