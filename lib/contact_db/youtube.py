"""
* 전체 설명
dao : scoped_session 객체
youtube 데이터베이스 테이블들:
 - YoutubeChannel, YoutubeChannelDetail
 - YoutubeVideo, YoutubeChat, YoutubeReple
"""
def select_information(dao, target_table):
    """
    select 구문 함수
    * input
      - dao : scoped_session 객체
      - target_table : 테이블 클래스 명 중 하나
        (TwitchChat, TwitchStream, TwitchStreamViewer,
        TwitchChannel, TwitchChannelDetail, TwitchGame, TwitchGameDetail)

    * output
      selected rows

    """
    if target_table:
        rows = dao.query(target_table).all()
        dao.remove()  # 세션을 제거(많은 db 사용에 의해 커넥션 지속적으로 유지되어 종료되지 않게 하기 위함)
        return rows


def delete_information(dao, target_table, target_data):
    """
    db 데이터 삭제 함수
    * input
      - dao : scoped_session 객체
      - target_table : 테이블 클래스 명 중 하나
        (YoutubeChannel, YoutubeChannelDetail
         YoutubeVideo, YoutubeChat, YoutubeReple)

    * output
      데이터 삭제 이후 1을 반환
      삭제가 진행되지 않았을 시 None 을 반환
    """
    if target_table == 'YoutubeChannel':
        dao.query('YoutubeChannel').filter_by(
            channel_id=target_data.get('channel_id'),
            channel_name=target_data.get('channel_name')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'YoutubeChannelDetail':
        dao.query('YoutubeChannelDetail').filter_by(
            channel_id=target_data.get('channel_id')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'YoutubeVideo':
        dao.query('YoutubeVideo').filter_by(
            channel_id=target_data.get('channel_id'),
            video_id=target_data.get('video_id'),
            title=target_data.get('title')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1
    
    elif target_table == 'YoutubeChat':
        dao.query('YoutubeChat').filter_by(
            chat_id=target_data('chat_id'),
            video_id=target_data('video_id'),
            chat_time=target_data('chat_time'),
            chatterer=target_data('chatterer')).first().delete(synchronize_session=False)
        dao.commit()
        dao.remove()
        return 1

    elif target_table == 'YoutubeReple':
        dao.query('YoutubeReple').filter_by(
            reple_id=target_data('reple_id'),
            video_id=target_data('video_id'),
            author=target_data('author')).first().delete(synchronize_session=False)
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
      - target_table : 테이블 클래스 명 중 하나
        (YoutubeChannel, YoutubeChannelDetail
         YoutubeVideo, YoutubeChat, YoutubeReple)
      - data_dict : 해당 테이블의 컬럼명을 key로 하고, 데이터를 value로 하는 딕셔너리
        ex) YoutubeChannel 이라면,
        {'channel_id': DGahT12aA34aGdg5, 'channel_name': '풍월량TV', 'channel_keyword': '게임, 소통, ...'}
    * output
      데이터 삽입 이후 1을 반환
      삽입이 진행되지 않았을 시 None 을 반환
    """
    def insert(member):
        """데이터 insert 후 커넥션 remove하는 함수
        insert_information 함수 안에서만 사용
        """
        dao.add(member)
        dao.commit()
        dao.remove()

    if target_table == 'YoutubeChannel':
        from lib.contact_db.member import YoutubeChannel  # 테이블클래스 import
        member = YoutubeChannel(data_dict.get('channel_id'),
        data_dict.get('channel_name'), data_dict.get('channel_keyword'))
        insert(member)
        return 1
    
    elif target_table == 'YoutubeChannelDetail':
        from lib.contact_db.member import YoutubeChannelDetail
        member = YoutubeChannelDetail(data_dict.get('channel_id'),
            data_dict.get('channel_name'), data_dict.get('channel_keyword'),
            data_dict.get('channel_video_cnt'))
        insert(member)
        return 1

    elif target_table == 'YoutubeVideo':
        from lib.contact_db.member import YoutubeVideo
        member = YoutubeVideo(data_dict.get('channel_id'),
            data_dict.get('video_id'), data_dict.get('title'),
            data_dict.get('upload_date'), data_dict.get('view_cnt'),
            data_dict.get('like_cnt'), data_dict.get('hate_cnt'),
            data_dict.get('reple_cnt'), data_dict.get('category'),
            data_dict.get('thumbnail'), data_dict.get('is_live'))
        insert(member)
        return 1
    
    elif target_table == 'YoutubeChat':
        from lib.contact_db.member import YoutubeChat
        member = YoutubeChat(data_dict.get('chat_id'),
            data_dict.get('video_id'), data_dict.get('chat_time'),
            data_dict.get('chatterer'), data_dict.get('chat_contents'),
            data_dict.get('broad_date'))
        insert(member)
        return 1
    
    elif target_table == 'YoutubeReple':
        from lib.contact_db.member import YoutubeReple
        member = YoutubeReple(data_dict.get('reple_id'),
            data_dict.get('video_id'), data_dict.get('upload_date'),
            data_dict.get('author'), data_dict.get('reple_contents'))
        insert(member)
        return 1

    else:
        print("잘못된 target_table 입력입니다.")
        raise ValueError('plz input right table class - hwasurr')
    

def update_information(dao, target_table):
    # 필요시 작성
    pass