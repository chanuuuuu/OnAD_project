# lib\meta_preproc\__init__.py
# 메타데이터 전처리 클래스

class MetaPreprocessor():
    # 멤버 변수
    dao = None  # db session

    broad_date = None  # 2018-12-19
    streamer_name = None  # 침착맨
    streamer_id = None  # 5615122
    homepage = None  # homepage url
    twitch_id = None  # zilioner
    logo = None  # logo url

    streams = None  # twitch_stream data
    stream_details = list()  # twitch_stream_detail data
    channel_details = list()  # twitch_channel_detail data
    # 멤버 함수
    def __init__(self, dao):
        self.dao = dao

    def get_stream(self, broad_date, streamer_name):
        """
        twitch_stream db에서 데이터를 받아온다
        * input
            broad_date : 방송 날짜
            streamer_name : 스트리머 이름
        * output
            [{'broad_date': 'yyyy-mm-dd',
            'streamer_name': 'streamer1',
            'stream_id': '12345678789',
            'stream_start': '2019-01-08T01:57:26Z'}, {}, {}, ... ], list
        """
        # allocate member variables
        self.broad_date = broad_date
        self.streamer_name = streamer_name

        # import DB query functions 
        from lib.contact_db.twitch import select_groupby_broad_date
        
        # import DB tables
        from lib.contact_db.member import TwitchChannel
        from lib.contact_db.member import TwitchStream

        # get stream data
        streams = select_groupby_broad_date(self.dao, TwitchStream,
            broad_date=broad_date, streamer_name=streamer_name)
        streams = list(map(lambda x : x.__dict__, streams))
        
        # create new dict for return
        self.streams = [{
            'broad_date': broad_date,
            'streamer_name': stream['streamer_name'],
            'stream_id': stream['stream_id'],
            'stream_start': stream['broad_date'],
            } for stream in streams]
        
        # extinct unuseable variable
        del streams

        # return value
        return self.streams

    def get_stream_detail(self):
        """
        get_stream 함수를 통해 얻은 stream_id 를 이용하여 해당 스트리밍의 세부 데이터를 가져오는 함수
        * output
            [{'time': [datetime.datetime(2019, 1, 8, 11, 0, 14),
                    datetime.datetime(2019, 1, 8, 11, 10, 12)],
            'title': ['오전 투기장 고급반 강좌 -> 블리자드 선물 보기 (후원음성 X)',
                    '오전 투기장 고급반 강좌 -> 블리자드 선물 보기 (후원음성 X)'],
            'viewer': [102, 957],
            'game_id': ['138585', '138585']}, ... ], list
        """
        # Import DB query functions 
        from lib.contact_db.twitch import select_information

        # Import DB tables
        from lib.contact_db.member import TwitchStreamDetail

        # Get stream details using stream_id
        for stream in self.streams:
            # for today's streams
            stream_id = stream['stream_id']
            rows = select_information(self.dao,
                TwitchStreamDetail, stream_id=stream_id)
        
            # Preprocess selected data
            details = [stream_detail.__dict__ for stream_detail in rows]

            times = [ detail['time'] for detail in details]
            title = [ detail['title'] for detail in details]
            viewer = [ detail['viewer'] for detail in details]
            game_id = [ detail['game_id'] for detail in details]

            data = {
                'time': times,
                'title': title,
                'viewer': viewer,
                'game_id': game_id,
            }

            # append preprocessed data to member variable
            self.stream_details.append(data)

        return self.stream_details

    def get_channel(self):
        """
        streamer_name을 이용하여 twitch_channel 정보를 가져오는 함수
        * output
            {homepage: homepage,
            twitch_id: twitch_id,
            logo: logo,
            }, dict
        """
        # Import DB query functions 
        from lib.contact_db.twitch import select_information

        # Import DB tables
        from lib.contact_db.member import TwitchChannel

        # Get channel informations 
        row = select_information(self.dao,
            TwitchChannel, streamer_name=self.streamer_name)[0].__dict__  # only one row exists

        self.homepage = row['homepage']
        self.twitch_id = row['streamer_twitch_id']
        self.logo = row['logo']
        self.streamer_id = row['streamer_id']

        return row

    def get_channel_detail(self):
        """
        streamer_id 를 통해 twitch_channel_detail 데이터 가져오는 함수
        """
        # Import DB query functions 
        from lib.contact_db.twitch import select_channel_detail

        # Import DB tables
        from lib.contact_db.member import TwitchChannelDetail

        # Get channel informations 
        rows = select_channel_detail(self.dao, TwitchChannelDetail,
            self.broad_date, streamer_id=self.streamer_id)
        
        details = list(map(lambda x : x.__dict__, rows))

        result = [{
            'time': detail['date'],
            'viewer': detail['viewer'],
            'follower': detail['follower'],
        } for detail in details]

        self.channel_details = result
        
    
    def jsonify(self):
        # json 파일로 제작
        pass

    def send_json(self):
        # json 파일을 보낸다
        pass