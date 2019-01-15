from komoran3py import KomoranPy
ko = KomoranPy()

# 사용자 사전 경로 지정
def Komoran3py(userdict)  : 
    """
    사용자 사전 경로
    """
    ko.set_user_dictionary(userdict)

# 채팅로그 불러오는 함수 
def Openlog(chatlog) : 
    """
    인자값 : 채팅로그 경로
    """
    with open(chatlog) as f : 
        chat = f.readlines()
    return chat

# Openlog or 직접 불러온 채팅 로그 넣으면 정규식으로 id, 날짜, 채팅 내용 구분해줌
def prepro_chat(chat, num) : 
    """ 
        num에는 그룹 선택
        0 = 전체, 1 = 시간(방송기준) 2 = ID 3 = 채팅
    """
    import re
    my = re.compile('\[([0-9:]*)\] <(\S*[ ]*\S*)> (\w.*)')
    word_list = []
    for line in text:
        mytext = my.search(line)
        if mytext :
            word_list.append(mytext.group(num))
    return word_list

# 전처리 된 채팅 로그 넣으면 형태소 분석 돌려서 형태소 리스트로 반환
def tokenize(word_list) :
    """ 
        전처리된 리스트
        prepro_chat함수의 리턴값 넣기
    """
    tokens_ko = []
    for wd in word_list : 
        for i in range(len(ko.pos(wd))) : 
            tokens_ko.append(ko.pos(wd)[i][0])
    return tokens_ko

# 형태소 리스트 넣으면 빈도분석 가능한 형태 전환 시킴
def nltk_text(tokens_ko) : 
    """
        tokenize 함수 리턴값 
    """
    tokens_ko_nltk = nltk.Text(tokens_ko)
    return tokens_ko_nltk

# Nltk_text 리턴값 넣으면, 상위 단어 리스트 num만큼 리턴
def top_words(tokens_ko_nltk, num) : 
    """
        nltk_text 함수 리턴값
        상위 단어 리스트 num 만큼 리턴
    """
    data=  tokens_ko_nltk.vocab().most_common(num)
    return data

# 형태소 분석하는데, num 값 이상의 글자 크기만 리턴해줌
def tokenize_over(num) : 
    """
        num 이상만큼의 글자 크기만 리턴
    """
    tokens_ko2 = []
    for wd in tokens_ko2 : 
        if len(wd) >= num: 
            tokens_ko2.append(wd)
    return tokens_ko2

# 분석된 데이터 pickle를 이용해서 파일로 저장
def pickle_data(name, data) : 
    """
        name에는 저장할 떄의 파일이름
        data는 저장할 data (Ex. 리스트, 딕셔너리 등등)
    """
    import pickle
    with open('{}.pickle'.format(name), 'wb') as f : 
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__' : 
    Openlog('../../../data/twitch_live_chat/#zilioner/2018-12-06_#zilioner.log')
    print("완료")
