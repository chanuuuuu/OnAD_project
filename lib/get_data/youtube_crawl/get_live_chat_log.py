import time
from bs4 import BeautifulSoup
import requests

def get_youtube_chatlog(video_id, channel_name):
    '''
    video_id(str) : 라이브 동영상 고유 ID  <!!주의!!> video_id에 일반 동영상 ID를 넣을 경우 아무것도 저장하지 않습니다.
    channel_name(str) : 채팅 로그를 txt로 저장할 때 스트리머 이름과 날짜가 제목에 오게 됩니다. 
                    따라서 stramer에 유튜브 스트리머 이름이나 채널 이름을 넣어주세요.

    !!참고!! 이 함수의 retrun값은 없습니다. 다만 video_id에 따라 라이브 동영상의 채팅로그가 
    txt 파일로 저장됩니다. (ex) 대도서관-YYYYMMDD.txt 
    '''
    print("{}의 채팅로그를 불러옵니다.".format(channel_name))
    
    from bs4 import BeautifulSoup
    import requests
    from datetime import datetime as dt

    target_url = "https://www.youtube.com/watch?v=" + video_id
    dict_str = ""     
    session = requests.Session ()
    headers ={ 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' }
    
    chat_log = []
    info = {}
    
    html = requests.get (target_url)
    soup = BeautifulSoup (html.text, "html.parser" )
    if soup.find('strong', 'watch-time-text') == None:
        print("비공개 동영상 입니다.")

    else:
        tmp_times = soup.find('strong', 'watch-time-text').text[14:-1].replace(".","-").replace(" ","")
        times = dt.strptime(tmp_times, "%Y-%m-%d").strftime("%Y-%m-%d")
        
         
            
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

            dict_str = dict_str.replace ( "false" , "False" ).replace ( "true" , "True" ).rstrip ( "  \n ;" )
            
            dics = eval (dict_str)
            continue_url =  dics [ "continuationContents" ] [ "liveChatContinuation" ] [ "continuations" ] [ 0 ] [ "liveChatReplayContinuationData" ] [ "continuation" ]
            next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url
            
            for samp in dics [ "continuationContents" ] [ "liveChatContinuation" ] [ "actions" ] [ 1 :] :
                
                tmp = samp ["replayChatItemAction" ] [ "actions" ] [ 0 ] [ "addChatItemAction" ] [ "item" ] [ "liveChatTextMessageRenderer" ]
                info["video_id"] = video_id
                info["video_pulished_at"] = times
                info["nickname"] = str(tmp['authorName']["simpleText"])
                info["timestamp"] = str(tmp [ "timestampText" ] [ "simpleText"])
                info["content"] = str(tmp[ "message" ] [ "simpleText" ])
                
                
                chat_log.append(info)
                
                info = {}
                
        except Exception as e:
            if len(str(e)) == 29:
                print("채팅로그를 받고 있습니다.")
                continue
            elif len(str(e)) == 32:
                print("{}의 채팅로그를 모두 받았읍니다.".format(channel_name))
                break
            elif len(str(e)) == 62:
                print("{} 에서 불러올 채팅로그가 없거나 해당 동영상이 비공개입니다.".format(video_id))
                break

    if len(info) == 0:
        return print("저장할 채팅로그가 없습니다.")
    else:
        return chat_log
        


