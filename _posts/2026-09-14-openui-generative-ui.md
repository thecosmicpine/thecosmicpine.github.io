---
layout: post
title: "텍스트로 끝나지 않는 AI 답변 — OpenUI"
date: 2026-09-14 21:07:00 +0900
categories: ["Notes"]
permalink: /posts/2026-09-14-openui-generative-ui/
---

AI의 답변은 꼭 문장으로 끝나야 할까. [OpenUI](https://github.com/thesysdev/openui)는 모델의 출력을 차트·표·폼 같은 **상호작용 가능한 화면**으로 바꾸는 MIT 라이선스의 Generative UI 프레임워크다.[1][2][7]

**초안 작성·문장 정리에 AI를 사용했다.** 해석은 정리자의 것이며 원문과 다를 수 있다.

- 출처: https://x.com/trendtech33566/status/2099438145494499525
- 코드: https://github.com/thesysdev/openui
- 문서·Playground: https://www.openui.com

## 이 문서가 다루는 문제

원문은 “AI의 답변이 문장으로만 끝나고 있지 않은가”라는 질문에서 출발한다. 텍스트로 설명하기보다 표로 비교하고, 차트로 추세를 보여주고, 폼으로 다음 행동을 받는 편이 나은 요청이 있다. OpenUI는 이때 모델이 임의의 HTML을 만드는 대신 애플리케이션이 허용한 컴포넌트로 응답을 구성하게 한다.[1][2]

원문이 소개한 기능은 네 가지다.

1. 차트·표·폼을 생성한다.
2. AI의 응답에 맞춰 UI를 순차적으로 표시한다.
3. 사용하게 할 컴포넌트 목록에서 모델 지시문을 만든다.
4. 전용 언어로 JSON 대비 최대 67%의 토큰 절감을 표방한다.

게시물은 당시 GitHub 스타를 약 9천 개라고 소개했다. 2026-09-15 확인 시 저장소는 9,306개였지만 이 수치는 계속 변한다.[1][7]

## 핵심 개념: UI를 위한 출력 언어

OpenUI의 중심에는 **OpenUI Lang**이 있다. 모델이 일반 텍스트나 JSON 대신, 허용된 컴포넌트를 조합하는 간결한 언어를 스트리밍하면 렌더러가 결과를 순차적으로 화면에 표시한다.[6]

Generative UI는 모델이 제품의 모든 화면을 마음대로 설계한다는 뜻이 아니다. 제품이 컴포넌트와 속성 계약을 먼저 정하고, 모델은 그 제한된 어휘 안에서 현재 요청에 맞는 조합을 생성한다.

## 작동 원리

공식 처리 흐름은 다음과 같다.[2][6]

1. 앱에서 사용할 컴포넌트를 정한다.
2. 컴포넌트 정의에서 시스템 프롬프트와 스키마를 만든다.
3. 모델이 줄 단위 OpenUI Lang을 스트리밍한다.
4. 렌더러가 도착한 줄을 파싱해 등록된 컴포넌트에 연결한다.
5. 구조를 먼저 그리고 데이터가 도착하는 대로 화면을 채운다.

등록되지 않았거나 유효하지 않은 출력은 검증 과정에서 제외될 수 있다. 따라서 결과의 범위는 모델만이 아니라 애플리케이션의 컴포넌트 라이브러리가 함께 결정한다.[6]

## 구조와 흐름

OpenUI는 세션 전체 기록을 자동으로 시각화하는 도구가 아니다. 세션 안에서 생성되는 특정 AI 응답을 UI로 렌더링하는 계층이다. 모델은 대화 문맥과 연결된 도구의 결과를 활용할 수 있지만, 화면에 표시할 데이터와 컴포넌트의 범위는 애플리케이션이 정한다.[5][6]

전체 흐름은 다음과 같다.

> 사용자 요청 → 에이전트·도구 처리 → OpenUI Lang 스트림 → 파서·검증 → 등록된 컴포넌트로 렌더링

공식 저장소는 역할별 패키지를 제공한다.[2]

- `@openuidev/lang-core`: 프레임워크에 의존하지 않는 파서·프롬프트·런타임 계층
- `@openuidev/react-lang`: React용 컴포넌트 정의와 스트리밍 렌더링
- `@openuidev/react-ui`: 내장 컴포넌트와 완성된 채팅 UI
- `@openuidev/react-headless`: 기존 React 채팅 화면에 붙이는 상태·어댑터
- `@openuidev/langchain`: LangChain·LangGraph 에이전트 연동
- `@openuidev/vue-lang`, `@openuidev/svelte-lang`: Vue 3·Svelte 5 연동
- `@openuidev/cli`: 앱 생성과 프롬프트·스키마 생성

React는 공식 지원이며 Vue와 Svelte 연동은 공식 README에서 커뮤니티 지원으로 구분한다. 따라서 “renderer-agnostic”은 핵심 언어와 구조가 특정 렌더러에 묶이지 않는다는 뜻이지, 모든 프레임워크의 지원 수준이 같다는 뜻은 아니다.[2]

## 적용하기 좋은 조건

OpenUI는 **사용자의 요청에 따라 화면 구성이 달라지는 AI 기능**에 어울린다. 대화 중 비교표를 만들거나, 필요한 입력 항목만 담은 폼을 띄우거나, 도구가 가져온 데이터를 차트와 대시보드로 보여주는 경우다. 공식 문서도 에이전트·코파일럿·대시보드·CRUD·모니터링 도구를 주요 활용처로 제시한다.[2][3][6]

특히 다음 조건에서 의미가 크다.

- 텍스트 설명보다 표·차트·폼이 이해나 행동에 유리할 때
- 모델의 응답을 기다리는 동안 UI를 점진적으로 보여주고 싶을 때
- 모델이 임의의 HTML을 만들게 하지 않고, 제품이 허용한 컴포넌트만 쓰게 하고 싶을 때
- 기존 채팅 UI나 에이전트에 Generative UI 렌더링을 추가할 때

반대로 화면이 항상 고정되어 있거나, 단순한 폼을 일반 코드로 충분히 만들 수 있다면 OpenUI를 넣을 이유가 작다. 모델 호출 없이 완전히 결정적인 화면이 필요한 기능도 기존 UI 구현이 더 단순하다.

## 적용 시나리오

다음은 OpenUI의 기능과 공식 처리 흐름을 상품 비교 요청에 적용한 가상 시나리오다.

- **배경:** 상담원이 고객에게 세 가지 SaaS 요금제의 가격과 기능 차이를 설명해야 한다.
- **목표:** 긴 설명 대신 비교표와 월 가격 차트를 만들고, 다음 상담 단계로 이동하는 버튼을 제공한다.
- **입력:** `Starter, Pro, Enterprise 요금제의 월 가격과 핵심 기능을 표와 막대 차트로 비교해 줘.`
- **단계:** 에이전트가 요금제 데이터를 가져온다 → 모델이 등록된 `Table`, `BarChart`, `Button`만 사용해 OpenUI Lang을 스트리밍한다 → 렌더러가 구조를 먼저 표시하고 데이터를 채운다.
- **기대 결과:** 세 요금제의 행을 가진 표, 가격 차트, 상담 계속 버튼이 한 응답 안에 나타난다.
- **실패 조건:** 모델이 등록되지 않은 컴포넌트를 요청하거나 필수 가격 데이터가 없으면 해당 UI 일부가 렌더링되지 않거나 불완전해진다.
- **검증:** 표의 행 수가 3개인지, 차트의 값이 입력 가격과 일치하는지, 버튼 이벤트가 애플리케이션의 허용된 동작에 연결되는지 확인한다.

## 실행 환경

가장 직접적인 환경은 **Node.js 20 이상을 사용하는 웹 애플리케이션**이다. CLI는 Next.js 기반 에이전트 앱, OpenUI 렌더러와 모델 호출용 서버 경로를 함께 구성한다.[4][5]

- 프런트엔드: React 중심의 공식 패키지와 UI 컴포넌트
- 다른 런타임: Vue 3·Svelte 5 연동 패키지
- 에이전트 백엔드: 기본 구성, Vercel AI SDK, LangGraph 등
- 모델 연결: OpenUI Gateway 또는 자체 OpenAI 호환 모델 제공자
- 기존 앱: assistant-ui·CopilotKit·커스텀 채팅 UI에 렌더러만 추가 가능

패키지가 역할별로 나뉘어 있어 전체 채팅 화면을 도입할 수도 있고, OpenUI Lang 파서·프롬프트·렌더러만 기존 앱에 붙일 수도 있다.[2][4]

## Hands-on

### 1. 버전

- Node.js 20 이상
- `@openuidev/cli` 0.3.0
- CLI 명령은 `@latest`를 사용하되 이 문서의 확인 시점 버전은 0.3.0이다.[8][10]

### 2. 전제조건

- npm을 사용할 수 있는 로컬 개발 환경
- OpenAI 호환 모델 제공자의 서버용 API 키
- 새 디렉터리와 의존성을 만들 수 있는 권한

API 키는 생성된 서버 경로에서만 사용한다. 브라우저 코드에 키를 넣지 않는다.[5]

### 3. 설치

```bash
npx @openuidev/cli@latest create \
  --name my-agent \
  --template openui-self-hosted \
  --no-immediate

cd my-agent
```

CLI 0.3.0의 대화형 기본값은 OpenUI Cloud다. 자체 OpenAI 호환 제공자를 사용할 때는 `--template openui-self-hosted`를 명시한다. `--no-immediate`는 설치 직후 개발 서버와 브라우저가 자동으로 열리는 것을 막는다.[8]

### 4. 최소 실행

설정 과정에서 키를 입력하지 않았다면 생성된 `.env`에 서버용 키를 넣는다.

```dotenv
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

그다음 개발 서버를 실행한다.

```bash
npm run dev
```

브라우저에서 `http://localhost:3000`을 열고 “두 제품을 비교하는 표를 만들어 줘” 또는 “문의 폼을 만들어 줘”처럼 **화면으로 답하기 좋은 요청**을 보낸다. 모델은 OpenUI Lang을 생성하고, 앱은 허용된 컴포넌트로 이를 스트리밍 렌더링한다.[5][6]

### 5. 예상 결과

- 터미널에 Next.js 개발 서버의 로컬 URL이 표시된다.
- 브라우저에 Agent Interface 채팅 화면이 열린다.
- 비교 요청을 보내면 일반 텍스트만이 아니라 등록된 표나 폼 컴포넌트가 점진적으로 표시된다.

### 6. 검증

먼저 런타임과 서버 응답을 확인한다.

```bash
node --version
curl -I http://localhost:3000
```

Node.js는 `v20` 이상이어야 한다. 서버가 실행 중이면 `curl`은 HTTP 응답 헤더를 반환한다. 이후 비교표의 행 수와 입력 데이터가 일치하는지 브라우저에서 확인한다.

### 7. 대표 오류

- **증상:** CLI가 실행되지 않거나 의존성 설치가 실패한다.  
  **원인:** Node.js가 20보다 낮거나 패키지 레지스트리에 연결할 수 없다.  
  **해결:** `node --version`을 확인하고 Node.js 20 이상에서 다시 실행한다. 네트워크와 npm 설정도 확인한다.
- **증상:** 채팅 화면은 열리지만 모델 응답이 실패한다.  
  **원인:** `.env`의 `OPENAI_API_KEY`가 없거나 사용하는 제공자와 호환되지 않는다.  
  **해결:** 서버용 환경 변수와 생성된 API 경로의 제공자 설정을 확인한다. 키를 브라우저 코드에 노출하지 않는다.
- **증상:** 응답 일부가 화면에 나타나지 않는다.  
  **원인:** 모델이 등록되지 않은 컴포넌트나 유효하지 않은 구조를 생성했다.  
  **해결:** 컴포넌트 라이브러리와 생성된 시스템 프롬프트가 일치하는지 확인한다. OpenUI Lang은 유효하지 않은 부분을 제외할 수 있다.[6]

## 의미와 한계

생성형 UI의 포인트는 AI가 임의의 화면을 만드는 데 있지 않다. **제품이 허용한 부품 안에서**, 답변에 맞는 인터페이스를 즉석에서 구성한다는 데 있다. 같은 기반으로 챗봇의 답변뿐 아니라 코파일럿과 앱의 작업 흐름도 만들 수 있다.[2]

프로젝트는 OpenUI Lang이 JSON보다 토큰을 최대 67% 적게 사용한다고 설명한다. 공식 벤치마크는 일곱 UI 시나리오에서 OpenUI Lang 4,800토큰, Vercel JSON-Render 10,180토큰, Thesys C1 JSON 9,948토큰을 보고한다. 전체 합계 기준 절감률은 각각 52.8%, 51.7%이고, 67%는 개별 contact-form 시나리오의 최대값이다.[2][9]

이 수치는 OpenUI 저장소가 GPT-5.2로 OpenUI Lang을 한 번 생성한 뒤 같은 AST를 다른 형식으로 변환하고 GPT-5 인코더로 센 자체 측정값이다. 독립 벤치마크가 아니며, 실제 비용과 지연은 모델·스키마·출력 길이·네트워크에 따라 달라진다.[9]

## 남는 한 줄

OpenUI는 “AI가 HTML을 써 준다”보다 **모델이 사용할 UI 어휘를 제품이 먼저 정하고, 답변이 오는 동안 그 어휘를 화면으로 렌더링한다**는 접근에 가깝다. 텍스트 답변 다음의 인터페이스를 설계할 때 살펴볼 만한 오픈소스다.

## Sources

[1] https://x.com/trendtech33566/status/2099438145494499525 — GitHub AI Projects Community X post
[2] https://raw.githubusercontent.com/thesysdev/openui/main/README.md — OpenUI README
[3] https://www.openui.com/docs — OpenUI Documentation
[4] https://www.openui.com/docs/getting-started — OpenUI Getting Started
[5] https://www.openui.com/docs/agent/getting-started/quickstart — OpenUI Agent Interface Quickstart
[6] https://www.openui.com/docs/openui-lang — OpenUI Lang Introduction
[7] https://api.github.com/repos/thesysdev/openui — 스타·라이선스·기본 브랜치
[8] https://raw.githubusercontent.com/thesysdev/openui/main/packages/openui-cli/README.md — CLI 0.3.0 사용법과 옵션
[9] https://raw.githubusercontent.com/thesysdev/openui/main/benchmarks/README.md — 토큰 벤치마크 방법과 결과
[10] https://raw.githubusercontent.com/thesysdev/openui/main/packages/openui-cli/package.json — CLI 패키지 버전 0.3.0
