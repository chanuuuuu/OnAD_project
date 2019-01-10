# 데이터 베이스에서 트위치 채팅 / 트위치 스트리밍 데이터 가져와
# 분석 데이터로 반환하는 모듈

def select_twitch_chat(db_url, streamer_id, target_date):
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
    query = """select * from twitch_chat where streamer_name = "%s" and broad_date ="%s"
    """ % (streamer_id, target_date)
    return pd.read_sql_query(query, db_url)


def select_stream_start_time(dao, db_url, streamer_id, target_date):
    """
    * inpurt
        db_url : 데이터 베이스 연결 url, str
        streamer_id : 스트리머의 트위치id, str ex)zilioner
    * output
        pandas.DataFrame객체
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

    # 트위치 시간대는 UTC 기준이므로 한국시간으로 +9시간 하여 변경
    broad = broad.apply(lambda x : x + pd.Timedelta("9hours"))
    for i in broad:
        if target_date == str(i.date()):
            return i.time()


def select_data_by_query(db_url, query):
    """
    db와 접촉하여 쿼리를 수행한 후 데이터 프레임으로 반환합니다.
    * input
        db_url : 데이터 베이스 연결 url, str
        query : 수행할 쿼리, str
    * output
        pandas.DataFrame 객체
    """
    import pandas as pd
    return pd.read_sql_query(query, db_url)


def select_streamer_id_by_name(dao, target_name='얍얍'):
    """
    스트리머 이름을 입력시 스트리머 id를 반환하는함수"""
    from lib.contact_db.member import TwitchChannel
    if target_name:
        name = dao.query(TwitchChannel.homepage).filter_by(streamer_name=target_name).first()
        if name :
            return name[0].split("/")[-1]


def select_exists_date(dao, target_id='yapyap30'):
    """
    채팅 데이터 중 db 에 존재하는 날짜만 반환하는 함수
    - input:
        target_id : 타겟 스트리머 아이디  
    - output:
        채팅 로그 데이터가 있는  날짜들 list
    """
    from lib.contact_db.member import TwitchChat

    if target_id:
        return dao.query(TwitchChat.broad_date).filter_by(streamer_name = target_id).all()