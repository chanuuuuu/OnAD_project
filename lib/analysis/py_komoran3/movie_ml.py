import pickle
def call_file_list(path) : 
    """
        path : 파일 경로
    """
    from os import listdir
    path_dir = path
    file_list = listdir(path_dir)
    return file_list

file_list = call_file_list('./movie140reviewcorpus-master/raw')

logs= []
for i, file in enumerate(file_list) : 
    with open('./movie140reviewcorpus-master/raw/{}'.format(file), 'r') as f : 
        logs.extend(f.readlines())
        print(file,'완료')

with open('movie_review.pickle', 'wb') as f : 
    pickle.dump(logs, f, pickle.HIGHEST_PROTOCOL)