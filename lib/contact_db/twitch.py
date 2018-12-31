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
        dao.remove()  # 세션을 제거(많은 db 사용에 의해 커넥션 지속적으로 유지되어 종료되지 않게 하기 위함)
        return rows

def select_groupby(dao, target_col):
    """
    select 구문 함수
    * input
      - dao : scoped_session 객체
      - target_table : 테이블 클래스명 중 하나
        (TwitchCaht, TwitchStream, TwitchStreamDetail,
        TwitchChannel, TwitchChannelDetail, TwitchGame, TwitchGameDetail)
      - target_col : 그룹으로 묶어 볼 컬럼명

    * output
      selected rows
    """
    rows = dao.query(target_col).group_by(target_col).all()
    rows = [ row[0] for row in rows]
    dao.remove()
    return rows

def delete_information(dao, target_table, target_data):
    """
    db 데이터 삭제 함수
    * input
      - dao : scoped_session 객체
      - target_table : 테이블 클래스 명 중 하나, 삭제할 데이터가 있는 테이블
        (TwitchChat, TwitchStream, TwitchStreamDetail,
        TwitchChannel, TwitchChannelDetail, TwitchGame, TwitchGameDetail)
      - target_data : 삭제할 데이터의 정보 딕셔너리
                          테이블의 컬럼명을 key로, 데이터를 value로 갖는 딕셔너리
    * output
      데이터 삭제 이후 1을 반환
      삭제가 진행되지 않았을 시 None 을 반환
    """
    if target_table == 'TwitchCaht':
        dao.query('TwitchChat').filter_by(
            viewer_id=target_data.get('viewer_id'),
            chat_time=target_data.get('chat_time')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'TwitchStream':
        dao.query('TwitchStream').filter_by(
            stream_id=target_data.get('stream_id'),
            streamer_id=target_data.get('streamer_id'),
            broad_date=target_data.get('broad_date')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'TwitchStream_setail':
        dao.query('TwitchStreamDetail').filter_by(
            stream_id=target_data.get('stream_id'),
            time=target_data.get('date')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1
    
    elif target_table == 'TwitchChannel':
        dao.query('TwitchChannel').filter_by(
            streamer_id=target_data('streamer_id'),
            streamer_name=target_data('streamer_name')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'TwitchChannelDetail':
        dao.query('TwitchChannelDetail').filter_by(
            streamer_id=target_data('streamer_id'),
            date=target_data('date')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'TwitchGame':
        dao.query('TwitchGame').filter_by(
            game_id=target_data('game_id'),
            game_name=target_data('game_name')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'TwitchGameDetail':
        dao.query('TwitchGameDetail').filter_by(
            game_id=target_data('game_id'),
            date=target_data('date')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'twitch_following':
        dao.query('TwitchFollowing').filter_by(
            user_id=target_data('user_id'),
            following_streamer=target_data('following_streamer'))\
            .first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    else:
        print("잘못된 target_table 입력입니다.")
        raise ValueError('plz input right table class - hwasurr')


def insert_information(dao, target_table, data_dict):
    """
    db 데이터 삽입 함수
    * input
      - dao : scoped_session 객체
      - target_table : 테이블 명 중 하나
        (TwitchCaht, TwitchStream, TwitchStreamDetail,
        TwitchChannel, TwitchChannelDetail, TwitchGame, TwitchGameDetail)
      - data_dict : 해당 테이블의 컬럼명을 key로 하고, 데이터를 value로 하는 딕셔너리
        ex) TwitchChat 이라면,
        {
            'viewer_id': 12345,
            'chat_time': '15:32:24',
            'chat_contents': '꿀잼'
        }의 형태
    * output
      데이터 삽입 이후 1을 반환
      삽입이 진행되지 않았을 시 None 을 반환
    """
    def insert(member):
        """데이터 insert 후 커넥션 remove하는 함수
        insert_information 함수 안에서만 사용
        """
        dao.add(member)

    if target_table == 'TwitchChat':
        from lib.contact_db.member import TwitchChat  # 테이블클래스 import
        member = TwitchChat(data_dict['chatterer'],
            data_dict['chat_time'], data_dict['chat_contents'])
        insert(member)
        return 1
    
    elif target_table == 'TwitchStream':
        from lib.contact_db.member import TwitchStream
        member = TwitchStream(data_dict.get('stream_id'), data_dict.get('streamer_id'),
            data_dict.get('streamer_name'), data_dict.get('broad_date'))
        insert(member)
        return 1

    elif target_table == 'TwitchStreamDetail':
        from lib.contact_db.member import TwitchStreamDetail
        member = TwitchStreamDetail(data_dict.get('stream_id'),
            data_dict.get('viewer'), data_dict.get('title'),
            data_dict.get('game_id'))
        insert(member)
        return 1
    
    elif target_table == 'TwitchChannel':
        from lib.contact_db.member import TwitchChannel
        member = TwitchChannel(data_dict.get('streamer_id'),
            data_dict.get('streamer_name'), data_dict.get('logo'),
            data_dict.get('homepage'))
        insert(member)
        return 1
    
    elif target_table == 'TwitchChannelDetail':
        from lib.contact_db.member import TwitchChannelDetail
        member = TwitchChannelDetail(data_dict.get('streamer_id'),
            data_dict.get('follower'), data_dict.get('viewer'))
        insert(member)
        return 1

    elif target_table == 'TwitchGame':
        from lib.contact_db.member import TwitchGame
        member = TwitchGame(data_dict.get('game_id'),
           data_dict.get('game_name'))
        insert(member)
        return 1
    
    elif target_table == 'TwitchGameDetail':
        from lib.contact_db.member import TwitchGameDetail
        member = TwitchGameDetail(data_dict.get('game_id'),
            data_dict.get('all_viewer'), data_dict.get('stream_this_game'))
        insert(member)
        return 1
    
    elif target_table == 'TwitchFollowing':
        from lib.contact_db.member import TwitchFollowing
        member = TwitchFollowing(data_dict.get('user_id'),
            data_dict.get('following_streamer'), data_dict.get('streamer_name'))
        insert(member)
        return 1
    
    else:
        print("잘못된 target_table 입력입니다.")
        raise ValueError('plz input right table class')
    

def update_information(dao, target_table):
    # 필요시 작성
    pass