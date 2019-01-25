


def model_maker():
    
    import os
    import pickle
    
    import pandas as pd
    
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.preprocessing import StandardScaler
    
    from sklearn import model_selection, metrics
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import f1_score
    
    print(os.getcwd())
    chat_data = os.listdir("../lib/analysis/data")[1:]
    datas = []
    print(chat_data)
    for data in chat_data:
        tmp = pd.read_csv('./data/{}'.format(data))
        datas.append(tmp)
    
    df = pd.concat(datas , axis=0, join='inner', ignore_index=True)
    df = df.set_index(keys=df.columns[0])
    
    X_train = df.iloc[:,:-1]
    y_train = df.iloc[:, -1]
    anal_data = df[:]
    anal_data["validation"] = y_train
    
    
    scaler = StandardScaler()
    X_train = scaler.fit(X_train).transform(X_train)
    
    print("{}를 사용하여 데이터 전처리".format(str(scaler).split("(")[0]))
    
    clf =  GaussianNB()    
    classifier_score = {}    
    clf.fit(X_train,  y_train)

    anal_data.index = pd.to_datetime(anal_data.index)
    anal_data = anal_data.sort_index()
    anal_data['date'] = anal_data.index
    anal_data['date'] = anal_data['date'].apply(lambda x : str(x.date()))
    
    
    with open("yapyap30_GaussianNB.pickle", 'bw') as f:
        pickle.dump(clf, f)
    
    print("정답 레이블의 개수", len(anal_data[anal_data["validation"] == 1]))

    return anal_data, clf


def soar_point(n):
    '''
    n (int or float)
    어떤 구간의 채팅빈도수 x와 x의 바로 직전 구간의 채팅빈도수 y 가 x > y * n 일 때 x의 구간을 '급상승'이라고 정의

    matplotlib을 통해 입력한 n에 따른 급상승 구간이 검은색 선으로 표시됨

    return soar_point (pandas.Dataframe)
    '''


    import pandas as pd

    from sklearn.naive_bayes import GaussianNB
    from sklearn.preprocessing import StandardScaler
    from sklearn import model_selection, svm, metrics
    from sklearn.metrics import f1_score
    
    from matplotlib import pyplot as plt
    from matplotlib import font_manager, rc
    import platform
    plt.rcParams['axes.unicode_minus'] = False
    if platform.system() == 'Darwin':    # 맥
        rc( 'font', family='AppleGothic' )
    elif platform.system() == 'Windows': # 윈도우
        # 폰트 차후 확인
        fontPath = 'c:/Windows/Fonts/malgun.ttf'
        fontName = font_manager.FontProperties( fname=fontPath ).get_name()
        rc( 'font', family=fontName )
    else:
        print('알수없는 시스템. 미적용')

    anal, model = model_maker()

    df = pd.read_csv("yapyap_2018_12_10.csv")
    df = df.set_index(keys=df.columns[0])
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df_data = df.iloc[:,:-1]
    df_label = df.iloc[:, -1]

    scaler = StandardScaler()
    df_data = scaler.fit(df_data).transform(df_data)

    pre = model.predict(df_data)
    df["pre"] = pre
    predict  = df[df.pre == 1]


    ##################################################
    # 예측 기준

    count = 0
    index = []
    data_set = {"soar":[], "upload":[]}
    for x in predict.index:
        if count * 1.5 < predict["cnt_chat"][x] and predict["cnt_chat"][x] > 12 :
            index.append(x)
            data_set["soar"].append(predict["cnt_chat"][x])
            data_set["upload"].append(predict["validation"][x])
        count = predict["cnt_chat"][x]
    tmp = pd.DataFrame(data=data_set, index=index)
    #######################################################################

    validation_ = df[df.validation == 1]
    validation = df[df.validation == 0]

    pre_1 = df[df.pre == 1]
    pre_0 = df[df.pre == 0]


    plt.figure(figsize=(16,8))

    plt.plot(validation.index, validation['cnt_chat'], color="green")
    plt.plot(pre_1.index, pre_1["cnt_chat"], color="y")
    plt.plot(validation_.index, validation_['cnt_chat'], color="red")
    plt.plot(soar_point.index, soar_point["soar"], color="black")



    plt.legend(["총 스트리밍 시간 중 'ㅋ' 빈도수", "예측치","실제 유튜브 업로드 구간", "급상승 포인트"],fontsize="15")

    plt.show()

    return soar_point

#########################################################

soar_point(1.8)