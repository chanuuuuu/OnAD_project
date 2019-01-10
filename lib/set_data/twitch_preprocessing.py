# 데이터 로드
def load_chatting(target_id='yapyap30', target_date='2018-12-10',
    twitch_chat_dir="./data/twitch_live_chat/"):
    """
    채팅로그 읽어오기
    - input : 
        *target_id => 채팅로그를 읽을 스트리머 이름, str
            ex) "yapyap30"
        *target_date => 채팅로그를 읽을 날짜, str
            ex) "2018-12-10"
    - output : 채팅로그 데이터프레임
        columns - 채팅로그
        index - 채팅시간
    """
    import re
    import pandas as pd
    
    chat_file = "#%s\\%s_#%s.log" % (target_id, target_date, target_id)
    # "#yapyap30\\2018-12-10_#yapyap30.log"
    print(chat_file)

    # 채팅로그 로딩
    with open(twitch_chat_dir + chat_file, 'r', encoding='utf-8') as fp:
        lines = fp.read().split("\n")
    
    # 채팅로그만 찾기
    ptn = re.compile(r'(\[.+\d{2}:\d{2}:\d{2}\]) <.+> .*')
    only_chat_lie = [i for i in lines if ptn.match(i)]
    
    # 시간 데이터만
    times = [ re.search(r'\[.+\]', line).group(0).replace("[", "").replace("]", "")
        for line in only_chat_lie ]

    # 채팅데이터만
    chattings = [line.split('> ')[1] for line in only_chat_lie]
    df = pd.DataFrame(index=times, data=chattings, columns=['chatting'])
    df['chat_time'] = df.index
    return df

def get_exists_days(target_id='yapyap30', 
    twitch_live_stream_dir="./data/twitch_chat/"):
    """
    data/twitch_chat 폴더안의 날짜들만을 반환하는 함수
    - input:
        target_id : 타겟 스트리머 아이디  
        twitch_live_stream_dir : 스트리머별 채팅 데이터 폴더

    - output:
        폴더안의 날짜들 list
    """
    import re
    import os

    target_dir = twitch_live_stream_dir + "#" + target_id
    
    return [file.split("_")[0] for file in  os.listdir(target_dir)]