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
        from lib.contact_db.twitch import insert_information
        
        # api 이용하여 데이터 받아오는 작업
        if table_name == "twitch_stream":
            list_result = get_twitch_stream.start()
            print("데이터 준비 완료")

        if table_name == "twitch_stream_detail":
            list_result = get_twitch_stream_detail.start()
            print("데이터 준비 완료")
        
        elif table_name == "twitch_game":
            list_result = get_twitch_game.start()
            print("데이터 준비 완료")
        
        elif table_name == "twitch_game_detail":
            list_result = get_twitch_game_detail.start()
            print("데이터 준비 완료")
        
        elif table_name == 'twitch_chat':
            list_result = get_twitch_chat.start()
            print("데이터 준비 완료")

        elif table_name == 'get_twitch_channel':
            list_result = get_twitch_channel.start()
            print("데이터 준비 완료")

        elif table_name == 'get_twitch_channel_detail':
            list_result = get_twitch_channel_detail.start()
            print("데이터 준비 완료")

        # db 적재 작업
        print("DB에 적재중")
        for data_dict in list_result:
            insert_information(self.dao, table_name, data_dict)

        self.dao.commit()
        self.dao.remove()
        print("완료")


if __name__ == "__main__":
    onad = OnAd()
    onad.get_data_twitch("twitch_stream_detail")
