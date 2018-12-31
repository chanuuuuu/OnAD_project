# 모든 프로그램을 관리하는 클래스
# 메소드 하나하나 = 하나의 기능

# DB매니저 import
from onad_db import DBManager

DB_URL = 'onad.cbjjamtlar2t.ap-northeast-2.rds.amazonaws.com'
DB_USER = 'onad'
DB_PASSWORD = 'rkdghktn12'
DB_DATABASE = 'onad'
DB_CHARSET = 'utf8mb4'
DB_LOGFLAG  = 'False'
DB_PORT = 3306

db_url = "mysql+pymysql://%s:%s@%s:%s/%s?charset=%s" % (
    DB_USER, DB_PASSWORD,
    DB_URL, DB_PORT,
    DB_DATABASE, DB_CHARSET
)

class OnAd():
    """
    모든 onad의 시스템을 관리하는 총괄 클래스
    """
    # 작업 디렉토리 설정
    data_dir = "./data/"
    twitch_live_stream_dir = data_dir + "twitch_live_stream/"
    twitch_chat_dir = data_dir + "twitch_live_chat/"
    
    # 멤버변수 선언
    dao = None
    

    # 멤버함수 선언
    def __init__(self):
        """db 초기화"""
        dao = DBManager.init(db_url, eval(DB_LOGFLAG))
        self.dao = dao
        DBManager.init_db()

    def get_data_twitch(self, table_name):
        """
        * input
         - table_name : twitch db의 테이블 명
        """
        from lib.get_data.twitch_api import get_twitch_stream
        from lib.get_data.twitch_api import get_twitch_stream_detail
        from lib.get_data.twitch_api import get_twitch_game
        from lib.get_data.twitch_api import get_twitch_game_detail
        from lib.get_data.twitch_api import get_twitch_chat
        from lib.get_data.twitch_api import get_twitch_channel
        from lib.get_data.twitch_api import get_twitch_channel_detail
        from lib.contact_db.twitch import select_groupby
        from lib.contact_db.twitch import select_all_information
        from lib.contact_db.twitch import insert_information
        from lib.contact_db.member import TwitchStream
        
        # api 이용하여 데이터 받아오는 작업
        if table_name == "TwitchStream":
            list_result = get_twitch_stream.start()
            print("데이터 준비 완료")

        if table_name == "TwitchStreamDetail":
            list_result = get_twitch_stream_detail.start()
            print("데이터 준비 완료")
        
        elif table_name == "TwitchGame":
            list_result = get_twitch_game.start()
            print("데이터 준비 완료")
        
        elif table_name == "TwitchGameDetal":
            list_result = get_twitch_game_detail.start()
            print("데이터 준비 완료")
        
        elif table_name == 'TwitchChat':
            list_result = get_twitch_chat.start()
            print("데이터 준비 완료")

        elif table_name == 'TwitchChannel':
            streamer_list = select_groupby(self.dao,
                TwitchStream.streamer_id)
            list_result = get_twitch_channel.start(streamer_list)
            print("데이터 준비 완료")

        elif table_name == 'TwitchChannelDetail':
            streamer_list = select_groupby(self.dao,
                TwitchStream.streamer_id)
            list_result = get_twitch_channel_detail.start(streamer_list)
            print("데이터 준비 완료")
        
        # db 적재 작업
        print("DB에 적재중")
        for data_dict in list_result:
            insert_information(self.dao, table_name, data_dict)

        self.dao.commit()
        self.dao.remove()
        print("완료")

    def set_data_twitch_chat(self, target_id, target_date):
        """
        채팅 데이터와 스트리밍 데이터를 전처리하여 (chat_df, viewer_df)로 반환
        * input
          - target_id : 대상 스트리머 아이디, str
            "yapyap30"의 형태
          - target_date : 대상 방송 날짜, str
            "2018-12-10"의 형태
        * output
          - tuple
          - (chat_df, viewer_df) 의 형태
        """
        from lib.set_data.twitch_preprocessing import load_chatting
        from lib.set_data.twitch_preprocessing import load_viewer_count

        # 채팅 데이터 로드
        chat_df = load_chatting(target_id=target_id,
            target_date=target_date,
            twitch_chat_dir=self.twitch_chat_dir)

        # 시간당 시청자수 데이터 로드
        viewer_df = load_viewer_count(target_id=target_id,
            target_date=target_date,
            twitch_live_stream_dir=self.twitch_live_stream_dir)
        return chat_df, viewer_df

    def anal_twitch_chat(self, chat_df, viewer_df, target_percentile):
        from lib.analysis.chat_count import start

        # 1초당 채팅을 바탕으로 한 하이라이트포인트(채팅빈도 다수 지역)
        result = start(chat_df, viewer_df, target_percentile=target_percentile)
        return result

    def anal_twitch_stream_start(self, viewer_df):
        from lib.analysis.stream_start_time import start
        start(viewer_df)


if __name__ == "__main__":
    onad = OnAd()
    # 데이터 적재
    # onad.get_data_twitch("TwitchChannelDetail")

    chat_df, viewer_df = onad.set_data_twitch_chat("beyou0728", "2018-12-05")
    onad.anal_twitch_stream_start(viewer_df)

    # 트위치 채팅편집점
    print(onad.anal_twitch_chat(chat_df, viewer_df, target_percentile=80))
