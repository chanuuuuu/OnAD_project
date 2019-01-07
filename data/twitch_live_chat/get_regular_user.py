
def week_user_check (date, streamer_id, count=5):
    '''
    date(str) : 'YYYY-MM-DD' 형태로 입력
    streamer(str) : 스트리머 ID를 정확하게 입력 (닉네임x)
    count(int) : date를 기준으로 일주일(7일) 안에 몇 명이 며칠(count)을 들어와서 채팅을 쳤는지 알려주는 수
                defalut = 5, 1 < count < 7
            (ex) 일주일 중에 5일 안에 채팅친 사람을 알고 싶다 = count에 '5'를 입력
            
    return => 일주일 동안 채팅을 친 사람 수(target_user, int), 일주일 간 count일 동안 꾸준히 들어와 채팅을 친 사람 수(big_fan, int)
    '''
    
    
    import re
    from datetime import datetime as dt
    from datetime import timedelta
    
    if not 0 < count < 8:
        return print("count는 1에서 7까지의 값만 입력이 가능합니다.")
    
    target_user = []
    big_fan = []
    
    for days in range(7):
        
        with open('./#{}/{}_#{}.log'.format(streamer_id, date, streamer_id),'r',encoding='utf-8') as f:
            chat_user = list({log.replace("\n"," ")[12:].split(">")[0].replace("<"," ") for log in f.readlines()[1:]})

        id_form = re.compile("[a-zA-Z0-9_+]{4,26}")
        
        for user in chat_user:
            
            if re.search(id_form,user):
                target_user.append(re.search(id_form, user).group())
                
        date = dt.strptime(date,"%Y-%m-%d" )
        date = (date - timedelta(1)).strftime("%Y-%m-%d")
        
    
    for user in target_user:
        if target_user.count(user) > count:
            big_fan.append(user)
            

    
    return len(target_user), len(big_fan)
    