def get_channel_info(channel_id, api_key="AIzaSyCzerFuw3AJr6o29InSBHBW9Rfy5xzIyTY"):
    '''
    channel_id : 채널 고유 ID
    api_key : API key 값
    
    retrun =>  channel_info(list)
               
               [채널 이름(str), 
               채널설립일자(str) - YYMMDD,
               채널설명(str), 
               채널 조회수(int), 
               구독자 수(int) - 공개했을 때만 return,
               동영상 수 (int) - 비공개 동영상이 포함됨,
               검색 키워드(list / str)  - 있을 경우에만 return,
               추천 채널의 현재 이름 (str) - 있을 경우에만 return,
               추천 채널 목록(list / 추천 채널 고유 ID(str) - 추천 채널 이름) - 있을 경우에만 return]
    
    
    '''
       
    import requests
    from bs4 import BeautifulSoup 

    api_key = api_key
    channel_id = channel_id
    page_token = ""
    channel_info = []

    param = ["snippet", "statistics", "brandingSettings"]
    channel_info = []
    
    for part in param:
        target_url ='''https://www.googleapis.com/youtube/v3/channels?part={}&id={}&key={}'''.format(part, channel_id, api_key) 
        session = requests.Session ()
        headers ={'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )
        api_dict = eval(soup.text.replace("false","False").replace("true","True"))
        
        if part == "snippet" :
            channel_info.append(api_dict["items"][0]['snippet']["title"]) # 채널제목
            channel_info.append(api_dict["items"][0]['snippet']['publishedAt'][:10].replace("-","")) #채널설립일자
            channel_info.append(api_dict["items"][0]['snippet']["description"].replace('\n', " ")) #채널설명
        
        elif part == "statistics":
        
            channel_info.append(api_dict["items"][0]["statistics"]['viewCount']) # 채널조회수
            channel_info.append(api_dict["items"][0]["statistics"]['subscriberCount']) #채널구독자수
            channel_info.append(api_dict["items"][0]["statistics"]['videoCount']) # 채널에 올린 동영상 수
        
        else:
            if "keywords" in api_dict["items"][0]["brandingSettings"]['channel'] :
                channel_info.append(api_dict["items"][0]["brandingSettings"]['channel']["keywords"].split(" ")) # 검색키워드
            
            if "featuredChannelsTitle" in api_dict["items"][0]["brandingSettings"]['channel']:
                channel_info.append(api_dict["items"][0]["brandingSettings"]['channel']["featuredChannelsTitle"]) # 추천채널 제목
            
            if "featuredChannelsUrls" in api_dict["items"][0]["brandingSettings"]['channel']:
                channel_info.append(api_dict["items"][0]["brandingSettings"]['channel']["featuredChannelsUrls"]) # 추천채널 목록
            
    for i in range(len(channel_info[-1])):
        target_url ='''https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'''.format(channel_info[-1][i], api_key) 
        session = requests.Session ()
        headers ={'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )
        api_dict = eval(soup.text.replace("false","False").replace("true","True"))
        channel_info[-1][i] = (channel_info[-1][i] + "," + api_dict["items"][0]['snippet']["title"]).split(",")
    
    
    return channel_info