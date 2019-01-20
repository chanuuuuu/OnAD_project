# 파일불러서 한 줄 씩 읽는  함수 
def openlog(path) : 
    """
        path : 경로 입력 
    """
    chatlog = '{}'.format(path)
    with open(chatlog) as f : 
        chat = f.readlines()
    return chat

# 분석된 데이터 pickle를 이용해서 파일로 저장
def pickle_data(path) : 
    """
        path : 경로 지정 및 파일 이름 지정
        data : data는 저장할 data 
    """
    import pickle
    with open(path, 'wb') as f : 
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


def cut_filename(filename, num = 3) : 
    """
        matching_2018-12-07_#cocopopp671.pickle 요래 생긴 파일이름 잘라 줌
        0 : '전체'
        1 : '날짜'
        2 : '_'
        3 : BJ_CODE (default)
        4 : .파일형식
    """
    import re
    my = re.compile('([\d]*[-][\d]*[-][\d]*)([_]*)([#\w.]*)([.][\w.]*)')
    txt = my.search(filename)
    mytxt = txt.group(num)
    return mytxt

def cut() : 
    import re
    reg = re.compile('\[([0-9:]*)\] <(\S*[ ]*\S*)> (\w.*)')
    return reg