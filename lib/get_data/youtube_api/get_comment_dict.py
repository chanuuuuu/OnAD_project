from bs4 import BeautifulSoup
import requests
from get_video_comments import get_video_comments_info
from get_subscriptions_info import get_subscriptions_info


video_ids = ["DXqJJPhiRaI"]
comments_info = []
for video_id in video_ids:
    tmp = get_video_comments_info(video_id)
    
    for i in range(len(tmp)):
        info = {}
        info["video_id"] = video_id
        info["reply_id"] = tmp[i][0]
        info["reply_nickname"] = tmp[i][1]
        info["reply_published_at"] = tmp[i][2]
        info["reply_content"] = tmp[i][3]
        info["reply_like"] = tmp[i][4]

        subscriptions_info = get_subscriptions_info(tmp[0])
        info["subscriptions_info"] = subscriptions_info

        comments_info.append(info)

print(comments_info)