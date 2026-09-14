---
layout: post
title: "텍스트로 끝나지 않는 AI 답변 — OpenUI"
date: 2026-09-14 21:07:00 +0900
categories: ["Tool"]
permalink: /posts/2026-09-14-openui-generative-ui/
---

AI의 답변은 꼭 문장으로 끝나야 할까. [OpenUI](https://github.com/thesysdev/openui)는 모델의 출력을 차트·표·폼 같은 **상호작용 가능한 화면**으로 바꾸는 오픈소스 Generative UI 프레임워크다.[1][2]

**초안 작성·문장 정리에 AI를 사용했다.** 해석은 작성자 것이며 원문과 다를 수 있다.

- 출처: https://x.com/trendtech33566/status/2099438145494499525
- 코드: https://github.com/thesysdev/openui
- 문서·Playground: https://www.openui.com
- 원문 메모: `초안/원문/2026-09-14-openui-generative-ui.md`

## 핵심은 UI를 위한 출력 언어

OpenUI의 중심에는 **OpenUI Lang**이 있다. 모델이 일반 텍스트나 JSON 대신, 허용된 컴포넌트를 조합하는 간결한 언어를 스트리밍하면 렌더러가 결과를 순차적으로 화면에 표시한다.[6]

흐름은 단순하다.[2]

1. 앱에서 사용할 컴포넌트를 정한다.
2. 그 목록으로 모델용 지시문을 만든다.
3. 모델이 OpenUI Lang을 스트리밍한다.
4. 렌더러가 출력을 차트·표·폼·레이아웃으로 그린다.

## 세션 결과를 UI로 보여준다는 뜻인가

정확히는 **세션 전체 기록을 자동으로 시각화하는 것이 아니라, 세션 안에서 생성되는 특정 AI 응답을 UI로 렌더링하는 것**이다. 모델은 대화 문맥과 연결된 도구의 결과를 활용할 수 있지만, 화면에 표시할 데이터와 컴포넌트의 범위는 애플리케이션이 정한다.[5][6]

예를 들어 사용자가 “세 상품을 비교해 줘”라고 요청하면 다음처럼 처리된다.

> 사용자 요청 → AI·도구 처리 → OpenUI Lang 응답 → 비교표·차트·버튼으로 렌더링

따라서 OpenUI는 세션 로그를 관리하는 도구가 아니다. **일반 텍스트로 끝나던 AI 답변을, 필요한 경우 상호작용 가능한 화면으로 바꾸는 렌더링 계층**에 가깝다.

## 언제 사용하면 좋은가

OpenUI는 **사용자의 요청에 따라 화면 구성이 달라지는 AI 기능**에 어울린다. 대화 중 비교표를 만들거나, 필요한 입력 항목만 담은 폼을 띄우거나, 도구가 가져온 데이터를 차트와 대시보드로 보여주는 경우다. 공식 문서도 에이전트·코파일럿·대시보드·CRUD·모니터링 도구를 주요 활용처로 제시한다.[2][3][6]

특히 다음 조건에서 의미가 크다.

- 텍스트 설명보다 표·차트·폼이 이해나 행동에 유리할 때
- 모델의 응답을 기다리는 동안 UI를 점진적으로 보여주고 싶을 때
- 모델이 임의의 HTML을 만들게 하지 않고, 제품이 허용한 컴포넌트만 쓰게 하고 싶을 때
- 기존 채팅 UI나 에이전트에 Generative UI 렌더링을 추가할 때

반대로 화면이 항상 고정되어 있거나, 단순한 폼을 일반 코드로 충분히 만들 수 있다면 OpenUI를 넣을 이유가 작다. 모델 호출 없이 완전히 결정적인 화면이 필요한 기능도 기존 UI 구현이 더 단순하다.

## 어떤 환경에서 사용하는가

가장 직접적인 환경은 **Node.js 20 이상을 사용하는 웹 애플리케이션**이다. CLI는 Next.js 기반 에이전트 앱, OpenUI 렌더러와 모델 호출용 서버 경로를 함께 구성한다.[4][5]

- 프런트엔드: React 중심의 공식 패키지와 UI 컴포넌트
- 다른 런타임: Vue 3·Svelte 5 연동 패키지
- 에이전트 백엔드: 기본 구성, Vercel AI SDK, LangGraph 등
- 모델 연결: OpenUI Gateway 또는 자체 OpenAI 호환 모델 제공자
- 기존 앱: assistant-ui·CopilotKit·커스텀 채팅 UI에 렌더러만 추가 가능

패키지가 역할별로 나뉘어 있어 전체 채팅 화면을 도입할 수도 있고, OpenUI Lang 파서·프롬프트·렌더러만 기존 앱에 붙일 수도 있다.[2][4]

## 가장 빠른 설정과 사용

새 앱을 만드는 기본 흐름은 다음과 같다.[4][5]

```bash
npx @openuidev/cli@latest create \
  --name my-agent \
  --template openui-self-hosted

cd my-agent
npm run dev
```

설정 과정에서 모델 제공자 키를 입력하거나, 생성된 환경 파일에 서버용 키를 넣는다.

```dotenv
OPENAI_API_KEY=sk-your-key-here
```

브라우저에서 `http://localhost:3000`을 열고 “두 제품을 비교하는 표를 만들어 줘” 또는 “문의 폼을 만들어 줘”처럼 **화면으로 답하기 좋은 요청**을 보낸다. 모델은 OpenUI Lang을 생성하고, 앱은 허용된 컴포넌트로 이를 스트리밍 렌더링한다.[5][6]

## 왜 의미가 있나

생성형 UI의 포인트는 AI가 임의의 화면을 만드는 데 있지 않다. **제품이 허용한 부품 안에서**, 답변에 맞는 인터페이스를 즉석에서 구성한다는 데 있다. 같은 기반으로 챗봇의 답변뿐 아니라 코파일럿과 앱의 작업 흐름도 만들 수 있다.[2]

프로젝트는 OpenUI Lang이 JSON보다 토큰을 최대 67% 적게 사용한다고 설명한다. 이는 프로젝트 측 수치이며 이 글에서 별도로 재현하지 않았다.[2][6]

## 남는 한 줄

OpenUI는 “AI가 HTML을 써 준다”보다 **모델이 사용할 UI 어휘를 제품이 먼저 정하고, 답변이 오는 동안 그 어휘를 화면으로 렌더링한다**는 접근에 가깝다. 텍스트 답변 다음의 인터페이스를 설계할 때 살펴볼 만한 오픈소스다.

## Sources

[1] https://x.com/trendtech33566/status/2099438145494499525 — GitHub AI Projects Community X post
[2] https://raw.githubusercontent.com/thesysdev/openui/main/README.md — OpenUI README
[3] https://www.openui.com/docs — OpenUI Documentation
[4] https://www.openui.com/docs/getting-started — OpenUI Getting Started
[5] https://www.openui.com/docs/agent/getting-started/quickstart — OpenUI Agent Interface Quickstart
[6] https://www.openui.com/docs/openui-lang — OpenUI Lang Introduction
