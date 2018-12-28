from bs4 import BeautifulSoup
import requests
from get_video_comments import get_video_comments_info
from get_subscriptions_info import get_subscriptions_info




def get_dict_comment_info(video_id):

        comments_info = []
        tmp = get_video_comments_info(video_id)

        for user in range(len(tmp)):
                info = {}
                info["video_id"] = video_id
                info["reply_id"] = tmp[user][0]
                info["reply_nickname"] = tmp[user][1]
                info["reply_published_at"] = tmp[user][2]
                info["reply_content"] = tmp[user][3]
                info["reply_like"] = tmp[user][4]

                subscriptions_info = get_subscriptions_info(tmp[0])
                info["subscriptions_info"] = subscriptions_info

                comments_info.append(info)

        return comments_info

print(get_dict_comment_info("vrNBP-PHvFM"))