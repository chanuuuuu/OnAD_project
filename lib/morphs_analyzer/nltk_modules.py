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