def get_channel_info(channel_id, is_user=None, api_key="AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak"):
    '''
    각 채널의 정보를 반환하는 함수
    * input
    channel_id : 채널 고유 ID
    is_user : 채널명이 user/유튜버이름 인지의 flag 값
        user인 경우 "user" 또는 True 입력
    api_key : API key 값
    
    * output
        channel_info(list)
            [채널 이름(str), 
            채널설립일자(str) - YY-MM-DD,
            채널설명(str), 
            채널 조회수(int), 
            구독자 수(int) - 공개했을 때만 return,
            동영상 수 (int) - 비공개 동영상이 포함됨,
            검색 키워드(list / str)  - 있을 경우에만 return,
            추천 채널 목록(list / 추천 채널 고유 ID(str) - 추천 채널 이름(str)) - 있을 경우에만 return]
    '''
    import requests
    from bs4 import BeautifulSoup

    if is_user: # user 라면(셀럽의 경우 user/youtuber-id 형식의 채널명을 가짐)
        # 채널 고유 id를 가져오기 위한 api 호출
        target_url = '''https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={}&key={}'''.format(channel_id, api_key) 
        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )
        api_dict = eval(soup.text.replace("false","False").replace("true","True"))
        channel_id = api_dict['items'][0]["id"]  # 기존의 channel_id와 같은 형식의 channel_id

    param = ["snippet", "statistics", "brandingSettings"]
    channel_info = []
    
    for part in param:
        target_url ='''https://www.googleapis.com/youtube/v3/channels?part={}&id={}&key={}'''.format(part, channel_id, api_key) 
        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )
        api_dict = eval(soup.text.replace("false","False").replace("true","True"))
        
        if part == "snippet" :
            channel_info.append(api_dict["items"][0][part]["title"])  # 채널제목
            channel_info.append(api_dict["items"][0][part]['publishedAt'][:10])  # 채널설립일자
            channel_info.append(api_dict["items"][0][part]["description"])  # 채널설명
            channel_info.append(api_dict["items"][0][part]["thumbnails"]['default']['url'])  # 썸네일
        
        elif part == "statistics":
            channel_info.append(api_dict["items"][0][part]['viewCount'])  # 채널조회수
            channel_info.append(api_dict["items"][0][part]['subscriberCount'])  # 채널구독자수
            channel_info.append(api_dict["items"][0][part]['videoCount'])  # 채널에 올린 동영상 수
        
        else:
            if "keywords" in api_dict["items"][0][part]['channel'] :
                channel_info.append(api_dict["items"][0][part]['channel']["keywords"].split(" "))  # 검색키워드
            
            if "featuredChannelsUrls" in api_dict["items"][0][part]['channel']:
                channel_info.append(api_dict["items"][0][part]['channel']["featuredChannelsUrls"])  # 추천채널 목록
            
                for i in range(len(channel_info[-1])):
                    target_url ='''https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'''.format(channel_info[-1][i], api_key) 
                    html = requests.get (target_url)
                    soup = BeautifulSoup (html.text, "html.parser" )
                    api_dict = eval(soup.text.replace("false","False").replace("true","True"))
                    channel_info[-1][i] = (channel_info[-1][i] + "," + api_dict["items"][0]['snippet']["title"]).split(",")
        
        channel_info.append(channel_id)  # 채널고유ID
    
    return channel_info