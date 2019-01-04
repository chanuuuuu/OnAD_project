
def start(api_key, channel_list, is_detail=None):
    '''
    채널정보를 딕셔너리들이 모인 리스트로 반환하는 함수
    *input
        - channel_list(list) : 채널고유ID 목록
    *output
        - [{채널정보}, {}, ...]
    '''
    import requests
    from bs4 import BeautifulSoup

    # 개별 채널 id로 api 접촉하여 데이터 받아옴
    def get_channel_info(api_key, channel_id, is_user=None):
        '''
        각 채널의 정보를 반환하는 함수
        * input
        channel_id : 채널 고유 ID
        is_user : 채널명이 user/유튜버이름 인지의 flag 값
            user인 경우 "user" 또는 True 입력
        api_key : API key 값
        
        * output
            channel_info(list)
            [채널 이름(str), 채널설립일자(str) - YY-MM-DD,채널설명(str), 검색 키워드(list / str) - 있을 경우에만 return,
            추천 채널 목록(list / 추천 채널 고유 ID(str) - 추천 채널 이름(str)) - 있을 경우에만 return]
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

        param = ["snippet", "brandingSettings"]
        # 데이터를 담을 그릇정의
        channel_info = {
            "channel_name": "",
            "published_at": "",
            "description": "",
            "thumbnail": "",
            "channel_id": "",
            "keyword": "",
            "recommend_channels": "",
        }
        
        for part in param:
            target_url ='''https://www.googleapis.com/youtube/v3/channels?part={}&id={}&key={}'''.format(part, channel_id, api_key) 
            html = requests.get (target_url)
            soup = BeautifulSoup (html.text, "html.parser" )
            api_dict = eval(soup.text.replace("false","False").replace("true","True"))
            if api_dict['items']:
                if part == "snippet":
                    channel_info['channel_name'] = api_dict["items"][0][part]["title"]  # 채널제목
                    channel_info['description'] = api_dict["items"][0][part]["description"]  # 채널설명
                    channel_info['published_at'] = api_dict["items"][0][part]['publishedAt'][:10]  # 채널설립일자
                    channel_info['thumbnail'] = api_dict["items"][0][part]["thumbnails"]['default']['url']  # 썸네일 주소
                    if api_dict['items'][0]:
                        channel_info['channel_id'] = api_dict['items'][0]['id']  # 채널고유ID
                
                else:  # brandingSettings
                    if "keywords" in api_dict["items"][0][part]['channel']:
                        # 검색키워드
                        channel_info['keyword'] = api_dict["items"][0][part]['channel']["keywords"]
                    else:
                        channel_info['keyword'] = ""
                    
                    if "featuredChannelsUrls" in api_dict["items"][0][part]['channel']:
                        # 추천채널 목록
                        channel_info['recommend_channels'] = api_dict["items"][0][part]['channel']["featuredChannelsUrls"]
                    else:
                        channel_info['recommend_channels'] = ""
                    
        return channel_info

    # 채널 리스트의 모든 항목들 하나하나의 채널 정보를 모은 리스트를 생성하여 반환
    for channel_id in channel_list:
        if "/user" in channel_id:
            # user 채널이라면
            channel_info = [get_channel_info(api_key, channel_id.replace("/user", ""), is_user=True) for channel_id in channel_list]
            # 채널 기본 정보를 반환
            return channel_info
        else:
            channel_info = [get_channel_info(api_key, channel_id) for channel_id in channel_list]
            # 채널 기본 정보를 반환
            return channel_info
    
