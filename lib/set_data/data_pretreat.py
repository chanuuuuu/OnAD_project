# 채팅 로그 파일 불러오는 함수

def open_twitch_chat(data, encoding) : 
    chat_text = open(data, encoding=encoding).readlines()
    return chat_text

# 채팅 로그 정규식으로 정규화 시키는 함수 ()
# group 0 전체
# group 1 시간
# group 2 ID
# group 3 채팅

def filter_twitch_chat(chat_text) : 
    import re
    
    text = chat_text
    cut_chat_log = re.compile('\[([0-9:]*)\] <(\S*[ ]*\S*)> (\S.*)')
    return cut_chat_log

# 정규식으로 그룹화 된 채팅로그에서 특정 그룹만을 리스트에 저장하여 반환 (0,1,2,3)
# group 0 전체
# group 1 시간
# group 2 ID
# group 3 채팅

def filter_twitch_chat(cut_chat_log, num) : 
    word_list = list()
    for line in text:
        mytext = my.search(line)
        if mytext :
            word_list.append(mytext.group(num))
    return word_list

# filter_twitch_chat의 리턴값을 공백으로 조인하는 함수
def filter_twitch_chat_join(word_list) : 
    word_list = word_list
    joined_word_list = ' '.join(word_list)
    return joined_word_list

