
from sqlalchemy import Column, String, Integer, Date, Text, Float, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 트위치 테이블
class TwitchChat(Base):
    """
    chat_id : 채팅의 번호
    chatterer : 채팅을 친 시청자의 이름
    chat_time : 채팅을 친 시간정보
    chat_contents : 채팅정보
    """
    __tablename__ = 'twitch_chat'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    chatterer = Column(String(50), unique=False)
    chat_time = Column(String(50), unique=False)
    chat_contents = Column(Text, unique=False)

    def __init__(self, viewer_id, chat_time,
        chat_contents):
        self.viewer_id = viewer_id
        self.chat_time = chat_time
        self.chat_contents = chat_contents

    def __repr__(self):
        return "%s, %s, %s" % (self.viewer_id,
        self.chat_time, self.chat_contents)


class TwitchStream(Base):
    """
    streamer_id : twitch 스트리머의 고유 ID
    stream_id : twitch 생방송의 고유 ID(this changes every stream )
    streamer_name : 해당 스트리머 이름
    broad_date : 해당 스트리밍의 방송시작날짜
    """
    __tablename__ = 'twitch_stream'
    code = Column(Integer, primary_key=True, autoincrement=True)
    stream_id = Column(String(50), unique=False)
    streamer_id = Column(String(50), unique=False)
    streamer_name = Column(String(50), unique=False)
    broad_date = Column(String(50), unique=False)

    def __init__(self, stream_id, streamer_id,
        streamer_name, broad_date):
        self.stream_id = stream_id
        self.streamer_id = streamer_id
        self.streamer_name = streamer_name
        self.broad_date = broad_date

    def __repr__(self,):
        return "%s, %s, %s, %s" % (self.stream_id,
            self.streamer_id, self.streamer_name, self.broad_date)


class TwitchStreamDetail(Base):
    """
    트위치 스트리밍의 세부정보를 담기 위한 테이블
    stream_id : twitch 생방송의 고유 ID( this changes every stream )
    viewer : 시청자수
    title : twitch 생방송의 제목
    game_id : 진행중인 게임의 고유 ID
    date : 시간 정보
    """
    __tablename__ = 'twitch_stream_detail'
    code = Column(Integer,  autoincrement=True)
    stream_id = Column(String(50), primary_key=True, unique=False)
    viewer = Column(Integer, unique=False)
    title = Column(String(150), unique=False)
    game_id = Column(String(50), unique=False)
    time = Column(Date, default=func.curdate())

    def __init__(self, stream_id,
        viewer, title, game_id):
        self.stream_id = stream_id
        self.viewer = viewer
        self.title = title
        self.game_id = game_id

    def __repr__(self,):
        return """%s, %s, %s, %s, %s""" % (self.stream_id,
            self.title, self.viewer, self.game_id, self.time)


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
    streamer_id = Column(String(50), unique=False)
    streamer_name = Column(String(50), unique=False)
    logo = Column(Text, unique=False)
    homepage = Column(Text, unique=False)

    def __init__(self, streamer_id ,streamer_name,
        logo, homepage):
        self.streamer_id = streamer_id
        self.streamer_name = streamer_name
        self.logo = logo
        self.homepage = homepage

    def __repr__(self):
        return "%s, %s, %s, %s, %s" % (self.code, self.streamer_id,
            self.streamer_name, self.logo, self.homepage)


class TwitchChannelDetail(Base):
    """
    트위치 채널의 세부정보를 담아놓는 테이블로
    잦은 업데이트가 필요한 테이블
    streamer_id : twitch 스트리머의 고유 ID
    date : 시간 정보
    follower : 팔로워의 수
    subscriber : 구독자의 수
    """
    __tablename__ = "twitch_channel_detail"
    streamer_id = Column(String(50),
        primary_key=True, unique=False)
    date = Column(Date, default=func.curdate())
    follower = Column(Integer, unique=False)
    subscriber = Column(Integer, unique=False)

    def __init__(self, streamer_id,
        follower, subscriber):
        self.streamer_id = streamer_id
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
    game_id = Column(String(50), primary_key=True, unique=False)
    game_name = Column(String(100), unique=False)

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
    game_id = Column(String(50), 
        primary_key=True, unique=False)
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
class ModelVersion(Base):
    """
    감성분석 모델의 버전정보를 담고있는 테이블
    version : 버전 정보
    date : 업데이트 날짜
    file_name : 모델 파일명
    f1_score : f1-score 점수
    accuracy : 정확도 점수
    comment : 코멘트
    """
    __tablename__ = "model_version"
    version = Column(Integer, primary_key=True)
    date = Column(Date, default=func.curdate())
    file_name = Column(String(100), unique=False)
    f1_score = Column(Float, unique=False)
    accuracy = Column(Float, unique=False)
    comment = Column(Text, unique=False)

    def __init__(self, version, date, file_name,
        f1_score, accuracy ,comment):
        self.version = version
        self.date = date
        self.file_name = file_name
        self.f1_score = f1_score
        self.accuracy = accuracy
        self.comment = comment

    def __repr__(self):
        return "%s %s %s %s %s %s" % (self.version,
            self.date, self.file_name, self.f1_score,
            self.accuracy, self.comment)

# 회원정보
class Creater(Base):
    """
    크리에이터 회원의 정보를 담는 테이블
    code : 회원 번호
    reg_date : 가입 일시
    flatform : 방송 플랫폼 정보
    creater_id : (youtube면 channel_id twitch면 streamer_id)
    user_id : onad 가입한 아이디
    user_pw : onad 가입한 비밀번호
    user_name : onad 가입한 이름
    nickname : 닉네임(creater 활동명)
    phone : 전화번호
    email : 이메일주소
    homepage : 홈페이지 주소
    broad_program : 방송 송출 프로그램 명

    * 다른 테이블과는 다르게 dict형태의 데이터를 집어넣어야 한다.
    {'code': code, 'flatform': flatform, ...}
    """
    __tablename__ = "creater"
    code = Column(Integer, primary_key=True, autoincrement=True)
    reg_date = Column(Date, default=func.curdate())
    flatform = Column(String(50), unique=False)
    creater_id = Column(String(50), unique=False)
    user_id = Column(String(20), unique=False)
    user_pw = Column(String(15), unique=False)
    user_name = Column(String(30), unique=False)
    nickname = Column(String(30), unique=False)
    phone = Column(String(30), unique=False)
    email = Column(String(100), unique=False)
    homepage = Column(Text, unique=False)
    broad_program = Column(String(30), unique=False)

    def __init__(self, data_dict):
        self.flatform = data_dict['flatform']
        self.creater_id = data_dict['creater_id']
        self.user_id = data_dict['user_id']
        self.user_pw = data_dict['user_pw']
        self.user_name = data_dict['user_name']
        self.nickname = data_dict['nickname']
        self.phone = data_dict['phone']
        self.email = data_dict['email']
        self.homepage = data_dict['homepage']
        self.broad_program = data_dict['broad_program']

    def __repr__(self):
        return """%s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s""" % (self.flatform,
            self.creater_id, self.user_id, self.user_pw,
            self.user_name, self.nickname, self.phone,
            self.email, self.homepage, self.broad_program)


class Advertiser(Base):
    """
    광고주 회원의 정보를 담는 테이블
    code : 회원 번호
    reg_date : 가입 일시
    user_id : onad 가입한 아이디
    user_pw : onad 가입한 비밀번호
    user_name : onad 가입한 이름 (담당자 명)
    phone : 담당자 전화번호
    email : 담당자 이메일주소
    corporation_name : 소속기업 명
    corporation_code : 소속기업의 코드
    
    * 다른 테이블과는 다르게 dict형태의 데이터를 집어넣어야 한다.
    {'user_id': user_pw, 'user_pw': user_pw, ...}
    """
    __tablename__ = "advertiser"
    code = Column(Integer, primary_key=True, autoincrement=True)
    reg_date = Column(Date, default=func.curdate())
    creater_id = Column(String(50), unique=False)
    user_id = Column(String(20), unique=False)
    user_pw = Column(String(15), unique=False)
    user_name = Column(String(30), unique=False)
    nickname = Column(String(30), unique=False)
    phone = Column(String(30), unique=False)
    email = Column(String(100), unique=False)
    corporation_name = Column(String(30), unique=False)
    corporation_code = Column(String(30), unique=False)

    def __init__(self, data_dict):
        self.creater_id = data_dict['creater_id']
        self.user_id = data_dict['user_id']
        self.user_pw = data_dict['user_pw']
        self.user_name = data_dict['user_name']
        self.nickname = data_dict['nickname']
        self.phone = data_dict['phone']
        self.email = data_dict['email']
        self.corporation_name = data_dict['corporation_name']
        self.corporation_code = data_dict['corporation_code']

    def __repr__(self):
        return """%s, %s, %s, %s, %s,
        %s, %s, %s, %s""" % (self.creater_id,
            self.user_id, self.user_pw, self.user_name,
            self.nickname, self.phone, self.email,
            self.corporation_name, self.corporation_code)


class Corporation(Base):
    """
    기업 정보를 담는 테이블
    code : 가입된 기업 번호
    corporation_code : 소속기업의 코드
    corporation_name : 소속기업 명
    nation : 소속 국가
    chief : 대표자 명
    product : 업종
    prior_product : 주요 상품 군
    homepage : 회사홈페이지
    corporation_num : 사업자 등록번호
    
    * 다른 테이블과는 다르게 dict형태의 데이터를 집어넣어야 한다.
    {'user_id': user_pw, 'user_pw': user_pw, ...}
    """
    __tablename__ = "corporation"
    code = Column(Integer, primary_key=True, autoincrement=True)
    corporation_code = Column(String(50), unique=False)
    corporation_name = Column(String(50), unique=False)
    nation = Column(String(30), unique=False)
    chief = Column(String(30), unique=False)
    product = Column(String(30), unique=False)
    prior_product = Column(String(30), unique=False)
    homepage = Column(String(100), unique=False)
    corporation_num = Column(String(50), unique=False)
    

    def __init__(self, data_dict):
        self.corporation_code = data_dict['corporation_code']
        self.corporation_name = data_dict['corporation_name']
        self.nation = data_dict['nation']
        self.chief = data_dict['chief']
        self.product = data_dict['product']
        self.prior_product = data_dict['prior_product']
        self.homepage = data_dict['homepage']
        self.corporation_num = data_dict['corporation_num']

    def __repr__(self):
        return """%s, %s, %s, %s,
        %s, %s, %s, %s""" % (self.corporation_code,
            self.corporation_name, self.nation, self.chief,
            self.product, self.prior_product, self.homepage,
            self.corporation_num)


# 유튜브 테이블
class YoutubeChannel(Base):
    """
    유튜브 채널정보를 담기위한 테이블
    channel_id : 유튜브에서 설정한 고유 ID
    channel_name : 채널 이름
    channel_keyword : 채널 검색 키워드 a, b, c, d, 의 형식
    """
    __tablename__ = 'youtube_channel'
    code = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(50), unique=False)
    channel_name = Column(String(30), unique=False)
    channel_keyword = Column(String(100), unique=False)

    def __init__(self, channel_id,
        channel_name, channel_keyword):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_keyword = channel_keyword

    def __repr__(self):
        return """%s, %s, %s""" % (self.channel_id,
            self.channel_name, self.channel_keyword)


class YoutubeChannelDetail(Base):
    """
    유튜브 채널의 세부 정보를 담기위한 테이블
    자주 업데이트 되는 항목들 모음
    channel_id : 유튜브에서 설정한 고유 ID
    subscriber : 채널 구독자 수
    channel_hit : 채널 조회 수
    channel_video_cnt : 채널 영상 수
    """
    __tablename__ = 'youtube_channel_detail'
    channel_id = Column(String(50), 
        primary_key=True, unique=False)
    subscriber = Column(Integer, unique=False)
    channel_hit = Column(Integer, unique=False)
    channel_video_cnt = Column(Integer, unique=False)

    def __init__(self, channel_id, channel_name,
        channel_hit, channel_video_cnt):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_hit = channel_hit
        self.channel_video_cnt = channel_video_cnt

    def __repr__(self):
        return """%s, %s, %s, %s""" % (self.channel_id,
            self.channel_name, self.channel_keyword,
            self.channel_video_cnt)


class YoutubeVideo(Base):
    """
    각 채널의 동영상들의 정보를 저장하는 테이블
    지속적인 업데이트(갈아끼우기) 필요한 테이블
    channel_id : 유튜브에서 설정한 채널의 고유 ID
    video_id : 영상의 고유 ID
    title : 영상 제목
    upload_date : 영상 게시 날짜
    view_cnt : 영상 조회수
    like_cnt : 좋아요 수
    hate_cnt : 싫어요 수
    reple_cnt : 댓글 수
    category : 카테고리
    thumbnail : 썸네일 주소
    is_live : 업로드된 라이브방송인지, 일반 영상인지의 여부
    """
    __tablename__ = 'youtube_video'
    channel_id = Column(String(100), unique=False)
    video_id = Column(String(100), primary_key=True, unique=False)
    title = Column(String(100), unique=False)
    upload_date = Column(String(50), unique=False)
    view_cnt = Column(Integer, unique=False)
    like_cnt = Column(Integer, unique=False)
    hate_cnt = Column(Integer, unique=False)
    reple_cnt = Column(Integer, unique=False)
    category = Column(String(50), unique=False)
    thumbnail = Column(Text, unique=False)
    is_live = Column(String(20), unique=False)

    def __init__(self, channel_id, video_id,
        title, upload_date, view_cnt, like_cnt,
        hate_cnt, reple_cnt, category, thumbnail, is_live):
        self.channel_id = channel_id
        self.video_id = video_id
        self.title = title
        self.upload_date = upload_date
        self.view_cnt = view_cnt
        self.like_cnt = like_cnt
        self.hate_cnt = hate_cnt
        self.reple_cnt = reple_cnt
        self.category = category
        self.thumbnail = thumbnail
        self.is_live = is_live

    def __repr__(self):
        return """%s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s,""" % (self.channel_id,
            self.video_id, self.title, self.upload_date,
            self.view_cnt, self.like_cnt, self.hate_cnt, 
            self.reple_cnt, self.category,
            self.thumbnail,self.is_live)


class YoutubeChat(Base):
    """
    유튜브 라이브 동영상의 채팅데이터를 저장하는 테이블
    chat_id : 채팅의 고유 번호
    video_id : 영상의 고유 ID
    chat_time : 채팅을 친 시간
    chatterer : 채팅을 친 시청자의 이름
    chat_contents : 채팅 내용
    broad_date : 방송 날짜
    """
    __tablename__ = 'youtube_chat'
    chat_id = Column(Integer, autoincrement=True, primary_key=True)
    video_id = Column(String(100), unique=False)
    chat_time = Column(String(50), unique=False)
    chatterer = Column(String(50), unique=False)
    chat_contents = Column(Text, unique=False)
    broad_date = Column(String(50), unique=False)
    
    def __init__(self, chat_id, video_id, chat_time,
        chatterer, chat_contents, broad_date):
        self.chat_id = chat_id
        self.video_id = video_id
        self.chat_time = chat_time
        self.chatterer = chatterer
        self.chat_contents = chat_contents
        self.broad_date = broad_date

    def __repr__(self):
        return """%s, %s, %s, %s, %s, %s""" % (self.chat_id,
            self.video_id, self.chat_time, self.chatterer,
            self.chat_contents, self.broad_date)


class YoutubeReple(Base):
    """
    유튜브 영상의 댓글정보를 저장하는 테이블
    reple_id : 채팅의 고유 번호
    video_id : 영상의 고유 ID
    upload_date : 댓글을 단 시간
    author : 댓글을 단 시청자의 이름
    reple_contents : 댓글 내용
    """
    __tablename__ = 'youtube_reple'
    reple_id = Column(String(100), primary_key=True, unique=False)
    video_id = Column(String(100), unique=False)
    upload_date = Column(String(50), unique=False)
    author = Column(String(50), unique=False)
    reple_contents = Column(Text, unique=False)
    
    def __init__(self, reple_id, video_id,
        upload_date, author, reple_contents):
        self.reple_id = reple_id
        self.video_id = video_id
        self.upload_date = upload_date
        self.author = author
        self.reple_contents = reple_contents

    def __repr__(self):
        return """%s, %s, %s, %s, %s""" % (self.reple_id,
            self.reple_id, self.upload_date,
            self.author, self.reple_contents)


