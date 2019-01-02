
def start(channel_list):
    '''
    채널정보를 딕셔너리들이 모인 리스트로 반환하는 함수
    *input
        - channel_list(list) : 채널고유ID 목록
    *output
        - [{채널정보}, {}, ...]
    '''
    from lib.get_data.youtube_api.get_channel_info import get_channel_info

    channel_info = []  # 최종 데이터들이 담기는 그릇
    for channel_id in channel_list:
        info_dict = {}  # 채널 하나하나의 데이터들이 담기는 그릇
        if "/user" in channel_id:
            # user 채널이라면
            info = get_channel_info(channel_id.replace("/user", ""), is_user=True)
        else:
            info = get_channel_info(channel_id)

        info_dict["channel_id"] = info[-1]
        info_dict["channel_name"] = info[0]
        info_dict["published_at"] = info[1]
        info_dict["description"] = info[2]
        info_dict["hits"] = info[4]

        if not info[4]:
            info_dict["subscribe_cnt"] = 'hidden'
        else:
            info_dict["subscribe_cnt"] = info[5]
        info_dict["total_video_cnt"] = info[6]
        
        if len(channel_info) == 7:
            info_dict["channel_keyword"] = info[7]
        elif len(channel_info) == 8:
            info_dict["channel_keyword"] = info[7]
            info_dict["channel_recommendation"] = info[8]
        else:
            info_dict["channel_keyword"] = "None"
            info_dict["channel_recommendation"] = "None"
    
    channel_info.append(info_dict)

    return channel_info
