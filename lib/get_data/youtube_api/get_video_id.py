
def get_video_id(api_key, channel_id):
    '''
    채널의 동영상들의 video_id를 반환하는 함수
    *input
        - channel_url(str) : 유튜버 채널의 고유 채널 ID 
        (도메인에서 직접 긁어올 시 "https://www.youtube.com/channel/***" 또는 "https://www.youtube.com/user/***"에서 * 부분)
        - api_key(str) : 자신의 API키   
        
    * output
        - result(list) : [일반 동영상 고유 ID(list), 라이브 동영상 고유 ID(list)](list)
    '''
    import requests
    from bs4 import BeautifulSoup
    import time

    if len(channel_id) == 24:  # 채널 id가 24자인 경우
        """
        video_ids 데이터 요청
        """
        # 파라미터 및 url 설정
        video_ids = []  # 데이터를 담을 그릇
        page_token = ""  # 다음 페이지 토큰을 담을 그릇
        target_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&pageToken={}&maxResults=50&key={}'.format(channel_id, page_token, api_key) 
        
        # 총 건수를 알아보기 위해 api 요청
        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser")

        # 요청을 dict로 변환
        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']

        # 총 요청 할 건수
        exe_set = round(total_results / results_per_page +0.5)

        if exe_set == 0:
            # 총 개수가 0인 경우는 일반 동영상이 없는 경우
            print("일반 동영상 없음")
        
        else:
            
            # 총 요청 건수 만큼 요청
            for _ in range(exe_set):
                # api 요청
                target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
                html = requests.get (target_url)
                soup = BeautifulSoup(html.text, "html.parser" )
                api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                # video_id 데이터를 추가
                for result_count in range(len(api_dict["items"])):
                    vd_id = api_dict["items"][result_count]["id"]["videoId"]
                    video_ids.append(vd_id)
                # 다음 페이지가 있으면 다음페이지를 긁도록
                if "nextPageToken" in api_dict:
                    page_token = api_dict["nextPageToken"]

        #################################################################################################################
        """
        live_video_ids 데이터 요청
        """
        
        target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&eventType=completed&type=video&maxResults=50&key={}'''.format(channel_id, api_key )

        # 총 건수를 알아보기 위한 api 요청
        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )
        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']

        # 총 요청할 건수
        exe_set = round(total_results / results_per_page +0.5)

        if exe_set == 0:
            print("라이브 동영상 없음")

        else:
            live_video_ids = []  # 데이터를 담을 그릇
            page_token = ""  # 다음 페이지 토큰을 담을 그릇
            # 총 요청 건수 만큼 요청
            for _ in range(exe_set):
                # api 요청
                target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
                html = requests.get (target_url)
                soup = BeautifulSoup (html.text, "html.parser" )
                api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                for result_count in range(len(api_dict["items"])):
                    # ilve 동영상 개수만큼 돌아 live_video_ids 리스트에 담는다
                    vd_id = api_dict["items"][result_count]["id"]["videoId"]
                    live_video_ids.append(vd_id)

                if "nextPageToken" in api_dict:
                    # 다음 페이지가 있다면 다음페이지를 요청하기 위해
                    page_token = api_dict["nextPageToken"]

        video_ids = list(set(video_ids) - set(live_video_ids))
        
        # video_ids : 라이브 영상이 아닌 영상들의 video_id 리스트
        # live_video_ids : 라이브 영상인 영상들의 video_id 리스트
        return [video_ids, live_video_ids]
    
    else:  # 채널 id가 24자가 아닌 경우
        """
        channel_ids 데이터 요청
        """
        from lib.get_data.youtube_api.user_to_channelid import user_to_channelid
        channel_id = user_to_channelid(channel_id, api_key)
        video_ids = []
        page_token = ""

        target_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&pageToken={}&maxResults=50&key={}'.format(channel_id, page_token, api_key) 

        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )
        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']
        exe_set = round(total_results / results_per_page +0.5)


        if exe_set == 0:
            print("일반 동영상 없음")

        else:
            for _ in range(exe_set):  # 총 요청건수 만큼
                time.sleep(0.5)
                # api 요청
                target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
                html = requests.get (target_url)
                soup = BeautifulSoup (html.text, "html.parser" )
                api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                # 데이터 적재
                for result_count in range(len(api_dict["items"])):
                    vd_id = api_dict["items"][result_count]["id"]["videoId"]
                    video_ids.append(vd_id)
                
                # 다음페이지 토큰 설정
                if "nextPageToken" in api_dict:
                    page_token = api_dict["nextPageToken"]

        ##############################################################################################################
        """
        live_channel_ids 요청
        """  
        live_video_ids = []
        page_token = ""
        target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&eventType=completed&maxResults=50&key={}'''.format(channel_id, api_key )

        html = requests.get (target_url)
        soup = BeautifulSoup (html.text, "html.parser" )
        api_dict = eval(soup.text.replace("false","False").replace("true","True"))

        total_results = api_dict['pageInfo']['totalResults']
        results_per_page = api_dict['pageInfo']['resultsPerPage']
        exe_set = round(total_results / results_per_page +0.5)

        if exe_set == 0:
            print("라이브 동영상 없음")

        else:
            for _ in range(exe_set):  # 총 요청 건수 만큼
                # api 요청
                target_url = '''https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=date&type=video&eventType=completed&pageToken={}&maxResults=50&key={}'''.format(channel_id, page_token, api_key)
                html = requests.get (target_url)
                soup = BeautifulSoup (html.text, "html.parser" )
                api_dict = eval(soup.text.replace("false","False").replace("true","True"))

                # 데이터 적재
                for result_count in range(len(api_dict["items"])):
                    vd_id = api_dict["items"][result_count]["id"]["videoId"]
                    live_video_ids.append(vd_id)
                # 다음 페이지 토큰 설정
                if "nextPageToken" in api_dict:
                    page_token = api_dict["nextPageToken"]
        ################################################################################################################
        video_ids = list(set(video_ids) - set(live_video_ids))
        
        return [video_ids, live_video_ids]

