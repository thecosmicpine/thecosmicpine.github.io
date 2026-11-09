---
layout: post
title: "제미나이 옴니 1.2 플래시로 AI 영상 싸게 만드는 법, 360p 초안으로 고르고 대화로 고친다"
date: 2026-11-09 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["제미나이", "GeminiOmni", "AI영상생성", "제미나이API", "AI비용"]
permalink: /posts/2026-11-09-gemini-omni-flash-video-cost/
description: "구글 Gemini Omni 1.2 Flash는 720p 1초 0.07달러, 한 번에 최대 15초다. 360p 초안으로 고르고 대화형 편집으로 고친 뒤 고해상도로 받는 순서와 해상도별 비용, 막히는 조건을 공식 문서로 정리했다."
image: /assets/img/posts/2026-11-09-gemini-omni-flash-video-cost.png
---

상품 소개 영상이나 광고 컷을 AI로 뽑아 보면, 돈은 마음에 드는 한 컷이 아니라 버리는 시도에서 샌다. 구글이 11월 5일 내놓은 Gemini Omni 1.2 Flash는 값을 30% 내리면서 "싸게 초안을 뽑고, 고칠 곳만 말로 고치고, 고른 것만 크게 받으라"는 작업 순서를 같이 내밀었다. 이 글을 읽으면 해상도별로 1초에 얼마가 드는지 계산하고, API로 초안부터 최종본까지 돈을 덜 쓰는 순서로 영상을 만들 수 있다.

{: .summary }
> - 720p 기준 **1초 0.07달러**, 이전 1.1보다 **30%** 싸다. 360p는 1초 **0.023달러**다.
> - 한 번에 **3~15초**를 1초 단위로 고르고, `previous_interaction_id`로 **같은 영상을 말로 고친다**.
> - 1.1 모델 호출은 **12월 3일**부터 자동으로 1.2로 넘어가 1.2 요금이 붙는다.

## 무엇이 바뀌었나: 15초, 30% 인하, 대화형 편집

Gemini Omni 1.2 Flash(`gemini-omni-1.2-flash`)는 글·이미지·영상을 받아 소리가 붙은 영상을 만드는 구글의 영상 모델이다. 구글 블로그에 따르면 이번 버전은 한 번에 만드는 길이를 10초에서 15초로 늘렸고, 같은 영상을 여러 차례 대화로 고치는 편집을 넣었으며, 값을 1.1보다 30% 내렸다. Gemini API 유료 등급과 Google Cloud에서 정식(GA)으로 쓸 수 있다.

<div class="stat-row">
  <div class="stat"><b>$0.07</b><span>720p 영상 1초 값</span></div>
  <div class="stat"><b>15초</b><span>한 번에 만드는 최대 길이</span></div>
  <div class="stat"><b>−30%</b><span>Omni 1.1 대비 인하 폭</span></div>
</div>

개발자가 아니어도 쓸 곳이 있다. 구글은 Google Vids에서 구글 계정이나 Workspace 구독으로 15초 클립을 추가 비용 없이 만들 수 있고, Gemini 앱의 15초 영상은 Google AI Ultra 구독자에게 차례로 열린다고 밝혔다. 이 글은 사용량만큼 돈이 나가는 API 쪽을 다룬다.

## 해상도별로 1초에 얼마가 드나

요금은 출력 토큰으로 매긴다. 720p 영상 1초가 5,792토큰이고, 100만 토큰에 12달러라서 1초에 약 0.07달러가 된다. 구글 요금 페이지가 밝힌 해상도별 값과 15초 한 편 값은 아래와 같다.

| 해상도 | 1초 값 | 15초 한 편 |
|---|---|---|
| 360p | $0.023 | 약 $0.35(계산값) |
| 720p(기본) | 약 $0.07 | 약 $1.04 |
| 1080p(업샘플링) | $0.104 | 약 $1.56(계산값) |
| 4K(업샘플링) | $0.209 | 약 $3.14(계산값) |

같은 15초라도 4K는 360p의 9배쯤 든다. 그래서 순서가 중요하다. 한 장면을 네 번 시도해 하나를 고른다고 하자. 처음부터 1080p로 네 번 뽑으면 약 6.24달러, 360p로 네 번 뽑고 고른 하나만 1080p로 다시 받으면 약 2.94달러다(둘 다 계산값).

## 돈을 덜 쓰는 순서: 초안 → 대화로 수정 → 고해상도

구글이 블로그와 클라우드 발표에서 권하는 흐름은 "360p나 720p로 빨리 초안을 잡고, 고칠 곳은 처음부터 다시 만들지 말고 후속 편집으로 고친 뒤, 가장 좋은 것을 1080p나 4K로 키우라"는 것이다. 공식 문서의 매개변수로 옮기면 이렇다.

1. Google AI Studio에서 API 키를 만들고 결제를 연결한다. 이 모델은 Gemini API 유료 등급에서 열린다
2. `response_format`에 `"resolution": "360p"`, `"duration": "15s"`처럼 해상도·길이를 넣어 초안을 뽑는다. 세로 영상은 `"aspect_ratio": "9:16"`
3. 고를 초안의 `id`를 `previous_interaction_id`로 넘기고, 바꿀 것 하나만 짧게 말한다. 끝에 "Keep everything else the same"을 붙인다
4. 마음에 드는 컷이 나오면 `"resolution": "1080p"`나 `"4k"`로 최종본을 받는다
5. 4MB가 넘는 영상은 `"delivery": "uri"`로 받아 상태가 ACTIVE가 될 때까지 기다렸다 내려받는다
{: .steps }

~~~python
from google import genai

client = genai.Client()

# 1) 360p·15초 초안
draft = client.interactions.create(
    model="gemini-omni-1.2-flash",
    input="A ceramic mug slowly rotating on a wooden table. "
          "In a single continuous shot. No dialogue.",
    response_format={"type": "video", "resolution": "360p", "duration": "15s"},
)

# 2) 같은 영상을 말로 고치기
fixed = client.interactions.create(
    model="gemini-omni-1.2-flash",
    previous_interaction_id=draft.id,
    input="Change the lighting to warm sunset. Keep everything else the same.",
)
~~~

문서는 편집 프롬프트를 짧게 쓰라고 한다. 길게 설명할수록 의도하지 않은 곳까지 바뀔 수 있어서다. 길이를 `duration`으로 정하면 프롬프트 안에 적은 길이는 무시된다. 이어 붙이기(확장)는 한 번에 3~10초씩, 전체 30초까지다.

{: .warning }
빠르게 받으려고 `store=false`를 주면 그 영상은 다음 턴에서 `previous_interaction_id`로 고칠 수 없다. 편집할 초안에는 쓰지 말고, 고칠 일 없는 최종본에만 쓴다.

## 시작 전에 확인할 제한

문서가 밝힌 막히는 조건 중 실무에서 자주 걸릴 것을 추렸다.

- **길이 조합**: 첫 프레임·끝 프레임 두 장으로 잇는 영상은 3~10초만 된다. 11~15초 영상에는 참조 영상을 1개(3초 이내)만 넣을 수 있고, 참조 이미지는 길이와 상관없이 최대 6장이다
- **빠진 설정**: 시스템 지시, temperature, top_p, 네거티브 프롬프트를 지원하지 않는다. 빼고 싶은 것은 "No dialogue"처럼 본문 프롬프트에 쓴다
- **언어**: 영어만 완전 지원이고 다른 언어는 평가하지 않았다고 문서에 적혀 있다. 한국어 프롬프트는 결과가 들쭉날쭉할 수 있다
- **표시**: 만든 영상에는 눈에 보이지 않는 SynthID 워터마크가 들어간다
- **1.1 사용자**: 12월 3일부터 `gemini-omni-1.1-flash` 호출이 코드 수정 없이 1.2로 넘어가고 1.2 요금으로 청구된다

{: .interpret }
대화형 편집은 매 턴 새 영상을 내놓는다고 문서는 설명한다. 요금이 출력 토큰 기준이니 고칠 때마다 그 길이만큼 값이 다시 붙는다고 보는 편이 안전하다. 편집이 "공짜 수정"이 아니라 "다시 뽑기보다 덜 빗나가는 시도"라는 뜻이고, 그래서 비싼 해상도에서 고치기보다 360p에서 고칠 곳을 다 고친 뒤 마지막에 한 번 키우는 쪽이 돈이 덜 든다.

## 마무리

이번 업데이트에서 눈여겨볼 것은 30% 인하 자체보다 해상도를 단계별로 나눠 쓰라는 설계다. AI 영상 예산을 짤 때 "한 편에 얼마"보다 "고르기 전까지 몇 번, 어느 해상도로 시도하나"를 먼저 정하면 같은 돈으로 더 많은 컷을 비교할 수 있다.

<details markdown="1">
<summary>출처 4곳</summary>

- Google 블로그, Anish Nangia, 「Gemini Omni 1.2 Flash: Fast and cost-effective with longer clips」(2026-11-05): [blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/)
- Google Cloud 블로그, John Nack, 「Gemini Omni 1.2 Flash: Fast, cost-effective, and reliable video generation and editing now generally available」(2026-11-06): [cloud.google.com](https://cloud.google.com/blog/products/ai-machine-learning/gemini-omni-1-2-flash-generally-available)
- Gemini API 문서, 「Generate and edit videos with Gemini Omni Flash」: [aistudio.google.com](https://aistudio.google.com/docs/omni)
- Gemini API 문서, 「Pricing」 Gemini Omni 1.2 Flash 항목: [aistudio.google.com](https://aistudio.google.com/docs/pricing#gemini-omni-1.2-flash)

</details>
