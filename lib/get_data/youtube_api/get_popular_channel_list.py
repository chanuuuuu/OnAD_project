




def get_youtube_popluar_channel_list (api_key="AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak"):
    '''
    api_key : api 키 값

    return => 실시간 인기 동영상 각각의 채널리스트 200개

    '''
    import requests
    from bs4 import BeautifulSoup 
    import json

    api_key = "AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak"
    page_token = ""

    target_url = '''https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=KR&pageToken={}&maxResults=5&key={}'''.format(page_token, api_key) 
    html = requests.get (target_url)
    api_dict = html.json()

    popular_channel_list = []


    while True:
            target_url = '''https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=KR&pageToken={}&maxResults=5&key={}'''.format(page_token, api_key) 
            html = requests.get (target_url)
            api_dict = html.json()

            for result_count in range(len(api_dict["items"])):
                popular_channel_list.append(api_dict["items"][result_count]["snippet"]["channelId"])

            if "nextPageToken" in api_dict:
                page_token = api_dict["nextPageToken"]

            else: break

    return popular_channel_list

print(get_youtube_popluar_channel_list())

