import time
from bs4 import BeautifulSoup
import requests

def get_youtube_chatlog(video_id, streamer):
    '''
    video_id(str) : 라이브 동영상 고유 ID  <!!주의!!> video_id에 일반 동영상 ID를 넣을 경우 아무것도 저장하지 않습니다.
    streamer(str) : 채팅 로그를 txt로 저장할 때 스트리머 이름과 날짜가 제목에 오게 됩니다. 
                    따라서 stramer에 유튜브 스트리머 이름이나 채널 이름을 넣어주세요.

    !!참고!! 이 함수의 retrun값은 없습니다. 다만 video_id에 따라 라이브 동영상의 채팅로그가 
    txt 파일로 저장됩니다. (ex) 대도서관-YYYYMMDD.txt 
    '''
    print("{}의 채팅로그를 불러옵니다.".format(streamer))
    from bs4 import BeautifulSoup
    import requests

    target_url = "https://www.youtube.com/watch?v=" + video_id
    dict_str = "" 
    chat_log = []
    session = requests.Session ()
    headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }
    times = ""
    chat_log.append(streamer)
    
    html = requests.get (target_url)
    soup = BeautifulSoup (html.text, "html.parser" )
    if soup.find('strong', 'watch-time-text') == None:
        print("비공개 동영상 입니다.")

    else:
        tmp_times = soup.find('strong', 'watch-time-text').text.split(":")[1][1:].split(".")[:3]
        for part in tmp_times:
            if len(part) == 2:
                part = "0" + part.strip(" ")
            times += part.strip(" ")
 
    for iframe in soup.find_all ( "iframe" ) :
         if "live_chat_replay"  in iframe [ "src" ] :
            next_url = iframe [ "src" ]
    while True :
        try :
            html = session.get (next_url, headers = headers)
            soup = BeautifulSoup (html.text, "lxml" )
            for scrp in soup.find_all ( "script" ) :
                 if  'window[\"ytInitialData\"]' in scrp.text :
                    dict_str = scrp.text.split ( "] = " )[1]

            dict_str = dict_str.replace ( "false" , "False" )
            dict_str = dict_str.replace ( "true" , "True" ) 
            dict_str = dict_str.rstrip ( "  \n ;" )
            dics = eval (dict_str)
            continue_url =  dics [ "continuationContents" ] [ "liveChatContinuation" ] [ "continuations" ] [ 0 ] [ "liveChatReplayContinuationData" ] [ "continuation" ]
            next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url
            for samp in dics [ "continuationContents" ] [ "liveChatContinuation" ] [ "actions" ] [ 1 :] :
                tmp = samp ["replayChatItemAction" ] [ "actions" ] [ 0 ] [ "addChatItemAction" ] [ "item" ] [ "liveChatTextMessageRenderer" ]
                chat_log.append([[str(tmp [ "timestampText" ] [ "simpleText"]),str(tmp['authorName']["simpleText"]),str( tmp[ "message" ] [ "simpleText" ])]])
        
        except Exception as e:
            if len(str(e)) == 29:
                print("현재까지 {}개의 채팅로그를 가져왔습니다.".format(len(chat_log)))
                continue
            elif len(str(e)) == 32:
                print("{}의 채팅로그를 모두 받았읍니다.".format(streamer))
                break
            elif len(str(e)) == 62:
                print("{} 에서 불러올 채팅로그가 없거나 해당 동영상이 비공개입니다.".format(video_id))
                break
     

    if len(chat_log) == 1:
        print("저장할 채팅로그가 없습니다.")
    else:
        print("*"*50)
        users = []
        for i in range(1,len(chat_log)):
            users.append(chat_log[i][0][1])
        with open("{}-{}.txt".format(streamer,times), mode='w', encoding="utf-8") as f:
            f.write("방송 제목 : " + chat_log[0] + "\n")
            f.write("전체 시청자 수 : {} / 전체 채팅 수 : {}".format(len(set(users)),len(chat_log[1:])) + "\n" )
            comment = [x[0] for x in chat_log[1:]]
            for i in chat_log:
                f.write("[" + i[0] + "]" + " " + "<" + i[1] + ">" + " " + i[2] + '\n')



