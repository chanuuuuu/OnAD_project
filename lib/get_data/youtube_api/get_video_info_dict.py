from bs4 import BeautifulSoup
import requests
from get_video_id import get_video_id
from get_video_info import get_video_info


urls = ["https://www.youtube.com/channel/UCkGtJLZHSCBP6DeWCp9SuJQ"]


video_info = []
for url in urls:
    
    channel_name = url.split("/")[-1]
    video_ids = get_video_id(url)

    for video_id in video_ids[0]:
        print(video_id)
        info = {}
        info["channel_name"] = channel_name
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
        info["channel_name"] = channel_name
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
        


print(video_info)
