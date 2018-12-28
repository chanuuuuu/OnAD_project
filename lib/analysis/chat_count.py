# 사용 모듈 가져오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
    

# 데이터 분석
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

def start(chatting_df, viewer_count_df, target_percentile=70):
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
    def viewer_mean_per_hour(target_hour='00'):
        return viewer_count_df[
            viewer_count_df['hour'] == target_hour
            ]['viewer'].astype(
                np.int32).values.mean().astype(
                    np.int32)

    # 시간 정보 00 ~ 24 까지
    hours = ["0"+str(i) if len(str(i))<=1 else str(i) for i in list(range(0,24))]

    # 방송을 한 날짜들
    target_date = viewer_count_df['date'].unique()[0]

    viewer_means = {}
    viewer_means[target_date] = [viewer_mean_per_hour(target_hour=target_hour)
        for target_hour in hours]
    
    # 인덱스 값뭉치 생성 "2018-12-10-00" 과 같이
    date_hour_index = [target_date+ "-" + str(hour) for hour in hours]

    # 00시의 평균 시청자수 데이터프레임
    target_viewer_df = pd.DataFrame(viewer_means[target_date],
        index=date_hour_index, columns=['mean_viewer'])

    # 시간별 평균 시청자 수과 그에 대한 총 시청자수 데이터를 병합
    target_viewer_df['hour'] = [i[-2:] for i in target_viewer_df.index]
    merged_df = chatting_df.merge(target_viewer_df, on='hour', right_index=True)

    # 시간별(초당) 평균 시청자수평균과 채팅수가 들어있는 데이터프레임
    chat_frequency_df = merged_df.pivot_table(index=merged_df.index, values='chatting', aggfunc=len)
    
    # 초당 최다 빈도 순 채팅빈도 리스트
    chat_frequency_per_sec = sorted(chat_frequency_df['chatting'].unique(), reverse=True)
    
    # 70% 분위수 - 일단은 70 분위수보다 높은 순간만
    many_chat_times = [ i for i in chat_frequency_per_sec
                            if i > np.percentile(chat_frequency_per_sec, target_percentile)]

    # 채팅 시간, 채팅 빈도수의 튜플로 데이터 정리
    highlight_times = []
    for highlight in many_chat_times:
        many_chat_time_df = chat_frequency_df[chat_frequency_df['chatting'] == highlight]
        for time in many_chat_time_df.index:
            highlight_times.append(time)

    highlight_times1 = []
    for highlight in many_chat_times:
        many_chat_time_df = chat_frequency_df[chat_frequency_df['chatting'] == highlight]
        for v in many_chat_time_df.values:
            highlight_times1.append(v[0])  # (채팅 수, hour) 중 0번째

    # 하이라이트 포인트 생성 (방송한 시간, )
    highlight_point = list(zip(highlight_times , highlight_times1))
    
    return sorted(highlight_point)
