---
layout: post
title: "Claude가 이미 할 수 있는 것들 — 기능·프롬프트 학습 메모"
date: 2026-09-13 00:50:47 +0900
categories: ["Claude"]
tags: ["learning", "agents", "tools", "harness", "skills"]
permalink: /posts/2026-09-13-claude-features-most-people-miss/
---

**한 줄:** Claude를 “채팅창에 질문하는 도구”로만 쓰면, 원문이 말하는 **Projects·Artifacts·Thinking·Memory·역할·브라우저/데스크탑·스케줄·Skills·Code·Design·캐시** 층을 거의 안 쓴다. 이 메모는 지도를 학습용으로 풀고, **문서 층 vs 구조적 하네스** 구분과 **핸즈온 시나리오**까지 붙인다.

[@AnatoliKopadze](https://x.com/AnatoliKopadze)의 X 아티클 [Claude Can Do All of This. Most People Have No Idea.](https://x.com/AnatoliKopadze/status/2057813254617858078)(2026-05-22)을 개념이 쌓이는 순서로 정리한다. 클릭 경로·요금제 세부는 UI가 자주 바뀌므로, **문제 → 기능이 고치는 것 → 원문 프롬프트/예 → 오늘 해볼 시나리오** 축으로 쓴다.  
**초안 작성·문장 정리에 AI를 사용했다.** 해석은 작성자 것이며 원문과 다를 수 있다. 프롬프트·숫자 주장은 원문 그대로다.

- 출처: https://x.com/AnatoliKopadze/status/2057813254617858078
- 작성자: Anatoli Kopadze (@AnatoliKopadze)
- 원제: Claude Can Do All of This. Most People Have No Idea.
- (참고) X 반응 — 좋아요 5,441 · 북마크 23,993 · 노출 약 17.1M · RT 865 (API 메타)

## 이 글이 푸는 문제

새 채팅을 열 때마다 Claude는 **너에 대해 빈 상태**로 시작한다. 이름·일·선호를 매번 다시 설명하고, 답은 텍스트 블록으로만 받고, 역할은 “친절한 어시스턴트” 기본값에 맡긴다. 원문은 그게 **기본 사용**이고, 아래에 깔린 제품·프롬프트 층을 모르면 “Claude가 할 수 있는 것”의 대부분을 놓친다고 본다.

| | 기본 채팅만 | 원문이 가리키는 층 |
|---|---|---|
| 기억 | 매 세션 재설명 | Projects / Memory / CLAUDE.md |
| 결과물 | 코드·문장 복붙 | Artifacts / Design / Code |
| 태도 | 동의·응원 편향 | 하드 멘토·악마의 변호 등 역할 |
| 손 | 네가 복사해 줌 | Chrome / Cowork / Schedule |

기능만 켠다고 워크플로가 자동으로 좋아지지는 않는다. **무엇을 기억하게 할지·어떤 역할로 말리게 할지·어디에 손을 닿게 할지**를 같이 설계해야 한다. 원문 권고: **오늘 하나만**.

## 문서만으로 구조적 하네스가 되나?

**안 된다 — 문서만으로는 플레이북에 가깝다.** 구조적 하네스는 “누가·언제·어떤 도구로·실패를 어떻게 거는지”까지 포함한다. 원문의 기능 목록을 그 렌즈로 나누면 이렇게 보인다.

| 층 | Claude 쪽에서 해당 | 하는 일 |
|---|---|---|
| **문서·규칙 (플레이북)** | Projects 지시, Memory, `CLAUDE.md`, Skills 설명 | 매번 같은 판단·톤·폴더·금지어를 **글로 고정** |
| **구조·동선 (하네스)** | Chrome / Cowork 권한, Schedule, Code 루프, Thinking on/off, 역할(멘토·반론), Artifacts/Design 산출 채널 | **손이 닿는 범위·실행 주기·검증·역할**을 고정 |

문서로 규칙을 세우고, 그 위에 도구·루프·게이트(역할 반박, Thinking, settle에 가까운 “성공 기준”)를 얹는 식이 맞다. 문서만 두껍게 하면 **스킬**에 가깝고, 손·루프 없이 “구조”라고 부르기 어렵다. 반대로 도구만 열고 문서가 없으면 매 세션이 제로에서 다시 설계된다.

이 메모의 핸즈온도 같은 순서를 따른다. **먼저 Projects/`CLAUDE.md`(문서) → 그다음 Artifacts·Chrome·Schedule·Code(구조)** .

## 한눈에 보는 지도

| # | 이름 | 한 줄 | 없으면 |
|---|---|---|---|
| 1 | Projects | 문서·상시 지시 고정 | 매 채팅 제로 |
| 2 | Artifacts | 옆 패널에 **돌아가는** 앱 | 코드만 복사 |
| 3 | Thinking | 답 전 단계 추론 표시 | 복잡한 결정에서 얕음 |
| 4 | Memory | 장기 프로필(기본 off) | 매번 자기소개 |
| 5–9 | 역할 프롬프트 | 멘토·반론·연습 등 | 동의 머신 |
| 10 | Chrome | 탭을 보고 클릭·폼 | 수동 복붙 |
| 11 | Cowork | 로컬 파일 직접 | 웹만 |
| 12 | Scheduled Tasks | 시각에 자동 실행 | 매번 네가 켬 |
| 13 | Skills | 능력 세트 설치 | 같은 설명 반복 |
| 14 | CLAUDE.md | 세션마다 자동 규칙 | 규칙 증발 |
| 15 | Claude Code | IDE/터미널 코딩 루프 | 스니펫만 |
| 16 | Claude Design | 시각·덱 (`claude.ai/design`) | 긴 디자인 세션 |
| 17 | Prompt Caching | API 큰 컨텍스트 캐시 | 매 호출 재처리 |

---

## 1. Projects — “기억되는 Claude”

**문제.** 채팅을 새로 열면 맥락이 사라진다.  
**기능.** 프로젝트를 만들고 문서를 올리고 **Project Instructions**에 상시 규칙을 쓴다. 다음 주에도 같은 프로젝트 안에서 이어진다. 원문: 이 아티클에서 하나만 고친다면 **Projects를 먼저**.

원문이 넣는 예시 골격(뉴스레터 프로젝트): About(독자·톤·규모) / Writing rules(짧은 문단, 금지 단어, 숫자>형용사) / Content rules(기본 개념 설명 금지, 반직관으로 리드) / File structure(`/drafts`, `/published`, `/research`).

### 핸즈온 A — 30분 Projects
1. 프로젝트 하나 생성. 이름 예: `TheCosmicPine` 또는 `업무-노트`.  
2. Project Instructions에 5~10줄: 네가 누구인지, 독자/동료, **싫어하는 답 형식**, 파일 규칙.  
3. 관련 md/PDF 2~3개 업로드.  
4. **새 채팅을 프로젝트 안에서** 열고, 맥락을 다시 안 설명한 채 “지난번에 말한 톤으로 초안 한 단락”만 요청.  
5. 성공 기준: 네가 다시 소개하지 않아도 톤·금지어가 지켜짐.

원문 Memory용 “나를 기억해” 프롬프트도 같은 층이다 — 이름·역할·초점·선호 말투·annoying 패턴을 한 번 저장하라고 시킴. Projects와 Memory를 섞어 쓰지 말고, **먼저 Projects 하나로** 감을 잡아도 된다.

---

## 2. Artifacts — 텍스트가 아니라 동작

**문제.** “코드만 주고 끝”이면 실행은 네 몫.  
**기능.** 옆 패널에 계산기·트래커·게임·차트처럼 **클릭되는 산출물**. SVG·인터랙티브 차트·Mermaid. 원문: 무료에서도 가능, 대부분 안 써 봄.

원문 즉시 프롬프트:

```
Build me a habit tracker as a working web app.

I want to track 5 daily habits.
Each day I can check them off.
Show a 7-day streak counter for each habit.
If I miss a day, the streak resets.

Design: dark background, clean minimal look.
Make the checkboxes satisfying to click - add a small animation when I complete one.
The data should persist if I refresh the page.
```

학습 포인트: 기술 스택을 묻지 말고 **동작·UX·지속성**을 적는다.

### 핸즈온 B — Artifacts 15분
1. 새 채팅(가능하면 Projects 안).  
2. 위 프롬프트를 그대로 붙여 넣고 Artifact로 연다.  
3. 체크 → 새로고침 → 데이터가 남는지 확인.  
4. 한 줄만 추가 요청: “습관 이름을 한국어로 바꾸고, 스트릭이 깨지면 빨간 테두리”.  
5. 성공 기준: 코드 복붙 없이 패널에서 동작.

---

## 3. Adaptive / Extended Thinking — 생각 과정을 보이게

**문제.** 복잡한 결정을 한 번에 답하면 패턴 매칭에 가깝다.  
**기능.** 켜면 단계적 추론을 거친 뒤 답한다. 단순 Q&A엔 과함. 원문: 같은 질문을 Thinking on/off로 **비교**해 보라.

원문 결정 프롬프트 골격: Option A/B + 상황 → 2·3차 결과, 감정적으로 과대/과소 평가, 빠진 정보, downside protection → **추천과 이유**.

### 핸즈온 C — Thinking 비교 20분
1. 실제 고민 하나를 A/B로 적는다 (이직 vs 잔류, 도구 A vs B 등).  
2. Thinking **끄고** 한 번, **켜고** 한 번.  
3. 표로: 가정 / 리스크 / 추천이 어떻게 달라졌는지 세 줄.  
4. 성공 기준: off 답에서 빠진 2·3차 결과가 on에 나타나는지 눈으로 확인.

---

## 4. Memory — 기본이 꺼져 있음

**문제.** 새 채팅마다 자기소개.  
**기능.** 켜면 직업·프로젝트·말투가 쌓여 새 채팅에도 맥락이 온다. 원문: 존재 자체를 모르는 사람이 많다. 설정·프라이버시는 계정에서 확인.

### 핸즈온 D — Memory 10분
1. Memory on.  
2. 원문 스타일로 “나를 기억해” 블록을 채운다 (이름·역할·현재 초점·말투·annoying).  
3. **완전히 새 채팅**에서 “내가 지금 뭐에 집중하는지 한 줄로”만 묻는다.  
4. 성공 기준: 재설명 없이 맞게 말함. 틀리면 정정하고 한 번 더.

---

## 5–9. 역할 프롬프트 — 동의 머신을 깨기

**문제.** 기본 Claude는 아이디어에 더하고 긍정한다. 원문: 그게 **거의 항상 틀린 기본값**.  
**기능.** 채팅 서두에 역할을 박으면 질문·반박·거절 방식이 바뀐다.

| 역할 | 하는 일 | 원문이 말하는 쓰임 |
|---|---|---|
| CBT-style (역할) | 조언 대신 질문·인지 왜곡 지적 | 왔다 갔다 하는 고민 |
| Hard mentor | 동의 끄고 약점·빈칸 | 비싼 실수 전 |
| Personal trainer | 일정·장비·부상 반영 12주 | 일반 루틴 사이트 대체 |
| Conversation practice | 상대 역할 + 디브리프 | 어려운 대화 전 |
| Devil’s advocate | 결정 **반대만** 최강으로 | 이미 마음 정한 직후 |
| Content research assistant | 반직관 각도·스토리 프레임 | 뉴스레터 리서치 |

**Hard mentor** 규칙(원문): 틀리면 구체적으로 반박 / 보고 싶지 않은 빈칸 / 어려운 질문 / “다른 한편으로는” 금지 / 끝은 **앞으로 가기 전 한 가지**.  
**Devil’s advocate**(원문): 긍정 균형 없음 · 가정 · 실패 3경로 · 과소평가 · “이게 진짜로 나쁘려면 뭘 믿어야 하나”.

주의: therapist 프롬프트는 **역할 연기**다. 실제 의료·상담 대체가 아니다.

### 핸즈온 E — 역할 2연타 25분
1. 확신 큰 아이디어 한 줄을 적는다.  
2. **Hard mentor** 프롬프트(원문)로 새 채팅 → 아이디어 붙여넣기.  
3. 같은 결정을 **Devil’s advocate** 채팅에서 다시.  
4. 노트에 “둘 다 공통으로 찌른 가정” 3개만 남긴다.  
5. 성공 기준: 응원 문장보다 **구체적 반박**이 더 김.

---

## 10. Claude in Chrome — 탭을 보는 손

**문제.** 다른 탭에서 Claude ↔ 페이지 복붙.  
**기능.** 확장으로 활성 탭을 보고 클릭·폼·이동. 원문: Chrome Web Store에서 설치 → 계정 로그인 → 사이드바.

원문 예 작업: 채용 목록 페이지에서 title / company / salary / 상위 3요건 추출 → 급여순 표 → **다음 페이지까지** 반복.

### 핸즈온 F — Chrome 20분
1. 확장 설치·로그인.  
2. 공개 채용/목록 페이지를 연다 (로그인·결제 화면은 피함).  
3. 원문 추출 프롬프트를 그대로 준다.  
4. 표가 나오면 한 페이지만 맞는지 눈으로 샘플 3행 검증.  
5. 성공 기준: 복붙 없이 표가 생김. (사이트 ToS·개인정보는 네가 책임.)

---

## 11–14. Cowork · Schedule · Skills · CLAUDE.md

**Cowork.** 데스크탑 앱이 파일 시스템을 직접 읽기/쓰기/정리. 웹 Claude의 “붙여넣기 병목”을 줄인다.  
**Scheduled Tasks.** 한 번 설정 후 시각·주기에 자동 실행. 원문 예: 평일 07:30 AI·크립토 뉴스 5건 → `brief-[date].md` (3분, fluff 금지).  
**Skills.** Cowork Customize → Skills / Browse plugins. 파워포인트·PDF 등 능력 세트를 설치하면 해당 작업에 자동 사용.  
**CLAUDE.md.** 프로젝트 폴더에 두면 **매 세션 시작 시 자동 로드** — 코딩 컨벤션·문체·사내 용어·브랜드.

### 핸즈온 G — “손이 닿는 층” 중 하나 30분
선택 1) **Schedule:** 원문 브리프 태스크를 그대로 스케줄에 넣고, 다음 평일 아침 `briefs/`에 파일이 생기는지 확인.  
선택 2) **CLAUDE.md:** 로컬 프로젝트 루트에 금지 단어·폴더 규칙 20줄 → 새 세션에서 “초안 써”만 하고 규칙 준수 여부 확인.  
선택 3) **Skills:** Browse plugins에서 문서/슬라이드 관련 하나 설치 → “이 메모를 1페이지 요약 슬라이드 골격으로” 한 번.  
성공 기준: 매 채팅에 같은 규칙을 **다시 안 적어도** 됨.

---

## 15–16. Claude Code · Claude Design

**Code.** 채팅 스니펫이 아니라 실제 환경에서 코드베이스를 읽고, 쓰고, 테스트를 돌리고, 에러를 읽어 고치는 루프. VS Code/JetBrains, GitHub Actions로 PR 리뷰/작성.  
**Design.** Anthropic Labs 쪽 시각 도구 — 원페이저·피치덱·프로토타입. `claude.ai/design`. PPTX/Canva/PDF/HTML. 원문: 디자이너가 아니면 3시간 Figma를 10분 대화로.

### 핸즈온 H — Code 또는 Design 40분
Code: 작은 레포에서 “테스트 실패 하나 고치고 PR 설명 초안”만 맡긴다. 네가 디프를 읽고 머지 여부만 결정.  
Design: Design에서 “블로그 소개 원페이저, 다크, 한 줄 가치제안” → HTML 또는 PDF 내보내기.  
성공 기준: **네가 복붙한 코드 블록이 아니라** 환경/내보내기 결과물이 남음.

---

## 17. Prompt Caching (API, 개발)

**문제.** 큰 system/문서/코드베이스를 **매 호출** 다시 넣으면 비용·지연.  
**기능.** `cache_control: ephemeral`로 서버 측 캐시. 원문 주장: 캐시 히트 시 캐시 토큰 **최대 약 90% 저렴** + 응답 빨라짐. **5분** 유지, 사용 시 타이머 리셋. system·큰 문서·tool 정의에 적용.

### 핸즈온 I — 캐시 개념 확인 (코드 있는 사람)
1. 긴 system 텍스트를 ephemeral로 두고, 유저 메시지만 바꿔 두 번 호출.  
2. 응답/사용량 메타에서 캐시 히트 여부를 확인(제공사 필드 기준).  
3. 성공 기준: “전체 청구 1/10”이 아니라 **캐시된 블록**이 싸졌는지 구분해서 기록. (90%는 원문의 캐시 토큰 주장.)

---

## 주간 핸즈온 로드맵 (원문 정신)

| 요일 | 하나만 |
|---|---|
| Day 1 | 핸즈온 A Projects |
| Day 2 | 핸즈온 B Artifacts |
| Day 3 | 핸즈온 C Thinking 또는 E 역할 |
| Day 4 | 핸즈온 D Memory 또는 G CLAUDE.md |
| Day 5 | 핸즈온 F Chrome **또는** H Code/Design |

한꺼번에 17개를 켜지 않는다. 원문 마무리: 존재만 알아도 절반, **오늘 하나만**.

## 한계

기능명·요금·UI는 시점에 따라 바뀐다(원문 2026-05). 역할 프롬프트 ≠ 전문가 면허. Prompt Caching 90%는 **캐시된 토큰** 주장이지 전체 청구 보장 아님. Chrome/Cowork에 탭·파일 권한을 주면 보이는 것까지 손이 닿는다 — 비밀·결제 화면은 분리. 핸즈온의 “성공 기준”은 내 정리이며, 원문은 프롬프트·기능 설명 중심이다.

## 남는 한 줄

Claude의 기본 채팅은 입구일 뿐이다. **문서(규칙)와 구조(손·루프·역할)** 를 하루에 하나씩 얹을 때 “매일 쓰는 도구”가 된다. 문서만으로 하네스가 완성되지는 않는다.

*학습용 정리. 프롬프트·수치는 원문. AI 보조 작성.*
