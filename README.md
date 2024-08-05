# 후기마당

## 1. Project Structure

<details>
<summary>backend</summary>

```
fastapi
 ┣ domain
 ┃ ┣ account
 ┃ ┃ ┣ crud.py
 ┃ ┃ ┣ router.py
 ┃ ┃ ┗ schemas.py
 ┃ ┣ comment
 ┃ ┃ ┣ crud.py
 ┃ ┃ ┣ router.py
 ┃ ┃ ┗ schemas.py
 ┃ ┗ review
 ┃    ┣ crud.py
 ┃    ┣ router.py
 ┃    ┗ schemas.py
 ┣ migrations
 ┣ test
 ┃ ┣ __init__.py
 ┃ ┣ conftest.py
 ┃ ┣ test_account.py
 ┃ ┣ test_comment.py
 ┃ ┗ test_review.py
 ┣ alembic.ini
 ┣ err_msg.py
 ┣ main.py
 ┣ models.py
 ┣ requirements.txt
 ┗ .env
```

- domain
    - account: 사용자 계정
    - comment: 댓글
    - review: 후기
- migrations: alembic으로 생성한 마이그레이션 파일이 있는 폴더
- test
    - conftest.py: 테스트에 공통적으로 사용되는 설정이나 fixture 모음
- .env: 환경변수 집합
    - `DB_HOST`: 호스트 주소
    - `DB_NAME`: 데이터베이스 이름
    - `DB_PORT`: 포트 번호
    - `DB_USER`: 계정명
    - `DB_PASS`: 계정 비밀번호
    - `SECRET_KEY`
    - `HASH_ALGORITHM`: 해시 알고리즘. HS256으로 지정했다.
    - `TOKEN_EXPIRE_MINUTES`: 로그인 시 부여되는 토큰의 유효시간. 60*24로 지정했다.

</details>

<details>
<summary>frontend</summary>

```
frontend
 ┣ src
 ┃ ┣ components
 ┃ ┃ ┣ Error.svelte
 ┃ ┃ ┗ Navigation.svelte
 ┃ ┣ lib
 ┃ ┃ ┣ api.js
 ┃ ┃ ┣ emoji.js
 ┃ ┃ ┗ store.js
 ┃ ┣ routes
 ┃ ┃ ┣ AccountCreate.svelte
 ┃ ┃ ┣ AccountLogin.svelte
 ┃ ┃ ┣ AccountMatch.svelte
 ┃ ┃ ┣ AccountProfile.svelte
 ┃ ┃ ┣ AccountUpdate.svelte
 ┃ ┃ ┣ CommentUpdate.svelte
 ┃ ┃ ┣ Index.svelte
 ┃ ┃ ┣ PasswordChange.svelte
 ┃ ┃ ┣ PasswordReset.svelte
 ┃ ┃ ┣ ReviewCreate.svelte
 ┃ ┃ ┣ ReviewDetail.svelte
 ┃ ┃ ┗ ReviewUpdate.svelte
 ┃ ┣ app.css
 ┃ ┗ App.svelte
 ┗ .env
```

- src
    - components: 내비게이션바와 오류 메시지 알림창 포함
    - lib: 공통적으로 사용되는 함수와 변수
    - routes: 엔드포인트마다 호출되는 페이지의 모음
- .env: 환경변수 집합
    - `VITE_SERVER_URL`: 백엔드 주소

</details>


## 2. 개발 환경 구축
1. `fastapi` 디렉토리에서 다음을 실행하여 가상환경을 생성하고 필요한 패키지를 설치한다.
```bash
$ python -m venv venv
$ pip install -r requirements.txt
```

2. `PostgreSQL`에서 다음을 실행한다. 이때 `db_name`은 `.env`에서 설정한 데이터베이스 이름이다.
```SQL
CREATE DATABASE `db_name`;
```

3. 가상환경을 활성화한 후 `fastapi` 디렉토리에서 다음을 실행한다.
```bash
$ alembic upgrade head
```

4. `frontend` 디렉토리에서 다음을 실행한다.
```bash
$ npm install
$ npm run build
```

5. `fastapi` 디렉토리에서 다음을 실행한다.
```bash
$ uvicorn main:app --reload
```

## 3. API 엔드포인트 목록

### account

<details>
<summary>가입 `POST` /api/account/create </summary>

- Request body

| name | type | description |
| --- | --- | --- |
| username | string | 아이디 |
| password1 | string | 비밀번호 |
| password2 | string | 비밀번호 확인 |
| email | string | 이메일 |
| birthday | date | 생년월일 |
| summary | string | 자기소개 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>회원정보 확인 `GET` /api/account/get/{username}</summary>

- Parameters

| name | type | description |
| --- | --- | --- |
| username | string | 아이디 |

- Response
    - `200`
    - `422`

</details>

<details>
<summary>로그인 `POST` /api/account/login</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| username | string | 아이디 |
| password | string | 비밀번호 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>회원정보 수정 `PUT` /api/account/update</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| id | number | 회원 일련번호 |
| username | string | 아이디 |
| email | string | 이메일 |
| birthday | date | 생년월일 |
| summary | string | 자기소개 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>회원 탈퇴 `DELETE` /api/account/delete</summary>

-Response
    - `204`

</details>

<details>
<summary>아이디, 이메일 정보 일치 확인 `POST` /api/account/match</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| username | string | 아이디 |
| email | string | 이메일 |

- Response
    - `200`
    - `422`

</details>

<details>
<summary>비밀번호 재설정 `POST` /api/account/reset</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| account_id | number | 회원 일련번호 |
| password1 | string | 비밀번호 |
| password2 | string | 비밀번호 확인 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>비밀번호 변경 `POST` /api/acocunt/change</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| account_id | number | 회원 일련번호 |
| password | string | 기존 비밀번호 |
| password1 | string | 새 비밀번호 |
| password2 | string | 새 비밀번호 확인 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>팔로우, 언팔로우 `POST` /api/account/follow</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| account_id | number | 회원 일련번호 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>작성한 후기 찾기 `GET` /api/account/reviews</summary>

- Parameters

| name | type | description |
| --- | --- | --- |
| account_id | number | 회원 일련번호 |
| page | number | 현재 페이지 |
| size | number | 페이지당 후기 수 |

- Response
    - `200`
    - `422`

</details>

<details>
<summary>작성한 댓글 찾기 `GET` /api/account/comments</summary>

- Parameters

| name | type | description |
| --- | --- | --- |
| account_id | number | 회원 일련번호 |
| page | number | 현재 페이지 |
| size | number | 페이지당 댓글 수 |

- Response
    - `200`
    - `422`

</details>

### review

<details>
<summary>후기 목록 불러오기 `GET` /api/review/list</summary>

- Parameters

| name | type | description |
| --- | --- | --- |
| page | number | 현재 페이지 |
| size | number | 페이지당 후기 수 |

- Response
    - `200`
    - `422`

</details>

<details>
<summary>특정 후기 불러오기 `GET` /api/review/detail/{review_id}</summary>

- Parameters

| name | type | description |
| --- | --- | --- |
| review_id | number | 후기 일련번호 |

- Response
    - `200`
    - `422`

</details>

<details>
<summary>후기 작성 `POST` /api/review/create</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| book | string | 책 제목 |
| subject | string | 제목 |
| content | string | 내용 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>후기 수정 `PUT` /api/review/update/{review_id}</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| book | string | 책 제목 |
| subject | string | 제목 |
| content | string | 내용 |
| review_id | number | 후기 일련번호 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>후기 삭제 `DELETE` /api/review/delete</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| review_id | number | 후기 일련번호 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>후기 좋아요 `POST` /api/review/like</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| review_id | number | 후기 일련번호 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>후기 싫어요 `POST` /api/review/dislike</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| review_id | number | 후기 일련번호 |

- Response
    - `204`
    - `422`

</details>

### comment

<details>
<summary>댓글 작성하기 `POST` /api/comment/create/{review_id}</summary>

- Parameters

| name | type | description |
| --- | --- | --- |
| review_id | number | 후기 일련번호 |

- Request body

| name | type | description |
| --- | --- | --- |
| content | string | 내용 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>댓글 수정하기 `PUT` /api/comment/update</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| content | string | 내용 |
| comment_id | number | 댓글 일련번호 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>특정 후기에 달린 댓글 불러오기 `GET` /api/comment/list/{review_id}</summary>

- Parameters

| name | type | description |
| --- | --- | --- |
| review_id | number | 후기 일련번호 |
| page | number | 현재 페이지 |
| size | number | 페이지당 댓글 수 |

- Response
    - `200`
    - `422`

</details>

<details>
<summary>특정 댓글 불러오기 `GET` /api/comment/detail/{comment_id}</summary>

- Parameters

| name | type | description |
| --- | --- | --- |
| comment_id | number | 댓글 일련번호 |

- Response
    - `200`
    - `422`


</details>

<details>
<summary>댓글 삭제 `DELETE` /api/comment/delete</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| comment_id | number | 댓글 일련번호 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>댓글 좋아요 `POST` /api/comment/like</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| comment_id | number | 댓글 일련번호 |

- Response
    - `204`
    - `422`

</details>

<details>
<summary>댓글 싫어요 `POST` /api/comment/dislike</summary>

- Request body

| name | type | description |
| --- | --- | --- |
| comment_id | number | 댓글 일련번호 |

- Response
    - `204`
    - `422`

</details>
