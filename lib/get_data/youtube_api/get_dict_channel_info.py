
def get_dict_channel_info(channel_id):
    '''
    channel_id(str) : 채널 고유 ID
    return => [{채널정보}]
    '''
    from bs4 import BeautifulSoup
    import requests
    from get_video_id import get_video_id
    from get_channel_info import get_channel_info

    channel_info = []
    info_dict = {}
    info = get_channel_info(channel_id)
    print(info)

    info_dict["channel_id"] = channel_id
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
        
    return channel_info

print(get_dict_channel_info("UCIYWRFi7y6fBqosN5m5xxWA"))