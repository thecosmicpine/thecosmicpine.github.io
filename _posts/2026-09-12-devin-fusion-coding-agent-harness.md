---
layout: post
title: "Devin Fusion — Lead+Sidekick 하네스가 가리키는 것"
date: 2026-09-12 14:39:32 +0900
categories: ["Tool"]
permalink: /posts/2026-09-12-devin-fusion-coding-agent-harness/
---

**한 줄:** Fusion은 Devin용 **Lead+Sidekick 이중 에이전트 하네스**이고, 같은 “코딩 에이전트”라도 Claude Code·Cursor·Aider·OpenHands는 하네스 구조가 다르다.

Cognition이 2026-09-11에 공개한 [Local Fusion](https://cognition.com/blog/local-fusion)과 [@dabit3 소개](https://x.com/dabit3/status/2098557144580735156)를 **인사이트**로 읽은 메모다. 설치 절차는 다루지 않는다.  
**초안 작성·문장 정리에 AI를 사용했다.** 해석은 작성자 것이며 원문과 다를 수 있다. 벤치 숫자는 Cognition·Artificial Analysis 쪽 주장이며 교차검증 전에는 과신하지 않는다. 라이선스는 2026-09-12 확인분(추측 없음).

## 남는 통찰

코딩 에이전트 논쟁의 축이 “어느 모델이 더 세냐”에서 **“모델을 어떻게 태우느냐(하네스)”** 로 옮겨 가고 있다. Fusion이 밀어주는 대립은 이것이다.

- **단순 라우팅:** 프롬프트만 보고 쉬운 일은 싼 모델, 어려운 일은 프론티어 — 그런데 “버그 고쳐”가 한 줄인지 전면 재설계인지는 조사 전에는 모른다. mid-task에 모델을 바꾸면 프롬프트 캐시도 깨진다.
- **Fusion:** Lead(프론티어)가 세션을 총괄하고, Sidekick(저렴·효율)에 **브리프·제약·성공 기준**만 넘긴다. 탐색·구현·테스트는 Sidekick, 계획·모호함·리뷰는 Lead. 대화 전체를 넘기지 않고 각자 컨텍스트·캐시를 유지한다.

즉 Fusion은 “싼 모델에 맡기고 기도”가 아니라, **프론티어가 항상 책임자인 이중 에이전트**다.

## Fusion이 뭔가 (개념)

- Devin Desktop·CLI에서 코드 작성·수정용 옵션.
- Lead + Sidekick **두 모델을 고른다**. Cognition 추천 페어: **Fable 5.1 + SWE-2**.
- 블로그 주장: 다른 모델 하네스 대비 최대 약 **39%** 더 효율(Artificial Analysis Coding Agent Index 등과의 평가 맥락). 표의 벤치별 비용 절감률은 Cognition 게시물 표 기준.
- 추가 관찰(원문): 토큰단가 비싼 Lead가 오히려 **태스크당 비용**을 낮출 수 있다 — 위임·브리프 품질이 왕복을 줄이기 때문. Sidekick도 “더 강한 쪽”이 리뷰 라운드를 줄여 Lead를 싸게 만들 수 있다고 한다. 평가 단위를 **price per token → price per task**로 옮기자는 메시지다.

## 용어: 코딩 에이전트 하네스

모델 위의 **운영 틀**이다. 도구 호출, 계획→실행→검증, 컨텍스트·캐시, 역할 분담이 여기 들어간다.  
모델 = 엔진, 하네스 = 차체·운전 규칙.

**하네스 라이선스 ≠ LLM API 약관.** 표의 라이선스는 하네스 코드/제품 기준이고, 호출하는 LLM API는 별도 약관·과금이다.

## 비교표 (구조·라이선스)

벤치 점수·달러는 제품·시점에 따라 달라지니, 형태·모델 운용·라이선스만 잡는다. 라이선스 열은 2026-09-12 확인.

| 하네스 | 형태 | 모델 운용 | 라이선스(확인된 것) | Fusion과 다른 점 |
|---|---|---|---|---|
| Devin Fusion | Desktop / CLI / Cloud | Lead + Sidekick 이중 | 상용 제품(Cognition). OSS 아님 — 이용약관·요금제 | 기준 |
| Devin 일반 | 클라우드·비동기 | 제품 모델 믹스 | 상용 제품(Cognition). OSS 아님 — 이용약관·요금제 | Fusion은 이중 에이전트 옵션 |
| Claude Code | 터미널 CLI | 단일 + 서브에이전트/스킬 | 독점. GitHub LICENSE.md: © Anthropic, Commercial Terms of Service | 오케스트레이션·훅이 두꺼움 |
| Cursor Agent / Cloud | IDE + 클라우드 VM | Composer·Rules / MCP | 상용 IDE·서비스(비OSS). Cursor ToS | 인라인 UX |
| OpenAI Codex | CLI + Cloud | 제품 모델 | CLI(`openai/codex`): **Apache-2.0**<br>Cloud/웹: OpenAI·ChatGPT 서비스 약관(별도) | 표면이 넓음 |
| Aider | 로컬 CLI | BYOM | **Apache-2.0** | git diff가 투명 |
| OpenHands | OSS | BYOM ReAct | 코어 **MIT**; `enterprise/` 는 PolyForm Free Trial(비OSS, 연 30일 제한 등) | 오픈소스 프레임워크 |
| SWE-agent | 연구 ACI | 단일 | **MIT**(princeton-nlp/SWE-agent) | 제약된 명령 인터페이스 |
| 단순 라우터 | 패턴 | 프롬프트로 모델 1개 선택 | 해당 없음(단일 제품 아님) | Fusion이 피하려는 방식 |

## 한 줄 지도 (언제 무엇을)

- 비용↓ + 프론티어 리뷰를 한 세션에 → **Fusion**
- 터미널·훅·스킬 중심 → **Claude Code**
- 에디터 안 인라인 → **Cursor**
- git diff 투명·로컬 BYOM → **Aider**
- OSS 프레임워크로 조립 → **OpenHands**

## 출처

- Cognition, *Introducing Fusion in Devin Desktop & CLI* (2026-09-11): https://cognition.com/blog/local-fusion
- @dabit3: https://x.com/dabit3/status/2098557144580735156
- (추가 참고 가능) Artificial Analysis coding agents · arXiv:2609.00006 Harness Engineering · OpenHands docs · SWE-agent 논문
- 라이선스 확인일: 2026-09-12 (각 제품 LICENSE/ToS·공개 표기 기준)

*인사이트용 정리. 벤치는 원문 주장. AI 보조 작성.*
