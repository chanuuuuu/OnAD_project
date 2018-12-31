# 채팅 로그 파일 불러오는 함수
# data = 파일경로, encoding = 인코딩 (보통 utf-8)
def open_twitch_chat(data, encoding) : 
    chat_text = open(data, encoding=encoding).readlines()
    return chat_text

# 채팅 로그 정규식으로 정규화 시키는 함수 ()
# group 0 전체
# group 1 시간
# group 2 ID
# group 3 채팅
# chat_text는 open_twich_chat 함수의 리턴값
#  chat_text = open_twitch_chat의 리턴값, num = 원하는 그룹 num
def filter_twitch_chat(chat_text, num) : 
    import re
    text = chat_text
    my = re.compile('\[([0-9:]*)\] <(\S*[ ]*\S*)> (\S.*)')
    word_list = list()
    for line in text:
        mytext = my.search(line)
        if mytext :
            word_list.append(mytext.group(num))
    return word_list

# filter_twitch_chat의 리턴값을 공백으로 조인하는 함수
# word_list = filter_twitch_chat 함수의 리턴값
def filter_twitch_chat_join(word_list) : 
    word_list = word_list
    joined_word_list = ' '.join(word_list)
    return joined_word_list
