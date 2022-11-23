# 가계부 서비스 API 개발

### ✅ <b>DRF</b>를 활용하여 가계부 서비스 서버의 <b>REST API</b>를 개발한 프로젝트 입니다.
### <b>JWT</b>를 이용하여 유저 인증을 하고, 기능에 따라 권한을 제한합니다.

<br>

## 🛠 사용 기술
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white">
<img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=MySQL&logoColor=white">
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=DockerL&logoColor=white">
<img src="https://img.shields.io/badge/NGINX-009639?style=flat&logo=NGINX&logoColor=white">
<img src="https://img.shields.io/badge/Guicorn-499848?style=flat&logo=Gunicorn&logoColor=white">
<img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=Git&logoColor=white">

<br>

## 📙 API 명세서
<img width="1034" alt="스크린샷 2022-08-25 오후 7 42 56" src="https://user-images.githubusercontent.com/76423946/186644463-af56a8ef-af10-4a26-8f1f-ced1f7dcb061.png">

- 유저 인증, 인가는 jwt 방식을 사용합니다. 
- 로그인할 경우, access 토큰과 refresh 토큰이 발급 됩니다. access 토큰은 유효시간이 20분으로 짧게 설정되어있기 때문에, 만료될 경우 함께 발급받은 refresh 토큰으로 재발급 받을 수 있습니다.
- 기능에 따라 권한을 제한하기 위해 커스텀 permission을 사용합니다. (IsOwnerOrAuthenticatedCreateOnly)
```
기본적으로 가계부 관련 모든 기능은 로그인 해야만 이용가능합니다.
그 중, 가계부 생성의 기능을 제외하고 조회, 수정, 삭제, 복구는 관리자와 작성자 본인만 이용 가능하기 때문에
커스텀 permission에서 POST 메소드를 제외한 나머지 메소드에서 특정 객체에 대한 권한을 확인하도록 개발 하였습니다.
``` 
- 가계부, 가계부 기록의 목록 조회의 경우에는 'is_deleted_파라미터의 유무로 삭제된 항목들을 보여줄 수 있습니다.

<details>
<summary>🚀 API 호출 테스트 결과</summary>
<div markdown="1">
<ul>
  <li>
    <p>회원가입</p>
    <img width="628" alt="스크린샷 2022-08-25 오후 8 31 25" src="https://user-images.githubusercontent.com/76423946/186653240-ab439a3d-bada-4a63-8f40-4aa5705ceb20.png">
  </li>
  <li>
    <p>로그인</p>
    <img width="744" alt="스크린샷 2022-08-25 오후 8 31 58" src="https://user-images.githubusercontent.com/76423946/186653344-2b0ba825-7fe0-4a52-8f40-514a9758238d.png">
  </li>
  <li>
    <p>토큰 재발급</p>
    <img width="742" alt="스크린샷 2022-08-25 오후 8 32 40" src="https://user-images.githubusercontent.com/76423946/186653456-33c62d7e-e51a-4752-86d5-914f3ba73164.png">
  </li>
  <li>
    <p>가계부 생성</p>
    <img width="742" alt="스크린샷 2022-08-25 오후 8 34 11" src="https://user-images.githubusercontent.com/76423946/186653617-bca90128-ff02-4787-b07d-fe9aa1f21fef.png">
  </li>
  <li>
    <p>가계부 목록 조회</p>
    <img width="749" alt="스크린샷 2022-08-25 오후 8 35 14" src="https://user-images.githubusercontent.com/76423946/186653843-bc452238-b186-4396-bc76-3d0dc1e3cd29.png">
  </li>
  <li>
    <p>삭제된 가계부 목록 조회</p>
    <img width="746" alt="스크린샷 2022-08-25 오후 8 37 06" src="https://user-images.githubusercontent.com/76423946/186654251-9dd4eafc-0bd4-48cd-a3f8-33f8eef1253d.png">
  </li>
  <li>
    <p>가계부 수정</p>
    <img width="746" alt="스크린샷 2022-08-25 오후 8 38 16" src="https://user-images.githubusercontent.com/76423946/186654496-b157c8f5-07ec-49fb-9c91-12011860b77a.png">
  </li>
  <li>
    <p>가계부 삭제</p>
    <img width="746" alt="스크린샷 2022-08-25 오후 8 36 36" src="https://user-images.githubusercontent.com/76423946/186654165-538fe9af-530c-406f-a734-b212ab97b6cc.png">
  </li>
  <li>
    <p>가계부 복구</p>
    <img width="746" alt="스크린샷 2022-08-25 오후 8 39 04" src="https://user-images.githubusercontent.com/76423946/186654670-f2f64ee4-3f18-42ea-8860-6e46af85e00e.png">
    </li>
  <li>
    <p>가계부 기록 생성</p>
    <img width="743" alt="스크린샷 2022-08-25 오후 8 40 00" src="https://user-images.githubusercontent.com/76423946/186654916-2307173f-8fc4-45ab-ba5c-9e4de0470a22.png">
  </li>
  <li>
    <p>가계부 기록 목록 조회</p>
    <img width="751" alt="스크린샷 2022-08-25 오후 8 41 17" src="https://user-images.githubusercontent.com/76423946/186655157-502c2e69-781e-456e-8cc7-82f7bbe44c18.png">
  </li>
   <li>
    <p>가계부 기록 상세 조회</p>
    <img width="749" alt="스크린샷 2022-08-25 오후 8 42 27" src="https://user-images.githubusercontent.com/76423946/186655373-d04c10cc-08d5-43c0-b747-c7c8f6a71e00.png">
  </li>
  <li>
    <p>가계부 기록 수정</p>
    <img width="749" alt="스크린샷 2022-08-25 오후 8 43 59" src="https://user-images.githubusercontent.com/76423946/186655724-ffe2cec2-dc8b-423d-b978-c07da8009649.png">
  </li>
  <li>
    <p>가계부 기록 삭제</p>
    <img width="749" alt="스크린샷 2022-08-25 오후 8 44 44" src="https://user-images.githubusercontent.com/76423946/186655821-a8880973-5b62-449d-bb11-4f7cedf769b4.png">
  </li>
  <li>
    <p>가계부 기록 복구</p>
    <img width="749" alt="스크린샷 2022-08-25 오후 8 45 20" src="https://user-images.githubusercontent.com/76423946/186655943-12de22f3-0673-4753-a4d6-88902a93884b.png">
  </li>
</ul>
</div>
</details>

<br>

## 📋 ERD
<img width="664" alt="스크린샷 2022-08-25 오후 7 57 49" src="https://user-images.githubusercontent.com/76423946/186647131-41ee7b44-ade9-48cc-9bc2-f2fb35985217.png">

- 가계부를 생성하고 가계부 마다 소득, 소비 내역을 기록할 수 있도록 AccountBook 모델과 AccountBookRecord 모델로 분리하고 두 테이블의 관계를 1:N으로 설정하였습니다.
- AccountBook 모델의 balance 필드는, 가계부 생성시 초기비용을 의미합니다.
- AccountBookRecord 모델의 amount 필드는 내역의 금액을 의미하며, 소득 내역일 경우 <b>양수이고</b> 소비 내역일 경우 <b>음수</b>로 기록할 수 있습니다.

<br>

## 🌍 배포
#### Docker, NginX, Gunicorn을 사용하여 AWS EC2 서버에 배포하였습니다.
➡️ [서비스 주소](13.124.201.55)

### 서비스 아키텍쳐
<img width="733" alt="스크린샷 2022-08-25 오후 8 19 58" src="https://user-images.githubusercontent.com/76423946/186651143-2494ef56-2111-4c9f-9b4c-a7d6442a6bbd.png">

<br>

## 🌱 테스트
<img width="505" alt="스크린샷 2022-08-25 오후 8 25 01" src="https://user-images.githubusercontent.com/76423946/186652086-58792373-2131-41c7-8661-59d21d4e1019.png">
<img width="614" alt="스크린샷 2022-08-25 오후 8 24 23" src="https://user-images.githubusercontent.com/76423946/186651886-d8ff49d8-c8ca-4712-b7ce-317ad1ee5207.png">

- Django에 내장된 테스트 모듈을 사용하여 유닛테스트를 진행하였습니다.
- 테스트 케이스를 작성함으로써, api와 관련된 코드에 수정사항이 생겼을때 정상작동의 여부를 간편하게 확인할 수 있었습니다. 

<br>

## ✨ Git 컨벤션, 코드 컨벤션
- git commit message template
```
# --- 제목(title) - 50자 이내로 ---
# <타입(type)> <제목(title)>
# 예시(ex) : Docs : #1 README.md 수정
# --- 본문(content) - 72자마다 줄바꾸기  ---
# 예시(ex) :
# - Workflow
# 1. 커밋 메시지에 대한 문서 제작 추가.
# 2. commit message docs add.
# --- 꼬리말(footer) ---
# <타입(type)> <이슈 번호(issue number)>
# 예시(ex) : Fix #122
# --- COMMIT END ---
# <타입> 리스트
#   Init    : 초기화
#   Feat    : 기능추가
#   Add     : 내용추가
#   Update  : 기능 보완 (업그레이드)
#   Fix     : 버그 수정
#   Refactor: 리팩토링
#   Style   : 스타일 (코드 형식, 세미콜론 추가: 비즈니스 로직에 변경 없음)
#   Docs    : 문서 (README.md, ignore파일 추가(Add), 수정, 삭제)
#   Test    : 테스트 (테스트 코드 추가, 수정, 삭제: 비즈니스 로직에 변경 없음)
#   Chore   : 기타 변경사항 (빌드 스크립트 수정 등)
#   Rename  : 이름(파일명, 폴더명, 변수명 등)을 수정하거나 옮기는 작업만인 경우
#   Remove  : 파일을 삭제하는 작업만 수행한 경우    
# ------------------
#     제목 첫 글자를 대문자로
#     제목은 명령문으로
#     제목 끝에 마침표(.) 금지
#     제목과 본문을 한 줄 띄워 분리하기
#     본문은 "어떻게" 보다 "무엇을", "왜"를 설명한다.
#     본문에 여러 줄의 메시지를 작성할 땐 "-" 혹은 "번호"로 구분
# ------------------
```
- git branch
```
main-feature의 flow로 진행합니다.

feature 브랜치 네이밍: feature/#{이슈번호}
```
- Code convention
```
- Class
    - Pascal case
- Function
    - snake case
- Variables
    - snake case
```

<br>

## 🖇 Lint, Formatter
<img width="723" alt="스크린샷 2022-07-26 오후 9 42 37" src="https://user-images.githubusercontent.com/76423946/181008499-a05933c7-c471-43a3-be6d-915a584724ad.png">

- isort, black, flake8을 이용하여 린트와 포메터를 설정했습니다.
- pre-commit 라이브러리를 이용하여 commit 전에 위 세 가지 라이브러리들을 실행시켜 코드를 일관화 합니다.

<br>

## 📌 태스크 관리
<img width="1132" alt="스크린샷 2022-08-25 오후 8 21 14" src="https://user-images.githubusercontent.com/76423946/186651347-16eb290e-f078-47cb-b8f7-e1c5e82531ef.png">


[프로젝트 링크](https://github.com/users/my970524/projects/4)
- 태스크를 깃허브의 issue로 생성하고 칸반보드로 관리하였습니다.
