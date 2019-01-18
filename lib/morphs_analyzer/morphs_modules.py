from komoran3py import KomoranPy
ko = KomoranPy()
ko.set_user_dictionary('/lib/morphs_analyzer/user_dictionary.txt')



# 형태소 분석된 거를 원래 문장단위로 리스트로 묶어서 리턴 / 이중 리스트
# 여기 for문 줄이기
def tokenize_tolist(x, depth = 1) :
    """
        text_array_flat : 1차 리스트 / flatten 함수의 리턴값
        depth : 반환될 리스트 형태 1 = 1차원 리스트, 2 = 2차원 리스트
    """
    
    
    tokens_ko_tolist = []
    line_list = []
    if depth == 1 : 
        for i in range(len(ko.pos(x))) : 
            tokens_ko_tolist.append(ko.pos(x)[i][0])

    if depth == 2 :
        for i in range(len(ko.pos(word))) : 
            line_list.append(ko.pos(word)[i][0])
            if i+1 == len(ko.pos(word)) : 
                tokens_ko_tolist.append(line_list)
                line_list = []
    return tokens_ko_tolist
