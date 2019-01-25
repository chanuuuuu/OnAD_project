from chat_wordcount import call_file_list
import pandas as pd

def cut_filename_csv(filename, num = 3) : 
    import re
    my = re.compile('([\d]*[-][\d]*[-][\d]*)([_]*)([#\w.]*)([.][\w.]*)([.][\w.]*)')
    txt = my.search(filename)
    mytxt = txt.group(num)
    return mytxt


def call_csv(folder, file) : 
    df = pd.read_csv('./new_matching_words/{0}/{1}'.format(folder, file), sep = '|', index_col = 'Unnamed: 0')
    return df


def remove_word(x):
    import ast

    tmp = list(df['morphs'][df['origin']== x])[0]
    series_tolist = ast.literal_eval(tmp)
    for wd in series_tolist:
        if wd in x : 
            target_index = x.index(wd)
            remove_word = x[target_index: target_index + len(wd)]
            x = x.replace(remove_word, "")
    return x.strip()

def del_whitespace(x) :
    import re
    pattern = re.compile(r'\s+')
    sentence = x
    catch = re.sub(pattern, ',', x)
    return catch

def mk_dir(dirpath) : 
    """
        dirpath : 체크할 폴더의 상대경로
    """
    import os
    dirname = dirpath
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

def pickle_data_catch_words(name, bj_code, data) : 
    """
        name : 파일이름 지정
        data : data는 저장할 data 
    """
    import pickle
    with open('./catch_words/{0}/{1}.pickle'.format(bj_code, name), 'wb') as f : 
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    
if __name__ == '__main__' : 
    folder_list = call_file_list('./new_matching_words')

    file_list = []
    for folder in folder_list : 
        file_list.extend(call_file_list('./new_matching_words/%s'%folder)) # 각 bj폴더
    
    for file in file_list :
        try : 
            print('%s 작업 시작'%file)
            folder_name = cut_filename_csv(file)
            print('csv 여는 중\n')
            df = call_csv(folder_name, file)
            print('csv 열기 완료\n')

            print('단어 추출 중\n')
            df['catch'] = df['origin'].apply(lambda x : remove_word(x))
            print('단어 추출 완료\n')
            df['catch'] = df['catch'].apply(lambda x : del_whitespace(x))
            print('공백제거')
            list_catch = list(df['catch'])
            
            mk_dir('./catch_words/%s'%folder_name)

            print('저장 중')
            pickle_data_catch_words('catch_{}'.format(file[:-8]),folder_name,list_catch)
            print('저장 완료\n')
        except Exception as e : 
            print(file, 'error')