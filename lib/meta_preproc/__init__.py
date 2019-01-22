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
    youtube_channel = None  # streamer's youtube channel
    youtube_channel_details = None  # streamer's youtube channel's detail data
    stream_avr_viewer_cnts = None  # average viewer count of stream
    stream_viewer_highest = None  # this stream's highest viewer count
    stream_contents = None  # this stream's unique contents list
    stream_contents_thumbnail = None  # stream's contents thumbnail list
    total_contents_unique = None  # total day unique contents
    total_contents_thumbnails = None  # total contents's thumbnail images
    total_contents_rate = None  # total day contents rate

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
        # allocate data to member variables
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
        from lib.contact_db.member import TwitchGame

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
            played_game_id = [ detail['game_id'] for detail in details]

            # get game names use game id
            unique_game_id = list(set(played_game_id))

            # query to get game names
            game_names = {game_id: select_information(self.dao,
                    TwitchGame, game_id=game_id).__dict__['game_name'] for game_id in unique_game_id}

            # allocate data to member variable
            self.stream_contents = list(game_names.values())

            played_game = list(map(lambda x: game_names[x], played_game_id))

            data = {
                'time': times,
                'title': title,
                'viewer': viewer,
                'game_id': played_game,
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
        self.youtube_channel = row['youtube_channel']

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
        
    def get_youtube_channel(self):
        """
        twitch_channel 테이블의 youtube_channel 정보를 통해 youtube channel detail 정보를 얻어오는 함수
        """
        # Import DB query functions 
        from lib.contact_db.youtube import select_information

        # Import DB tables
        from lib.contact_db.member import YoutubeChannelDetail

        # get channel details use contracted streamer's youtube channel id
        rows = select_information(self.dao, YoutubeChannelDetail,
             channel_id=self.youtube_channel, target_date=self.broad_date)

        rows = list(map(lambda x : x.__dict__, rows))

        # preprocess data
        hit_cnts = [row.get('hit_cnt') for row in rows]
        times = [row.get('date') for row in rows]
        subscribe_cnts = [row.get('subscribe_cnt') for row in rows]
        total_video_cnts = [row.get('total_video_cnt') for row in rows]

        # allocate data to member variable
        self.youtube_channel_details = {
                'hit_cnt': hit_cnts,
                'time': times,
                'subscribe_cnt': subscribe_cnts,
                'total_video_cnt': total_video_cnts,
            }

        return self.youtube_channel_details

    def get_stream_other_metrics(self):
        """
        오늘 방송에 대한 만들어 내야 하는 지표를 만들어 주는 함수
        1. 오늘 평균시청자수
        2. 오늘 시청자 수 최고점
        3. 단골 시청자 수( 주 o회 채팅 출석)  - 분석모듈에서.
        4. 오늘 진행 한 컨텐츠(트위치 카테고리)  self.stream_contents
        5. 오늘 방송 컨텐츠들 썸네일
        """
        from lib.contact_db.twitch import select_information
        from lib.contact_db.member import TwitchGame

        import numpy as np
        
        details = [detail for detail in self.stream_details]

        # 1. make today's viewer average count
        self.stream_avr_viewer_cnts = [np.around(np.mean(detail.get("viewer"))) for detail in details]

        # 2. make today's viewer highest point
        self.stream_viewer_highest = [np.max(detail.get("viewer")) for detail in details]

        # 3 -> function of analysis module

        # 4 -> already exist. self.stream_contents

        # 5. make today's contents thumbnails
        self.stream_contents_thumbnail = [select_information(self.dao,
            TwitchGame, game_name=game_name).__dict__['thumbnail']
            for game_name in self.stream_contents]

    def get_week_other_metrics(self):
        """
        1주간 방송에 대한 지표 만들어 주는 함수
        1. 1주 간 자주하는 컨텐츠(트위치 카테고리) - 1일 단위
        2. 1주 간 팔로워 증가  - 1일 단위
        3. 1주 간 유튜브 구독자 증가  - 1일 단위
        4. 1주 간 유튜브 영상 증가  - 1일 단위
        5. 1주 간 평균 시청자수  - 1일 단위
        6. 1주 간의 모든 컨텐츠 썸네일
        """
        from lib.contact_db.twitch import select_information
        from lib.contact_db.member import TwitchGame

        import numpy as np

        # 1. get data for a week

        # function should be appended later

    def get_all_broad_other_metrics(self, streamer_name):
        """
        지금껏의 모든 방송에 대한 지표를 만들어 주는 함수
        1. 컨텐츠 비율 (트위치 카테고리별 비율)
        2. 인기 영상 클립
        3. 지금껏의 모든 방송 컨텐츠
        4. 지금껏의 모든 방송 컨텐츠 썸네일
        """
        from lib.contact_db.twitch import select_information

        from lib.contact_db.member import TwitchStream
        from lib.contact_db.member import TwitchStreamDetail
        from lib.contact_db.member import TwitchGame

        import numpy as np

        self.streamer_name = streamer_name

        # get all stream detail
        streams = select_information(self.dao,
            TwitchStream, streamer_name=streamer_name)

        stream_ids = list(map(lambda x : x.__dict__['stream_id'], streams))

        stream_details = [select_information(self.dao,
            TwitchStreamDetail, stream_id=stream_id)
            for stream_id in stream_ids]

        # stream detail data only
        detail_only = [detail.__dict__ for day in stream_details for detail in day]

        # contents column variables only
        contents_only = [ detail['game_id'] for detail in detail_only]

        # get game names use game id
        unique_game_id = list(set(contents_only))

        # query to get game names
        game_names = {game_id: select_information(self.dao,
                TwitchGame, game_id=game_id).__dict__['game_name'] for game_id in unique_game_id if select_information(self.dao,
                TwitchGame, game_id=game_id)}

        # 3. total unique contents
        self.total_contents_unique = sorted(list(game_names.values()))

        # total played contents
        total_played_contents = list(map(lambda x: game_names.get(x), contents_only))
        total_played_contents = [contents for contents in total_played_contents if contents is not None]

        # played contents count
        cnt_contents = [total_played_contents.count(i) for i in self.total_contents_unique]

        # 1. played contents rate
        self.total_contents_rate = [ np.round(i/len(cnt_contents)) for i in cnt_contents]

        # 4. total contents's thumbnails 
        self.total_contents_thumbnails = [select_information(self.dao,
            TwitchGame, game_name=game_name).__dict__['thumbnail']
            for game_name in self.total_contents_unique]

    def jsonify(self):
        """
        모든 메타 데이터를 json으로 변환하여 반환
        """
        import json

        # 한 방송의 정보
        oneday_dict = {
            "meta":{
                "streamer_name": self.streamer_name,
                "twitch_id": self.twitch_id,
                "broad_date": self.broad_date,
                "homepage": self.homepage,
                "logo": self.logo,
                "youtube_channel": self.youtube_channel,
            },
            "streams": self.streams,
            "viewer_average": self.stream_avr_viewer_cnts,
            "viewer_highest": self.stream_viewer_highest,
            "contents": self.stream_contents,
            "contents_thumbnails": self.stream_contents_thumbnail,
            "stream_details": self.stream_details,
            "twitch_channel_details": self.channel_details,
            "youtube_channel_details": self.youtube_channel_details,
        }
        print(oneday_dict)

        # 지금껏 모든 방송의 정보
        total_broad_dict = {
            "streamer_name": self.streamer_name,
            "broaded_contents": self.total_contents_unique,
            "contents_thumbnails": self.total_contents_thumbnails,
            "broaded_contents_rate": self.total_contents_rate
        }
        print(total_broad_dict)

        # datetime.datetime 객체는 json으로 만들지 못하므로 strftime() 사용해야 할 듯


    def send_json(self):
        # json 파일을 보낸다
        pass