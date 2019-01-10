# 사용 모듈 가져오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
    

# 시청자 수 데이터 분석
def changes_viewer_analysis(self, viewer_count_df, date='2018-12-06', hour=None,):
    """
    input : 
        *chatting_df :
            load_chatting 의 반환값
        *viewer_count_df :
            load_viewer_count 의 반환값
        *date :
            "2018-12-06" 형태의 타겟 날짜
        *hour :
            "00" ~ "23" 형태의 나겟 시간
            없다면 날짜에 대한 그래프만 반환
    output :
        hour가 없다면 그 날짜에 대한 시청자수 추이
        hour가 있다면 그 날짜의 그 시간에 대한 시청자수 추이
        *plt.show()
    """
    if not hour:
        # 날짜별
        viewer_count_df[viewer_count_df['date'] == date]['viewer'].astype(np.int32).plot(kind='bar', figsize=(15,3))
        plt.show()
    else:
        only_targetdata_df = viewer_count_df[viewer_count_df['date'] == date]
        try:
            only_hour_df = only_targetdata_df[only_targetdata_df['hour'] == hour]
            ax = only_hour_df['viewer'].astype(np.int32).plot(kind='bar', figsize=(15,3))
            plt.setp(ax.get_xticklabels(), visible=False)
            plt.show()
        except TypeError:
            print("시청자가 없는 시간입니다.")

# 채팅 편집점 알고리듬
def start(anal_df, target_percentile=60, anal_type='spot'):
    """
    시청자 수 고려해서 편집점 잡는 것 다시 고려해보기
    지금은 방송을 한 그 당시의 시간을 토대로 분석하는데,
    이후 방송시작시간을 00:00:00 으로 설정해보아야 함.
    input : 
        chatting_df :
            load_chatting 의 반환값
        viewer_count_df :
            load_viewer_count 의 반환값
        target_percentile:
            초당 채팅빈도값 들 중 기준으로 잡는 중위수의 퍼센테이지
    output:
        채팅 빈도가 갑작스럽게 높아진 구간들
        [(방송시간, 채팅빈도), ...]
    """
    import numpy as np
    # 채팅 빈도 기준점 설정
    threshold = np.percentile(anal_df['cnt_chat'].unique(), target_percentile)

    if anal_type.lower() == "section":
        # 편집점을 기준으로 앞 뒤로 구간을 설정하여 제공
        pass
    
    elif anal_type.lower() == "spot":
        return anal_df[anal_df['cnt_chat'] > threshold]
    
