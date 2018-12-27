# 사용 모듈 가져오기
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
    
class OnadAnalysis():
    def __init__(self):
        # 작업 디렉토리 설정
        self.working_dir = 'C:\\Users\\idec\\Desktop\\onad_project\\'
        self.data_dir = self.working_dir + "data\\"
        self.live_stream_dir = self.data_dir + "live_stream\\"
        self.chat_dir = self.data_dir + "logs\\"

    # 데이터 로드
    def load_chatting(self, target_id='yapyap30', target_date='2018-12-10'):
        """
        채팅로그 읽어오기
        - input : 
            *target_id => 채팅로그를 읽을 스트리머 이름, str
                ex) "yapyap30"
            *target_date => 채팅로그를 읽을 날짜, str
                ex) "2018-12-10"
        - output : 채팅로그 데이터프레임
            columns - 채팅로그
            index - 채팅시간
        """
        self.chat_file = "#%s\\%s_#%s.log" % (target_id, target_date, target_id)
        # "#yapyap30\\2018-12-10_#yapyap30.log"

        # 채팅로그 로딩
        with open(self.chat_dir + self.chat_file, 'r', encoding='utf-8') as fp:
            lines = fp.read().split("\n")
        
        # 채팅로그만 찾기
        ptn = re.compile(r'(\[\d{2}:\d{2}:\d{2}\]) <.+> .*')
        only_chat_lie = [i for i in lines if ptn.match(i)]
        
        # 시간 데이터만
        times = [line.split(" ")[0].replace("[", "").replace("]", "") for line in only_chat_lie]

        # 채팅데이터만
        chattings = [line.split('> ')[1] for line in only_chat_lie]
        df = pd.DataFrame(index=times, data=chattings, columns=['chatting'])
        df['hour'] = [i[:2] for i in df.index]

        return df

    def load_viewer_count(self, target_id='yapyap30'):
        """
        분단위 시청자수
        - input:
            target_id : 타겟 스트리머 아이디  

        - output:
            target_id로 지정한 스트리머의 viewer_count 데이터프레임
            columns : [name, id, viewer]
            index : streaming_time
        """
        # 분당 스트리밍 중인 스트리머, 시청자수 파일 불러오기
        ptn = re.compile(r'live_stream_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}.txt')

        # 위 패턴에 맞는(live_stream txt 데이터만)
        viewer_count_files = [file for file in os.listdir(self.live_stream_dir) if ptn.match(file)]

        # {0000 : [스트리머 리스트]} 와 같이 dict로 생성
        viewer_count_dict = {}
        for viewer_count_file in viewer_count_files:
            # 파일 하나하나 읽어 {시간: [스트리머 리스트] } 의 형태로 만듦
            with open(self.live_stream_dir + viewer_count_file, 'r', encoding='utf-8') as fp:
                viewer_count_datasets = fp.read().split('\n')

            time = viewer_count_file[12:-4]
            # 딕셔너리 형태로
            viewer_count_dict[time] = viewer_count_datasets
        
        # 생성된 dict 를 바탕으로 DataFrame 생성
        view_df_list = []
        for i, v in viewer_count_dict.items():
            df1 = pd.DataFrame([v1.split()[:3] for v1 in v])
            df1['streaming_time'] = i
            view_df_list.append(df1)

        # 리스트 안에 들어가있는 여러 데이터프레임들을 하나의 데이터 프레임으로
        view_df = pd.concat(view_df_list)

        # 데이터 프레임 컬럼명
        col = ['name', 'id', 'viewer', 'streaming_time']
        view_df.columns = col
        
        # streaming_time 을 인덱스로 설정
        view_df = view_df[view_df['id'] == target_id].set_index('streaming_time')

        # 날짜, 시간, 분 컬럼 추가
        view_df['date'] = list(pd.Series(view_df.index).apply(lambda x : x[:-6]))
        view_df['hour'] = list(pd.Series(view_df.index).apply(lambda x : x[-5:-3]))
        view_df['minute'] = list(pd.Series(view_df.index).apply(lambda x : x[-2:]))

        return view_df
    
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

    def highlight_point_analysis(self, chatting_df, viewer_count_df, target_percentile=70):
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
        def viewer_mean_per_hour(date='2018-12-06', target_hour='00'):
            asdf = viewer_count_df[viewer_count_df['date'] == date]
            return asdf[asdf['hour'] == target_hour].viewer.astype(np.int32).values.mean().astype(np.int32)

        hours = ["0"+str(i) if len(str(i))<=1 else str(i) for i in list(range(0,24))]

        # 방송을 한 날짜들
        exists_days = viewer_count_df['date'].unique()

        viewer_means = {}
        for i in exists_days:
            viewer_means[i] = [viewer_mean_per_hour(date=i,
                                                    target_hour=target_hour)
                                                    for target_hour in hours]
        
        # 인덱스 값뭉치 생성 "2018-12-10-00" 과 같이
        date_hour_index = [ exists_days[5]+ "-" +str(hour) for hour in hours]

        # 00시의 평균 시청자수 데이터프레임
        target_viewer_df = pd.DataFrame(viewer_means[exists_days[5]],index=date_hour_index, columns=['mean_viewer'])

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


# 테스트
if __name__ == "__main__":
    analkit = OnadAnalysis()

    # 데이터 불러오기
    chat_df = analkit.load_chatting(target_id='yapyap30', target_date="2018-12-09")
    viewer_df = analkit.load_viewer_count(target_id='yapyap30')
    
    # 시간대별 시청자 추이
    # analkit.changes_viewer_analysis(viewer_df, "2018-12-07",)

    # 채팅 빈출 구간
    highlight_spots = analkit.highlight_point_analysis(chat_df, viewer_df, target_percentile=70)
    print(highlight_spots)

