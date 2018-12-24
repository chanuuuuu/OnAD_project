"""
데이터베이스 시작파일
시작시 
테이블 생성함"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBManager():
    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag=None):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag)
        DBManager.__session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=DBManager.__engine
        ))
        global dao
        
        dao = DBManager.__session

    @staticmethod
    def init_db():
        from lib.contact_db.member import Base
        Base.metadata.create_all(bind=DBManager.__engine)

dao = None

DB_URL = 'onad.cbjjamtlar2t.ap-northeast-2.rds.amazonaws.com'
DB_USER = 'onad'
DB_PASSWORD = 'rkdghktn12'
DB_DATABASE = 'onad'
DB_CHARSET = 'utf8mb4'
DB_LOGFLAG  = 'True'
DB_PORT = 3306

db_url = "mysql+pymysql://%s:%s@%s:%s/%s?charset=%s" % (
    DB_USER, DB_PASSWORD,
    DB_URL, DB_PORT,
    DB_DATABASE, DB_CHARSET
)

if __name__ == "__main__":
    DBManager.init(db_url, eval(DB_LOGFLAG))
    DBManager.init_db()
    print('완료')