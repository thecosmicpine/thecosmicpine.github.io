---
layout: post
title: "Devin Fusion — Lead+Sidekick 하네스가 가리키는 것"
date: 2026-09-12 14:39:32 +0900
categories: ["Tool"]
tags: ["devin", "harness", "agents", "fusion"]
permalink: /posts/2026-09-12-devin-fusion-coding-agent-harness/
---

**한 줄:** Fusion은 Devin용 **Lead+Sidekick 이중 에이전트 하네스**이고, 같은 “코딩 에이전트”라도 Claude Code·Cursor·Aider·OpenHands는 하네스 구조가 다르다. 가격 이야기의 축은 token당이 아니라 **태스크당**이다.

Cognition이 2026-09-11에 공개한 [Local Fusion](https://cognition.com/blog/local-fusion)과 [@dabit3 소개](https://x.com/dabit3/status/2098557144580735156)를 다시 짠 메모다. 설치 절차는 다루지 않는다.  
**초안 작성·문장 정리에 AI를 사용했다.** 해석은 작성자 것이며 원문과 다를 수 있다. 벤치·달러 숫자는 Cognition(및 그들이 인용한 Artificial Analysis·Vals AI) 주장이며 교차검증 전에는 과신하지 않는다. 라이선스는 2026-09-12 확인분(추측 없음).

## 이 글이 푸는 문제

코딩 에이전트 논쟁의 축이 “어느 모델이 더 세냐”에서 **“모델을 어떻게 태우느냐(하네스)”** 로 옮겨 가고 있다. 싼 모델에만 맡기거나, 프롬프트만 보고 모델을 갈아끼우는 **단순 라우팅**은 겉보기엔 싸 보이지만, “버그 고쳐”가 한 줄인지 전면 재설계인지는 조사 전에는 모른다. mid-task에 모델을 바꾸면 프롬프트 캐시도 깨진다.

Fusion이 밀어주는 대립은 이것이다.

| | 단순 라우팅 | Fusion (Lead + Sidekick) |
|---|---|---|
| 누가 책임자인가 | 초기에 고른 모델 1개 | **Lead(프론티어)가 세션 총괄** |
| 위임 | 프롬프트 난이도 추정 | Lead가 **브리프·제약·성공 기준**만 넘김 |
| 컨텍스트 | mid-task 교체 시 캐시 깨지기 쉬움 | 각자 컨텍스트·캐시 유지, 대화 전체는 안 넘김 |
| 실패 모드 | 싼 모델에 맡기고 기도 | Lead가 리뷰·회수 가능 |

즉 Fusion은 “싼 모델에 맡기고 기도”가 아니라, **프론티어가 항상 책임자인 이중 에이전트**다. 하네스만 켠다고 비용·품질이 자동으로 좋아지지는 않는다 — Lead·Sidekick 페어와 브리프 품질이 태스크당 비용을 가른다.

## Fusion이 뭔가 (개념)

- Devin Desktop·CLI에서 코드 작성·수정용 옵션.
- Lead + Sidekick **두 모델을 고른다**. Cognition 추천 페어: **Fable 5.1 + SWE-2**.
- 블로그 주장: 다른 모델 하네스 대비 최대 약 **39%** 더 효율(Artificial Analysis Coding Agent Index 등과의 평가 맥락).
- 추가 관찰(원문): 토큰단가 비싼 Lead가 오히려 **태스크당 비용**을 낮출 수 있다 — 위임·브리프 품질이 왕복을 줄이기 때문. Sidekick도 “더 강한 쪽”이 리뷰 라운드를 줄여 Lead를 싸게 만들 수 있다고 한다. 평가 단위를 **price per token → price per task**로 옮기자는 메시지다.

## 가격·벤치 (Cognition 게시 표)

아래 달러는 Cognition이 Artificial Analysis·Vals AI와 평가했다고 밝힌 **태스크당 비용(주장)** 이다. 점수·달러는 시점에 따라 달라질 수 있다. (출처: [Local Fusion](https://cognition.com/blog/local-fusion), 2026-09-11)

| Benchmark | Fable 5.1 | Fusion (Fable 5.1 + SWE-2) | Astra | Fusion (Astra + SWE-2) |
|---|---|---|---|---|
| DeepSWE 1.1 | 64.3 / **$14.63** | 63.1 / **$7.88 (−46%)** | 67.6 / $7.88 | 67.3 / **$4.69 (−40%)** |
| Terminal-Bench 4 | 57.6 / **$17.46** | 56.1 / **$13.37 (−23%)** | 55.6 / $10.08 | 50.0 / **$6.06 (−40%)** |
| SWE-Atlas QnA | 64.8 / **$7.57** | 65.9 / **$5.00 (−34%)** | 61.8 / $5.72 | 59.4 / **$3.59 (−37%)** |
| Vals Code Migration | 54.6 / **$70.97** | 57.3 / **$42.00 (−41%)** | 67.7 / $44.36 | 61.3 / **$35.51 (−20%)** |
| FrontierCode 1.1 (Extended) | 63.6 / **$2.68** | 63.5 / **$1.67 (−38%)** | 63.1 / $2.62 | 63.4 / **$2.34 (−11%)** |

읽는 법: 같은 Lead라도 Fusion(Sidekick 붙임)이 **태스크당 달러**를 크게 깎는 칸이 많다. 점수는 대체로 비슷하거나 소폭 변동 — “싸게 쓰기 위해 점수를 버린다”기보다 **같은 급 성능을 태스크당 비용으로 줄인다**는 쪽에 가깝다(원문 주장).

### Sidekick list price vs 태스크당

원문은 Sidekick의 **list price(/Mtok)** 와 FrontierCode에서의 **Fusion 태스크당**을 같이 보여 준다.

| Sidekick | List price | Astra (high) Fusion, FrontierCode |
|---|---|---|
| GPT-5.6 Luna (high) | **$0.20/Mtok** | 62.0 @ **$2.39** |
| SWE-2 (medium) | **$0.75/Mtok (+275%)** | 63.4 @ **$2.34 (−2%)** |

토큰단가는 SWE-2가 훨씬 비싸 보이지만, 태스크당은 거의 같거나 오히려 조금 낮다. 강한 Sidekick이 왕복·리뷰를 줄여 Lead 비용을 깎는다는 원문 논리다.

Lead 쪽도 같은 축이다. 원문: Opus 4.8 대신 Fable 5를 Lead로 쓰면 토큰단가는 약 2배인데, 같은 Sidekick 기준 세션 비용은 평균 **약 9% 낮고** FrontierCode 점수는 더 높았다고 한다 — 더 이른 위임·더 나은 브리프 때문.

### Devin 제품 구독 (공식 가격 페이지)

Fusion 벤치 달러와 **별층**이다. 구독은 쿼터·제품 접근이고, 위 표는 평가 태스크당 비용 주장이다. ([devin.ai/pricing](https://devin.ai/pricing), 확인 시점 2026-09-12)

| Plan | 가격 | 이 메모에 닿는 점 |
|---|---|---|
| Free | **$0**/월 | 가벼운 쿼터, 모델 제한 |
| Pro | **$20**/월 | 프론티어 모델 쿼터↑, Devin Cloud, **SWE-2 무료**(Desktop·CLI, 페이지 표기: through October 10, 2026) |
| Max | **$200**/월 | Pro + 훨씬 큰 쿼터 |
| Teams | **$80**/월 플랜 + **$40**/월 per full seat | 협업·중앙 결제 |
| Enterprise | 맞춤 | SSO·전용 배포 등 |

쿼터를 넘기면 추가 사용은 API 가격으로 산다고 적혀 있다. Fusion 자체는 Lead/Sidekick을 고르는 **하네스 모드**이고, “Fusion만의 별도 월정액”으로 적혀 있지는 않다.

정리: 가격을 볼 때 **(1) 구독·쿼터**와 **(2) 벤치 태스크당·/Mtok 주장**을 섞지 말 것. Fusion 논증의 핵은 (2)의 price-per-task다.

## 용어: 코딩 에이전트 하네스

모델 위의 **운영 틀**이다. 도구 호출, 계획→실행→검증, 컨텍스트·캐시, 역할 분담이 여기 들어간다.  
모델 = 엔진, 하네스 = 차체·운전 규칙.

**하네스 라이선스 ≠ LLM API 약관.** 표의 라이선스는 하네스 코드/제품 기준이고, 호출하는 LLM API는 별도 약관·과금이다.

## 비교표 (구조·라이선스)

벤치 점수·달러는 위 Cognition 표를 보면 되고, 여기서는 형태·모델 운용·라이선스만 잡는다. 라이선스 열은 2026-09-12 확인.

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

- 비용↓ + 프론티어 리뷰를 한 세션에 → **Fusion** (위 태스크당 표가 그 주장의 근거)
- 터미널·훅·스킬 중심 → **Claude Code**
- 에디터 안 인라인 → **Cursor**
- git diff 투명·로컬 BYOM → **Aider**
- OSS 프레임워크로 조립 → **OpenHands**

## 한계

벤치 달러는 Cognition이 공개한 평가 맥락이다. 실제 제품 세션·쿼터·ACU 과금과 1:1로 같다고 단정하지 않는다. 라이선스·요금제는 시점 확인이 필요하고, 설치·클릭 경로는 논외다.

## 출처

- Cognition, *Introducing Fusion in Devin Desktop & CLI* (2026-09-11): https://cognition.com/blog/local-fusion
- @dabit3: https://x.com/dabit3/status/2098557144580735156
- (추가 참고 가능) Artificial Analysis coding agents · arXiv:2609.00006 Harness Engineering · OpenHands docs · SWE-agent 논문
- 라이선스 확인일: 2026-09-12 (각 제품 LICENSE/ToS·공개 표기 기준)

*Tool용 정리. 벤치·가격은 원문 주장. AI 보조 작성.*
