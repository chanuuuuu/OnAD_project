
def start(api_key, target_file):
    '''
    * input:
        api_key : api 키 값
        target_file : 파일이 있는 경로

    * output:
        return값 없음 => 'data/youtube_channels/' 경로에 youtube_channels.txt로 실시간 인기 동영상의 채널이 추가됨
    '''
    import requests
    from bs4 import BeautifulSoup 
    import json
    import os

    # api요청
    page_token = ""
    target_url = '''https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=KR&pageToken={}&maxResults=5&key={}'''.format(page_token, api_key) 
    html = requests.get(target_url)
    api_dict = html.json()

    popular_channel_list = []  # 채널 리스트가 담길 그릇
    while True:
        target_url = '''https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=KR&pageToken={}&maxResults=5&key={}'''.format(page_token, api_key) 
        html = requests.get(target_url)
        api_dict = html.json()

        for result_count in range(len(api_dict["items"])):
            popular_channel_list.append(api_dict["items"][result_count]["snippet"]["channelId"])

        if "nextPageToken" in api_dict:
            page_token = api_dict["nextPageToken"]

        else: break

    with open(target_file, 'r') as f:
        past_list = f.read().split("\n")[:-1]
    

    popular_channel_list = past_list + [channel_id for channel_id in popular_channel_list if channel_id not in past_list ]
    with open(target_file, 'w') as f: 
        for channel_id in popular_channel_list:
            f.write(channel_id + "\n")
    
