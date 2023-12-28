# Movie Cookie

## 1. 개요

-   **Movie Cookie**는 영화와 관련된 웹사이트 입니다.
-   영화 정보 검색, 영화 추천, 회원 간 커뮤니티 기능이 있습니다.

## 2. 배포 URL 및 사용한 기술스택

### 2-1. 배포 URL

> 링크: http://13.125.92.100/

```
<TEST 계정>
아이디: test1234
비밀번호: testest1234
```

### 2-2. GitHub 레포지토리 주소

-   **Back-End**

    > https://github.com/team-gingerbread/movie-cookie

-   **Front-End**
    > https://github.com/team-gingerbread/movie-cookie-fe

### 2-3. 사용한 기술스택

-   **Back-End**

    -   개발<br>
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">

    -   배포<br>
        <img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"> <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white"> <img src="https://img.shields.io/badge/gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white">

-   **Front-End**

    -   개발<br>
        <img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">

    -   배포<br>
        <img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"> <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white">

## 3. 코딩 컨벤션

### 3-1. 네이밍 컨벤션

-   **snake_case** : Python 변수, 함수, 파일명, 폴더명
-   **PascalCase** : 클래스
-   **camelCase** : JavaScript 변수, 함수
-   **kebab-case** : URL, HTML, CSS
-   **UPPER_CASE** : 상수
-   **is_variable** : Boolean 값
-   **$variable** : JavaScript HTML DOM 조작

### 3-2. Gitmoji 메시지

-   commit 메시지: "{gitmoji} {형식}: {내용}"
    -   예시 : **"✨ADD: post app 생성"**
-   형식: ADD, REMOVE, MOVE, UPDATE
-   gitmoji
    -   [🎉] : 프로젝트 첫 시작
    -   [✨] : 기능 추가
    -   [⚡] : 기능 업데이트
    -   [🐛] : 버그 수정
    -   [🎨] : 코드 형식 정리
    -   [💄] : UI 스타일 추가
    -   [🔥] : 파일 제거
    -   [🚚] : 파일 이동
    -   [🚀] : 배포 관련
    -   [📝] : README 작성

### 3-3. GitHub 브랜치 전략

-   GitHub Flow 전략 사용
-   배포용 브랜치 : **main**
-   개발용 브랜치 : **dev**
-   기능 추가 / 버그 수정 : GitHub Issue를 생성하여 개별 브랜치 생성, 작업 완료 후 dev 브랜치로 Pull Request & Merge
-   개발이 완료된 브랜치는 삭제
-   배포 단계에 main 브랜치로 dev 브랜치를 Merge
-   GitHub Actions를 이용하여 배포 자동화

## 4. 역할 분담 및 개발 일정

### 4-1. 역할 분담

| 박종훈    | 김윤재   | 이병관    | 편해선    |
| --------- | -------- | --------- | --------- |
| 영화 정보 | 커뮤니티 | 회원 관리 | 영화 추천 |

-   영화 정보 (박종훈)

    -   영화 정보 검색(KMDB API 이용)
    -   영화 한줄평 기능
    -   선호 영화 표시 기능

-   커뮤니티 (김윤재)

    -   회원 간의 커뮤니티
    -   영화와 관련된 유저 게시판 기능
    -   커뮤니티의 댓글, 대댓글 기능

-   회원 관리 (이병관)

    -   서비스 이용자의 계정 생성 및 관리
    -   JSON Web Token을 이용한 사용자 인증 기능
    -   사용자의 프로필 관리 기능

-   영화 추천 (편해선)
    -   사용자에게 알맞은 영화 추천
    -   KMDB와 박스오피스 데이터를 사용한 추천도 계산
    -   추천 영화 저장 기능

### 4-2. 개발 일정

WBS 넣을 예정

## 5. 프로젝트 구조

### 5-1. 폴더 구조

-   **Back-End**

```
📦movie-cookie
 ┣ 📂.vscode
 ┃ ┗ 📜settings.json
 ┣ 📂__pycache__
 ┣ 📂accounts
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📂migrations
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┣ 📜0001_initial.py
 ┃ ┃ ┣ 📜0002_initial.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜permissions.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜views.py
 ┣ 📂community
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📂migrations
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┣ 📜0001_initial.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜views.py
 ┣ 📂config
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜settings.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜wsgi.py
 ┣ 📂movieinfo
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📂migrations
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┣ 📜0001_initial.py
 ┃ ┃ ┣ 📜0002_delete_gptanalysis.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜permissions.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜utils.py
 ┃ ┗ 📜views.py
 ┣ 📂recommend
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📂migrations
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┣ 📜0001_initial.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜cron.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜permissions.py
 ┃ ┣ 📜schema_examples.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜views.py
 ┣ 📂static
 ┃ ┣ 📜foreign.csv
 ┃ ┗ 📜korean.csv
 ┣ 📜.env
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┣ 📜cron.log
 ┣ 📜manage.py
 ┣ 📜requirements.txt
 ┗ 📂venv
```

-   **Front-End**

```
📦movie-cookie-fe
 ┣ 📂.vscode
 ┃ ┗ 📜settings.json
 ┣ 📂accounts
 ┃ ┣ 📂login
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂mypage
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂mypage-edit
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂script
 ┃ ┃ ┣ 📜login.js
 ┃ ┃ ┣ 📜mypage-edit.js
 ┃ ┃ ┣ 📜mypage.js
 ┃ ┃ ┗ 📜signup.js
 ┃ ┣ 📂signup
 ┃ ┃ ┗ 📜index.html
 ┃ ┗ 📂style
 ┃ ┃ ┣ 📜login.css
 ┃ ┃ ┣ 📜mypage.css
 ┃ ┃ ┗ 📜signup.css
 ┣ 📂community
 ┃ ┣ 📂detail
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂script
 ┃ ┃ ┣ 📜detail.js
 ┃ ┃ ┣ 📜index.js
 ┃ ┃ ┗ 📜write.js
 ┃ ┣ 📂style
 ┃ ┃ ┗ 📜style.css
 ┃ ┣ 📂write
 ┃ ┃ ┗ 📜index.html
 ┃ ┗ 📜index.html
 ┣ 📂img
 ┃ ┣ 📜background.jpg
 ┃ ┣ 📜default.jpg
 ┃ ┗ 📜profile_basic.png
 ┣ 📂movieinfo
 ┃ ┣ 📂detail
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂script
 ┃ ┃ ┣ 📜detail.js
 ┃ ┃ ┗ 📜index.js
 ┃ ┣ 📂style
 ┃ ┃ ┗ 📜style.css
 ┃ ┗ 📜index.html
 ┣ 📂recommend
 ┃ ┣ 📂detail
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂list
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂script
 ┃ ┃ ┣ 📜detail.js
 ┃ ┃ ┣ 📜list.js
 ┃ ┃ ┗ 📜recommend.js
 ┃ ┣ 📂style
 ┃ ┃ ┗ 📜recommend.css
 ┃ ┗ 📜index.html
 ┣ 📂script
 ┃ ┣ 📜base.js
 ┃ ┣ 📜token.js
 ┃ ┗ 📜url.js
 ┣ 📂style
 ┃ ┣ 📜base.css
 ┃ ┗ 📜main.css
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┗ 📜index.html
```

### 5-2. 데이터베이스 ERD 구조

<img src='./readme/ERD.jpg'>

### 5-3. API 구조

| app:accounts                 | HTTP Method | 설명                       | 로그인 권한 필요 | 사용자 본인 권한 필요 |
| ---------------------------- | ----------- | -------------------------- | ---------------- | --------------------- |
| signup/                      | POST        | 회원가입 요청              |                  |                       |
| login/                       | POST        | 로그인 요청                |                  |                       |
| logout/                      | POST        | 로그아웃 요청              |                  |                       |
| password/change/             | POST        | 비밀번호 변경 요청         | O                | O                     |
| token/refresh/               | POST        | 인증토큰 재발급 요청       | O                | O                     |
| api/user-profile/`<int:id>`/ | GET         | 프로필 조회 요청           | O                | O                     |
| api/user-profile/`<int:id>`/ | PATCH       | 프로필 수정 요청           | O                | O                     |
| api/liked-movies/            | GET         | 좋아요 누른 영화 조회 요청 | O                | O                     |
| api/watched-movies/          | GET         | 본 영화 조회 요청          | O                | O                     |
| api/watchlist-movies/        | GET         | 볼 영화 조회 요청          | O                | O                     |

| app:community                 | HTTP Method | 설명                       | 로그인 권한 필요 | 작성자 권한 필요 |
| ----------------------------- | ----------- | -------------------------- | ---------------- | ---------------- |
| /                             | GET         | 전체 글 리스트 요청        |                  |                  |
| /                             | POST        | 글 생성 요청               | O                |                  |
| /?search=`<str:query>`/       | GET         | 글 검색 요청               |                  |                  |
| `<int:post_id>`/              | GET         | 글 내용 조회 요청          |                  |                  |
| `<int:post_id>`/              | PATCH       | 글 내용 수정 요청          | O                | O                |
| `<int:post_id>`/              | DELETE      | 글 내용 삭제 요청          | O                | O                |
| comments/                     | POST        | 댓글 생성 요청             | O                |                  |
| comments/`<int:comment_id>`/  | PATCH       | 댓글 수정 요청             | O                | O                |
| comments/`<int:comment_id>`/  | DELETE      | 댓글 삭제 요청             | O                | O                |
| view/comments/                | GET         | 전체 댓글 조회 요청        |                  |                  |
| view/comments/`<int:post_id>` | GET         | 해당 글의 댓글 리스트 요청 |                  |                  |

| app:movieinfo                                     | HTTP Method | 설명                              | 로그인 권한 필요 | 작성자 권한 필요 |
| ------------------------------------------------- | ----------- | --------------------------------- | ---------------- | ---------------- |
| search/                                           | POST        | 영화 검색 요청                    |                  |                  |
| detail/                                           | GET         | 전체 영화 정보 요청               |                  |                  |
| detail/`<int:movie_id>`/                          | GET         | movie_id 영화 정보 상세 요청      |                  |                  |
| detail/`<int:movie_id>`/onelinecritic/            | GET         | movie_id 영화 한줄평 전체 요청    |                  |                  |
| detail/`<int:movie_id>`/onelinecritic/            | POST        | movie_id 영화 한줄평 작성 요청    | O                |                  |
| detail/`<int:movie_id>`/onelinecritic/`<int:pk>`/ | PATCH       | movie_id 영화 pk 한줄평 수정 요청 | O                | O                |
| detail/`<int:movie_id>`/onelinecritic/`<int:pk>`/ | DELETE      | movie_id 영화 pk 한줄평 삭제 요청 | O                | O                |

| app:recommend | HTTP Method | 설명                              | 로그인 권한 필요 | 사용자 본인 권한 필요 |
| ------------- | ----------- | --------------------------------- | ---------------- | --------------------- |
| genres/       | GET         | 영화 추천 후보들의 장르 목록 조회 |                  |                       |
| generate/     | POST        | 영화 추천 실행                    |
| /             | GET         | 추천 받은 영화 목록 조회          | O                |                       |
| /             | POST        | 추천 받은 영화 저장               | O                |                       |
| `<int:id>`/   | GET         | 추천 정보 상세 조회               | O                | O                     |
| `<int:id>`/   | PATCH       | 추천 정보 수정                    | O                | O                     |
| `<int:id>`/   | DELETE      | 추천 정보 삭제                    | O                | O                     |

> [Swagger로 API 테스트하기](http://52.79.54.190/api/schema/swagger-ui/) <br>

### 5-4. 배포 아키텍쳐 구조

<img src='./readme/배포구조.png'>

## 6. UI 목업

> [Figma 작업](https://www.figma.com/file/EIGbPjQYZGzfL36iznhRsm/Movie-Cookie?type=design&node-id=25%3A6&mode=design&t=USAO0M0PDikvYeYQ-1)

### 6-1. 메인 페이지

<img src='./readme/메인.png'>

### 6-2. 회원 관리 페이지

<img src='./readme/회원관리.png'>

### 6-3. 커뮤니티 페이지

<img src='./readme/커뮤니티.png'>

### 6-4. 영화 정보 페이지

<img src='./readme/무비인포.png'>

### 6-5. 영화 추천 페이지

<img src='./readme/영화추천.png'>
