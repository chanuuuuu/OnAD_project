
def start(channel_list, is_detail=None):
    '''
    채널정보를 딕셔너리들이 모인 리스트로 반환하는 함수
    *input
        - channel_list(list) : 채널고유ID 목록
    *output
        - [{채널정보}, {}, ...]
    '''
    from lib.get_data.youtube_api.get_channel_info import get_channel_info

    channel_info = []  # 최종 데이터들이 담기는 그릇
    channel_detail_info = []  # channel_detail 최종 데이터들이 담기는 그릇

    for channel_id in channel_list:
        youtube_channel_dict = {}  # 채널 하나하나의 데이터들이 담기는 그릇
        youtube_channel_detail_dict = {}  # 채널 하나하나의 세부데이터들이 담기는 그릇
        if "/user" in channel_id:
            # user 채널이라면
            info = get_channel_info(channel_id.replace("/user", ""), is_user=True)
        else:
            info = get_channel_info(channel_id)

        youtube_channel_dict["channel_name"] = info[0]
        youtube_channel_dict["published_at"] = info[1]
        youtube_channel_dict["description"] = info[2]
        youtube_channel_dict["thumbnail"] = info[3]
        youtube_channel_dict["channel_id"] = info[4]
        youtube_channel_dict["keyword"] = info[-2]
        youtube_channel_dict["recommend_channels"] = info[-1]

        youtube_channel_detail_dict["hit_cnt"] = info[5]
        youtube_channel_detail_dict["subscribe_cnt"] = info[6]
        youtube_channel_detail_dict["total_video_cnt"] = info[7]
        

        channel_info.append(youtube_channel_dict)
        channel_detail_info.append(youtube_channel_detail_dict)

    if is_detail: # 채널 detail 정보를 반환
        return channel_detail_info
    else:  # 채널 기본 정보를 반환
        return channel_info
