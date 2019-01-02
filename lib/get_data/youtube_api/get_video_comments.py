
def get_video_comments_info(video_id, api_key="AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak"):
    '''
    비디오 당 댓글의 정보
    video_id = 동영상 고유 ID(str), api_key = api 키 값(str)    
    return => 댓글 정보 comments_info (list)
             [작성자의 채널 고유 ID(str), 작성자 이름(str), 작성 날짜(str, YYMMDD), 댓글내용(str), 댓글의 좋아요 수(int)]
    
    '''
    import requests
    from bs4 import BeautifulSoup 
    import json

    page_token = ""

    target_url = '''https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={}&order=time&pageToken={}&maxResults=100&key={}'''.format(video_id, page_token, api_key) 
    html = requests.get (target_url)
    api_dict = html.json()

    total_results = api_dict['pageInfo']['totalResults']
    results_per_page = api_dict['pageInfo']['resultsPerPage']
    exe_set = round(total_results / results_per_page +0.5)

    comments_info = []
    if exe_set == 0:
        print("댓글 없음")
    
    else:
        while True:
            target_url = '''https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={}&order=time&pageToken={}&maxResults=100&key={}'''.format(video_id, page_token, api_key) 
            html = requests.get (target_url)
            api_dict = html.json()

            for result_count in range(len(api_dict["items"])):
                tmp = []
                # 댓글 작성자의 채널 고유 ID
                tmp.append(api_dict['items'][result_count]["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]['value'])
                # 댓글 작성자 이름
                tmp.append(api_dict['items'][result_count]["snippet"]["topLevelComment"]["snippet"]['authorDisplayName']) 
                # 댓글 작성 날짜
                tmp.append(api_dict['items'][result_count]["snippet"]["topLevelComment"]["snippet"]["publishedAt"][2:10]\
                    .replace("-",""))
                # 댓글내용
                tmp.append(api_dict['items'][result_count]["snippet"]["topLevelComment"]["snippet"]["textOriginal"].\
                    replace("<br />", ' ').replace(" &quot;", '"').replace("&quot; ", '"').replace("\n"," ")) 
                # 댓글의 좋아요 수
                tmp.append(api_dict['items'][result_count]["snippet"]["topLevelComment"]["snippet"]["likeCount"]) 

                comments_info.append(tmp)

            if "nextPageToken" in api_dict:
                page_token = api_dict["nextPageToken"]
                
            else: break
                    
                    
    return comments_info
