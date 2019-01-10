# 분석용 데이터셋을 만들기 위한 전처리 모듈

def set_low_dataset(df, start_time, target_date):
    """
    채팅데이터와 시작시간을 기준으로 시작시간을 00:00:00으로 하여 시작하는
    데이터프레임을 반환해주는 함수
    * input
        df = 데이터베이스에서 꺼내 온 채팅데이터 원본, pd.DataFrame
        start_time = 데이터베이스에서 꺼내 온 스트리밍 시작시간, str
    * output
        pd.DataFrame
    """
    import pandas as pd
    start_time = pd.to_datetime(target_date + " " + start_time)

    df['streamtime'] = df['chat_time'].apply(lambda x : target_date + " " + x)
    df['streamtime'] = pd.to_datetime(df['streamtime'])
    df['streamtime'] = df['streamtime'].apply(lambda x : x - start_time)
    df.set_index('streamtime', inplace=True)

    # 시작 시간부터의 채팅로그 데이터 프레임
    df = df[df.index > "00:00:00"]

    # 필요없는 행 삭제
    del df['chat_id']
    del df['streamer_name']

    return df

def set_anal_dataset(low_df, word_list=None):
    """
    채팅로그 low data 를 분석용 데이터셋으로 변환하여 반환하는 함수
    """
    # ** 생각할 거리 **
    # 흥미 반응 카테고리 단어 (긍정반응)
    # 부정 반응 카테고리 단어 (부정반응)
    # 플래그 반응('유하', '유튜브하이' 등) 카테고리 단어
    # 스트리머 별 특정단어 (ex_공혁준->혁준아, 얍얍->얍마이무, 등) ?

    # 기본적인 채팅빈도 피봇 테이블 생성
    pivot_df = low_df.pivot_table(index=low_df.index, aggfunc=len, values='chatterer')
    pivot_df.columns = ['cnt_chat']  # 컬럼 이름 할당

    # 채팅당 특정 단어수 체크하여 변수로 할당
    if word_list:  # 단어리스트를 인자로 넣은 경우 해당 리스트 단어들의 빈도컬럼을 생성
        for word in word_list:
            low_df["cnt_" + word] = low_df.chat_contents.apply(lambda x : x.count(word_list.get(word)))
        
        for col in low_df:  # 시간을 인덱스로 가지고, 단어리스트의 단어들의 빈도를 컬럼으로 하는 테이블 생성
            pivot_df[col] = low_df.pivot_table(index = low_df.index,
                aggfunc=sum, values=col)[col]

    else:  # word_list를 인자로 넣지 않은 경우
        # 기본적인 단어들의 빈도 컬럼을 생성
        low_df['cnt_ㅋ'] = low_df.chat_contents.apply(lambda x : x.count("ㅋ"))
        low_df['cnt_ㄵ'] = low_df.chat_contents.apply(lambda x : x.count("ㄵ"))
        low_df['cnt_ㄴㅈ'] = low_df.chat_contents.apply(lambda x : x.count("ㄴㅈ"))
        low_df['cnt_오'] = low_df.chat_contents.apply(lambda x : x.count("오"))
        low_df['cnt_와'] = low_df.chat_contents.apply(lambda x : x.count("와"))
        low_df['cnt_유하'] = low_df.chat_contents.apply(lambda x : x.count("유하"))
    
        # 시간당 피봇 테이블에 특정 단어의 빈도를 컬럼으로 하는 피봇 테이블 생성
        pivot_df["cnt_ㅋ"] = low_df.pivot_table(index = low_df.index, aggfunc=sum, values='cnt_ㅋ')['cnt_ㅋ']
        pivot_df["cnt_ㄵ"] = low_df.pivot_table(index = low_df.index, aggfunc=sum, values='cnt_ㄵ')['cnt_ㄵ'] +\
                            low_df.pivot_table(index = low_df.index, aggfunc=sum, values='cnt_ㄴㅈ')['cnt_ㄴㅈ']
        pivot_df["cnt_오"] = low_df.pivot_table(index = low_df.index, aggfunc=sum, values='cnt_오')['cnt_오']
        pivot_df["cnt_와"] = low_df.pivot_table(index = low_df.index, aggfunc=sum, values='cnt_와')['cnt_와']
        pivot_df["cnt_유하"] = low_df.pivot_table(index = low_df.index, aggfunc=sum, values='cnt_유하')['cnt_유하']

    return pivot_df