

def start(video_id):
    """
    한 영상의 댓글 정보를 가져오는 함수
    * input:
        video_id(str) : 비디오 고유 id
    * output:
        [{댓글정보}, {댓글정보2}, ...]
    """
    from bs4 import BeautifulSoup
    import requests
    from lib.get_data.youtube_api.get_video_comments import get_video_comments_info

    comments_info = []
    tmp = get_video_comments_info(video_id)

    for user in tmp:
        info = {}
        info["reply_id"] = user[0]
        info["video_id"] = video_id
        info["upload_date"] = user[2]
        info["author_name"] = user[1]
        info["reple_contents"] = user[3]
        info["reply_like"] = user[4]

        comments_info.append(info)

    return comments_info
