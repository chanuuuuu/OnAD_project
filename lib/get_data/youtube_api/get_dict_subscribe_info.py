from bs4 import BeautifulSoup
import requests
from get_video_comments import get_video_comments_info
from get_subscriptions_info import get_subscriptions_info


def get_dict_subscribe_info(video_id):
    
        subscribe_info = []

        tmp = get_video_comments_info(video_id)

        for user in range(len(tmp)):
                info = {}

                info["video_id"] = video_id
                info["reply_id"] = tmp[user][0]

                subscriptions_info = get_subscriptions_info(tmp[user][0])

                if subscriptions_info == "hidden": 
                    continue
                else :
                    info["subscriptions_info"] = subscriptions_info

                subscribe_info.append(info)

        return subscribe_info

print(get_dict_subscribe_info("9zsGJDzxdHo"))