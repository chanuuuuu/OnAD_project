

def get_dict_video_info(channel_id):
    '''
    한 채널의 비디오 목록을 반환하는 함수
    channel_id(str) : 채널 고유 ID
    return => [{일반 동영상 정보}, {라이브 동영상 정보}]
    '''
    from bs4 import BeautifulSoup
    import requests
    from get_video_id import get_video_id
    from get_video_info import get_video_info
    
    video_info = []
    video_ids = get_video_id(channel_id)
    for video_id in video_ids[0]:
        info = {}
        info["channel_id"] = channel_id
        tmp = get_video_info(video_id)
        info["video_id"] = tmp[0]
        info["title"] = tmp[1]
        info["description"] = tmp[2]
        info["upload_date"] = tmp[3]
        info["tag"] = tmp[4]
        info["category"] = tmp[5]
        info["thumbnail"] = tmp[6]
        info["view_cnt"] = tmp[7]
        info["like_cnt"] = tmp[8]
        info["hate_cnt"] = tmp[9]
        info["reple_cnt"] = tmp[11]
        info["Is_live_streaming_video"] = "False"

        video_info.append(info)
        

    for video_id in video_ids[1]:
        info = {}
        info["channel_id"] = channel_id
        tmp = get_video_info(video_id)
        info["video_id"] = tmp[0]
        info["title"] = tmp[1]
        info["description"] = tmp[2]
        info["upload_date"] = tmp[3]
        info["tag"] = tmp[4]
        info["category"] = tmp[5]
        info["thumbnail"] = tmp[6]
        info["view_cnt"] = tmp[7]
        info["like_cnt"] = tmp[8]
        info["hate_cnt"] = tmp[9]
        info["reple_cnt"] = tmp[11]
        info["Is_live_streaming_video"] = "True"

        video_info.append(info)

    return video_info
