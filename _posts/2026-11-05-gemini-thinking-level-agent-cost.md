---
layout: post
title: "제미나이 API 에이전트 비용 줄이는 법, 출력 토큰 상한 대신 thinking_level을 낮춘다"
date: 2026-11-05 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["제미나이", "AI에이전트", "API비용", "생각수준"]
permalink: /posts/2026-11-05-gemini-thinking-level-agent-cost/
description: "max_output_tokens를 줄여도 제미나이의 생각 토큰은 줄지 않는다. 구글이 공개한 50문항 시험과 공식 문서로, thinking_level부터 낮추고 라우터는 언제 붙일지 정리했다."
image: /assets/img/posts/2026-11-05-gemini-thinking-level-agent-cost.png
mermaid: true
---

AI 코딩 에이전트를 API로 돌리면 청구서는 질문 하나보다 루프가 만든다. 같은 작업을 끝내려고 모델을 여러 번 부르고, 부를 때마다 모델은 화면에 안 보이는 '생각 토큰'을 쓴다. 구글 클라우드 AI의 세르지오 빌라니가 11월 3일 구글 개발자 블로그에 이 비용을 줄이는 시험 결과를 올렸다. 이 글을 읽으면 제미나이 에이전트에서 어떤 설정부터 손대야 비용이 실제로 줄고, 어떤 설정은 답만 망가뜨리는지 가를 수 있다.

{: .summary }
> - `max_output_tokens`를 300으로 줄여도 쉬운 작업의 생각 토큰은 **거의 같았고**, 어려운 작업 25개 중 **7개**가 망가졌다.
> - 먼저 할 일은 `thinking_level`을 **low**로 내리는 것이다. 시험에선 이 설정 하나로 50문제를 **모두 맞혔다**.
> - 라우터(쉬운 작업은 싼 모델로)는 그다음, **짧고 독립된 작업**에만 붙인다. 긴 문맥은 한 모델에 둬야 캐시 할인이 남는다.

## 토큰 단가보다 '성공한 작업당 비용'을 본다

글의 출발점은 지표다. 100만 토큰당 가격은 내려가는데 에이전트 청구서는 오른다. 그래서 글은 기준을 '성공한 작업당 비용'으로 바꾸자고 한다. 루프를 돈 횟수, 도구 호출, 재시도, 생각 단계까지 모두 더한 돈을 검증을 통과한 작업 수로 나눈 값이다.

제미나이에서는 생각 토큰도 출력 요금으로 계산된다. 공식 문서는 생각이 켜져 있으면 응답 요금이 출력 토큰과 생각 토큰의 합이라고 적었다. 쉬운 질문에도 모델이 깊게 생각하면 그만큼 출력 요금을 더 내는 셈이다.

단가도 곧 오른다. 요금 페이지 기준 Gemini 3.8 Flash는 2026년 12월 31일까지의 값이 2027년 1월 1일부터 두 배가 된다.

| 모델 (유료 등급 표준) | 입력, 100만 토큰 | 출력·생각, 100만 토큰 |
|---|---|---|
| 3.8 Flash, 12월 31일까지 | 0.75달러 | 3.75달러 |
| 3.8 Flash, 1월 1일부터 | 1.50달러 | 7.50달러 |
| 3.5 Flash-Lite | 0.30달러 | 2.50달러 |

## max_output_tokens를 줄여도 생각은 줄지 않는다

흔한 실수는 출력 토큰 상한을 낮추면 모델이 쉬운 일에 덜 쓸 거라고 기대하는 것이다. 시험에서 gemini-3.8-flash를 상한 300과 4096으로 나눠 돌렸더니, 쉬운 작업 27개에서 쓴 생각 토큰이 거의 같았다. 쉬운 답은 애초에 상한 근처까지 가지 않았기 때문이다.

대신 어려운 작업 25개 중 7개가 깨졌다. 6개는 생각하다가 자리가 모자라 답을 내지 못했고, 1개는 생각을 줄여 끼워 맞추다 틀렸다. 쉬운 작업에서는 상한을 건 쪽이 오히려 조금 더 비쌌다고 한다.

공식 문서도 같은 말을 한다. `max_output_tokens`에는 생각 토큰이 포함되고, 이 값은 생각 수준을 바꾸지 않는 강제 차단선이다. 생각하다 한도에 걸리면 상태가 `incomplete`로 끝나고 답이 잘리거나 비는데, 그때까지 쓴 생각 토큰은 청구된다.

{: .warning }
출력 상한을 너무 낮추면 돈은 그대로 나가고 답만 사라질 수 있다. 문서는 비용이나 지연을 줄이려면 작은 `max_output_tokens` 대신 `thinking_level`을 low나 medium으로 낮추라고 권한다.

## 먼저 thinking_level을 low로 내린다

제미나이 모델은 기본으로 요청의 난도에 맞춰 생각량을 스스로 정하고, `thinking_level`로 이를 조절한다. 문서의 표를 보면 gemini-3.8-flash는 기본이 medium이고 low·medium·high를 고를 수 있다. gemini-3.5-flash-lite는 기본이 가장 낮은 minimal이다.

시험에서 라우터 없이 가장 강했던 설정은 Gemini 3.8 Flash에 생각 수준 low였다. 50문제를 모두 맞혔고, 기본 설정보다 비용이 꽤 적었다고 글은 적었다. 공식 문서의 파이썬 예시(Interactions API)는 설정 한 줄이다.

~~~python
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="...",
    generation_config={"thinking_level": "low"},
)
~~~

손대는 순서는 이렇게 잡을 수 있다.

1. 지금 에이전트가 쓰는 생각 토큰을 잰다. 응답의 `total_thought_tokens` 값을 로그로 모은다
2. `thinking_level`을 low로 내리고, 같은 작업 묶음으로 정답률을 다시 본다
3. low에서 틀리는 작업이 생길 때만 라우터나 더 높은 생각 수준을 붙인다
{: .steps }

글은 에이전트 기록과 생각 토큰 수를 Cloud Logging·BigQuery로 보내 어떤 작업이 돈을 쓰는지, 잘림이나 재시도가 비용을 부풀리는지 보라고 했다.

## 라우터는 그다음, 짧은 작업에만 붙인다

라우터는 작업마다 난도를 먼저 가려 쉬운 건 싼 모델로, 어려운 건 비싼 모델로 보내는 층이다. 시험에선 모든 작업을 Flash-Lite에 먼저 보내고, 분류기가 복잡하다고 본 것만 3.8 Flash low로 올렸다. 50문제 모두 정답이었고, low 일괄 설정보다 비용과 응답 시간을 줄일 수 있었다고 한다. 다만 프롬프트가 짧아 작업당 비용 차이는 작았고, 대화형 에이전트에선 덜 기다리는 쪽이 더 큰 이득이라고 글은 적었다.

Flash-Lite만 썼다면 쉬운 작업은 0.5초 만에 답했지만 어려운 작업 25개 중 6개를 놓쳤다. 분류기는 이 6개를 모두 복잡하다고 표시했다. 분류기를 정규식과 프롬프트 길이 규칙으로 대신하면 어떨까. 규칙을 만든 16문항에선 93.8%를 맞혔지만, 처음 보는 34문항에선 70.6%로 23.2%포인트 떨어졌다. 쿠버네티스 YAML에서 포트 하나 꺼내기처럼 길지만 쉬운 작업은 괜히 올려 보냈고, 짧지만 여러 단계인 코드 추적은 쉬운 쪽으로 보냈다.

분류기에 묻는 방식도 갈렸다. '쉬움/어려움' 중 고르라는 넓은 질문에는 거의 다 쉬움이라고 답했다. "한 단계를 넘는 계산·시뮬레이션·추론이 필요한가"라는 예/아니오 질문 하나로 바꾸자 제대로 갈라졌다. 시험에 쓴 분류기는 외부 회사 TypeSafe의 Jev이고, 구글은 이 회사와 제휴가 없으며 추천도 아니라고 밝혔다. 구글 쪽 대안으로는 공개 가중치 모델 DiffusionGemma로 같은 분류를 돌리는 코드랩을 소개했다.

~~~mermaid
flowchart TD
  A[에이전트 작업] --> B{긴 문맥 반복?}
  B -- 예 --> C[한 모델 고정·캐시]
  B -- 아니오 --> D{여러 단계 추론?}
  D -- 아니오 --> E[Flash-Lite]
  D -- 예 --> F[Flash low]
~~~

라우터와 캐시는 서로 반대로 당긴다. 실제 코딩 에이전트는 저장소 지도나 도구 정의 같은 큰 문맥을 매 턴 다시 보낸다. 컨텍스트 캐싱을 쓰면 이 부분을 다시 보내는 값이 75~90% 줄지만, 캐시는 모델 하나에 묶인다. 턴마다 Flash-Lite와 Flash를 오가면 캐시를 둘 두거나 할인을 잃는다. 그래서 글은 로그 파싱·스키마 검사처럼 짧고 독립된 작업만 라우팅하고, 긴 문맥 턴은 한 모델에 두라고 했다.

모델 고르기도 작업에 맞춘다. 글은 짧은 확인·추출이 대부분이면 Flash 설정이 맞고, Gemini 3.1 Pro는 깊은 추론이 필요한 작업에 아끼라고 했다. 시험에선 Pro 설정이 짧은 코드 보안 검토 프롬프트 2개를 거절했는데 Flash는 답했다. 보안 검토를 맡길 생각이라면 실제로 쓸 설정에서 그 프롬프트를 먼저 돌려 봐야 한다.

{: .interpret }
이 시험의 무게는 '라우터가 이긴다'보다 'low 하나로 이미 충분했다'에 있어 보인다. 라우터는 low에서 틀리기 시작할 때 꺼낼 다음 카드에 가깝다. 시험은 설정마다 한 번씩, 짧은 50문항으로 돌렸고 구체적인 비용 숫자는 원문의 표 이미지에만 있다. 내 작업에서 다시 재 보기 전에는 절감 폭을 단정하기 어렵다.

## 마무리

에이전트 비용을 줄이는 첫 손질은 새 도구를 붙이는 일이 아니라 이미 있는 설정 한 줄이다. 3.8 Flash 단가가 두 배가 되는 1월 전에 생각 토큰부터 재 두면, 라우터가 필요한지도 숫자로 답할 수 있다.

<details markdown="1">
<summary>출처 3곳</summary>

- Google Developers Blog, Sergio Villani, 「Cost per task: Using cheap classifiers to route across Gemini models and thinking levels」(2026-11-03): [developers.googleblog.com](https://developers.googleblog.com/cost-per-task-using-cheap-classifiers-to-route-across-gemini-models-and-thinking-levels/)
- Google AI for Developers, 「Gemini thinking」(생각 수준 표·max_output_tokens·요금): [ai.google.dev](https://ai.google.dev/gemini-api/docs/thinking)
- Google AI for Developers, 「Gemini Developer API pricing」: [ai.google.dev](https://ai.google.dev/gemini-api/docs/pricing)

</details>
