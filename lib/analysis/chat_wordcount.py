from py_komoran3.komoran3py import KomoranPy
ko = KomoranPy()
ko.set_user_dictionary('./py_komoran3/user_dictionary.txt')

# 채팅로그 불러오는 함수 
def openlog( bj_code, filename, platform = 'twitch_live_chat') : 
    """
    '../../data/{0}/{1}/{2}'.format(platform, bj_code, filename)
    platform : 플랫폼 폴더명 (기본 : twitch_live_chat)
    bj_code : bj 폴더명
    filename : 로그 파일이름
    """
    chatlog = '../../data/{0}/{1}/{2}'.format(platform, bj_code, filename)
    with open(chatlog) as f : 
        chat = f.readlines()
    return chat

# Openlog or 직접 불러온 채팅 로그 넣으면 정규식으로 id, 날짜, 채팅 내용 구분해줌
def preprocessing_chat(chat, num = 3) : 
    """ 
        chat : chat에는 채팅로그 넣기
        num : 그룹 선택 / 안주면 기본값 3 (0 = 전체, 1 = 시간(방송기준) 2 = ID 3 = 채팅)
    """
    import re
    text = chat
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
        word_list : 전처리된 리스트(prepro_chat함수의 리턴값 넣기)
    """
    tokens_ko = []
    for wd in word_list : 
        for i in range(len(ko.pos(wd))) : 
            tokens_ko.append(ko.pos(wd)[i][0])
    return tokens_ko

# 형태소 리스트 넣으면 빈도분석 가능한 형태 전환 시킴
def nltk_text(tokens_ko) : 
    """
        tokens_ko :  tokenize 함수 리턴값 
    """
    import nltk
    tokens_ko_nltk = nltk.Text(tokens_ko)
    return tokens_ko_nltk

# Nltk_text 리턴값 넣으면, 상위 단어 리스트 num만큼 리턴
def top_words(tokens_ko_nltk, num = 100) : 
    """
        tokens_ko_nltk : nltk_text 함수 리턴값
        num : 상위 단어 리스트 num 만큼 리턴 / 기본값 100
    """
    data=  tokens_ko_nltk.vocab().most_common(num)
    return data

# 형태소 분석하는데, num 값 이상의 글자 크기만 리턴해줌
def tokenize_over(tokens_ko, num = 2) : 
    """
        num : 원하는 글자 크기 / 기본값 : 2 (num보다 큰 수만 출력)
    """
    tokens_ko2 = []
    for wd in tokens_ko : 
        if len(wd) >= num: 
            tokens_ko2.append(wd)
    return tokens_ko2

# 분석된 데이터 pickle를 이용해서 파일로 저장
def pickle_data(name, bj_code, data) : 
    """
        name : 파일이름 지정
        data : data는 저장할 data 
    """
    import pickle
    with open('./top_words/{0}/{1}.pickle'.format(bj_code, name), 'wb') as f : 
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# 폴더 내 파일을 리스트로 리턴해주는 함수
def call_file_list(path) : 
    """
        path : 파일 경로
    """
    from os import listdir
    path_dir = path
    file_list = listdir(path_dir)
    return file_list

# 디렉토리 체크해서 디렉토리 없으면 디렉토리 만들어줌
def mk_dir(dirpath) : 
    """
        dirpath : 체크할 폴더의 상대경로
    """
    import os
    dirname = dirpath
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

if __name__ == '__main__' : 
    try : 
        bj_list = call_file_list('../../data/twitch_live_chat')
        for bj in bj_list : 
            file_list = call_file_list('../../data/twitch_live_chat/%s'%bj)
            for file in file_list :
                log = openlog(bj, file)
                print('%s로그 불러오기 완료' %file)

                word_list = preprocessing_chat(log)
                print('%s로그 전처리 완료'%file)

                tokens_ko = tokenize(word_list)
                print('%s로그 토큰화 완료'%file)

                tokens_ko2 = tokenize_over(tokens_ko)
                print('2글자 이상 추출')

                tokens_ko_nltk = nltk_text(tokens_ko)
                print('%s로그 자연어처리 완료'%file)
                
                tokens_ko_nltk2 = nltk_text(tokens_ko2)
                print('%s로그 2글자 이상자연어처리 완료'%file)

                top_data = top_words(tokens_ko_nltk)
                print('%s상위 단어 추출 완료'%file)

                top_data2 = top_words(tokens_ko_nltk2)
                print('%s상위 2단어이상 추출 완료'%file)

                mk_dir('./top_words/{}'.format(bj))
                
                pickle_data('%s기본형태소'%file[:-4],bj,top_data)
                print('기본형태소 파일저장')

                pickle_data('%s2글자이상형태소'%file[:-4],bj,top_data2)
                print('2글자이상형태소 파일저장')

    except Exception as e : 
            print('stopped due to ', e)
    print('$$$$$$$$$$$ ALL DONE $$$$$$$$$$$$$$$')
