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

    def get_data_twitch(self, table_name,
        target_streamer="yapyap30", broad_date="2018-12-05"):
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
            list_result = get_twitch_chat.start(target_streamer, broad_date)
            print("채팅 수 : %s" % len(list_result))
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

    def set_existdays_chat_data(self, target_id):
        """
        target_id스트리머의 트위치 채팅 폴더의 파일들 중 존재하는 날짜만 반환
        target_id : 스트리머의 아이디 ex)yapyap30"""
        from lib.set_data.twitch_preprocessing import get_exists_days
        return get_exists_days(target_id, self.twitch_chat_dir)

    def anal_twitch_chat(self, chat_df, viewer_df, target_percentile):
        from lib.analysis.chat_count import start

        # 1초당 채팅을 바탕으로 한 하이라이트포인트(채팅빈도 다수 지역)
        result = start(chat_df, viewer_df, target_percentile=target_percentile)
        return result

    def anal_twitch_stream_start(self, viewer_df):
        from lib.analysis.stream_start_time import start
        start(viewer_df)


if __name__ == "__main__":
    import os
    import sys
    onad = OnAd()

    # 데이터 적재
    if sys.argv == "-twitch -chat":
        # 채팅 데이터 폴더안의 모든 스트리머 폴더를 돌면서 채팅 데이터를 DB에 적재
        for dr in os.listdir(onad.twitch_chat_dir):
            streamer = dr.split("#")[1]  # 스트리머 이름
            exists_days = onad.set_existdays_chat_data(streamer)  # 존재하는 파일들의 날짜데이터
            
            # 스트리머별 이미 적재된 날짜 모으기
            from lib.contact_db.member import TwitchChat
            from lib.contact_db.twitch import select_groupby
            db_existday = select_groupby(onad.dao, TwitchChat.broad_date,
                target_streamer=streamer)
            # 튜플안에 있는 항목을 밖으로 빼 튜플 제거 [(1,), (2,), ..]
            db_existday = [i[0] for i in db_existday]  
            
            # 예외 처리 시작
            print("스트리머 이름: %s" % streamer)
            print("파일이 존재하는 최신 날짜 %s" % exists_days[-1])
            if db_existday:
                print("디비에 존재하는 최신 날짜 %s이므로 바로 다음 날부터 적재" % db_existday[-1])
                
                # 채팅로그 파일이 디비에 덜 적재된 경우로
                # 디비에 존재하는 최신날짜 다음날 부터 다시 디비에 적재
                target_date = set(exists_days) - (set(exists_days) & set(db_existday))
                # 파일에는 있고 디비에 없는 날짜 데이터
                if target_date:
                    for i, days in enumerate(target_date):
                        onad.get_data_twitch("TwitchChat", streamer, days)
                        print("%s %s/%s 완료" % (streamer, i+1, len(target_date)))
                else:
                    # 디비에 모든 파일 적재된 경우
                    print("모든 파일 디비에 적재 완료되었으므로 다음으로 넘어감")
                    continue
            else:
                print("디비에 파일 없으므로 처음부터 적재시작")
                # 디비에 하나도 적재되지 않은 경우로 파일이 존재하는 첫날 부터 디비에 적재
                for i, days in enumerate(exists_days):
                        onad.get_data_twitch("TwitchChat", streamer, days)
                        print("%s %s/%s 완료" % (streamer, i+1, len(exists_days)))


        
            
    
    # # 채팅로그, 시청자수 데이터 로드
    # chat_df, viewer_df = onad.set_data_twitch_chat("beyou0728", "2018-12-05")
    # 트위치 스트리밍 시작시간을 찾아 보여주는 함수
    # onad.anal_twitch_stream_start(viewer_df)

    # # 트위치 채팅편집점
    # print(onad.anal_twitch_chat(chat_df, viewer_df, target_percentile=80))
