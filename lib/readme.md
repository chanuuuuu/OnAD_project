# 온애드/lib
## library화 한 onad 기능들

- analysis : 분석관련 기능모음
>- 예를들어, 시각화를 시켜주는 함수

- contact_db : 데이터베이스와 접촉하는 기능모음
>- 예를들어, db에서 데이터를 가져옴  
> 하지만 지금은 db를 사용하지 않기 때문에 크게 신경을 쓰지 않아도 됨.  
> 이후 추가하게 될 사항임

- get_data : 크롤러 및 api사용과 같이 데이터를 수집하는 기능 모음
> 하위 디렉토리
>- /twitch_crawl  
>- /twitch_api  
>- /youtube_crawl  
>- /youtube_api  

- model_fitting : ML 관련된 기능 모음
>- 예로, 가공된 학습데이터를 불러들여 훈련시키는 함수, 예측하는 함수 ( 더 세세히 나누고 추가할 필요성이 보임)

- set_data : 데이터를 가공 및 전처리하는 기능 모음
>- 예를 들어 pandas.DataFrame 으로 반환하는 함수