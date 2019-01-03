

def start(api_key, video_id):
    """
    비디오 하나에, 댓글을 쓴 사람 중 구독정보를 열어 둔 사람의 구독정보를 반환하는 함수
    시간 좀 걸림
    * input
        - video_id(int) : 유튜브 영상의 고유ID
    * output
        dict
        [{video_id:"", replier_id:"", subscription:""}, ...]
    """
    from bs4 import BeautifulSoup
    import requests
    from lib.get_data.youtube_api.get_video_comments import get_video_comments_info
    from lib.get_data.youtube_api.get_subscriptions_info import get_subscriptions_info

    tmp = get_video_comments_info(api_key, video_id)

    for user in tmp:
        subscriptions = get_subscriptions_info(api_key, user[0])

        if subscriptions is not "hidden":
            result = [{
                "video_id": video_id,
                "replier_id": user[0],
                "subscription": subscription
            } for subscription in subscriptions]

    return result
