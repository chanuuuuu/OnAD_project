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
    youtube_channel_id_file = data_dir + "youtube_channels/youtube_channels.txt"
    log_dir = "batch/logs/"

   
    # 멤버변수 선언
    dao = None
    youtube_api_key = "AIzaSyCzerFuw3AJr6o29InSBHBW9Rfy5xzIyTY"

    # 멤버함수 선언
    def __init__(self):
        """db 초기화"""
        dao = DBManager.init(db_url, eval(DB_LOGFLAG))
        self.dao = dao
        DBManager.init_db()

    # 트위치 데이터 수집기
    def get_data_twitch(self, table_name,
        target_streamer="yapyap30", broad_date="2018-12-05"):
        """
        * input
         - table_name : twitch db의 테이블 명
         - target_streamer : 채팅 데이터를 가져 올 스트리머 이름
         - broad_date : 채팅 및 시청자 수 데이터를 가져 올 방송 날짜
        """
        from lib.get_data.twitch_api import get_twitch_stream
        from lib.get_data.twitch_api import get_twitch_game
        from lib.get_data.twitch_api import get_twitch_game_detail
        from lib.get_data.twitch_api import get_twitch_chat
        from lib.get_data.twitch_api import get_twitch_channel
        from lib.get_data.twitch_api import get_twitch_following
        from lib.get_data.twitch_api import get_twitch_clip
        from lib.contact_db.twitch import insert_information
        from lib.contact_db.twitch import select_groupby

        list_result = None

        # api 이용하여 데이터 받아오는 작업
        if table_name == "TwitchStream":
            print("api 요청 시도")
            list_result = get_twitch_stream.start()[0]  # (메타데이터, 세부데이터) 를 반환함
            print("데이터 준비 완료")

        if table_name == "TwitchStreamDetail":
            print("api 요청 시도")
            list_result = get_twitch_stream.start()[1]  # (메타데이터, 세부데이터) 를 반환함
            print("데이터 준비 완료")

        elif table_name == "TwitchGame":
            print("api 요청 시도")
            list_result = get_twitch_game.start()
            print("데이터 준비 완료")
        
        elif table_name == "TwitchGameDetail":
            print("api 요청 시도")
            list_result = get_twitch_game_detail.start()
            print("데이터 준비 완료")
        
        elif table_name == 'TwitchChat':
            print("폴더읽어오는 중")
            list_result = get_twitch_chat.start(target_streamer, broad_date)
            print("채팅 수 : %s" % len(list_result))
            print("데이터 준비 완료")

        elif table_name == 'TwitchChannel':
            from lib.contact_db.member import TwitchStream
            streamer_ids = select_groupby(self.dao,
                TwitchStream.streamer_id)
            print("api 요청 시도")
            list_result = get_twitch_channel.start(streamer_ids)[0] # 데이터 요청
            print("채널 데이터 준비 완료")

        elif table_name == 'TwitchChannelDetail':
            from lib.contact_db.member import TwitchStream
            streamer_ids = select_groupby(self.dao,
                TwitchStream.streamer_id)
            print("api 요청 시도")
            list_result = get_twitch_channel.start(streamer_ids)[1] # 데이터 요청
            print("채널 데이터 준비 완료")
        
        elif table_name == "TwitchFollowing":
            streamer_ids = select_groupby(self.dao,
                TwitchStream.streamer_id)
            print("api 요청 시도")
            list_result = get_twitch_following.start(streamer_ids)
            print("데이터 준비 완료")

        elif table_name == "TwitchClip":
            from lib.contact_db.member import TwitchChat
            from lib.contact_db.member import TwitchStream
            # 채팅로그를 모으는 스트리머만 가져오기
            streamer_names = select_groupby(self.dao,
                TwitchChat.streamer_name)
            # 스트리머 고유 id 가져오기
            streamer_ids = [ select_groupby(self.dao,
                    TwitchStream.streamer_id,
                    target_streamer=streamer)
                    for streamer in streamer_names]
            print("api 요청 시도")
            print("스트리머 수 : %s" % len(streamer_ids))
            list_result = get_twitch_clip.start(streamer_ids, \
                started_at=None, ended_at=None)
            print("클립 수 : %s" % len(list_result))
            print("데이터 준비 완료")
        
        # db 적재 작업
        if list_result:
            print("%s DB에 적재중" % table_name)
                # 스트리머 리스트를 group by 하여 가져오는 것을
                # 여기서 수행하여야 적게 함. 
            for i, data_dict in enumerate(list_result):
                insert_information(self.dao, table_name, data_dict)
                if (i+1) % 50 == 0:
                    print("%s/%s 인서트 완료" % (i + 1, len(list_result)))

        print("디비에 커밋 중")
        self.dao.commit()
        print("디비에 커밋 완료")
        self.dao.remove()
        print("완료")

    # 유튜브 데이터 수집기
    def get_data_youtube(self, table_name,
        api_key=youtube_api_key):
        from lib.get_data.youtube_api import get_youtube_channel
        from lib.get_data.youtube_api import get_youtube_channel_detail
        from lib.get_data.youtube_api import get_youtube_video
        from lib.get_data.youtube_api import get_youtube_reple
        from lib.get_data.youtube_api import get_youtube_subscription
        from lib.get_data.youtube_api import get_youtube_channel_ids
        from lib.contact_db.youtube import insert_information
        from lib.contact_db.youtube import select_information
        from lib.contact_db.youtube import select_groupby
        
        # 유튜브 채널id리스트 최신화 및 채널id리스트 로딩
        print("유튜브 채널리스트 로딩 중")
        get_youtube_channel_ids.start(self.youtube_api_key,
            self.youtube_channel_id_file)
        with open(self.youtube_channel_id_file, 'r') as fp:
            channel_list = fp.read().split('\n')
        print("유튜브 채널리스트 로딩 완료")

        if table_name == "YoutubeChannel":
            print("api 요청시작")
            list_result = get_youtube_channel.start(self.youtube_api_key, channel_list)
            print("데이터 준비 완료")

        elif table_name == "YoutubeChannelDetail":
            print("api 요청시작")
            list_result = get_youtube_channel_detail.start(self.youtube_api_key, channel_list)
            print("데이터 준비 완료")

        elif table_name == "YoutubeVideo":
            print("api 요청시작")
            list_result = get_youtube_video.start(self.youtube_api_key, channel_list)
            print("데이터 준비 완료")
        
        elif table_name == "YoutubeReple":
            from lib.contact_db.member import YoutubeVideo
            video_id_list = select_groupby(self.dao, YoutubeVideo.id)  # 라이브영상이 아닌 비디오 데이터만
            print("api 요청시작")
            list_result = get_youtube_reple.start(self.youtube_api_key, video_id_list)
            print("데이터 준비 완료")
        
        elif table_name == "YoutubeSubscription":
            from lib.contact_db.member import YoutubeVideo
            video_id_list = select_groupby(self.dao, YoutubeVideo.id)  # 라이브영상이 아닌 비디오 데이터만
            print("api 요청시작")
            list_result = get_youtube_subscription.start(self.youtube_api_key, video_id_list)
            print("데이터 준비 완료")
        
        print("DB에 적재중")
        for i, data_dict in enumerate(list_result):
            insert_information(self.dao, table_name, data_dict)
            print("%s/%s 인서트 완료" % (i + 1, len(list_result)))
        print("디비에 커밋 중")
        self.dao.commit()
        print("디비에 커밋 완료")
        self.dao.remove()
        print("완료")

    # 트위치 채팅 데이터 가져오기 (폴더에서)
    def set_twitch_chat_folder(self, target_id, target_date):
        """
        채팅 데이터와 스트리밍 데이터를 전처리하여 (chat_df, viewer_df)로 반환
        * input
          - target_id : 대상 스트리머 아이디, str
            "yapyap30"의 형태
          - target_date : 대상 방송 날짜, str
            "2018-12-10"의 형태
        * output
          - pd.DataFrame
        """
        from lib.set_data.twitch_preprocessing import load_chatting
        import pandas as pd

        # 채팅 데이터 로드
        chat_df = load_chatting(target_id=target_id,
            target_date=target_date,
            twitch_chat_dir=self.twitch_chat_dir)
        
        chat_df['streamtime'] = pd.to_datetime(chat_df['chat_time'])
        chat_df.set_index('streamtime', inplace=True)
        pivot_df = chat_df.pivot_table(index=chat_df.index, aggfunc=len, values='chatterer')
        pivot_df.columns = ['cnt_chat']  # 컬럼 이름 할당

        return pivot_df

    # 트위치 채팅데이터가 존재하는 날짜만 가져오기 (db에서)
    def get_existdays_chat_data(self, target_id):
        """
        target_id스트리머의 트위치 채팅 데이터베이스에서 중 존재하는 날짜만 반환
        target_id : 스트리머의 아이디 ex)yapyap30
        """
        from lib.contact_db.anal_data import select_exists_date
        return select_exists_date(self.dao, target_id)
    
    # 트위치 채팅 데이터 가져오기(db에서)
    def set_twitch_chat_db(self, streamer_id, target_date):
        from lib.contact_db.anal_data import select_twitch_chat
        from lib.contact_db.anal_data import select_stream_start_time
        from lib.contact_db.anal_data import select_streamer_id_by_name
        from lib.set_data.analset_preprocessing import set_low_dataset
        from lib.set_data.analset_preprocessing import set_anal_dataset

        # 채팅로그 데이터 로드
        chat_df = select_twitch_chat(db_url, streamer_id, target_date)
        print(chat_df)
        # 방송 시작 시간 데이터 로드
        start_time = select_stream_start_time(self.dao, db_url,
            streamer_id, target_date)

        # 방송 시작 시간을 기준으로 한 채팅로그 데이터로 전처리
        low_df = set_low_dataset(chat_df, start_time, target_date)

        # 시간별 채팅빈도, 특정단어 빈도를 가진 분석용 테이블 생성
        anal_df = set_anal_dataset(low_df)
        return anal_df

    # 트위치 채팅 빈도분석하여 편집점 반환
    def anal_twitch_chat(self, anal_df, target_percentile):
        from lib.analysis.chat_count import start
        # 1초당 채팅을 바탕으로 한 하이라이트포인트(채팅빈도 다수 지역)
        result = start(anal_df, target_percentile=target_percentile)
        return result

if __name__ == "__main__":
    import os
    import sys
    import datetime
    import time

    onad = OnAd()
    # 데이터 적재
    if len(sys.argv) == 1:
        print("OnAd is the only one platform which is connect a creator with corporation")
        print("we try to make better world.")
    else:  # 인자가 있는 경우
        # 트위치 데이터 가져오기
        if sys.argv[1] == "-twitchstream":
            """
            트위치 스트리밍 데이터 받아와 db에 적재
            매일 매분 - 짧은시간에 가능 ( 1 ~ 2초 )
            * twitchstreamdetail 과 함께 동작
            ** 중복되는 스트리머 있으면 안들어가게 예외처리
            """
            log_dir = onad.log_dir + "TwitchStream/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_twitch("TwitchStream")
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "TwitchStream" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "TwitchStream" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        elif sys.argv[1] == "-twitchstreamdetail":
            """
            트위치 스트리밍 세부 데이터 받아와 db에 적재
            매일 매분 - 짧은시간에 가능 ( 1 ~ 2초 )
            """
            log_dir = onad.log_dir + "TwitchStreamDetail/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_twitch("TwitchStreamDetail")
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "TwitchStreamDetail" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "TwitchStreamDetail" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        elif sys.argv[1] == "-twitchgame":
            """
            트위치 게임(번호, 이름) 데이터 받아와 db에 적재
            매주 한번 최신화
            * twitchgamedetail 과 함께 동작
            ** 중복되는 게임 있으면 안들어가게 예외처리
            """
            log_dir = onad.log_dir + "TwitchGame/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_twitch("TwitchGame")
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "TwitchGame" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "TwitchGame" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        elif sys.argv[1] == "-twitchgamedetail":
            """
            트위치 게임별 시청자수, 스트림 수 데이터 받아와 db에 적재
            매일 매분 - 짧은 시간에 가능
            """
            log_dir = onad.log_dir + "TwitchGameDetail/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_twitch("TwitchGameDetail")
                
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "TwitchGameDetail" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "TwitchGameDetail" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        elif sys.argv[1] == "-twitchchat":
            """
            채팅 데이터 폴더안의 모든 스트리머 폴더를 돌면서 채팅 데이터를 DB에 적재
            매일 한번돌림
            """
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            for dr in os.listdir(onad.twitch_chat_dir):
                streamer = dr.split("#")[1]  # 스트리머 이름
                exists_days = onad.get_existdays_chat_data(streamer)  # 존재하는 파일들의 날짜데이터
                
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
                    target_date = sorted(list(set(exists_days) - (set(exists_days) & set(db_existday))))
                    print("DB에 넣는 날짜: %s" % target_date[:-1])
                    # 파일에는 있고 디비에 없는 날짜 데이터
                    if target_date:
                        for i, day in enumerate(target_date[:-1]):
                            # 제일 최신의 날은 오늘 날짜로, 채팅로그를 쌓고 있기 떄문에 넣지 않음
                            onad.get_data_twitch("TwitchChat", streamer, day)
                            print("%s %s/%s %s작업 완료" % (streamer, i+1, len(target_date), day))
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
                log_dir = onad.log_dir + "TwitchChat/"
                if not os.path.exists(log_dir):
                    os.mkdir(log_dir)
                
                runtime = time.time() - stime
                with open(log_dir + "TwitchChat" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")

        elif sys.argv[1] == "-twitchchannel":
            """
            트위치 채널 메타데이터 (스트리머이름,로고,홈페이지) 받아와 db에 저장
            스트리머 id가 필요하므로 twitchstream 이후에 실행
            스트리머 하나하나를 다 돌아야 하므로 시간 소요됨
            * 하루 또는 일주일에 한번 (자주할 필요 없다)
            ** 있으면 넣지않음 / 바뀐다면 업데이트
            """
            log_dir = onad.log_dir + "TwitchChannel/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_twitch("TwitchChannel")
                
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "TwitchChannel" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "TwitchChannel" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        elif sys.argv[1] == "-twitchchanneldetail":
            """
            트위치 채널 세부데이터(팔로워수, 채널방문자수) 받아와 db에 저장
            스트리머 id가 필요하므로 twitchstream 이후에 실행
            스트리머 하나하나를 다 돌아야 하므로 시간 소요됨
            * 매일 한번
            ** 있는 데이터 다시 안들어가게
            """
            log_dir = onad.log_dir + "TwitchChannelDetail/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_twitch("TwitchChannelDetail")
                
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "TwitchChannelDetail" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "TwitchChannelDetail" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        elif sys.argv[1] == "-twitchclip":
            """
            클립데이터 받아와 db에 적재
            매일 한번, 방송 이후에가 적절한데.. 그냥 밤에 한번
            """
            log_dir = onad.log_dir + "TwitchClip/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_twitch("TwitchClip")
                
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "TwitchClip" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "TwitchClip" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        elif sys.argv[1] == "-twitchfollowing":
            """
            스트리머에 대한 팔로우 데이터를 가져와 db에 저장
            한 스트리머당 5분가량 소요/ 전체 스트리머를 돌리면 긴 시간이 필요
            ** 중복되는 행은 또 다시 들어가지 않도록 예외처리
            ** 중복되지 않는 경우만 다시 넣는다.
            일주일에 한번 / 한달에 한번
            """
            log_dir = onad.log_dir + "TwitchFollowing/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_twitch("TwitchFollowing")
                
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "TwitchFollowing" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "TwitchFollowing" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")
        
        # 유튜브 데이터 가져오기
        elif sys.argv[1] == "-youtubechannel":
            """
            유튜브 채널정보를 가져와 db에 저장
            ** 중복되는 행은 또 다시 들어가지 않도록 예외처리
            ** 중복되지 않는 경우만 다시 넣는다.(업데이트)
            일주일에 한번가량
            """
            log_dir = onad.log_dir + "YoutubeChannel/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_youtube("YoutubeChannel")
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "YoutubeChannel" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "YoutubeChannel" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")
            
        elif sys.argv[1] == "-youtubechanneldetail":
            """
            유튜브 채널 세부정보 가져와 db 저장
            하루 여러번 10분에 한번
            """
            log_dir = onad.log_dir + "YoutubeChannelDetail/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_youtube("YoutubeChannelDetail")
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "YoutubeChannelDetail" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "YoutubeChannelDetail" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")
        
        elif sys.argv[1] == "-youtubevideo":
            """
            유튜브 영상 데이터 받아와 디비에 적재
            오랜시간 걸림"""
            log_dir = onad.log_dir + "YoutubeVideo/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_youtube("YoutubeVideo")
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "YoutubeVideo" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "YoutubeVideo" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        elif sys.argv[1] == "-youtubechat":
            "차후 추가 예정"
        
        elif sys.argv[1] == "-youtubereple":
            """
            유튜브 영상리스트를 돌며 리플을 가져와 적재함
            오랜 시간동안 돌아가며, 과다한 요청
            """
            log_dir = onad.log_dir + "YoutubeChat/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_youtube("YoutubeChat")
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "YoutubeChat" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "YoutubeChat" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")
        
        elif sys.argv[1] == "-youtubesubscription":
            """
            유튜브 영상리스트를 돌며 리플 가져오고,
            그 리플아이디를 통해 그 사용자의 구독정보를 가져옴
            오랜 시간동안 돌아가며, 과다한 요청
            """
            log_dir = onad.log_dir + "YoutubeSubscription/"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            stime = time.time()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                onad.get_data_youtube("YoutubeSubscription")
                runtime = time.time() - stime
                print("소요시간 : %.4s" % (time.time() - stime))
                with open(log_dir + "YoutubeSubscription" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, "success"))
                    fp.write("\n")
            except Exception as e:
                with open(log_dir + "YoutubeSubscription" + date + ".txt", 'a') as fp:
                    fp.write("datetime:%s runtime:%s result:%s" % (nowtime, runtime, e))
                    fp.write("\n")

        # 분석
        elif sys.argv[1] == "-analysis":
            # python onad_runner.py -analysis yapyap30 2018-12-13
            if sys.argv[2]:
                streamer = sys.argv[2]
                if sys.argv[3]:
                    target_date = sys.argv[3]
                    print("분석 작업")
                    # 채팅로그, 시청자수 데이터 로드
                    chat_df, viewer_df = onad.set_twitch_chat_folder(streamer, target_date)
                    # 트위치 채팅편집점
                    print(onad.anal_twitch_chat(chat_df, target_percentile=60))
                else: print("타겟 날짜를 입력하세요")
            else: print("스트리머 이름 입력하세요")
        
        elif sys.argv[1] == "-analtwitch":
            if sys.argv[2]:
                streamer = sys.argv[2]
                if sys.argv[3]:
                    target_date = sys.argv[3]
                    print(onad.set_twitch_chat_db(streamer, target_date))



