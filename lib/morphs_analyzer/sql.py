"""
* 전체 설명
dao : scoped_session 객체
twitch 데이터베이스 테이블들:
    (TwitchCaht, TwitchStream, TwitchStreamDetail,
    TwitchChannel, TwitchChannelDetail, TwitchGame, TwitchGameDetail)
"""

def select_all_information(dao, target_table):
    """
    select 구문 함수
    * input
      - dao : scoped_session 객체
      - target_table : 테이블 클래스 명 중 하나
        (TwitchChat, TwitchStream, TwitchStreamDetail,
        TwitchChannel, TwitchChannelDetail, TwitchGame, TwitchGameDetail)

    * output
      selected rows

    """
    if target_table:
        rows = dao.query(target_table).all()
        # dao.remove()  # 세션을 제거(많은 db 사용에 의해 커넥션 지속적으로 유지되어 종료되지 않게 하기 위함)
        return rows

def select_groupby(dao, target_col, target_streamer=None):
    """
    select 구문 함수
    * input
      - dao : scoped_session 객체
      - target_col : 그룹으로 묶어 반환 될 클래스(테이블)의 멤버변수(컬럼)
            ex) TwitchChat.broad_date
      - target_streamer : 추가적 조건으로 추가할 스트리머이름

    * output
      selected rows
    """
    if not target_streamer:
        rows = dao.query(target_col).group_by(target_col).all()
        rows = [ row[0] for row in rows]  # [(1,), (2,), ...] 의 형식이기에
        return rows
    else:
        rows = dao.query(target_col).group_by(
            target_col).filter_by(
                streamer_name=target_streamer).all()
        return rows