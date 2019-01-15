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
def start(anal_df, target_percentile=70, anal_type='spot',
    target_column='summation', section_term=20):
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
        anal_type:
            반환 받을 편집점의 형태
            spot - 초 단위의 편집점
            section - 초 단위의 편집점 +- 20초의 구간 
        target_column :
            편집점의 기준으로 삼을 컬럼을 정의
            cnt_chat , cnt_ㅋ, cnt_?, cnt_유하, summation, summation+? 중 하나
        section_term :
            편집 구간의 앞 뒤 범위를 설정
            1s ~ 30s 사이의 값
    output:
        채팅 빈도가 갑작스럽게 높아진 구간들
        DataFrame
    """
    import numpy as np
    import pandas as pd
    # 채팅 빈도 기준점 설정
    
    # 스케일링 작업
    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler()
    scailed_df = pd.DataFrame(sc.fit_transform(anal_df), index=anal_df.index, columns=anal_df.columns)
    scailed_df['summation'] = scailed_df['cnt_chat'] + scailed_df['cnt_ㅋ']
    threshold = np.percentile(scailed_df['summation'].unique(), target_percentile)
    
    if anal_type.lower() == "section":
        # 편집점을 기준으로 앞 뒤로 구간을 설정하여 제공
        point = scailed_df[scailed_df['summation'] > threshold]

        point_sections = []  # 편집점 구간이 담길 그릇 정의
        for i in point.index:
            # 앞뒤 구간 설정
            point_section_start = i - pd.Timedelta("%ss" % section_term)
            point_section_end = i + pd.Timedelta("%ss" % section_term)
            point_section = pd.date_range(point_section_start, point_section_end)
            point_sections.extend(point_section)
        
        # 구간 편집점에 해당하는 데이터만 있는 데이터 프레임 반환
        anal_df['stream_time'] = anal_df.index
        anal_df['label'] = anal_df['stream_time'].apply(lambda x : 1 if x in point_sections else 0)
        # return point
        return anal_df[anal_df['label'] == 1]
    
    elif anal_type.lower() == "spot":
        return scailed_df[scailed_df['summation'] > threshold]

    elif anal_type.lower() == "ml":
        # 단순 채팅 편집점이 아닌
        # 머신러닝을 통한 모델의 편집점 평가
        pass
    
