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
    popular_clips = None  # popular clips for a month
    follower_period = None  # follower of certain period

    streams = None  # twitch_stream data
    stream_details = list()  # twitch_stream_detail data
    channel_details = list()  # twitch_channel_detail data

    one_day_json = None  # 결과
    total_broad_json = None  # 결과

    # 멤버 함수
    def __init__(self, dao):
        self.dao = dao

    # 스트리밍 데이터
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
            'stream_start': '2019-01-08 01:57:26'}, {}, {}, ... ] # 시간바꿀 필요 있음(세계기준시 +9H)
            list
        """
        # allocate data to member variables
        self.broad_date = broad_date
        self.streamer_name = streamer_name

        # import DB query functions 
        from lib.contact_db.twitch import select_groupby_broad_date
        
        # import DB tables
        from lib.contact_db.member import TwitchChannel
        from lib.contact_db.member import TwitchStream

        # import time things
        import datetime
        from dateutil.parser import parse

        # get stream data
        streams = select_groupby_broad_date(self.dao, TwitchStream,
            broad_date=broad_date, streamer_name=streamer_name)
        streams = list(map(lambda x : x.__dict__, streams))

        # adjust time data which is UTC timezone, but we need seoul timeznoe, +9Hours
        seoul_time_zone = datetime.timedelta(seconds=3600 * 9)
        
        # create new dict for return
        self.streams = [{
            'broad_date': broad_date,
            'streamer_name': stream['streamer_name'],
            'stream_id': stream['stream_id'],
            'stream_start':(parse(stream['broad_date'].replace("T"," ").replace("Z", "")) \
                            + seoul_time_zone).strftime("%Y-%m-%d %H:%M:%S"),
            } for stream in streams]
        
        # extinct unuseable variable
        del streams

        # return value
        return self.streams

    # 스트리밍 세부사항
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

        self.stream_details = list()
        # Get stream details using stream_id
        for stream in self.streams:
            # for today's streams
            stream_id = stream['stream_id']
            rows = select_information(self.dao,
                TwitchStreamDetail, stream_id=stream_id)
            if rows:
                # Preprocess selected data
                details = [stream_detail.__dict__
                    for stream_detail in rows
                    if stream_detail.__dict__['time'] is not None]

                times = [ detail['time'].strftime("%Y-%m-%d %H:%M:%S") for detail in details]
                title = [ detail['title'] for detail in details]
                viewer = [ detail['viewer'] for detail in details]
                played_game_id = [ detail['game_id'] for detail in details]

                # get game names use game id
                unique_game_id = list(set(played_game_id))

                # query to get game names
                game_names = {game_id: select_information(self.dao,
                        TwitchGame, game_id=game_id).__dict__['game_name']
                        for game_id in unique_game_id
                        if select_information(self.dao, TwitchGame, game_id=game_id)}

                # allocate data to member variable
                self.stream_contents = list(game_names.values())

                played_game = list(map(lambda x: game_names.get(x), played_game_id))

                data = {
                    'time': times,
                    'title': title,
                    'viewer': viewer,
                    'game_id': played_game,
                }
                # append preprocessed data to member variable
                self.stream_details.append(data)

        return self.stream_details

    # 트위치 채널 데이터
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

    # 트위치 채널 세부사항 데이터
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
            'time': detail['date'].strftime("%Y-%m-%d %H:%M:%S"),
            'viewer': detail['viewer'],
            'follower': detail['follower'],
        } for detail in details]

        self.channel_details = result

    # 유튜브 채널 데이터      
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
        times = [row.get('date').strftime("%Y-%m-%d %H:%M:%S") for row in rows]
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

    # 하루의 스트림데이터로 만들어내는 데이터
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
        
        # 1. make today's viewer average count
        self.stream_avr_viewer_cnts = [int(np.around(np.mean(detail.get("viewer")))) for detail in self.stream_details]

        # 2. make today's viewer highest point
        self.stream_viewer_highest = [int(np.max(detail.get("viewer"))) for detail in self.stream_details]

        # 3 -> function of analysis module

        # 4 -> already exist. self.stream_contents

        # 5. make today's contents thumbnails
        self.stream_contents_thumbnail = [select_information(self.dao,
            TwitchGame, game_name=game_name).__dict__['thumbnail']
            for game_name in self.stream_contents]

    # 한달 데이터로 만들어내는 데이터
    def get_month_other_metrics(self, streamer_name):
        """
        한달 간 방송에 대한 지표 만들어 주는 함수
        2. 팔로워 증가  
        3. 평균 시청자수  - 1일 단위  **

        # 고려해 볼 지표
        4. 유튜브 구독자 증가  - 1일 단위
        5. 유튜브 영상 수 증가  - 1일 단위
        6. 모든 컨텐츠 썸네일
        """
        from lib.contact_db.twitch import select_days_information
        from lib.contact_db.twitch import select_days_information_by_stream_id
        from lib.contact_db.twitch import select_information

        from lib.contact_db.member import TwitchChannelDetail
        from lib.contact_db.member import TwitchChannel
        from lib.contact_db.member import TwitchStream
        from lib.contact_db.member import TwitchStreamDetail

        import numpy as np
        import pandas as pd
        import datetime
        from dateutil import parser

        # 멤버 변수로 할당
        self.streamer_name = streamer_name

        now = datetime.datetime.now()
        a_month_ago = (now - datetime.timedelta(days=15))
        
        # 기간동안의 팔로워 수
        streamer_id = select_information(self.dao, TwitchChannel.streamer_id, streamer_name=streamer_name)
        if streamer_id:
            streamer_id = list(map(lambda x : x[0], streamer_id))

            details = select_days_information(self.dao, TwitchChannelDetail,
                streamer_id=streamer_id, a_month_ago=a_month_ago.strftime("%Y-%m-%d"))
            
            details = list(map(lambda x: x.__dict__, details))

            follower = list(map(lambda x: x.get('follower'), details))
            date = list(map(lambda x: x.get('date').strftime("%Y-%m-%d %H:%M:%S"), details))
            viewer = list(map(lambda x: x.get('viewer'), details))

            self.follower_period = {
                "date": date,
                "follower": follower ,
                "channel_viewer": viewer}
            
        # stream_id 구하기
        streams = select_information(self.dao, TwitchStream, streamer_name=streamer_name)
        if streams:
            streams = list(map(lambda x: x.__dict__, streams))

            streams = list(map(lambda x: {
                "stream_id": x.get('stream_id'),
                "broad_date": x.get('broad_date').split("T")[0]
            }, streams))
            
            # stream_id
            stream_ids = [ stream.get("stream_id")
                for stream in streams
                if parser.parse(stream.get('broad_date')) >= a_month_ago ]

        # 평균 시청자수
        month_stream_details = [i.__dict__ for stream_id in stream_ids
            for i in select_days_information_by_stream_id(self.dao,
            TwitchStreamDetail, a_month_ago=a_month_ago, stream_id=stream_id)]

        times = [x.get('time').strftime("%Y-%m-%d") for x in month_stream_details]
        viewers = [x.get('viewer') for x in month_stream_details]
        
        df = pd.DataFrame(viewers, index=times, columns=['viewers'])
        df = df.pivot_table(index=df.index)

        times = list(df.index)
        viewers = [int(i[0]) for i in df.values]

        self.month_viewer_cnt = {
            "date": times,
            "viewer_avr": viewers,
            }

    # 모든 방송을 토대로 만들어내는 데이터
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
        from lib.contact_db.member import TwitchClip

        import numpy as np
        import datetime

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
        self.total_contents_rate = [ float(np.round(i/len(cnt_contents))) for i in cnt_contents]

        # 4. total contents's thumbnails 
        self.total_contents_thumbnails = [select_information(self.dao,
            TwitchGame, game_name=game_name).__dict__['thumbnail']
            for game_name in self.total_contents_unique]

        # 2. popular clips in this month
        from lib.contact_db.twitch import select_clip
        
        thismonth = datetime.datetime.now().date().strftime("%Y-%m")

        clips = select_clip(self.dao,
            TwitchClip, thismonth, streamer_name=self.streamer_name)

        self.popular_clips = [{
            'title': clip.__dict__['title'],
            'created_at': clip.__dict__['created_at'],
            'clip_id': clip.__dict__['clip_id'],
            'url': clip.__dict__['url'],
            'thumbnail': clip.__dict__['thumbnail'],
            'viewer_count': clip.__dict__['viewer_count']} for clip in clips]

    # 하루의 메타 데이터 json화
    def one_day_jsonify(self):
        """
        한 방송 정보 데이터를 json으로 변환하여 반환
        """
        import json

        # 한 방송의 정보
        one_day_dict = {
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
        self.one_day_json = (json.dumps(one_day_dict, ensure_ascii=False, indent='\t'))

    # 한달 메타 데이터 json화
    def one_month_jsonify(self):
        import json
        month_dic = {
            "follower_growups": self.follower_period,
            "viewer_avr": self.month_viewer_cnt
        }
        self.one_month_json = json.dumps(month_dic, ensure_ascii=False, indent="\t")
        
        # 1 주일간의 방송 정보
        # append later

    # 모든 방송의 메타 데이터 json화
    def total_broad_jsonify(self):
        """
        지금껏의 모든 방송 정보 데이터를 json으로 변환하여 반환
        """
        import json
        # 지금껏 모든 방송의 정보
        total_broad_dict = {
            "streamer_name": self.streamer_name,
            "broaded_contents": self.total_contents_unique,
            "contents_thumbnails": self.total_contents_thumbnails,
            "broaded_contents_rate": self.total_contents_rate,
            "popular_clips": self.popular_clips
        }
        self.total_broad_json = (json.dumps(total_broad_dict, ensure_ascii=False, indent='\t'))

    # 하루데이터 json 저장
    def save_one_day_json(self, folder_path):
        """
        하루 방송의 데이터를 json 파일로 저장
        """
        import json
        # json 파일을 저장한다
        with open(folder_path + self.streamer_name + "_" + self.broad_date + ".json",
            "w", encoding="utf-8") as fp:
            fp.write(self.one_day_json)
    
    # 한달 데이터 json 저장
    def save_month_json(self, folder_path):
        """
        일주일 데이터를 json 파일로 저장
        """
        import json
        import datetime
        # json 파일을 저장한다
        with open(folder_path + self.streamer_name + "_" +
            datetime.datetime.now().strftime("%Y-%m-%d") + ".json",
            "w", encoding="utf-8") as fp:
            fp.write(self.one_month_json)

    # 모든 방송 메타 데이터 json 저장
    def save_total_broad_json(self, folder_path):
        """
        지금껏 모든 방송의 메타 데이터를 json 파일로 저장
        """
        import json
        # json 파일을 저장한다
        with open(folder_path + self.streamer_name + "_" +
            datetime.datetime.now().strftime("%Y-%m-%d") + ".json",
            "w", encoding="utf-8") as fp:
            fp.write(self.total_broad_json)
