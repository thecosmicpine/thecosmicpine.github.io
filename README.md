# Sungwoon Lee's Blog

개인 블로그 - GitHub Pages + Jekyll

**Live Site:** [https://hs-billion.github.io](https://hs-billion.github.io)

## 포스트 작성 방법

1. `_posts/` 디렉토리에 새 파일 생성
2. 파일명 형식: `YYYY-MM-DD-title.md` (예: `2026-09-05-my-post.md`)
3. 파일 상단에 Front Matter 추가:

```markdown
---
layout: post
title: "포스트 제목"
date: YYYY-MM-DD HH:MM:SS +0900
categories: [카테고리1, 카테고리2]
---

여기에 본문 작성...
```

4. 변경사항을 커밋하고 푸시하면 자동으로 배포됩니다.

## 로컬 개발 환경 (선택사항)

```bash
# 의존성 설치
bundle install

# 로컬 서버 실행
bundle exec jekyll serve

# 브라우저에서 http://localhost:4000 접속
```

## 방문자 확인

이 블로그는 **외부 분석 도구를 사용하지 않습니다** (Google Analytics, GoatCounter 등 제외).

방문자 통계는 GitHub 저장소 관리자만 확인할 수 있습니다:

1. GitHub 저장소 페이지 접속: [https://github.com/hs-billion/hs-billion.github.io](https://github.com/hs-billion/hs-billion.github.io)
2. **Insights** 탭 클릭
3. 왼쪽 메뉴에서 **Traffic** 선택
4. 최근 14일간의 방문자 통계 확인:
   - **Unique visitors** (순 방문자 수)
   - **Views** (조회수)

> **참고:** GitHub Insights는 저장소 소유자만 접근 가능하며, 방문자 데이터는 최근 14일간만 제공됩니다. 쿠키나 외부 추적 스크립트를 사용하지 않아 방문자 프라이버시를 보호합니다.

## 기술 스택

- Jekyll (GitHub Pages 호환)
- Minima theme
- GitHub Pages 자동 배포
