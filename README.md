![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)

# BOOKSNAP

Instagram 클론코딩을 참고하여 만든 **독서 기록 웹 서비스**입니다.
사용자는 책 사진을 업로드하고 독서 기록을 남길 수 있습니다.
이 웹 서비스의 이름인 **BOOKSNAP** 또한 이러한 의미를 담고 있습니다.
다른 사용자의 기록을 피드 형식으로 확인할 수 있는 서비스를 목표로 합니다.

---

## Project Goal

- Django 기반 웹 서비스 구조 이해
- SNS 아키텍처 직접 구현
- 기능 단위 개발 및 Git 버전 관리 연습
- 실제 서비스 형태의 포트폴리오 구축

---

## Tech Stack

- Python 3.14
- Django
- Bootstrap 5
- SQLite3
- Git / GitHub

---

## Implemented Features

- navbar 레이아웃 구현(BOOKSNAP 로고 제작 포함)
- 회원가입 / 로그인 기능
- 게시글 업로드 (이미지 + 텍스트)
- 피드 화면 구현
    - 좋아요 기능
    - 북마크 기능 
    - 댓글 기능
- 프로필 페이지
  - 프로필 수정
  - 내가 올린 피드 모아보기
  - 좋아요 / 북마크 피드 모아보기

---

## In Progress

- 회원가입 / 로그인 기능
- 게시글 업로드 (이미지 + 텍스트)
- 피드 화면 구현
- 좋아요 기능
- 댓글 기능
- 프로필 페이지

---

## Roadmap

- 팔로우 기능
- 프로필 페이지
  - 팔로워 / 팔로잉 수 표시
  - 팔로워 / 팔로잉 목록 조회
- 다른 사람 프로필로 이동 기능
- 게시글 업로드(확장)
  - 읽은 페이지, 장르, 제목, 작가 입력
  - 해시태그 기반 관련 게시물 추천
- 독서 통계 기능
  - 워간 / 연간 독서 기록

---

## Current Structure
```
Reading-Record-WEB
├─ INSTAGRAM/
├─ static/
│ └─ images/
├─ templates/
├─ manage.py
├─ requirements.txt
├─ .gitignore
```
---

## 🏃 Run Locally

```bash
git clone https://github.com/lizzyeon/Reading-Record-WEB.git
cd Reading-Record-WEB

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```
---

## Development Log

개발 과정 및 문제 해결 기록은 DEVLOG.md 파일에 정리하고 있습니다.


