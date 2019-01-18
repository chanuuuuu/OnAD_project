def rate_sentiment(x) : 
    sentiment_list = []
    score = 0
    
    for i in range(len(x)) : 
        if x[i] in new_word_dic.keys() : 
            sentiment_list.append(new_word_dic[x[i]])
            if i+1 == len(x) : 
                score = sum(sentiment_list)
                
                return score
        
        elif x[i] not in new_word_dic.keys() : 
            sentiment_list.append(0)
            if i+1 == len(x) :
                score = sum(sentiment_list)
                
                return score
        
        else : return 'Nan'
