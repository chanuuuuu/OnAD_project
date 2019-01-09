# 분석에 필요한 데이터를 가져오는 함수

def get_data_by_query(db_url, query):
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

