# lib\analysis\__init__.py
import numpy as np
import pandas as pd

class Analyzer():
    anal_df = None  # 분석용 데이터 셋

    target_percentile = None  # 타겟 중위수

    anal_type = None  # 초 단위 편집점, 구간 단위 편집점, 머신러닝 편집점

    target_column = None  # 편집점 계산에 사용될 컬럼 명

    section_term = None  # 구간단위 편집점의 구간 단위

    ml_model = None  # 머신러닝 모델

    hot_point = None  # 편집점
    soar_point = None  # 채팅 급상승
    hot_point_per_time = None  # 시간기준당 편집점

    # 데이터 로드
    def load(self, anal_data):
        # data 폴더
        self.anal_df = pd.read_csv(anal_data, sep=",")

        self.anal_df['chat_time'] = pd.to_datetime(self.anal_df['chat_time'])
        self.anal_df = self.anal_df.set_index('chat_time')
        
        return self.anal_df
    
    # 채팅기반 편집점 알고리듬
    def hot_point_start(self, target_percentile=70, anal_type='spot',
        target_column='summation', section_term=10):
        """
        시청자 수 고려해서 편집점 잡는 것 다시 고려해보기
        지금은 방송을 한 그 당시의 시간을 토대로 분석하는데,
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
        self.target_percentile = target_percentile
        self.target_column = target_column
        
        # 스케일링 작업
        from sklearn.preprocessing import MinMaxScaler
        sc = MinMaxScaler()

        self.scailed_df = pd.DataFrame(sc.fit_transform(self.anal_df),
            index=self.anal_df.index, columns=self.anal_df.columns)
        self.scailed_df['summation'] = self.scailed_df['cnt_chat'] + self.scailed_df['cnt_ㅋ']

        # 채팅 빈도 기준점 설정
        threshold = np.percentile(self.scailed_df[target_column].unique(), target_percentile)
        
        if anal_type.lower() == "section":
            # 편집점을 기준으로 앞 뒤로 구간을 설정하여 제공
            point = self.scailed_df[self.scailed_df[target_column] > threshold]

            point_sections = []  # 편집점 구간이 담길 그릇 정의
            for i in point.index:
                # 앞뒤 구간 설정
                point_section_start = i - pd.Timedelta("%ss" % section_term)
                point_section_end = i + pd.Timedelta("%ss" % section_term)
                point_section = pd.date_range(point_section_start, point_section_end, freq='s')
                point_sections.extend(point_section)
            
            # 구간 편집점에 해당하는 데이터만 있는 데이터 프레임 반환
            self.anal_df['stream_time'] = self.anal_df.index
            self.anal_df['label'] = self.anal_df['stream_time'].apply(lambda x : 1 if x in point_sections else 0)
            
            self.hot_point = self.anal_df[self.anal_df['label'] == 1]
            # return point
            return self.hot_point
        
        elif anal_type.lower() == "spot":
            self.hot_point = self.scailed_df[self.scailed_df[target_column] > threshold]
            return self.hot_point

    # 시간 단위 당 채팅기반 편집점 알고리듬
    def hot_point_per_time_start(self, time_type="1Min",
        target_column="summation", target_percentile=85):
        """
        시간 기준에 따른 하이라이트 포인트를 반환
        """
        anal_df = self.anal_df.resample(time_type).sum()
        # 수정

        from sklearn.preprocessing import MinMaxScaler
        sc = MinMaxScaler()

        scailed_df = pd.DataFrame(sc.fit_transform(anal_df),
            index=anal_df.index, columns=anal_df.columns)
        scailed_df['summation'] = scailed_df['cnt_chat'] + scailed_df['cnt_ㅋ']

        threshold = np.percentile(scailed_df[target_column].unique(), target_percentile)

        self.hot_point_per_time = anal_df[scailed_df[target_column] > threshold]

        print(self.hot_point_per_time)

        return self.hot_point_per_time
        
    # 머신러닝 기반 편집점 알고리듬
    def ml_hot_point_start(self, model_file):
        # 단순 채팅 편집점이 아닌 머신러닝을 통한 모델의 편집점 평가
        
        # 머신러닝 모델 로드
        import pickle

        with open(model_file, 'rb') as fp:
            model = pickle.load(fp)

        # 스케일링 작업
        from sklearn.preprocessing import MinMaxScaler
        sc = MinMaxScaler()

        self.scailed_df = pd.DataFrame(sc.fit_transform(self.anal_df), index=self.anal_df.index, columns=self.anal_df.columns)
        self.scailed_df['summation'] = self.scailed_df['cnt_chat'] + self.scailed_df['cnt_ㅋ']

        # 예측
        print(model.predict(self.scailed_df))
    
    # 급상승 구간 알고리듬
    def soar_point_start(self):
        """
        이전 채팅보다 3배 이상 올라간 부분을 반환
        """
        count = 0
        index = []
        data = []
        for x in self.anal_df.index:
            if count * 3 < self.anal_df["cnt_chat"][x] and self.anal_df["cnt_chat"][x] > 10 :
                index.append(x)
                data.append(self.anal_df["cnt_chat"][x])
            count = self.anal_df["cnt_chat"][x]
        self.soar_point = pd.DataFrame(data=data, index=index, columns=["soar"])

        return self.soar_point

    # json 파일형식으로 encoding
    def jsonify(self, analyzed_data_folder):
        """
        분석된 편집점 데이터를 json 파일로 생성
        """
        # json 형태 설정
        anal_df = None  # 분석용 데이터 셋
        target_percentile = None  # 타겟 중위수
        anal_type = None  # 초 단위 편집점, 구간 단위 편집점, 머신러닝 편집점
        target_column = None  # 편집점 계산에 사용될 컬럼 명
        section_term = None  # 구간단위 편집점의 구간 단위
        ml_model = None  # 머신러닝 모델
        hot_point = None  # 편집점
        soar_point = None  # 채팅 급상승
        hot_point_per_time = None  # 시간기준당 편집점

        {
            "times": ["00:00:01", "00:01:01", "00:02:02", "00:03:02"] ,
            "cnt_chat": [123, 1234, 12345, 123456],
            "hot_point_per_min": {
                "time": ["03:02:02", "03:05:34", " 04:00:12"],
                "sentimental_score": [12, 23, 34, 45],
                "cnt_chat": [4444, 5555, 6666],
            },
            "soar_point": {
                "time": ["03:02:02", "03:05:34", " 04:00:12"],
                "cnt_chat": [4444, 5555, 6666],
            }
        }

        # json.dumps
        

    # 파일 저장
    def save_json(self): pass