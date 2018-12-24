import requests
from bs4 import BeautifulSoup 

api_key = "AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak"



def convert_user_to_channelid(user_name, api_key):
       
    import requests
    from bs4 import BeautifulSoup 

    api_key = api_key
    user_name = user_name


    target_url = '''https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={}&maxResults=50&key={}'''.format(user_name, api_key) 

    session = requests.Session ()
    headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }

    html = requests.get (target_url)
    soup = BeautifulSoup (html.text, "html.parser" )

    api_dict = eval(soup.text.replace("false","False").replace("true","True"))
    
    channel_id = api_dict['items'][0]['snippet']['channelId']
    
    return channel_id


def get_video_id_for_channelId(channel_url, api_key):
    '''
    channel_id : 유튜버 채널의 고유 채널 ID ("https://www.youtube.com/channel/~" 또는 "https://www.youtube.com/user/~" )
    api_key : 자신의 API키   
        
    return값 :  일반 동영상 고유 ID(list) 
                라이브 동영상 고유 ID(list)
                [총 동영상 수(int), 일반 동영상 수(int), 라이브 동영상 수(int)]

    '''
    import requests
    from bs4 import BeautifulSoup 
    
    
    if "channel" in channel_url:  
        
        api_key = api_key
        channel_id = channel_url.split("/")[-1]
        page_token = ""

        target_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&pageToken={}&maxResults=50&key={}'.format(channel_id, page_token, api_key) 

        session = requests.Session ()
        headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }

        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )

        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']
        exe_set = round(total_results / results_per_page +0.5)

        video_ids = []
        live_video_ids = []

        if exe_set == 0:
            return print("표시할 내용이 없음")

        else:
            for total_set in range(exe_set):

                    target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
                    session = requests.Session ()
                    headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }
                    html = requests.get (target_url)
                    soup = BeautifulSoup (html.text, "html.parser" )
                    api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                    for result_count in range(len(api_dict["items"])):
                                vd_id = api_dict["items"][result_count]["id"]["videoId"]
                                video_ids.append(vd_id)

                    if "nextPageToken" in api_dict:
                        page_token = api_dict["nextPageToken"]
                        print(api_dict["nextPageToken"])

        ##############################################################################################################    
        page_token = ""

        target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&eventType=completed&type=video&maxResults=50&key={}'''.format(channel_id, api_key )

        session = requests.Session ()
        headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }

        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )

        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']

        exe_set = round(total_results / results_per_page +0.5)

        if exe_set == 0:
            return print("표시할 내용이 없음")

        else:
              for total_set in range(exe_set):

                    target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
                    session = requests.Session ()
                    headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }
                    html = requests.get (target_url)
                    soup = BeautifulSoup (html.text, "html.parser" )
                    api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                    for result_count in range(len(api_dict["items"])):
                                vd_id = api_dict["items"][result_count]["id"]["videoId"]
                                live_video_ids.append(vd_id)

                    if "nextPageToken" in api_dict:
                        page_token = api_dict["nextPageToken"]
                        print(api_dict["nextPageToken"])

        ################################################################################################################

        all_video_ids_count = len(video_ids)
        live_video_ids_count = len(live_video_ids)
        video_ids = list(set(video_ids) - set(live_video_ids))
        video_ids_count = len(video_ids)
        
        return video_ids, live_video_ids, [all_video_ids_count, video_ids_count, live_video_ids_count]
    
    ##############################################################################################################
    elif "user" in channel_url:
        api_key = api_key
        channel_id = convert_user_to_channelid(channel_url.split("/")[-1], api_key)
        page_token = ""

        target_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&forUsername={}&order=date&type=video&pageToken={}&maxResults=50&key={}'.format(channel_id, page_token, api_key) 

        session = requests.Session ()
        headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }

        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )

        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']
        exe_set = round(total_results / results_per_page +0.5)

        video_ids = []
        live_video_ids = []

        if exe_set == 0:
            return print("표시할 내용이 없음")

        else:
            for total_set in range(exe_set):

                    target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&forUsername={}&order=date&type=video&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
                    session = requests.Session ()
                    headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }
                    html = requests.get (target_url)
                    soup = BeautifulSoup (html.text, "html.parser" )
                    api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                    for result_count in range(len(api_dict["items"])):
                                vd_id = api_dict["items"][result_count]["id"]["videoId"]
                                video_ids.append(vd_id)

                    if "nextPageToken" in api_dict:
                        page_token = api_dict["nextPageToken"]
                        print(api_dict["nextPageToken"])

           
        page_token = ""

        target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&forUsername={}&order=date&eventType=completed&type=video&maxResults=50&key={}'''.format(channel_id, api_key )

        session = requests.Session ()
        headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }

        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )

        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']

        exe_set = round(total_results / results_per_page +0.5)

        if exe_set == 0:
            return print("표시할 내용이 없음")

        else:
              for total_set in range(exe_set):

                    target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&forUsername={}&order=date&type=video&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
                    session = requests.Session ()
                    headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }
                    html = requests.get (target_url)
                    soup = BeautifulSoup (html.text, "html.parser" )
                    api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                    for result_count in range(len(api_dict["items"])):
                                vd_id = api_dict["items"][result_count]["id"]["videoId"]
                                live_video_ids.append(vd_id)

                    if "nextPageToken" in api_dict:
                        page_token = api_dict["nextPageToken"]
                        print(api_dict["nextPageToken"])

        

        all_video_ids_count = len(video_ids)
        live_video_ids_count = len(live_video_ids)
        video_ids = list(set(video_ids) - set(live_video_ids))
        video_ids_count = len(video_ids)
        
        return video_ids, live_video_ids, [all_video_ids_count, video_ids_count, live_video_ids_count]






