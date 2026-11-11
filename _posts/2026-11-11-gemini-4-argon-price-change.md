---
layout: post
title: "제미나이 4 아르곤 API 요금, 12월 1일부터 2배: 남은 3주에 비용 다시 계산하고 Flex·Batch로 나누는 법"
date: 2026-11-11 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["제미나이", "Gemini4Argon", "AI요금", "제미나이API", "AI비용"]
permalink: /posts/2026-11-11-gemini-4-argon-price-change/
description: "구글 Gemini 4 Argon의 출시 할인가가 11월 30일에 끝나 입력·출력 단가가 두 배가 된다. 청구서가 얼마나 오르는지 계산하는 법과 Flex·Batch·생각 수준·캐시로 줄이는 순서를 정리했다."
image: /assets/img/posts/2026-11-11-gemini-4-argon-price-change.png
mermaid: true
---

구글의 최상위 모델 Gemini 4 Argon을 API로 붙여 둔 팀이라면 12월 청구서가 달라진다. 요금 페이지에 적힌 지금 가격은 "11월 30일까지"의 출시 할인가이고, 12월 1일부터는 입력과 출력 단가가 모두 두 배가 된다. 이 글을 읽으면 우리 서비스의 아르곤 비용이 12월에 얼마가 될지 직접 계산하고, 어떤 요청을 Flex·Batch나 낮은 생각 수준으로 옮길지 정할 수 있다.

{: .summary }
> - Gemini 4 Argon 표준 요금은 100만 토큰당 입력 **2→4달러**, 출력 **10→20달러**로 **12월 1일**에 오른다.
> - **Flex·Batch**는 12월 이후에도 표준의 절반이라, 기다려도 되는 요청을 옮기면 **지금 표준 가격**을 그대로 낸다.
> - 출력 단가에는 **생각 토큰**이 들어간다. 옮기기 어려운 요청은 `thinking_level`을 낮춰 보는 게 먼저다.

## 무엇이 바뀌나: 할인가에 끝나는 날짜가 적혀 있다

Gemini API 요금 페이지와 'Gemini 4 Argon 새 기능' 문서는 아르곤의 지금 가격을 "출시 할인가(introductory pricing)"라고 부르고, 11월 30일까지라고 못 박았다. 12월 1일부터 바뀌는 단가는 처리 방식마다 이렇다(100만 토큰당, 유료 등급).

| 처리 방식 | 11월 30일까지 (입력 / 출력) | 12월 1일부터 (입력 / 출력) |
|---|---|---|
| Standard | 2달러 / 10달러 | 4달러 / 20달러 |
| Flex·Batch | 1달러 / 5달러 | 2달러 / 10달러 |
| Priority | 3.60달러 / 18달러 | 7.20달러 / 36달러 |

캐시에 맞은 입력 토큰도 0.10달러에서 0.20달러로 같이 오른다. 아르곤은 무료 등급에서 쓸 수 없고, 문서는 "모델이 처리하는 모든 토큰"에 요금이 붙는다고 적었다. 생각 토큰, 그리고 검색 그라운딩을 쓸 때 들어가는 내부 도구 지시문과 함수 선언까지 포함된다.

{: .note }
OpenAI 요금 페이지도 GPT-5.6 Sol의 프로모션 가격이 11월 30일까지라고 적어 두었다. 다만 그 뒤 가격은 페이지에 없어서 이 글의 계산에는 넣지 않았다.

## 내 청구서는 얼마나 오르나: 토큰 수에 새 단가를 곱한다

계산은 단순하다. 지난달 아르곤 사용량에서 입력·출력(생각 포함)·캐시 적중 토큰을 따로 뽑아 12월 단가를 곱하면 된다. 캐시에 맞은 토큰 수는 응답의 `usage.total_cached_tokens`에서 볼 수 있다고 캐싱 문서는 안내한다.

예를 들어 한 번에 입력 2만 토큰, 출력 4천 토큰을 쓰는 에이전트 요청을 하루 1,000번 보낸다고 하자. 캐시는 없다고 가정한 계산값이다.

<div class="stat-row">
  <div class="stat"><b>80달러</b><span>11월 Standard 하루 비용(계산값)</span></div>
  <div class="stat"><b>160달러</b><span>12월 Standard 하루 비용(계산값)</span></div>
  <div class="stat"><b>80달러</b><span>12월 Flex·Batch 하루 비용(계산값)</span></div>
</div>

입력 2,000만 토큰과 출력 400만 토큰이 하루에 쌓이니, 11월에는 40달러+40달러, 12월 표준으로는 80달러+80달러다. 같은 요청을 Flex나 Batch로 돌리면 12월에도 지금 표준 가격과 같은 80달러가 나온다.

{: .interpret }
단가가 오르는 날짜는 정해져 있지만 어느 요청을 어떤 방식으로 보낼지는 우리가 정한다. 12월 청구서가 실제로 두 배가 될지는 남은 3주 동안 요청을 얼마나 나눠 두느냐에 달려 있다.

## 어디로 옮길까: 응답을 얼마나 기다릴 수 있는지로 나눈다

Flex 문서는 네 가지 처리 방식을 가격과 지연 시간으로 비교한다. Flex는 표준의 50% 가격에 1~15분 안팎을 목표로 응답하는 동기 호출이고, 남는 연산 자원을 쓰는 '최선 노력' 방식이라 요청이 밀려날 수 있다. Batch는 같은 50% 가격에 비동기로 처리하며, 목표 처리 시간은 24시간이다(문서는 대부분 훨씬 빨리 끝난다고 적었다). Priority는 표준보다 75~100% 비싸지만 몇 초 안에 응답한다.

~~~mermaid
flowchart TD
  A[아르곤 요청] --> B{바로 답이 필요?}
  B -- 예 --> C[Standard 유지]
  B -- 몇 분 OK --> D[Flex 50%]
  B -- 하루 OK --> E[Batch 50%]
  C --> F{쉬운 작업?}
  F -- 예 --> G[low로 낮추기]
~~~

Flex로 옮기는 데는 요청에 값 하나만 더하면 된다. 문서의 파이썬 예시는 `service_tier='flex'`를 붙인다. 문서가 꼽은 Flex 용도는 오프라인 평가(LLM 심사 회귀 테스트), CRM 갱신 같은 백그라운드 에이전트, 데이터 보강이다. Batch API는 지금 generateContent API에서만 쓸 수 있다는 점도 문서에 적혀 있다.

~~~python
interaction = client.interactions.create(
    model="gemini-4-argon",
    input="...",
    service_tier="flex",
)
~~~

## 옮길 수 없는 요청은: 생각 수준과 캐시부터 본다

사용자가 화면 앞에서 기다리는 요청은 Standard에 남겨야 한다. 이때 줄일 수 있는 건 출력 쪽이다. 아르곤의 출력 단가에는 생각 토큰이 포함되고, 생각 수준은 `low`, `medium`(기본), `high` 세 단계다. 구글은 세 단계로 모두 평가해 품질 기준을 넘는 가장 낮은 단계를 고르라고 권하고, 토큰을 덜 쓰고 싶으면 출력 상한 대신 생각 수준을 낮추라고 안내한다.

1. 대표 요청 묶음을 `low`·`medium`·`high`로 한 번씩 돌린다
2. 품질 기준을 넘는 가장 낮은 단계를 고른다
3. 출력 상한을 32K 아래로 걸어 두었다면 최소 32,768로 올린다(문서 권고, 생각이 답을 잘라 먹지 않게)
4. 긴 공통 내용은 프롬프트 맨 앞에 두어 캐시 적중을 노린다
{: .steps }

캐시는 아르곤에서 방식이 다르다. 직접 만드는 명시적 캐시(`cachedContents`)는 지원하지 않고, 4,096토큰 이상 프롬프트에 자동으로 걸리는 암묵적 캐시만 된다. 맞으면 입력이 95% 싸진다. 에이전트처럼 여러 턴을 이어 가는 경우 새 요청이 이전 요청보다 2,050토큰 이상 늘어나야 앞 요청 전체가 캐시되고, 그보다 적게 늘면 마지막 2,050토큰을 표준 입력 단가로 다시 처리한다고 문서는 설명한다.

{: .warning }
Flex는 요청이 밀려날 수 있는 방식이다. 결제·주문처럼 실패하면 안 되는 흐름을 옮길 때는 재시도와 Standard 대체 경로를 먼저 만들어 둔다.

## 마무리

출시 할인가는 '지금 가격'이 아니라 '끝나는 날짜가 정해진 가격'이다. 구글 요금 페이지에는 Gemini 3.8 Flash도 12월 31일까지의 가격과 내년 1월 1일부터 두 배가 되는 가격이 함께 적혀 있다. 아르곤만 정리하고 끝내기보다, 쓰고 있는 모델마다 요금 페이지에서 날짜가 붙은 줄을 찾아 달력에 적어 두는 편이 다음 청구서를 덜 놀랍게 만든다.

<details markdown="1">
<summary>출처 6곳</summary>

- Google AI for Developers, 「Gemini Developer API pricing」 Gemini 4 Argon·Gemini 3.8 Flash 항목: [ai.google.dev](https://ai.google.dev/gemini-api/docs/pricing#gemini-4-argon)
- Google AI for Developers, 「What's new in Gemini 4 Argon」(요금·마이그레이션 체크리스트·생각 수준): [ai.google.dev](https://ai.google.dev/gemini-api/docs/whats-new-gemini-4-argon)
- Google AI for Developers, 「Gemini 4 Argon」 모델 페이지: [ai.google.dev](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)
- Google AI for Developers, 「Flex inference」: [ai.google.dev](https://ai.google.dev/gemini-api/docs/flex-inference)
- Google AI for Developers, 「Batch API」·「Context caching」: [ai.google.dev](https://ai.google.dev/gemini-api/docs/batch-api), [ai.google.dev](https://ai.google.dev/gemini-api/docs/caching)
- OpenAI, 「Pricing」(GPT-5.6 Sol 프로모션 기간): [developers.openai.com](https://developers.openai.com/api/docs/pricing)

</details>
