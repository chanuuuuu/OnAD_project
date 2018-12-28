from bs4 import BeautifulSoup
import requests
from get_video_id import get_video_id
from get_channel_info import get_channel_info


'''
[채널 이름(str), 
채널설립일자(str) - YYMMDD,
채널설명(str), 
채널 조회수(int), 
구독자 수(int) - 공개했을 때만 return,
동영상 수 (int) - 비공개 동영상이 포함됨,
검색 키워드(list / str)  - 있을 경우에만 return,
추천 채널의 현재 이름 (str) - 있을 경우에만 return,
추천 채널 목록(list / 추천 채널 고유 ID(str) - 추천 채널 이름(str)) - 있을 경우에만 return]
'''

channel_ids = ["UCIYWRFi7y6fBqosN5m5xxWA"]
channel_info = []

for ids in channel_ids:
    info_dict = {}
    info = get_channel_info("UCIYWRFi7y6fBqosN5m5xxWA")
    info_dict["channel_id"] = ids
    info_dict["channel_title"] = info[0]
    info_dict["channel_published_at"] = info[1]
    info_dict["channel_description"] = info[2]
    info_dict["channel_hits"] = info[3]
    if not info[4]:
        info_dict["subscribe_count"] = 'hidden'
    else:
         info_dict["subscribe_count"] = info[4]
    info_dict["total_video_count"] = info[5]
    
    if len(channel_info) == 7:
        info_dict["channel_keyword"] = info[6]
    elif len(channel_info) == 8:
        info_dict["channel_keyword"] = info[6]
        info_dict["channel_recommendaion"] = info[7]
    else:
        info_dict["channel_keyword"] = "None"
        info_dict["channel_recommendaion"] = "None"

    channel_info.append(info_dict)
    
print(channel_info)

