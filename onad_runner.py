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

    def get_data_twitch_stream(self):
        # api 통해 데이터받아오기
        from lib.get_data.twitch_api import get_twitch_stream
        list_result = get_twitch_stream.start()

        # 데이터를 db에 적재
        from lib.contact_db.twitch import insert_information
        for data_dict in list_result:
            print(data_dict)
            print(type(data_dict))
            result = insert_information(self.dao, "twitch_stream", data_dict)
            if result : print("DB적재 완료")
            else: print("DB적재 미완료")
    
    def get_data_twitch_game(self):
        from lib.get_data.twitch_api import get_twitch_game
        get_twitch_game.start()


if __name__ == "__main__":
    onad = OnAd()
    onad.get_data_twitch_game()
