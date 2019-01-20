# 분석 데이터 전처리 클래스
class Preprocessor():
    # 멤버 변수
    streamer = None  # 스트리머 이름, str
    broad_date = None  # 방송 날짜, str
    chat_df = None  # 채팅로그 데이터, pd.DataFrame
    pivot_df = None  # 채팅 빈도 피봇 데이터, pd.DataFrame
    
    # 멤버함수

    # /data 폴더로부터 채팅로그 데이터 로드
    def load_from_folder(self, target_id='yapyap30', target_date='2018-12-10',
        twitch_chat_dir="./data/twitch_live_chat/"):
        """
        채팅로그 읽어 데이터 프레임으로 반환
        - input : 
            *target_id => 채팅로그를 읽을 스트리머 이름, str
                ex) "yapyap30"
            *target_date => 채팅로그를 읽을 날짜, str
                ex) "2018-12-10"
        - output : 채팅로그 데이터프레임
            columns - 채팅로그
            index - 채팅시간
        """
        import re
        import pandas as pd

        # 객체의 속성으로 스트리머 이름, 방송날짜 부여
        self.streamer = target_id
        self.broad_date = target_date
        
        # 채팅 로그 파일 설정
        chat_file = "#%s\\%s_#%s.log" % (target_id, target_date, target_id)
        # "#yapyap30\\2018-12-10_#yapyap30.log"

        # 채팅로그 로딩
        with open(twitch_chat_dir + chat_file, 'r', encoding='utf-8') as fp:
            lines = fp.read().split("\n")

        # 채팅로그만 찾기
        ptn = re.compile(r'(\[.+\]) <.+> .*')
        only_chat_line = [i for i in lines if ptn.match(i)]
        
        # 시간 데이터만
        times = [ re.search(r'\d\d:\d\d:\d\d', line).group(0).replace("[", "").replace("]", "")
            for line in only_chat_line ]

        # 채팅데이터만
        chattings = [line.split('> ')[1] for line in only_chat_line]

        # 시청자 아이디만
        chatterer = [ re.search(r'<.+>', line).group(0) for line in only_chat_line]

        # 시간을 인덱스로, 채팅내용, 시간을 컬럼으로 하는 데이터 프레임 생성
        df = pd.DataFrame(index=times,
            data=chatterer,
            columns=['chatterer'])

        df['chat_time'] = df.index
        df['chat_contents'] = chattings
        df.index =  df['chat_time'].apply(lambda x : target_date + " " + x).apply(lambda x : pd.to_datetime(x))

        # 멤버변수 chat_df 를 이 데이터 프레임으로 설정
        self.chat_df = df

        return df

    # DB로부터 채팅로그 데이터 로드
    def load_from_db(self, db_url, streamer_id, target_date):
        """
        db와 접촉하여 트위치 채팅 데이터를 가져오는 쿼리를 수행한 후 데이터 프레임으로 반환합니다.
        * input
            db_url : 데이터 베이스 연결 url, str
            streamer_id : 채팅로그를 가져 올 스트리머의 id, str ex)zilioner
            target_date : 채팅로그를 가져 올 날짜 ex)2018-01-07, str
        * output
            pandas.DataFrame 객체
        """
        import pandas as pd

        # 객체의 속성으로 스트리머 이름과 방송날짜 부여
        self.streamer = streamer_id
        self.broad_date = target_date

        query = """select * from twitch_chat where streamer_name = "%s" and broad_date ="%s"
        """ % (streamer_id, target_date)
        
        chat_df = pd.read_sql_query(query, db_url)
        # 필요없는 컬럼 삭제
        del chat_df['chat_id']
        del chat_df['streamer_name']
        del chat_df['broad_date']

        # 시간을 인덱스로
        chat_df.index = chat_df['chat_time'].apply(lambda x : target_date + " " + x).apply(lambda x : pd.to_datetime(x))
        self.chat_df = chat_df

        return chat_df

    # 1월 이후의 데이터의 경우 시작시간을 기준으로 00:00:00 부터 시작하는 컬럼 생성
    def set_start_time(self, dao, db_url, chat_df, streamer_id, target_date):
        """
        * input
            dao : DB session
            db_url : 데이터 베이스 연결 url, str
            streamer_id : 스트리머의 트위치id, str ex)zilioner
            target_date : 방송 날짜
        * output
            방송 시작 시간을 반환
        """
        import pandas as pd
        from lib.contact_db.member import TwitchChannel
        
        # 스트리머 아이디 -> 스트리머 이름 가져오기
        streamer_name = dao.query(TwitchChannel.streamer_name).filter_by(
            streamer_twitch_id=streamer_id)

        # 방송 시작 시간 가져오기
        query = """select broad_date from twitch_stream where streamer_name = '%s'
        """ % streamer_name[0]  # ("얍얍", )의 형태로 나옴

        start_df = pd.read_sql_query(query, db_url)
        broad = pd.to_datetime(start_df['broad_date'])
        del start_df

        # 트위치 시간대는 UTC 기준이므로 한국시간으로 +9시간 하여 변경
        broad = broad.apply(lambda x : x + pd.Timedelta("9hours"))
        for i in broad:
            if target_date == str(i.date()):
                stream_start_time = str(i.time())
        
        # 시작 시간데이터 삽입 작업
        start_time = pd.to_datetime(target_date + " " + stream_start_time)
        chat_df['stream_time'] = chat_df['chat_time'].apply(lambda x : target_date + " " + x)
        chat_df['stream_time'] = chat_df['stream_time'].apply(lambda x : pd.to_datetime(x) - start_time)

        self.chat_df = chat_df
        return chat_df

    # 감성 분석 컬럼 생성 작업
    def create_sentimental_score(self, sentimental_dict_path,
        user_dict_path, chat_df):
        from lib.morphs_analyzer.komoran3py import KomoranPy
        import pickle

        ko = KomoranPy()

        # 감성사전 로딩
        with open(sentimental_dict_path, 'rb') as f:
            shinjo_dict = pickle.load(f)

        # 감성 사전 추가
        shinjo_dict['우와'] = 1
        shinjo_dict['와'] = 1
        shinjo_dict['개꿀'] = 1
        shinjo_dict['개꿀잼'] = 1.2
        shinjo_dict['기모띠'] = 1
        shinjo_dict['꿀잼'] = 1.2
        shinjo_dict['재밌네'] = 1
        shinjo_dict['대박'] = 1
        shinjo_dict['유하'] = 1.5
        shinjo_dict['재밌다'] = 1
        shinjo_dict['ㄵ'] = -1
        shinjo_dict['노잼'] = -1
        shinjo_dict['노답'] = -1
        shinjo_dict['개노답'] = -1
        shinjo_dict['ㅅㅂ'] = -1.5
        shinjo_dict['ㅄ'] = -1
        shinjo_dict['ㅂㅅ'] = -1
        shinjo_dict[';'] = 0
        a = 'ㅋ'  # ㅋ을 감성점수 1점으로 할당
        for _ in range(20):
            shinjo_dict[a] = 0.5
            a += 'ㅋ'

        # 사용자 사전 추가
        ko.set_user_dictionary(user_dict_path)
        
        # 형태소 분석한 결과 컬럼 생성
        print("감성 분석 - 형태소 분석 시작")
        chat_df['chat_morphs'] = chat_df['chat_contents'].apply(lambda x : [ i[0] for i in ko.pos(x)])
        print("감성 분석 - 형태소 분석 완료")
    

        # 감성 분석 점수 함수 정의
        def check(x) : 
            sentiment_list = []
            score = 0
            for i in range(len(x)): 
                if x[i] in shinjo_dict.keys(): 
                    sentiment_list.append(shinjo_dict[x[i]])
                    if i+1 == len(x) :
                        score = sum(sentiment_list)
                        return score

                elif x[i] not in shinjo_dict.keys(): 
                    sentiment_list.append(0)
                    if i+1 == len(x):
                        score = sum(sentiment_list)
                        return score

        # 감성 분석 점수화 (문장당 감성점수 부여 작업)
        chat_df['sentiment_score'] = chat_df['chat_morphs'].apply(lambda x : check(x))

        del chat_df['chat_morphs']  # 필요없는 컬럼 삭제

        self.chat_df = chat_df

        # ko 인스턴스 제거 (메모리 확보)
        del ko

        return chat_df

    # 빈도를 기준으로 피봇테이블 작업
    def pivotting(self, chat_df, index_type='kr'):
        """
        채팅 로그 데이터프레임을 채팅 빈도를 기준으로 한 피봇테이블로 변환
        input
            chat_df : 채팅로그 데이터프레임
            index_type : 피봇테이블의 인덱스를 절대시간으로 할 것인지(default), 스트리밍 시작시간을 기준으로 00:00:00 과 같이 할 것인지의 플래그 값
        """
        # 채팅빈도를 기준으로 피봇팅
        if index_type == "kr":
            pivot_df = self.chat_df.pivot_table(index=self.chat_df.index, aggfunc=len, values='chat_contents')
        elif index_type == "streamstart":
            pivot_df = self.chat_df.pivot_table(index=self.chat_df['stream_time'], aggfunc=len, values='chat_contents')

        pivot_df.columns = ['cnt_chat']  # 컬럼 이름 할당

        # 멤버함수로 설정
        self.pivot_df = pivot_df
        return pivot_df

    # 초당 특정 단어 빈도를 세어 피봇 테이블 작업
    def append_word_count_column(self, chat_df, pivot_df, word_list=None):
        """
        채팅로그 데이터 프레임에서
        특정단어리스트 안의 요소들 하나하나에 대해 초당 단어 빈도를 세어
        피봇 테이블에 추가
        input
            - chat_df : 채팅로그 데이터 프레임
            - pivot_df : 초별 채팅로그 빈도 수 피봇테이블
            - word_list : 초당 단어 빈도 컬럼으로 추가할 단어 리스트
        output
            - 초당 단어빈도가 추가된 피봇테이블
        """
        # 감성 점수 추가
        pivot_df['sentiment_score'] = chat_df.pivot_table(index=chat_df.index,
            values='sentiment_score', aggfunc=sum)['sentiment_score']

        # 초당 특정 단어수 체크하여 변수로 할당
        # 단어리스트를 인자로 넣은 경우 해당 리스트 단어들의 빈도컬럼을 생성
        # 단어리스트를 넣지 않은 경우 기본 단어리스트 사용
        if not word_list:
            word_list = ["ㅋ", "ㄵ", "ㄴㅈ", "오", "와", "유하", "ㅅㅂ"]

        for word in word_list:
            # 컬럼 이름 설정
            col = "cnt_" + word
            
            # 특정 단어 수 컬럼 생성
            chat_df[col] = chat_df.chat_contents.apply(lambda x : x.count(word))

            # 해당 초의 특정 단어 빈도 수 컬럼을 pivot_df에 추가
            pivot_df[col] = chat_df.pivot_table(index = chat_df.index,
                aggfunc=sum, values=col)[col]

            # 멤버 변수 피봇테이블에 할당
            self.pivot_df = pivot_df
        return pivot_df
        
    # 피클파일로 피봇된 분석 데이터프레임 저장
    def save_to_pickle(self, save_file_name):
        """
        pivot_df 를 로컬 저장소에 pickle 파일로 저장하는 함수
        input
            - 데이터프레임 피클파일이 저장될 경로
        """
        self.pivot_df.to_pickle(save_file_name)
        return 1
    
    # csv 파일로 피봇된 분석 데이터프레임 저장
    def save_to_csv(self, save_path):
        """
        pivot_df 를 로컬 저장소에 csv 파일로 저장하는 함수
        input
            - 데이터프레임 csv file이 저장될 경로
        """
        self.pivot_df.to_csv(save_path)
        return 1
        
    # 메모리 초기화
    def init(self,):
        """
        이전 작업으로부터 남아있는 메모리 제거
        """
        if self.streamer:
            del self.streamer
        
        if self.broad_date:
            del self.broad_date
        
        if self.chat_df is not None:
            del self.chat_df
        
        if self.pivot_df is not None:
            del self.pivot_df


