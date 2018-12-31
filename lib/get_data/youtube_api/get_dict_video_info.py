from bs4 import BeautifulSoup
import requests
from get_video_id import get_video_id
from get_video_info import get_video_info
from youtube_crawl.get_live_chat_log import get_youtube_chatlog
from lib.get_data.youtube_crawl import get_live_chat_log


def get_dict_video_info(channel_id):
    '''
    channel_id(str) : 채널 고유 ID
    return => [{일반 동영상 정보}, {라이브 동영상 정보}]
    '''
    video_info = []
    video_ids = get_video_id(channel_id)
    for video_id in video_ids[0]:
        print(video_id)
        info = {}
        info["channel_name"] = channel_id
        tmp = get_video_info(video_id)
        info["video_id"] = tmp[0]
        info["video_title"] = tmp[1]
        info["video_description"] = tmp[2]
        info["video_published_at"] = tmp[3]
        info["video_tag"] = tmp[4]
        info["video_category"] = tmp[5]
        info["video_thumbnail"] = tmp[6]
        info["video_hits"] = tmp[7]
        info["video_like"] = tmp[8]
        info["video_dislike"] = tmp[9]
        info["video_save_playlist"] = tmp[10]
        info["video_comments_count"] = tmp[11]
        info["Is_live_streaming_video"] = "False"

        video_info.append(info)
        

    for video_id in video_ids[1]:
        print(video_id)
        info = {}
        info["channel_name"] = channel_id
        tmp = get_video_info(video_id)
        info["video_id"] = tmp[0]
        info["video_title"] = tmp[1]
        info["video_description"] = tmp[2]
        info["video_published_at"] = tmp[3]
        info["video_tag"] = tmp[4]
        info["video_category"] = tmp[5]
        info["video_thumbnail"] = tmp[6]
        info["video_hits"] = tmp[7]
        info["video_like"] = tmp[8]
        info["video_dislike"] = tmp[9]
        info["video_save_playlist"] = tmp[10]
        info["video_comments_count"] = tmp[11]
        info["Is_live_streaming_video"] = "True"

        video_info.append(info)

        get_live_chat_log(tmp[0], channel_id)

        
    return video_info


