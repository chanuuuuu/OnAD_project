# utf-8 encoding
from lib.contact_db import Base
from sqlalchemy import Column, String, Integer, Date, Text
from sqlalchemy.sql.expression import func

# 트위치 테이블
class TwitchChat(Base):
    """
    viewer_id : 채팅을 친 시청자의 ID
    chat_time : 채팅을 친 시간정보
    chat_contents : 채팅정보
    """
    __tablename__ = 'twitch_chat'
    code = Column(Integer, primary_key=True, autoincrement=True)
    viewer_id = Column(String(50), unique=False)
    chat_time = Column(String(), unique=False)
    chat_contents = Column(Text(), unique=False)

    def __init__(self, viewer_id, chat_time,
        chat_contents):
        self.viewer_id = viewer_id
        self.chat_time = chat_time
        self.chat_contents = chat_contents

    def __repr__(self):
        return """<%s, %s, %s, %s, %s, %s>""" % (self.viewer_id,
        self.chat_time, self.chat_contents)


class TwitchStream(Base):
    """
    stream_id : twitch 생방송의 고유 ID
    streamer_id : twitch 스트리머의 고유 ID
    broad_date : 해당 스트리밍의 방송날짜
    """
    __tablename__ = 'twitch_stream'
    code = Column(Integer, primary_key=True, autoincrement=True)
    stream_id = Column(Integer, unique=False)
    streamer_id = Column(Integer, unique=False)
    broad_date = Column(String(50), unique=False)

    def __init__(self, stream_id,
        streamer_id, broad_date):
        self.stream_id = stream_id
        self.streamer_id = streamer_id
        self.broad_date = broad_date

    def __repr__(self,):
        return """<%s, %s, %s, %s>""" % (self.stream_id,
            self.streamer_id, self.broad_date)


class TwitchChannel(Base):
    """
    트위치 채널정보를 담아놓는 테이블
    streamer_id : twitch 스트리머의 고유 ID
    streamer_name : 스트리머의 이름(닉네임)
    logo : 스트리머 로고의 주소
    homepage : 스트리머 방송국 홈페이지
    """
    __tablename__ = "twitch_channel"
    code = Column(Integer, primary_key=True, autoincrement=True)
    streamer_id = Column(Integer, unique=True)
    streamer_name = Column(String(), unique=True)
    logo = Column(String(300), unique=True)
    homepage = Column(String(300), unique=True)

    def __init__(self, streamer_id ,streamer_name,
        logo, homepage):
        self.streamer_id = streamer_id
        self.streamer_name = streamer_name
        self.logo = logo
        self.homepage = homepage

    def __repr__(self):
        return """%s %s %s %s %s""" % (self.code, self.streamer_id,
            self.streamer_name. self.logo, self.homepage)


class TwitchChannelDetail(Base):
    """
    트위치 채널의 세부정보를 담아놓는 테이블로
    잦은 업데이트가 필요한 테이블
    streamer_id : twitch 스트리머의 고유 ID
    date : 날짜
    follower : 팔로워의 수
    subscriber : 구독자의 수
    """
    __tablename__ = "twitch_channel_detail"
    streamer_id = Column(Integer, primary_key=True, unique=True)
    date = Column(Date, default=func.curdate())
    follower = Column(Integer, unique=False)
    subscriber = Column(Integer, unique=False)

    def __init__(self, streamer_id, date,
        follower, subscriber):
        self.streamer_id = streamer_id
        self.date = date
        self.follower = follower
        self.subscriber = subscriber
    
    def __repr__(self):
        return "%s %s %s %s" % (self.streamer_id,
            self.date, self.follower, self.subscriber)


class TwitchGame(Base):
    """
    트위치에서 제공하는 게임정보를 담아놓는 테이블
    game_id : 트위치에서 설정한 게임의 고유 ID
    game_name : 게임 이름
    """
    __tablename__ = "twitch_game"
    game_id = Column(Integer, primary_key=True, unique=True)
    game_name = Column(String(100), unique=True)

    def __init__(self, game_id, game_name):
        self.game_id = game_id
        self.game_name = game_name

    def __repr__(self):
        return "%s %s" % (self.game_id, self.game_name)


class TwitchGameDetail(Base):
    """
    twitch_game 테이블의 세부사항을 담아놓는 테이블
    잦은 업데이트가 필요한 테이블
    game_id : 트위치에서 설정한 게임의 고유 ID
    date : 현재 날짜
    all_viewer : 이 게임을 시청하는 총 시청자
    stream_this_game : 이 게임을 방송중인 스트리밍의 수
    """
    __tablename__ = "twitch_game_detail"
    game_id = Column(Integer, primary_key=True, unique=True)
    date = Column(Date, default=func.curdate())
    all_viewer = Column(Integer, unique=False)
    stream_this_game = Column(Integer, unique=False)

    def __init__(self, game_id, all_viewer, stream_this_game):
        self.game_id = game_id
        self.all_viewer = all_viewer
        self.stream_this_game = stream_this_game

    def __repr__(self):
        return "%s %s %s" % (self.game_id,
            self.game_name, self.stream_this_game)

# 모델 버전관리

# 회원정보

# 유튜브 테이블
class YoutubeChannel(Base):
    pass


class YoutubeVideoList(Base):
    pass


class YoutubeVideo(Base):
    pass


class YoutubeChat(Base):
    pass


class YoutubeReple(Base):
    pass
