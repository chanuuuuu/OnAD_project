

def start(api_key, video_ids):
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
    for video_id in video_ids:
        tmp = get_video_comments_info(api_key, video_id)
        for user in tmp:
            info = {}
            info["reply_id"] = user[0]
            info["video_id"] = video_id
            info["upload_date"] = user[2]
            info["author_name"] = user[1]
            info["reple_contents"] = user[3]
            info["like_cnt"] = user[4]

            # 최종 데이터 그릇에 추가
            comments_info.extend(info)

    return comments_info
