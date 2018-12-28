


def get_video_info(video_id, api_key="AIzaSyDoxv6yPVLKSMJwXVF0-HKnkdl0DcgE8Ak"):
    '''
    video_id_list : 비디오 고유 ID(str) ,api_key : api 키값(str)
    
    return =>  동영상 정보 (list)
               [동영상 제목(str), 동영상 설명(str), 동영상 게시 일자(str,YYMMDD),
               동영상 태그(str), 동영상 카테고리와 분류 번호(str), 동영상 썸네일 주소(str),
               조회수(int), 좋아요 수(int), 싫어요 수(int), 즐겨찾기 수(int), 댓글 수(int)]
    '''
    
    import requests
    from bs4 import BeautifulSoup 

    categories = {'1': '영화/애니메이션', '2': '자동차', '10': '음악', '15': '동물', '17': '스포츠', '18': '단편 영화', '19': '여행/이벤트',
     '20': '게임', '21': '동영상 블로그', '22': '인물/블로그', '23': '코미디', '24': '엔터테인먼트', '25': '뉴스/정치', '26': '노하우/스타일',
     '27': '교육', '28': '과학기술', '30': '영화', '31': '애니메/애니메이션', '32': '액션/모험', '33': '고전', '34': '코미디', '35': '다큐멘터리',
     '36': '드라마', '37': '가족', '38': '외국', '39': '공포', '40': '공상과학/판타지', '41': '스릴러', '42': '단편', '43': '프로그램','44': '예고편'}
    
    video_id = video_id
    api_key = api_key
    param = ["snippet", "statistics"]
    video_info = []

    for part in param:    
            target_url = '''https://www.googleapis.com/youtube/v3/videos?part={}&id={}&key={}'''.format(part, video_id, api_key) 
            session = requests.Session ()
            headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }
            html = requests.get (target_url)
            soup = BeautifulSoup (html.text, "html.parser" )
            api_dict = eval(soup.text.replace("false","False").replace("true","True"))


            if part == "snippet":
                video_info.append(video_id)
                video_info.append(api_dict["items"][0]["snippet"]["title"])  # 동영상 제목
                video_info.append(api_dict["items"][0]["snippet"]["description"].replace("\n"," "))  # 동영상 설명
                video_info.append(api_dict["items"][0]["snippet"]['publishedAt'][2:10].replace("-","")) # 동영상 게시 일자
                if 'tags' in api_dict["items"][0]["snippet"]:
                    video_info.append(api_dict["items"][0]["snippet"]['tags'])  # 동영상 태그
                else:
                    video_info.append("None")
                video_info.append(categories[api_dict["items"][0]["snippet"]["categoryId"]] + "(" + api_dict["items"][0]["snippet"]["categoryId"] + ")")  # 동영상 카테고리
                video_info.append(api_dict["items"][0]["snippet"]["thumbnails"]["medium"]['url'])  # 동영상 썸네일 주소

            else:
                video_info.append(api_dict["items"][0]["statistics"]['viewCount'])  # 조회수
                video_info.append(api_dict["items"][0]["statistics"]["likeCount"])  # 좋아요 수
                video_info.append(api_dict["items"][0]["statistics"]["dislikeCount"])  # 싫어요 수
                video_info.append(api_dict["items"][0]["statistics"]["favoriteCount"])  # 즐겨찾기 (나중에 볼 영상) 수
                video_info.append(api_dict["items"][0]["statistics"]["commentCount"]) # 댓글 수
    
    return video_info           