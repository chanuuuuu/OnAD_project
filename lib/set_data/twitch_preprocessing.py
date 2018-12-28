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

    # 채팅로그 로딩
    with open(twitch_chat_dir + chat_file, 'r', encoding='utf-8') as fp:
        lines = fp.read().split("\n")
    
    # 채팅로그만 찾기
    ptn = re.compile(r'(\[\d{2}:\d{2}:\d{2}\]) <.+> .*')
    only_chat_lie = [i for i in lines if ptn.match(i)]
    
    # 시간 데이터만
    times = [line.split(" ")[0].replace("[", "").replace("]", "") for line in only_chat_lie]

    # 채팅데이터만
    chattings = [line.split('> ')[1] for line in only_chat_lie]
    df = pd.DataFrame(index=times, data=chattings, columns=['chatting'])
    df['hour'] = [i[:2] for i in df.index]

    return df

def load_viewer_count(target_id='yapyap30', target_date="2018-12-10",
    twitch_live_stream_dir="./data/twitch_live_stream/"):
        """
        분단위 시청자수
        - input:
            target_id : 타겟 스트리머 아이디  
            target_date : 타겟 날짜
            twitch_live_stream_dir : 라이브스트리밍 데이터 폴더

        - output: pd.DataFrame
            target_id로 지정한 스트리머의 viewer_count 데이터프레임
            columns : [name, id, viewer]
            index : streaming_time
        """
        import re
        import pandas as pd
        import os

        # 분당 스트리밍 중인 스트리머, 시청자수 파일 불러오기
        ptn = re.compile(r'live_stream_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}.txt')

        # 위 패턴에 맞는(live_stream txt 데이터만)
        viewer_count_files = [file for file in os.listdir(twitch_live_stream_dir) if ptn.match(file)]
        
        viewer_count_files = [ file for file in viewer_count_files if target_date in str(file)]

        # {0000 : [스트리머 리스트]} 와 같이 dict로 생성
        viewer_count_dict = {}
        for viewer_count_file in viewer_count_files:
            # 파일 하나하나 읽어 {시간: [스트리머 리스트] } 의 형태로 만듦
            with open(twitch_live_stream_dir + viewer_count_file, 'r', encoding='utf-8') as fp:
                viewer_count_datasets = fp.read().split('\n')

            time = viewer_count_file[12:-4]
            # 딕셔너리 형태로
            viewer_count_dataset = [data for data in viewer_count_datasets if target_id in str(data)]
            viewer_count_dict[time] = viewer_count_dataset
        
        # 생성된 dict 를 바탕으로 DataFrame 생성
        view_df_list = []
        for i, v in viewer_count_dict.items():
            df1 = pd.DataFrame([v1.split()[:3] for v1 in v])
            df1['streaming_time'] = i
            view_df_list.append(df1)

        # 리스트 안에 들어가있는 여러 데이터프레임들을 하나의 데이터 프레임으로
        view_df = pd.concat(view_df_list, sort=False)

        # 데이터 프레임 컬럼명
        col = ['name', 'id', 'viewer', 'streaming_time']
        view_df.columns = col
        
        # streaming_time 을 인덱스로 설정
        view_df = view_df.set_index('streaming_time')

        # 날짜, 시간, 분 컬럼 추가
        view_df['date'] = list(pd.Series(view_df.index).apply(lambda x : x[:-6]))
        view_df['hour'] = list(pd.Series(view_df.index).apply(lambda x : x[-5:-3]))
        view_df['minute'] = list(pd.Series(view_df.index).apply(lambda x : x[-2:]))

        return view_df