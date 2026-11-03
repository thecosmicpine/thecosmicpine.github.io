---
layout: post
title: "robots.txt로 AI 학습 거부하는 법, 회사별 봇 대신 __usage_ai-training 한 그룹으로"
date: 2026-11-03 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["robotstxt", "AI학습거부", "IETF", "GoogleExtended", "웹사이트운영"]
permalink: /posts/2026-11-03-robots-txt-ai-training-opt-out/
description: "구글·마이크로소프트·OpenAI·앤트로픽이 따르겠다고 한 robots.txt 공용 'AI 학습' 표시를 어떻게 적는지, 검색 노출과 크롤링은 왜 그대로인지, 회사별 시작 시점과 함께 정리했다."
image: /assets/img/posts/2026-11-03-robots-txt-ai-training-opt-out.png
mermaid: true
---

블로그나 회사 사이트 글이 AI 학습에 쓰이는 게 싫으면 지금까지는 회사마다 다른 봇 이름을 찾아 robots.txt에 하나씩 적어야 했다. 10월 30일 구글이 이 일을 한 번에 끝내는 공용 표시를 지원하겠다고 밝혔고, 마이크로소프트와 앤트로픽, OpenAI도 같은 표시를 따르겠다고 했다. 이 글을 읽으면 내 사이트 robots.txt에 무엇을 몇 줄 넣어야 하는지, 그 줄이 검색 노출과 크롤링에는 왜 영향을 주지 않는지, 회사마다 언제부터 읽는지 판단할 수 있다.

{: .summary }
> - robots.txt에 **`User-Agent: __usage_ai-training`** 그룹 하나를 넣고 `Disallow: /`를 쓰면 "AI 학습에 쓰지 마라"는 뜻이 된다.
> - 이 표시는 **학습 용도만** 말한다. 크롤링 허용 여부와 구글·빙 검색 노출은 바뀌지 않는다.
> - 읽기 시작하는 때가 다르다: 앤트로픽은 구현 시작, 마이크로소프트는 **2027년 2월 1일**, 구글은 2027년 초, OpenAI는 "몇 달 안".

## 무엇이 바뀌었나: 봇 이름이 아니라 '용도' 이름

이번 표시는 앤트로픽의 표준 담당 Kevin Kelley가 인터넷 표준 기구 IETF에 낸 개인 초안 「Machine-Readable Training Preference Signal」(draft-kelley-aipref-training-preference-signal-00)에 들어 있다. 핵심은 robots.txt의 `User-Agent` 줄에 실제 봇 이름 대신 '정책 토큰'이라는 용도 이름을 적는 것이다. 초안이 정한 첫 정책 토큰이 `__usage_ai-training`이다.

새 지시어나 문법은 없다. 경로를 적는 방식, 가장 긴 경로가 이기는 규칙, 그룹 구조는 기존 robots.txt 표준(RFC 9309)을 그대로 쓴다. 그래서 이 토큰을 모르는 기존 파서는 처음 보는 봇 그룹처럼 그냥 건너뛴다. 초안이 말하는 'AI 학습'은 생성형 AI 모델의 학습된 파라미터를 바꾸는 데 쓰는 것이고, 분류·순위 매기기처럼 생성이 아닌 일에만 쓰는 모델의 학습은 들어가지 않는다.

## 어떻게 적나: 그룹 하나, 경로별로

가장 단순한 형태는 사이트 전체에 대해 학습을 거부하는 두 줄이다. 초안의 예시처럼 일부 경로만 허용으로 남길 수도 있다.

~~~text
User-Agent: __usage_ai-training
Disallow: /
Allow: /press-kit/
~~~

이렇게 쓰면 `/press-kit/` 아래는 학습 '찬성', 나머지 전체는 학습 '반대'로 읽힌다. 마이크로소프트 빙 블로그는 특정 경로만 거부하는 형태(`Disallow: /example-path/`)도 예로 든다. 아무 그룹도 없으면 "표시하지 않음"이고, 빙은 이를 허용으로 본다고 밝혔다.

| 상황 | 적는 법 | 읽히는 뜻 |
|---|---|---|
| 전체 거부 | `Disallow: /` | 모든 경로 학습 반대 |
| 일부만 거부 | `Disallow: /blog/` | 그 경로만 반대 |
| 아무것도 안 씀 | 그룹 없음 | 표시 없음(빙은 허용으로 처리) |

{: .warning }
`User-Agent: *` 그룹에 적은 규칙은 이 표시로 치지 않는다. 초안은 와일드카드 그룹을 정책 토큰과 맞춰 읽지 말라고 못 박았다. "전체 봇 Disallow를 이미 해 뒀으니 됐다"가 아니라, `__usage_ai-training` 이름을 직접 적은 그룹이 따로 있어야 한다.

## 왜 검색에서 안 사라지나: 크롤링 규칙과 따로 논다

초안은 이 토큰이 크롤링 지시가 아니라고 분명히 한다. 각 회사 봇은 자기 이름(예: Googlebot, Bingbot)으로 된 규칙을 전과 똑같이 읽고, 학습 표시는 그와 별개로 '가져간 뒤 무엇에 쓰나'만 말한다. 크롤링 자체를 막고 싶으면 지금처럼 봇 이름 그룹으로 막아야 한다.

그래서 구글 검색이나 빙 검색 노출은 그대로다. 구글은 이 토큰으로 학습을 거부하고 Google-Extended를 따로 적지 않은 사이트를, Google-Extended를 막은 것처럼 해석하겠다고 했다. 구글 크롤러 문서에 따르면 Google-Extended는 검색 순위나 검색 포함에는 영향이 없다.

{: .interpret }
구글 문서에서 Google-Extended는 Gemini 모델 학습뿐 아니라 Gemini 앱의 그라운딩(답할 때 검색 색인 내용을 가져다 쓰는 것)도 관리한다. 공용 토큰 거부가 'Google-Extended 거부'로 읽힌다면, Gemini 앱 답변에 내 글이 근거로 걸리는 기회도 함께 줄 수 있다. 구글이 "Google-Extended를 명시적으로 허용한 사이트는 Gemini 앱 그라운딩으로 노출과 클릭을 받을 수 있다"고 따로 적은 이유로 읽힌다.

## 회사별 시작 시점과 같이 쓸 설정

공용 표시를 넣어도 회사별 설정은 계속 작동한다. 초안은 구체적인 표현이 일반적인 표현보다 앞선다고 하고, 회사가 자기 전용 토큰을 공용 토큰보다 구체적인 것으로 볼 수 있다고 열어 두었다. 학습은 막고 Gemini 그라운딩은 열어 두고 싶다면 공용 토큰으로 거부하면서 Google-Extended를 따로 허용하는 식의 조합이 가능하다는 뜻이다.

| 회사 | 언제부터 | 근거 |
|---|---|---|
| 앤트로픽 | 구현 시작(서비스 전체 적용엔 시간 걸림) | Kelley의 IETF 메일 |
| 마이크로소프트 | 2027년 2월 1일, 다시 크롤링할 때부터 | 빙 블로그 |
| 구글 | 2027년 초 | 구글 크롤러 문서·블로그 |
| OpenAI | "몇 달 안" | Engadget 보도 |

빙은 페이지 단위 설정도 따로 받는다. 학습은 `<meta name="Bingbot" content="ai-training:disallow">` 태그나 `X-Robots-Tag` 헤더로, 답변 근거로 쓰는 그라운딩은 페이지 단위로만 정한다. 지금 NoArchive·NoCache로 AI 사용을 막아 둔 사이트라면, 빙은 2027년 3월 1일 뒤로 이 둘을 학습·그라운딩 거부로 읽지 않는다고 했다.

~~~mermaid
flowchart TD
  A[내 글 AI 학습 싫다] --> B{검색 노출은 유지?}
  B -- 예 --> C[공용 토큰 Disallow]
  B -- 아니오 --> D[봇 이름으로 크롤링 차단]
  C --> E{Gemini 근거 노출 원함?}
  E -- 예 --> F[Google-Extended Allow]
  E -- 아니오 --> G[공용 토큰만 둔다]
~~~

넣는 순서는 다음과 같다.

1. 사이트의 robots.txt를 열어 지금 있는 회사별 그룹(Google-Extended 등)을 확인한다
2. 맨 아래에 `User-Agent: __usage_ai-training` 그룹을 새로 만들고 `Disallow:` 경로를 적는다
3. 허용으로 남길 경로가 있으면 같은 그룹에 `Allow:`로 적는다
4. Gemini 그라운딩 노출을 지키려면 Google-Extended 그룹을 따로 두고 허용으로 적는다
5. 기존 회사별 거부 그룹은 지우지 않는다. 회사들이 읽기 시작하는 날이 서로 다르다
{: .steps }

{: .note }
이 표시는 법이 아니라 회사들의 약속이고, 이미 가져간 글을 되돌리지도 못한다(Engadget). 초안 자체도 2027년 5월 3일 만료되는 '진행 중인 작업'이라 이름이나 해석이 바뀔 수 있다.

## 마무리

이번 변화의 실질은 "거부 버튼이 하나로 모였다"보다 "학습과 검색, 그라운딩이 서로 다른 스위치가 됐다"에 가깝다. 검색에는 나오되 학습에는 안 쓰이고, AI 답변의 근거로는 걸리게 하는 식의 조합을 사이트 운영자가 고를 수 있게 됐다. 다만 각 스위치를 읽기 시작하는 날이 회사마다 다르니, 2027년 상반기까지는 회사별 그룹과 공용 그룹을 함께 두는 편이 안전하다.

<details markdown="1">
<summary>출처 6곳</summary>

- Google Search Central Blog, 「Supporting a shared AI training control for websites」(2026-10-30): [developers.google.com](https://developers.google.com/search/blog/2026/10/ai-training-control)
- Google, 「Google's common crawlers」 Google-Extended 항목: [developers.google.com](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended)
- IETF, draft-kelley-aipref-training-preference-signal-00: [datatracker.ietf.org](https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/)
- Kevin Kelley, IETF ai-control 메일링 리스트 「New draft」(2026-10-30): [mailarchive.ietf.org](https://mailarchive.ietf.org/arch/msg/ai-control/mddjatOxSR0h6GmLRBWlc839c7w/)
- Microsoft Bing Blog, 「Your content, your choice: clearer preferences for training and grounding」(2026-10-30): [blogs.bing.com](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/)
- Engadget, 「Google joins OpenAI and Anthropic in promising new scraping controls」(2026-10-31): [engadget.com](https://www.engadget.com/2303225/google-openai-anthropic-ai-crawling-controls/)

</details>
