

def GaussianNB_for_streamer(data_path):
    """
    data_path : 스트르머의 한 방송에 대한 동영상 시간과 채팅빈도수 등이 포함된 CSV 파일

    return => {GaussianNB : 정확도(float),f1-score(float), 실제 유트브에 업로드 된 편집점 대비 모델이 예측한 편집점의 일치율(float)}(dict)
              streamer 데이터 (pandas.Dataframe)             


    """
    
    import os
    import pickle
    
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.preprocessing import MinMaxScaler

    from sklearn import model_selection, svm, metrics
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import f1_score
    
    
    chat_data = os.listdir("{}".format(data_path))
    datas = []
    for data in chat_data:
        tmp = pd.read_csv('./{}/{}'.format(data_path, data))
        datas.append(tmp)
    
    df = pd.concat(datas , axis=0, join='inner', ignore_index=True)
    df = df.set_index(keys=df.columns[0])
    
    X_train, X_test, y_train, y_test = train_test_split(df.iloc[:,:-1], df.iloc[:, -1], random_state=0)
    anal_data = X_test[:]
    anal_data["validation"] = y_test
    
    
    scaler = MinMaxScaler()
    X_train = scaler.fit(X_train).transform(X_train)
    X_test = scaler.fit(X_test).transform(X_test)
    
    
    
    classifier = GaussianNB()
    classifier_score = {}
    
    classifier.fit(X_train,  y_train)
    pre = classifier.predict(X_test)
    anal_data["{}".format(str(classifier).split("(")[0])] = pre
    ac_score = metrics.accuracy_score(y_test, pre)
    f1 = f1_score(y_test, pre)
    classifier_score["{}".format(str(classifier).split("(")[0])] = [ac_score, f1,
                                                                    len(anal_data[anal_data["{}".format(str(classifier).split("(")[0])] == 1]) / len(anal_data[anal_data["validation"] == 1]) * 100]
        
    
    anal_data.index = pd.to_datetime(anal_data.index)
    anal_data = anal_data.sort_index()
    anal_data['date'] = anal_data.index
    anal_data['date'] = anal_data['date'].apply(lambda x : str(x.date()))
    
    return classifier_score, anal_data