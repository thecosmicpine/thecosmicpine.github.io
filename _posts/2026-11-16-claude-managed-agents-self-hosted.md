---
layout: post
title: "Claude Managed Agents 자체 호스팅 고르는 법, 샌드박스만 들일까 서비스까지 들일까"
date: 2026-11-16 11:50:00 +0900
categories: ["Claude"]
tags: ["클로드", "AI에이전트", "자체호스팅", "매니지드에이전트", "에이전트보안"]
permalink: /posts/2026-11-16-claude-managed-agents-self-hosted/
description: "Anthropic이 Claude Managed Agents를 회사 클라우드나 사내 서버에 통째로 설치하는 자체 호스팅을 비공개 베타로 냈다. 세 가지 운영 방식 중 고르는 기준, 빠지는 기능, 첫 설치 순서를 공식 문서로 정리했다."
image: /assets/img/posts/2026-11-16-claude-managed-agents-self-hosted.png
mermaid: true
---

빌드가 깨지면 고치고, 알림이 오면 분류하는 AI 에이전트를 회사 코드에 붙이려 하면 보안팀이 먼저 묻는다. 코드는 어디서 돌고, 대화 기록은 어디에 남고, 비밀 키는 누가 쥐느냐다. Anthropic은 11월 12일 Claude Managed Agents를 회사 클라우드나 사내 서버에 통째로 설치하는 '자체 호스팅(self-hosted)'을 비공개 베타로 냈다. 이 글을 읽으면 세 가지 운영 방식 가운데 우리 팀에 맞는 것을 고르고, 자체 호스팅으로 옮길 때 잃는 기능과 새로 떠안는 일을 미리 따져 볼 수 있다.

{: .summary }
> - 운영 방식은 **셋**이다. 전부 Anthropic이 돌리는 **클라우드 샌드박스**, 도구 실행만 우리 쪽에 두는 **자체 호스팅 샌드박스**, 서비스까지 들이는 **자체 호스팅 Managed Agents**.
> - 세션 기록을 **우리 DB(PostgreSQL 16 이상)**에 둬야 하거나 모델 호출을 **Bedrock·Foundry·자체 게이트웨이**로 보내야 할 때만 서비스까지 들인다.
> - 자체 호스팅 서버에는 **웹훅·예약 실행·Files API·기본 문서 스킬**이 없다. 옮기기 전에 이 목록부터 대조한다.

## 무엇이 바뀌었나: '샌드박스만'에서 '서비스 전부'로

Managed Agents는 Claude를 오래 일하는 에이전트로 돌리는 API 묶음이다. 에이전트 루프(하네스), 명령을 실행하는 샌드박스, 자격 증명 보관, 세션 기록을 Anthropic이 제공한다. 처음에는 전부 Anthropic이 운영했고, 이후 코드만은 회사 안에서 돌려야 하는 팀을 위해 샌드박스만 직접 두는 방식이 추가됐다.

이번에 나온 자체 호스팅은 여기서 한 걸음 더 간다. 공식 문서는 세 방식을 "무엇을 누가 호스팅하나"로 나눈다.

| 방식 | 샌드박스 / 서비스 | 모델 |
|---|---|---|
| 클라우드 샌드박스(기본) | Anthropic / Anthropic | Anthropic |
| 자체 호스팅 샌드박스 | 우리 / Anthropic | Anthropic |
| 자체 호스팅 Managed Agents | 우리 / 우리 | Anthropic 또는 우리가 고른 곳 |

API는 호스팅 서비스와 같아서 SDK와 `ant` CLI가 그대로 붙는다. 신청은 Anthropic 계정 담당 팀을 통해서만 받는다.

## 어느 방식을 고를까: 질문 두 개로 갈린다

문서의 권고는 분명하다. 잘 모르겠으면 클라우드 환경으로 시작하고, 도구가 우리 인프라에서 돌아야 할 때만 자체 호스팅 샌드박스를 고른다. 서비스까지 들이는 것은 세션 기록 저장 위치나 모델 호출 경로를 직접 정해야 할 때다.

~~~mermaid
flowchart TD
  A[에이전트 운영 방식] --> B{사내망에서 실행?}
  B -- 아니오 --> C[클라우드 샌드박스]
  B -- 예 --> D{기록·모델도 직접?}
  D -- 아니오 --> E[샌드박스만 자체]
  D -- 예 --> F[전부 자체 호스팅]
~~~

둘째 질문에서 헷갈리기 쉬운 점이 있다. 샌드박스만 우리 쪽에 둬도 파일과 프로세스는 우리 서버에 남지만, 대화 기록과 도구 결과는 Anthropic이 운영하는 Managed Agents 서비스로 간다. 모델이 도구 결과를 받아야 다음 행동을 고를 수 있어서다. 자체 호스팅 Managed Agents에서는 세션 기록이 우리 데이터베이스에 남는다. 다만 모델을 부를 때마다 지금까지의 대화와 도구 입력·결과는 우리가 고른 추론 제공자(기본값은 Claude API)로 나간다.

모델 호출 경로는 서버 설정 `inference.provider` 한 줄로 바꾼다. 기본값 `anthropic` 외에 Amazon Bedrock(`bedrock`), Claude Models on Google Cloud(`vertex`), Microsoft Foundry(`foundry`), 자체 모델 게이트웨이(`gateway`)를 고를 수 있다. 에이전트 정의는 `claude-opus-5-5` 같은 Claude API 모델 ID를 그대로 쓰고, 서버가 제공자에 맞게 바꿔 준다.

## 서비스를 들이면 우리가 맡는 것

문서가 말하는 한 벌의 배포는 이렇게 생겼다.

- **서버(`cma-server`)**: API를 받고 에이전트 루프를 돌리며 에이전트·세션·기록을 저장한다. 셸이나 파일 도구는 직접 실행하지 않는다
- **데이터베이스**: PostgreSQL 16 이상. 없으면 메모리에만 저장해 재시작하면 지워진다
- **워커**: 서버에서 일을 받아 샌드박스 안에서 셸·파일 도구를 실행한다
- **서버 콘솔**: 서버 주소의 웹페이지. 사내 ID 공급자로 로그인한다

자격 증명도 셋으로 나뉜다. 앱이 서버를 부를 때 쓰는 서버 API 키, 서버만 쥐는 추론 자격 증명(Claude API 키나 클라우드 자격 증명), 워커가 한 환경의 작업 대기열에 붙을 때 쓰는 환경 키다. 앱과 워커는 모델 호출용 키를 몰라도 된다.

{: .warning }
문서는 에이전트의 bash 도구가 워커 프로세스의 권한과 네트워크 접근을 그대로 가진 "진짜 셸"이고, 워커는 그 셸을 격리하지 않는다고 적었다. 격리는 워커를 무엇 안에서 돌리느냐에서 나온다. Docker Compose 스택과 Helm 차트는 세션마다 컨테이너·파드를 따로 띄우지만, 워커를 직접 띄운다면 지켜야 할 것이 없는 일회용 컨테이너나 VM 안에서 돌려야 한다.

Anthropic 발표는 설계 원칙 네 가지를 함께 내놨다. 에이전트 루프와 샌드박스를 분리하고, 자격 증명은 샌드박스 밖 프록시가 요청에 붙이며, 환경마다 접속 가능한 호스트를 목록으로 제한하고, 모든 세션 기록을 OpenTelemetry로 내보낸다는 것이다. 자체 호스팅에서는 자격 증명을 회사 시크릿 매니저에 둘 수도 있다.

## 옮기기 전에 대조할 것: 빠지는 기능

자체 호스팅 서버는 호스팅 서비스와 같은 API지만 예외가 꽤 있다. 호스팅 쪽에서 만든 에이전트·스킬·자격 증명·메모리 저장소와 세션 기록은 하나도 복사되지 않으니 서버에서 다시 만들어야 한다.

| 없는 기능 | 대신 할 일(문서 기준) |
|---|---|
| 웹훅 | 이벤트 스트림을 따라가거나 이벤트 목록을 조회 |
| 예약 실행(scheduled deployments) | cron 같은 자체 스케줄러로 세션 시작 |
| 파일 리소스·Files API | 워커 작업 폴더에 파일을 두고, 이미지·PDF는 base64로 |
| 기본 docx·pdf·pptx·xlsx 스킬 | 스킬 저장소에서 받아 사용자 스킬로 올리기 |
| 클라우드 환경 | 모든 환경에 자체 워커 배치 |

기본값이 달라지는 것도 있다. MCP 서버와 Git 호스트는 서버 설정에 적어 둔 곳만 연결되고, 웹 검색·웹 가져오기 도구는 설정에서 켜기 전까지 꺼져 있다. MCP 도구 결과는 기본 100KiB를 넘으면 잘리고 나머지는 사라진다. 멀티에이전트는 미리 나열한 하위 에이전트(1~20개)에게만 일을 넘길 수 있다.

## 처음 띄워 보는 순서(개발용)

빠른 시작 문서는 한 대의 머신에서 Docker Compose로 서버·PostgreSQL·워커를 띄운다. 준비물은 릴리스 압축 파일(계정 담당 팀에 요청), Claude API 키, Compose 플러그인이 있는 최신 Docker Engine, CPU 2개 이상, `openssl`과 `ant` CLI다.

1. 압축을 풀고 그 안의 `compose` 폴더로 들어간다
2. `.env` 파일에 DB 비밀번호, Claude API 키, 서버 API 키, 저장 비밀 암호화 키를 넣고 권한을 600으로 둔다(비밀번호와 키는 `openssl rand`로 만든다)
3. `docker compose up --build -d`로 띄우고 로그에 `cma-server listening`이 나올 때까지 본다
4. `curl -s http://127.0.0.1:8400/cma-server/readyz`가 `"status":"ready"`를 돌려주는지 확인한다
5. 다른 터미널에서 `ANTHROPIC_BASE_URL`을 서버 주소로, `ANTHROPIC_API_KEY`를 서버 API 키로 바꾸고 `ant`로 에이전트와 세션을 만든다
{: .steps }

문서는 이 Compose 스택이 평문 HTTP를 쓰는 개발용이며 운영에는 릴리스에 든 Helm 차트 두 개를 권한다고 적었다. 에이전트 도구가 그 머신의 컨테이너에서 돌기 때문에 지킬 것이 없는 머신을 쓰라는 경고도 붙어 있다.

{: .interpret }
자체 호스팅은 "더 안전한 버전"이라기보다 책임을 옮기는 선택이다. 기록 보관과 모델 경로를 직접 정하는 대신 서버 보안, 릴리스 설치, 워커 격리, 이상 사용 탐지를 우리 팀이 맡는다. 데이터 위치 요건이 없다면 클라우드나 샌드박스만 자체 호스팅하는 쪽이 운영 부담 대비 얻는 것이 크다.

## 마무리

자체 호스팅 신청서를 내기 전에 할 일은 서버 사양 계산보다 지금 쓰는 기능 목록을 '빠지는 기능' 표와 맞춰 보는 것이다. 웹훅으로 세션을 시작하거나 기본 문서 스킬에 기대는 흐름이 있다면, 그 대체 경로부터 설계해 둬야 베타 접근을 받은 날 바로 옮길 수 있다.

<details markdown="1">
<summary>출처 6곳</summary>

- Anthropic, 「Operate Claude Managed Agents inside your security perimeter」(2026-11-12): [claude.com](https://claude.com/resources/articles/self-hosted-claude-managed-agents)
- Claude Platform Docs, 「Self-hosted Claude Managed Agents」: [platform.claude.com](https://platform.claude.com/docs/en/managed-agents/self-hosted)
- Claude Platform Docs, 「Differences from the hosted service」: [platform.claude.com](https://platform.claude.com/docs/en/managed-agents/self-hosted/differences)
- Claude Platform Docs, 「Choosing an agent environment」: [platform.claude.com](https://platform.claude.com/docs/en/managed-agents/choosing-an-environment)
- Claude Platform Docs, 「Get started with self-hosted Claude Managed Agents」: [platform.claude.com](https://platform.claude.com/docs/en/managed-agents/self-hosted/quickstart)
- Claude Platform Docs, 「Inference provider」: [platform.claude.com](https://platform.claude.com/docs/en/managed-agents/self-hosted/inference-provider)

</details>
