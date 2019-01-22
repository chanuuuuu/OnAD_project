"""
* 전체 설명
dao : scoped_session 객체
twitch 데이터베이스 테이블들:
    (TwitchCaht, TwitchStream, TwitchStreamDetail,
    TwitchChannel, TwitchChannelDetail, TwitchGame, TwitchGameDetail)
"""

def select_information(dao, target_table, **kwargs):
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
    if not kwargs:
        rows = dao.query(target_table).all()
        return rows
    else:
        if len(kwargs) == 1:
            for key, value in kwargs.items():
                if key.lower() == "streamer_id":
                    rows = dao.query(target_table).filter_by(streamer_id=value).all()

                if key.lower() == "streamer_name":
                    rows = dao.query(target_table).filter_by(streamer_name=value).all()

                if key.lower() == "stream_id":
                    rows = dao.query(target_table).filter_by(stream_id=value).all()

                if key.lower() == "broad_date":
                    rows = dao.query(target_table).filter_by(broad_date=value).all()

                if key.lower() == "streamer_twitch_id":
                    rows = dao.query(target_table).filter_by(streamer_twitch_id=value).all()   

                if key.lower() == "game_id":
                    rows = dao.query(target_table).filter_by(game_id=value).first()      

                if key.lower() == "game_name":
                    rows = dao.query(target_table).filter_by(game_name=value).first()   

            return rows

        elif len(kwargs) == 2:
            dic1, dic2 = kwargs.items()
            key1, value1 = dic1
            key2, value2 = dic2
            rows = dao.query(target_table).filter(key1==value1, key2==value2).all()

def select_channel_detail(dao, target_table, broad_date, **kwargs):
    for key, value in kwargs.items():
        if key == 'streamer_id':
            from lib.contact_db.member import TwitchChannelDetail
            rows = dao.query(target_table).filter(TwitchChannelDetail.date.like(
                "%{}%".format(broad_date))).filter_by(
                streamer_id=value).all()
    return rows

def select_groupby_broad_date(dao, target_col,
    broad_date=None, streamer_name=None):
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
    from lib.contact_db.member import TwitchStream
    if not broad_date:
        rows = dao.query(target_col).group_by(target_col).all()
        rows = [ row[0] for row in rows]  # [(1,), (2,), ...] 의 형식이기에
        return rows
    else:
        """예제 쿼리
        select * from twitch_stream
        where streamer_name = "침착맨"
        and broad_date like "2019-01-14%";
        """
        rows = dao.query(target_col).filter(TwitchStream.broad_date.like(
            "%{}%".format(broad_date))).filter_by(
                streamer_name=streamer_name).all()
        return rows

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

def select_groupby(dao, target_col, **kwargs):
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
    if not kwargs:
        rows = dao.query(target_col).group_by(target_col).all()
        rows = [ row[0] for row in rows]  # [(1,), (2,), ...] 의 형식이기에
        return rows
    else:
        if len(kwargs) == 1:
            for key, value in kwargs.items():
                if key == "streamer_name":
                    rows = dao.query(target_col).group_by(
                        target_col).filter_by(
                            streamer_name=value).all()
                    return rows
                elif key == "streamer_id":
                    rows = dao.query(target_col).group_by(
                        target_col).filter_by(
                            streamer_id=value).all()
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
    from sqlalchemy import update
    
    def insert(member):
        """데이터 insert 후 커넥션 remove하는 함수
        insert_information 함수 안에서만 사용
        """
        dao.add(member)
    if data_dict:
        if target_table == 'TwitchChat':
            from lib.contact_db.member import TwitchChat  # 테이블클래스 import
            member = TwitchChat(data_dict['streamer_name'],
                data_dict['broad_date'], data_dict['chatterer'],
                data_dict['chat_time'], data_dict['chat_contents'])
            insert(member)
            return 1
        
        elif target_table == 'TwitchStream':
            from lib.contact_db.member import TwitchStream
            stream_list = select_groupby(dao, TwitchStream.stream_id)
            if data_dict.get('stream_id') in stream_list:  # 기존 목록에 같은것이 있으면 넣지 않음
                return 
            else:  # 없으면 테이블 객체로 만들어 넣음
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
            # 기존 목록 불러오기
            streamer_list = select_groupby(dao, TwitchChannel.streamer_id)

            # 기존 목록에 있는 경우 업데이트
            if data_dict.get('streamer_id') in streamer_list:
                update(TwitchChannel).where( # 업데이트
                    TwitchChannel.streamer_id == data_dict.get('streamer_id')).values(
                        streamer_id=data_dict.get('streamer_id'),
                        streamer_name=data_dict.get('streamer_name'),
                        streamer_twitch_id=data_dict.get('streamer_twitch_id'),
                        logo=data_dict.get('logo'),
                        homepage=data_dict.get('homepage'),
                    )
                return 1
            
            # 기존 목록에 없는 경우 삽입
            else:
                member = TwitchChannel(data_dict.get('streamer_id'),
                    data_dict.get('streamer_name'), data_dict.get('streamer_tiwtch_id'),
                    data_dict.get('logo'), data_dict.get('homepage'))
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
            game_list = select_groupby(dao, TwitchGame.game_id)
            
            if data_dict.get('game_id') in game_list:
                update(TwitchGame).where(  # 업데이트
                    TwitchGame.game_id == data_dict.get('game_id')).values(
                        game_id=data_dict.get('game_id'),
                        game_name=data_dict.get('game_name')
                    )
                return 1
            else:  # 없다면 그냥 삽입
                member = TwitchGame(data_dict.get('game_id'),
                data_dict.get('game_name'), data_dict.get('thumbnail'),)
                insert(member)
                return 1
        
        elif target_table == 'TwitchGameDetail':
            from lib.contact_db.member import TwitchGameDetail
            member = TwitchGameDetail(data_dict.get('game_id'),
                data_dict.get('all_viewer'), data_dict.get('stream_this_game'))
            insert(member)
            return 1

        elif target_table == 'TwitchClip':
            from lib.contact_db.member import TwitchClip
            # 중복인지 비교하기위해 기존의 데이터 불러오기
            clip_list = select_groupby(dao, TwitchClip.clip_id,
                streamer_id=data_dict.get('streamer_id'))
            
            # [(1,), (2,), ...] 의 형식이므로
            clip_list = list(map(lambda x : x[0], clip_list))

            # 기존 목록에 있는 경우 업데이트
            if data_dict.get('clip_id') in clip_list:  #update
                update(TwitchClip).where(  # 업데이트
                    TwitchClip.clip_id == data_dict.get('clip_id')).values(
                        streamer_name=data_dict.get('streamer_name'),
                        streamer_id=data_dict.get('streamer_id'),
                        clip_id=data_dict.get('clip_id'),
                        user_id=data_dict.get('user_id'),
                        created_at=data_dict.get('created_at'),
                        title=data_dict.get('title'),
                        url=data_dict.get('url'),
                        viewer_count=data_dict.get('viewer_count'),
                        thumbnail=data_dict.get('thumbnail'),
                    )
                return 1
            else:  # insert
                member = TwitchClip(data_dict.get('streamer_name'),
                    data_dict.get('streamer_id'), data_dict.get('clip_id'),data_dict.get('user_id'),
                    data_dict.get('created_at'), data_dict.get('title'),
                    data_dict.get('url'), data_dict.get('viewer_count'),
                    data_dict.get('thumbnail'))
                insert(member)
                return 1
        
        elif target_table == 'TwitchFollowing':
            from lib.contact_db.member import TwitchFollowing
            member = TwitchFollowing(data_dict.get('user_id'),
                data_dict.get('following_streamer'), data_dict.get('streamer_name'),
                data_dict.get('followed_at'))
            insert(member)
            return 1
        
        else:
            print("잘못된 target_table 입력입니다.")
            raise ValueError('plz input right table class')

def update_information(dao, target_table):
    # 필요시 작성
    pass