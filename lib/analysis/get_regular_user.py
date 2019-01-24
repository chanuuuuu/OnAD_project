def start (date, streamer_id, period=6, visit=5):
    '''
    > 함수 인자 설명
        - date(str) : 'YYYY-MM-DD' 형태로 입력. 
        - streamer(str) : 스트리머 ID를 정확하게 입력 (닉네임X)
        - period : date를 기준으로 period일 전부터 date까지 몇 명이 방송에 들어와 채팅을 쳤는지를 알아볼 변수. 일 단위로 입력 (defalut = 6)
        !! 주의 !!  date도 전체 기간에 포함되므로, 일주일의 정보를 알고 싶다면 'period=6'으로 설정할 것.``
        - visit(int) : date를 기준으로 period일 전부터 몇 명이 'visit일'  이상을 방송에 들어와 채팅을 쳤는지를 알아볼 변수. 일 단위로 입력 (defalut = 5)
        ``(ex) 2018년 12월 26일을 기준으로 일주일 동안 5일 이상 방송에서 채팅을 친 사람의 수를 알고 싶다면?
            -> start ("2018-12-31", streamer, period=6, visit=5)`` 

        
     !! 주의 !! date를 기준으로 period 값에 해당하는 채팅 데이터가 없을 시 결과값이 정확하지 않을 수 있음.
                
    >  return : [int, int, [str]]
    -  설정한 기간 안에 채팅을 친 모든 사람의 수(target_user, int)
    - 설정한 기간 안에 visit만큼 채팅을 친 사람 수(big_fan, int)
    -  채팅 데이터가 없는 일자의 로그 이름(list, str) : 빈칸일 경우 정상.
    '''
    
    import re
    from datetime import datetime as dt
    from datetime import timedelta
    import os
    
    
    txt_dir = "../../data/twitch_live_chat"
    target_user = []
    file_not_exist = []
    big_fan = []
    count = 0
    
    while count < period:
        if '{}_#{}.log'.format(date, streamer_id) not in os.listdir(txt_dir + '/#{}'.format(streamer_id)):
            print("!!주의!! {}의 {}일자 채팅로그 데이터가 없어서 건너뜁니다. 결과가 정확하지 않을 수 있습니다.".format(streamer_id,date))
            date = dt.strptime(date,"%Y-%m-%d" )
            date = (date - timedelta(1)).strftime("%Y-%m-%d")
            
            file_not_exist.append('{}_#{}.log'.format(date,streamer_id))
            count += 1
            
            continue
        

        with open(txt_dir + '/#{}/{}_#{}.log'.format(streamer_id, date, streamer_id),'r',encoding='utf-8') as f:
            chat_user = list({log.replace("\n"," ")[12:].split(">")[0].replace("<"," ") for log in f.readlines()[1:]})

        id_form = re.compile("[a-zA-Z0-9_+]{4,26}")

        for user in chat_user:
            if re.search(id_form,user):
                target_user.append(re.search(id_form, user).group())

        date = dt.strptime(date,"%Y-%m-%d")
        date = (date - timedelta(1)).strftime("%Y-%m-%d")
        count += 1
        
    for user in target_user:
        if target_user.count(user) == visit:
            big_fan.append(user)

    return [len(target_user), len(big_fan), file_not_exist]