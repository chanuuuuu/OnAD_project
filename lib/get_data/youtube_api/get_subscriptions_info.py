

def get_subscriptions_info (user_id, api_key= "AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak") :
    '''
    댓글 쓴 사람의 어떤 채널을 구독했는지 정보
    user_ids(str) : 사용자 고유 ID
    api_key(str) : api 키값

    return => subscriptions_info(dict) {video_id: str, user_id : str, channel_id : str}
    '''
    
    import requests
    from bs4 import BeautifulSoup 
    import json

    # api 요청
    api_key = api_key
    page_token = ""
    target_url = '''https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId={}&order=alphabetical&pageToken={}&maxResults=50&key={}'''.format(user_id, page_token, api_key)  
    html = requests.get (target_url)
    soup = BeautifulSoup (html.text, "html.parser" )
    api_dict = eval(soup.text.replace("false","False").replace("true","True"))
    
    if not "items" in api_dict:
        # 구독 정보를 열어두지 않은 경우
        return "hidden"
    else:
        # 구독 정보를 열어 둔 경우
        subscriptions_info = []

        for result_count in range(len(api_dict["items"])):
            subscriptions_info.append(api_dict["items"][result_count]['snippet']['resourceId']['channelId'])

        while True:
            if "nextPageToken" in api_dict:
                page_token = api_dict["nextPageToken"]

                target_url = '''https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId={}&order=alphabetical&pageToken={}&maxResults=50&key={}'''.format(user_id, page_token, api_key)  
                html = requests.get (target_url)
                soup = BeautifulSoup (html.text, "html.parser" )
                api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                for result_count in range(len(api_dict["items"])):
                    subscriptions_info.append(api_dict["items"][result_count]['snippet']['resourceId']['channelId'])
            else: 
                break

    return subscriptions_info

