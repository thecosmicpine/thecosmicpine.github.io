---
layout: post
title: "Meta의 Muse, 이름 하나에 담긴 모델·비서·기기와 일을 맡기기 전 확인할 것"
date: 2026-10-13 17:13:00 +0900
categories: ["Muse"]
permalink: /posts/2026-10-13-meta-muse-before-delegating/
description: "요즘 IT 뉴스에 \"Meta Muse\"라는 이름이 자주 나온다. 그런데 기사마다 가리키는 대상이 조금씩 다르다. 어떤 기사는 AI 모델 얘기를 하고, 어떤 기사는 앱 얘기를 하고, 또 어떤 기사는 기기 얘기를 한다."
image: /assets/img/posts/2026-10-13-meta-muse-before-delegating.jpg
---

![Meta의 Muse, 이름 하나에 담긴 모델·비서·기기와 일을 맡기기 전 확인할 것](/assets/img/posts/2026-10-13-meta-muse-before-delegating.jpg)

요즘 IT 뉴스에 "Meta Muse"라는 이름이 자주 나온다. 그런데 기사마다 가리키는 대상이 조금씩 다르다. 어떤 기사는 AI 모델 얘기를 하고, 어떤 기사는 앱 얘기를 하고, 또 어떤 기사는 기기 얘기를 한다. 이 글을 읽고 나면 Muse라는 이름 아래 무엇이 있는지, 그리고 이런 'AI 비서'에게 일을 맡기기 전에 무엇을 따져 봐야 하는지 정리할 수 있다.

## Muse는 하나가 아니라 '가족'의 이름이다

Muse는 Meta가 2026년에 새로 꺼낸 브랜드다. 하나의 제품이 아니라 여러 제품을 묶는 이름으로 쓰인다.

먼저 모델이 있다. 2026년 4월 Meta의 초지능 연구 조직(Meta Superintelligence Labs)이 첫 모델 Muse Spark를 내놓았다. 8월에는 누구나 내려받아 쓸 수 있는 공개 가중치 모델 Muse Glimmer가 나왔고, 10월 12일에는 가장 성능이 높다는 Muse Wonder와 Muse Wonder Full이 발표됐다.

다음은 우리가 실제로 쓰는 서비스다. 9월 8일 발표된 개인 AI 에이전트 'Muse' 앱이다. 개발자용으로는 터미널에서 코드를 짜 주는 Muse Code가 따로 있다. 여기에 Muse와 연결해 쓰는 기기(Muse Charm, Muse Gadgets)까지 더해지면서 이름이 점점 넓어지고 있다.

정리하면 Muse Spark·Glimmer·Wonder는 '머리', Muse 앱은 그 머리를 쓰는 '비서', Gadgets는 비서가 손을 뻗는 '도구'라고 보면 헷갈림이 줄어든다.

## 대답하는 AI에서 '일하는' AI로

Muse 앱이 기존 챗봇과 다른 점은 질문에 답하는 데서 끝나지 않고 일을 대신 처리한다는 것이다. Meta가 든 예시는 이렇다. 이메일 보내기, 여행 예약, 웹 양식 채우기, 가격 협상. 인스타그램에 저장해 둔 레시피 릴스를 장보기 목록으로 바꾸거나, 친구들의 식단 제한을 기억해 두었다가 저녁 초대장을 보낼 때 반영하는 식이다. 앱을 닫아도 작업은 계속된다.

이게 가능한 이유는 Muse가 내 휴대폰이 아니라 클라우드에 있는 전용 컴퓨터(Meta는 'Muse Secure VM'이라고 부른다)에서 돌아가기 때문이다. 사람이 컴퓨터 앞에 앉아 일하듯, Muse도 자기 컴퓨터에서 브라우저를 열고 연결된 앱을 쓴다. 앱, 웹사이트([muse.ai](http://muse.ai/)), WhatsApp 메시지로 일을 시킬 수 있고, 스마트 글라스와 Mac 연동도 예고됐다.

## 남에게 카드를 맡길 때처럼, 권한 설계가 핵심이다

일을 대신 하는 AI는 편한 만큼 위험도 크다. 메일을 '읽는' 것과 '보내는' 것, 상품을 '찾는' 것과 '결제하는' 것은 전혀 다른 문제다. 그래서 이런 서비스는 똑똑함보다 권한을 어떻게 나누는지를 먼저 봐야 한다.

Meta가 내세운 장치는 다음과 같다.

인터넷 문지기: 'Sentinel'이라는 별도 에이전트가 승인하지 않으면 Muse의 어떤 동작도 인터넷에 나가지 않는다고 한다.

민감한 행동 전 확인: 메일 발송이나 구매처럼 되돌리기 어려운 일은 실행 전에 사용자에게 묻는다.

권한 선택: 어떤 앱을 연결할지, 그 앱에서 읽기만 할지 쓰기까지 할지를 사용자가 고른다. 언제든 회수할 수 있다.

결제 분리: 저장된 비밀번호나 결제 수단은 Muse가 직접 보지 못하고, 결제는 일회용 카드 방식(Link by Stripe)을 쓴다.

기록과 삭제: 무엇을 했는지 기록을 볼 수 있고, AI 학습에서 빠지거나 특정 내용을 '잊게' 할 수 있다.

물론 이건 Meta의 설명이다. 실제로 그렇게 작동하는지는 써 본 사람들의 검증이 쌓여야 알 수 있다.

## 'AI가 걸었다던 전화'를 사람이 걸었다

그 검증이 필요한 이유를 보여 준 일이 이미 있었다. 9월 말 미국 매체 404 Media는 Muse가 가게에 대신 전화를 걸어 예약해 주는 기능을 시험하면서, 일부 통화를 실제로는 콜센터 직원이 걸었다고 보도했다. 사내 공지에는 통화를 끝까지 마치기 위해 '사람 상담원 층'을 추가했다는 표현이 있었다고 한다. 한 테스트에서는 상대방이 사람이라는 사실을 통화가 끝난 뒤에야 알았다는 기록도 나왔다.

이후 Meta가 사람 상담원 통화를 거둬들였다는 보도가 있었고, Meta는 "준비가 되고 적절히 알릴 수 있을 때만 출시하겠다"는 입장을 냈다. 다만 얼마나 많은 통화가 사람에게 넘어갔는지는 밝혀지지 않았다.

이 사건이 말해 주는 건 단순하다. 'AI가 해 준다'는 말 뒤에 실제로 누가, 어떤 방식으로 일하는지는 사용자가 알기 어렵다. 그래서 공개된 설명과 실제 동작이 일치하는지 지켜보는 눈이 필요하다.

## 실제로 써 본 사람들은 무엇을 맡겼나

출시 후 몇 주 동안 미국 기자와 제품 전문가들이 직접 써 본 기록이 나왔다. 잘된 일과 안 된 일이 꽤 분명하게 갈린다.

이사업체 견적 받기. 야후 파이낸스의 대니얼 하울리 기자는 이사업체 비교를 맡겼다. Muse는 지금 주소와 새 주소, 방 개수, 계단이나 엘리베이터 여부, 연락처를 물은 뒤 근처 업체 네 곳을 찾아 견적 요청을 보냈다. 약 2분 뒤 두 업체에서 전화가 왔고 나머지는 메일로 답했다. 기자는 "이런 일 때문에 AI 비서를 쓰게 될 것"이라고 평했다.

판타지 풋볼 선수 교체. 같은 기자는 야후 판타지 계정을 연결하고 다음 주 예상 점수가 높은 수비팀을 찾게 했다. Muse는 캔자스시티를 영입 신청하고 그린베이를 방출했고, 다음 날 실제로 반영됐다.

게임 구매는 마지막 버튼 앞에서 멈췄다. 닌텐도 스위치 2 게임 구매에서는 Muse가 결제 화면까지 가서 총액과 결제 카드를 정리한 뒤, 구매 버튼은 기자에게 누르게 했다. 앞에서 말한 '민감한 행동 전 확인'이 실제로 이렇게 작동한다.

가족 아침 소식지. 제품 전문가 클레어 보는 가족 캘린더, 메일, 아이들 일정을 바탕으로 아침 소식지를 만들게 했고, 한 번에 나온 PDF를 두고 "지금까지 다른 AI로 만든 어떤 것보다 예쁘다"고 했다. 반면 운동화 구매는 "별로"였고, 영화 IMAX 티켓 구매는 "훨씬 나았다"고 적었다.

실패한 사례도 있다. 글루텐 프리 맥주를 파는 식당을 찾아 달라는 요청에 Muse는 몇 년 전 문을 닫은 가게를 추천했다. 식당 전화번호를 묻자 번호를 알려 준 뒤 다른 번호로 바꿨고, 처음 번호는 확인 없이 지어낸 것이라고 인정했다.

정리하면 Muse는 여러 곳에 연락을 돌리거나 연결된 계정 안에서 정해진 일을 처리하는 데 강하고, 가게 정보나 전화번호처럼 바깥 사실을 확인해야 하는 일에서는 아직 사람이 다시 봐야 한다.

## 공짜일까, 얼마일까

Muse 앱은 기본적으로 무료다. 여기에 사용량이 많은 사람을 위한 유료 요금제가 붙는다. 출시 당시 보도 기준으로 Power는 월 20달러, Maximum은 월 100달러다. 10월 12일 발표된 새 모델 Muse Wonder도 앱에서는 이 구독자에게 먼저 제공된다. Meta는 장기적으로 Muse를 통한 거래에서 작은 수수료를 받는 방식으로 돈을 벌 계획이라고 밝혔다.

## 그래서 지금 우리에게는

현재 Muse 앱은 미국에서만 순차적으로 열리고 있다. 한국에서 바로 써 볼 수는 없지만, 같은 방향의 서비스는 이미 여러 회사가 내놓고 있고 곧 우리 일상에도 들어올 가능성이 높다.

그때 따져 볼 질문은 세 가지면 충분하다.

1. 이 AI는 내 대신 무엇을 '읽고', 무엇을 '실행'하는가.

2. 되돌릴 수 없는 일(송금, 발송, 구매) 앞에서 나에게 먼저 묻는가.

3. 실제로 일하는 주체가 누구인지 알 수 있는가.

Muse는 'AI 비서'가 대화 상대를 넘어 대리인이 되어 가는 흐름을 가장 크게 보여 주는 사례다. 얼마나 많은 일을 해 주는지보다, 얼마나 투명하게 일하는지가 앞으로 이런 서비스를 고르는 기준이 될 것이다.

## 출처

Yahoo Finance, Daniel Howley, "Meta's Muse is an impressively capable AI agent, despite some hiccups" (2026-09-23): [https://finance.yahoo.com/technology/article/metas-muse-is-an-impressively-capable-ai-agent-despite-some-hiccups-173310662.html](https://finance.yahoo.com/technology/article/metas-muse-is-an-impressively-capable-ai-agent-despite-some-hiccups-173310662.html)

Lenny's Newsletter, Claire Vo, "Muse review: The personal AI agent that gets consumer UX right" (2026-09-16): [https://www.lennysnewsletter.com/p/muse-review-the-personal-ai-agent](https://www.lennysnewsletter.com/p/muse-review-the-personal-ai-agent)

Meta, "Introducing Muse: The World's First Personal AI Agent Built for Everyone" (2026-09-08): [https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)

Meta, "Introducing Muse Wonder and Muse Wonder Full: Frontier Models for Agents" (2026-10-12): [https://about.fb.com/news/2026/10/introducing-muse-wonder-models/](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/)

Meta AI, Muse Spark 모델 페이지: [https://dev.meta.ai/models/muse-spark](https://dev.meta.ai/models/muse-spark)

Wikipedia, "Muse Spark": [https://en.wikipedia.org/wiki/Muse_Spark](https://en.wikipedia.org/wiki/Muse_Spark)

TechCrunch, "Everything new coming to Meta's AI agent Muse" (2026-09-23): [https://techcrunch.com/2026/09/23/everything-new-coming-to-metas-ai-agent-muse/](https://techcrunch.com/2026/09/23/everything-new-coming-to-metas-ai-agent-muse/)

404 Media, "Meta Tests Muse AI Agent Calls That Are Actually Made By Humans in a Call Center": [https://404media.co/meta-tests-muse-ai-agent-calls-that-are-actually-made-by-humans-in-a-call-center](https://404media.co/meta-tests-muse-ai-agent-calls-that-are-actually-made-by-humans-in-a-call-center)

Cybernews, "Meta's Muse AI call feature secretly relies on humans": [https://cybernews.com/ai-news/meta-muse-ai-call-feature-uses-humans/](https://cybernews.com/ai-news/meta-muse-ai-call-feature-uses-humans/)

CNBC, "Meta debuts Muse Wonder AI model in latest test of users' willingness to pay" (2026-10-12): [https://www.cnbc.com/2026/10/12/meta-muse-wonder-ai-model-agent.html](https://www.cnbc.com/2026/10/12/meta-muse-wonder-ai-model-agent.html)
