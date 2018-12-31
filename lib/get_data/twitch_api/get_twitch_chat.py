def start(streamer_name, broad_date):
    """
    * input
    - streamer_name : 채팅내용을 db에 집어넣을 스트리머 아이디
    - broad_date : 채팅내용을 db에 집어넣을 방송 날짜
    """
    import re
    import os

    data_dir = "./data/"
    chat_dir = data_dir + "twitch_live_chat/"

    chat_file = "#%s/%s_#%s.log" % (streamer_name, broad_date, streamer_name)

    if not os.path.exists("#%s" % streamer_name):
        print("data 폴더에 %s 폴더가 없음" % streamer_name)
    else:
        with open(chat_dir + chat_file, 'r', encoding='utf-8') as fp:
            lines = fp.read().split('\n')
            
        ptn = re.compile(r'(\[\d{2}:\d{2}:\d{2}\]) <.+> .*')
        all_line = [i for i in lines if ptn.match(i)]

        # 시간 데이터만  line.split(" ")[0].replace("[", "").replace("]", "")
        # 채팅데이터만 line.split('> ')[1]
        # 아이디 데이터만 re.search(r'(<.+>)', line).group(0)
        inform = [
            {
                "chatterer": re.search(r'(<.+>)', line).group(0),
                "chat_time": line.split(" ")[0].replace("[", "").replace("]", ""),
                "chat_contents": line.split('> ')[1]
            } for line in all_line
                ]

        return inform