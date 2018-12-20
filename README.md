# 온애드 프로젝트를 위한 레파지토리

## 1. 디렉토리 설정


* lib : 각 모듈들
* docs : 문서작업
* onad_web : 웹페이지 관련
각 세부 사항은 해당 디렉토리의 README.md 파일에 있음.

## 2. 사용법 및 룰

* branch 룰
  - master : 최종본
  - develop : 작업본
  - **`대부분의 경우 develop브랜치에 commit 하기 바람`**
  - master branch에 커밋하는 경우 : 해당기능을 최종 완성시에만(토의 이후)

* 기본 용어
  - **`branch`** : master의 가지 (다른 작업을 한 이후 master에 합치는 식)
  - **`commit`** : 지금 상태를 스냅샷 찍어 기록을 남긴다고 생각하면됨  
    다 남기 때문에 예전으로 돌아갈 수 있음  
    하지만 이는 로컬pc에서만 저장됨 github에 올리기 위해서는 push
  - **`push`** : 커밋한 상태인 로컬pc의 상태로 github를 최신화시키는 것
  - **`pull`** : 가장 최신의 상태를 로컬pc로 가져오는 것

* vscode 에서 git사용:
  - git이 없다면 설치
  - 이후 cmd 창에서
    > git config --global user.name "이름"
    > git config --global user.email "이메일"
  
  - 이후 현재 레파지토리의 clone or download 클릭
  - url 복사
  - vscode 열고, ctrl + shift + p
  - 명령창에 git:clone 입력 또는 클릭
  - 폴더 선택창이 뜰텐데, 빈 폴더 하나 생성하여 확인클릭
  - 작업한 이후 vscode의 왼쪽 탭 3번째 가지모양 클릭
  - 체크모양의 Commit 단추 누르면 commit이 됨 (**코멘트입력** : 고친내용 or 추가한내용_181218_강화수)
  
* commit 룰
  - commit은 뭔가가 바뀌면 바로바로 하는게 좋을 것 같아보임.(바뀜의 단위는 자신의 기준)
  - **`하교 전 저녁에는 push, 출첵 후 아침에는 pull 하는게 바람직할 듯`**
  - push, pull 모두 ''' 단추를 누르면 할 수 있음. **(push 는 commit 이후!!)**
  - develop에 commit할 경우 push to -> origin -> develop 선택
