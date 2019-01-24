from lib.analysis.chat_wordcount import call_file_list
from lib.analysis.chat_word_catch import cut_filename
import pickle

# pickle 불러와서 로드해줌
def open_pickle(bj_code, file_name) : 
    """
        bj_code : bj 이름
        file_name : 불러올 피클 파일 이름
    """
    with open('./catch_words/{}/{}'.format(bj_code, file_name), 'rb') as f : 
        text = pickle.load(f)
    return text


def tag_word(file_path,text_split,num) : 
    file=open(file_path,'w')
    for wd in text_split : 
        if len(wd) >= num : 
            file.write('%s\tNNP\n'%wd)
    file.close()




if __name__ == '__main__' : 
        
    folder_list = call_file_list('./catch_words')
    
    file_list = []
    for folder in folder_list : 
        file_list.extend(call_file_list('./catch_words/%s'%folder))


    for file in file_list : 
        bj_code = cut_filename(file)
        print('%s 텍스트 열기'%file)
        text = open_pickle(bj_code, file)

        text_str = ','.join(text)
        text_split = text_str.split(',')
        print('%s 저장하기'%file)
        tag_word('../../data/sentiment_dictionary/tmp_user_dict.txt', text_split, 2)

    