---
layout: post
title: "Muse, Dots, Grok Bot: 세 AI 비서에게 일을 맡기는 방식은 어떻게 다를까"
date: 2026-10-16 19:50:00 +0900
categories: ["AI와 기술"]
tags: ["Muse", "Dots", "Grok Bot", "AI에이전트"]
permalink: /posts/2026-10-16-muse-dots-grok-bot-compared/
---

![세 개의 빛나는 구슬](/assets/img/posts/2026-10-16-muse-dots-grok-bot.png)

올가을 거대 AI 회사 세 곳이 거의 같은 시기에 '일하는 AI'를 내놓았다. xAI의 Grok Bot(8월 11일), Meta의 Muse(9월 8일), OpenAI의 Dots(9월 29일)다. 셋 다 질문에 답하는 데서 그치지 않고, 클라우드에 있는 자기 컴퓨터에서 브라우저를 열고 앱에 로그인해 일을 끝낸다. 겉모습이 비슷하니 "결국 다 같은 것 아닌가" 싶지만, 일을 맡기는 방식과 위험을 막는 방식은 꽤 다르다. 이 글은 세 서비스를 기능 목록이 아니라 '어떤 사람이 무엇을 맡기기에 맞는가'라는 기준으로 나눠 본다.

## 공통점: 내 컴퓨터가 아니라 '비서의 컴퓨터'에서 일한다

세 서비스 모두 사용자의 휴대폰이나 노트북이 아니라 회사가 마련한 클라우드 컴퓨터에서 작업한다. Muse는 이를 'Muse Secure VM'이라 부르고, Dots와 Grok Bot도 각자 클라우드 컴퓨터와 브라우저를 쓴다. 그래서 앱을 닫거나 노트북을 덮어도 일이 계속된다.

이 구조는 편리하지만 한 가지를 뜻한다. 비서가 내 계정으로 로그인해 일하는 동안, 그 로그인 정보와 파일은 비서의 컴퓨터에 남는다. 세 서비스를 비교할 때 가장 먼저 볼 것은 성능이 아니라 '그 컴퓨터에 무엇이 남고, 누가 그것을 볼 수 있는가'다.

## 차이 1: 비서를 몇 명 두는가

**Muse**는 한 사람에게 한 명의 개인 비서다. 메일, 쇼핑, 여행 예약 같은 생활 속 일을 하나의 비서에게 맡기는 구조다.

**Dots**도 출발은 한 명이다. 기본 dot 하나가 여러 책임을 맡고, 필요하면 그 dot이 일을 나눠 병렬로 처리한다. ChatGPT에서 대화하던 흐름을 그대로 이어 가는 느낌에 가깝다.

**Grok Bot**은 처음부터 '팀'을 전제로 한다. 받은편지함 담당, 경비 담당, 채용 담당처럼 역할별 Bot을 여러 개 만들고, 총괄 Bot이 이들을 지휘하게 할 수 있다. Bot끼리 단체 대화방에서 일을 넘기기도 한다. 한 번 시범을 보여 주면 그 과정을 루틴으로 저장해 다음부터 혼자 반복하는 기능도 있다.

정리하면, 내 일을 한 비서와 계속 상의하고 싶다면 Muse나 Dots, 역할을 나눠 관리하고 싶다면 Grok Bot 쪽이 맞는다.

## 차이 2: 위험한 일 앞에서 어떻게 멈추는가

일을 대신 하는 AI의 핵심은 '되돌릴 수 없는 일' 앞에서 멈추는 장치다.

**Muse**는 메일 발송이나 구매처럼 민감한 행동 전에 사용자에게 확인한다. 'Sentinel'이라는 별도 에이전트가 승인하지 않으면 어떤 동작도 인터넷으로 나가지 않으며, 결제는 일회용 카드 방식을 쓰고 Muse는 저장된 비밀번호나 결제 수단을 직접 보지 못한다고 Meta는 설명한다.

**Dots**는 연결된 정보에서 먼저 도울 일을 찾아 제안하기도 하는데, OpenAI는 이 선제적 조사를 읽기 전용으로 제한한다고 밝힌다. 외부 발송이나 지출에는 별도의 승인 절차가 적용된다.

**Grok Bot**은 승인이 필요한 행동이 오면 작업 내용과 입력값을 보여 주고 '한 번 허용 / 항상 허용 / 거부'를 고르게 한다. 비밀번호, 2단계 인증, 결제 확인은 사용자가 직접 화면을 넘겨받아 처리한다. 다만 주의할 점이 있다. xAI 문서는 한 사용자의 모든 Bot이 하나의 클라우드 컴퓨터를 함께 쓰며, 파일과 브라우저 로그인이 Bot 사이에 공유된다고 설명한다. Bot을 나눈다고 보안 칸막이가 생기는 것은 아니고, Bot을 삭제해도 그 컴퓨터의 파일과 로그인은 남을 수 있다.

## 차이 3: 누가, 얼마에 쓸 수 있는가

**Muse**는 기본 무료이고, 사용량이 많은 사람을 위한 유료 요금제(출시 당시 보도 기준 월 20달러·100달러)가 있다. 다만 현재 미국에서만 순차적으로 열리고 있다.

**Dots**는 무료나 Plus 요금제에는 없다. 성인 Pro 사용자(월 100달러부터)와 Business Premium 사용자에게 첫 dot이 포함되고, Pro는 유럽경제지역·스위스·영국을 제외한 지원 시장에서 순차적으로 열린다.

**Grok Bot**은 SuperGrok 요금제와 Cursor의 Pro·Teams 요금제에 포함돼 있다. 기존 Grok·Cursor 사용량과 별도의 Bot 전용 사용량이 붙는다.

세 서비스 모두 아직 베타이거나 순차 출시 단계라, 지역과 계정에 따라 실제로 쓸 수 있는지는 각 서비스 화면에서 확인해야 한다. 공개된 자료만으로는 세 서비스의 속도나 정확도를 같은 조건에서 비교할 수 없다는 점도 기억해 둘 만하다.

## 그래서 무엇을 고를까

세 서비스의 성격을 한 줄씩 정리하면 이렇다.

- **Muse**: 생활 속 잡일을 맡기는 무료 개인 비서. 결제·발송 같은 위험한 순간의 안전장치를 전면에 내세운다.
- **Dots**: ChatGPT를 오래 써 온 사람이 대화의 맥락을 그대로 이어 맡기는 비서. 진입 비용이 가장 높다.
- **Grok Bot**: 여러 역할을 나눠 맡기고 서로 인계하게 하는 'AI 팀'. 대신 Bot 사이의 자료 공유를 이해하고 써야 한다.

어느 쪽이든 처음에는 결과를 직접 확인할 수 있는 작은 일 하나로 시작하는 것이 좋다. 그리고 세 가지를 확인하자. 이 비서가 무엇을 읽고 무엇을 실행하는지, 되돌릴 수 없는 일 앞에서 나에게 묻는지, 일이 끝난 뒤 남은 자료와 로그인을 어떻게 정리하는지. 비서를 고르는 기준은 얼마나 많은 일을 하느냐보다, 내가 그 일을 얼마나 잘 통제할 수 있느냐다.

## 출처

- xAI, "Introducing Grok Bot" (2026-08-11): [x.ai](https://x.ai/news/introducing-grok-bot)
- xAI, "Grok Bot is now included with more plans" (2026-08-26): [x.ai](https://x.ai/news/grok-bot-more-plans)
- xAI Docs, Grok Bot 승인·보안·개인정보: [docs.x.ai](https://docs.x.ai/grok-bot/approvals-security-and-privacy)
- xAI Docs, Grok Bot 개요: [docs.x.ai](https://docs.x.ai/grok-bot/overview)
- OpenAI, "Introducing dots" (2026-09-29): [openai.com](https://openai.com/index/introducing-dots/)
- OpenAI Help Center, "Getting started with your dot": [help.openai.com](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot)
- OpenAI Help Center, Dots 개인정보·보안·안전 FAQ: [help.openai.com](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)
- Meta, "Introducing Muse: The World's First Personal AI Agent Built for Everyone" (2026-09-08): [about.fb.com](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
- TechCrunch, "Everything new coming to Meta's AI agent Muse" (2026-09-23): [techcrunch.com](https://techcrunch.com/2026/09/23/everything-new-coming-to-metas-ai-agent-muse/)
