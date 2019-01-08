def startt (date, streamer_id, period=7, visit=5):
    '''
    date(str) : 'YYYY-MM-DD' 형태로 입력
    streamer(str) : 스트리머 ID를 정확하게 입력 (닉네임X)
    period : date를 기준으로 period 동안에 몇 명이 방송에 들어와 채팅을 쳤는지를 알아볼 변수. 일 단위로 입력 (defalut = 7) 
    visit(int) : date를 기준으로 period 동안에 몇 명이 'count일'을 방송에 들어와 채팅을 쳤는지를 알아볼 변수. 일 단위로 입력
                (defalut = 5)
    
    (ex) 2018년 12월 26일을 기준으로 일주일 동안 5일 이상 방송에 들어와 채팅을 친 사람의 수를 알고 싶다면?
     -> start ("2018-12-31", streamer, period=7, visit=5)
     
     !! 주의 !! date를 기준으로 period 값에 해당하는 채팅 데이터가 없을 시 결과값을 리턴하지 않음
            
    return => [일주일 동안 채팅을 친 사람 수(target_user, int), 
              일주일 간 count일 동안 꾸준히 들어와 채팅을 친 사람 수(big_fan, int)]
    '''
    
    import re
    from datetime import datetime as dt
    from datetime import timedelta


    txt_dir = "../../data/twitch_live_chat"
    target_user = []
    big_fan = []
    count = 0
    try:
        while count < period:
            
            with open(txt_dir + '/#{}/{}_#{}.log'.format(streamer_id, date, streamer_id),'r',encoding='utf-8') as f:
                chat_user = list({log.replace("\n"," ")[12:].split(">")[0].replace("<"," ") for log in f.readlines()[1:]})
            
            id_form = re.compile("[a-zA-Z0-9_+]{4,26}")
            
            for user in chat_user:
                if re.search(id_form,user):
                    target_user.append(re.search(id_form, user).group())
                    
            date = dt.strptime(date,"%Y-%m-%d" )
            date = (date - timedelta(1)).strftime("%Y-%m-%d")
    
            count += 1
            
        for user in target_user:
            if target_user.count(user) >= visit:
                big_fan.append(user)

    except FileNotFoundError:
        return print("{}의 {}일자 이전의 채팅로그 파일이 없습니다".format(streamer_id, date))
    

    return [len(target_user), len(big_fan)]
