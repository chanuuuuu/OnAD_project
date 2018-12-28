import requests
from bs4 import BeautifulSoup 

api_key = "AIzaSyCzerFuw3AJr6o29InSBHBW9Rfy5xzIyTY"




def user_to_channelid(user_name, api_key="AIzaSyCzerFuw3AJr6o29InSBHBW9Rfy5xzIyTY"):
    import requests
    from bs4 import BeautifulSoup 

    api_key = "AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak"
    user_name = user_name


    target_url = '''https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={}&key={}'''.format(user_name, api_key) 

    session = requests.Session ()
    headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }

    html = requests.get (target_url)
    soup = BeautifulSoup (html.text, "html.parser" )

    api_dict = eval(soup.text.replace("false","False").replace("true","True"))
    
    channel_id = api_dict['items'][0]["id"]
    
    return channel_id


def get_video_id(channel_url, api_key="AIzaSyCzerFuw3AJr6o29InSBHBW9Rfy5xzIyTY"):
    '''
    channel_url : 유튜버 채널의 고유 채널 ID ("https://www.youtube.com/channel/~" 또는 "https://www.youtube.com/user/~" )
    api_key : 자신의 API키   
        
    return => [일반 동영상 고유 ID(list/str), 라이브 동영상 고유 ID(list/str)](list)
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
            print("일반 동영상 없음")

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
            print("라이브 동영상 없음")

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

        ################################################################################################################

        all_video_ids_count = len(video_ids)
        live_video_ids_count = len(live_video_ids)
        video_ids = list(set(video_ids) - set(live_video_ids))
        video_ids_count = len(video_ids)
        
        return [video_ids, live_video_ids]
    
    
    elif "user" in channel_url:
        api_key = api_key

        channel_id = user_to_channelid(channel_url.split("/")[-1], api_key)

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
            print("일단 동영상 없음")

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

                        
        ##############################################################################################################    
        page_token = ""

        target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&eventType=completed&maxResults=50&key={}'''.format(channel_id, api_key )

        session = requests.Session ()
        headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }

        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )

        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']

        exe_set = round(total_results / results_per_page +0.5)

        if exe_set == 0:
            print("라이브 동영상 없음")

        else:
              for total_set in range(exe_set):

                    target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&eventType=completed&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
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

        ################################################################################################################

        video_ids = list(set(video_ids) - set(live_video_ids))
        
        return [video_ids, live_video_ids]