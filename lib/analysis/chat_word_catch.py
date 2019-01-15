from chat_wordcount import call_file_list, preprocessing_chat, tokenize, mk_dir, openlog
from py_komoran3.komoran3py import KomoranPy
ko = KomoranPy()
ko.set_user_dictionary('./py_komoran3/user_dictionary.txt')
import os
import time


# 전처리 후 문장들을 2중 리스트로 반환
def preprocessing_chat_tolist(chat, num = 3) : 
    """ 
        chat : chat에는 채팅로그 넣기
        num : 그룹 선택 / 안주면 기본값 3 (0 = 전체, 1 = 시간(방송기준) 2 = ID 3 = 채팅)
    """
    import re
    text = chat
    my = re.compile('\[([0-9:]*)\] <(\S*[ ]*\S*)> (\w.*)')
    word_tolist = []
    for line in text:
        mytext = my.search(line)
        if mytext :
            word_tolist.append([mytext.group(num)])
    return word_tolist

    # 형태소 분석된 거를 원래 문장단위로 리스트로 묶어서 리턴 / 이중 리스트
    # 여기 for문 줄이기
def tokenize_tolist(text_array_flat) :
    """
        text_array_flat : 1차 리스트 / flatten 함수의 리턴값
    """
    tokens_ko_tolist = []
    line_list = []
    for word in text_array_flat : 
        for i in range(len(ko.pos(word))) : 
            line_list.append(ko.pos(word)[i][0])
            if i+1 == len(ko.pos(word)) : 
                tokens_ko_tolist.append(line_list)
                line_list = []
    return tokens_ko_tolist

    # preprocessing_tolist 리턴값과 tokenize_tolist 리턴값 넣으면, 추가되거나 너무 작게
# 쪼개진 형태소와 문장이 튜플로 묶인후, 그 튜플을 모은 리스트가 반환
def matching(word_array_flat, tokens_ko_tolist) : 
    """
        word_list : 전처리, 리스트화 된 채팅 로그 (preprocessing_tolist 리턴값)
    """
    matching_list = []
    for i , value in enumerate(word_array_flat):
        try : 
            for target in tokens_ko_tolist[i]:
                if target not in value:
                    matching_list.append((tokens_ko_tolist[i], value))
        except Exception as e : 
            print(e, target, value)
    return matching_list

def pickle_data_matching_words(name, bj_code, data) : 
    """
    name : 파일이름 지정
    data : data는 저장할 data 
    """
    import pickle
    with open('./new_matching_words/{0}/{1}.pickle'.format(bj_code, name), 'wb') as f : 
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# 2차 리스트를 1차로 줄여줌 
def flatten_list(word_tolist) : 
    import numpy as np
    """
        word_tolist : 2차 리스트 / preprocessing의 리턴값
    """
    word_array = np.array(word_tolist)
    word_array_flat = word_array.flatten()
    return word_array_flat

# 매칭 리스트를 데이터 프레임으로 바꿔주는 함수 
def to_array(matching_list) : 
    """
        matching_list : 매칭리스트 / matching 함수의 리턴값
    """
    import numpy as np
    import pandas as pd
    match_arr = np.array(matching_list)
    word_dataframe = pd.DataFrame(match_arr)
    return word_dataframe

def cut_filename(filename, num = 3) : 
    import re
    my = re.compile('([\d]*[-][\d]*[-][\d]*)([_]*)([#\w.]*)([.][\w.]*)')
    txt = my.search(filename)
    mytxt = txt.group(num)
    return mytxt


if __name__ == '__main__' : 

    folder_list = call_file_list('../../data/twitch_live_chat')

    file_list = []
    for folder in folder_list : 
        file_list.extend(call_file_list('../../data/twitch_live_chat/%s'%folder)) # 각 bj폴더
    for file in file_list : 
        start_time = time.time()    

        folder_name = cut_filename(file)
        # if os.path.exists('./matching_words/{0}/matching_{1}.pickle'.format(folder, file[:-4])) : 
        #     print('존재')
        # else : 
        #     print('nononoo')
        # print('./matching_words/{0}/matching_{1}.pickle'.format(folder, file[:-4]))
        if os.path.exists('./new_matching_words/{}/{}.csv'.format(folder_name, file)) : 
            print('이미 존재 넘어감\n')
            continue
        
        print('로그추출중')
        log = openlog(folder_name,file) # bj폴더 내에서 로그 읽음
        print('%s_log추출\n'%file)

        print('word_tolist 생성중')
        word_tolist = preprocessing_chat_tolist(log) # word_tolist 반환
        print('%s_word_tolist 생성\n'%file)

        print('리스트 축소 중 ')
        word_array_flat = flatten_list(word_tolist)
        print('리스트 축소 완료\n')


        print('tokens_ko_tolist 생성중')
        tokens_ko_tolist = tokenize_tolist(word_array_flat) # token_ko_tolist 반환
        print('%s_tokens_ko_tolist 생성'%file)

        print('매칭중')
        matching_list = matching(word_array_flat, tokens_ko_tolist)
        print('매칭완료\n')

        word_dataframe = to_array(matching_list)
        print('데이터 프레임화 완료\n')
        
        try : 
            word_dataframe = word_dataframe.drop_duplicates([1])
            print('데이터 프레임 내 중복 행 제거\n')
        except Exception as e : 
            print(e,'진행')
        word_dataframe = word_dataframe.reset_index()
        print('인덱스 재설정\n')

        word_dataframe = word_dataframe.drop('index',axis=1)
        print('인덱스 열 제거\n')

        word_dataframe = word_dataframe.rename(columns={0:'morphs', 1:'origin'})
        print('열 이름 변경\n')

        mk_dir('./new_matching_words/%s'%folder_name) # matching폴더 없으면 생성해줌

        word_dataframe.to_csv('./new_matching_words/{}/{}.csv'.format(folder_name, file), sep = '|', mode = 'w')
        # pickle_data_matching_words('matching_{}'.format(file[:-4]), folder, matching_list )
        
        end_time = time.time() - start_time
        print('소요시간 : ', end_time, '\n')
        print('저장완료')
