---
layout: post
title: "안드로이드 스튜디오에서 Claude·Codex 에이전트 쓰는 법, Rabbit 2의 BYOA는 설정 한 곳에서 고른다"
date: 2026-11-07 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["안드로이드스튜디오", "AI코딩에이전트", "BYOA", "ACP", "클로드"]
permalink: /posts/2026-11-07-android-studio-byoa-claude-codex/
description: "안드로이드 스튜디오 Rabbit 2부터 Claude Agent·Codex·Antigravity 등 40개 넘는 코딩 에이전트를 IDE 안에서 고른다. 켜는 곳, 에이전트가 쓰는 도구, 요금제가 갈리는 지점을 공식 문서로 정리했다."
image: /assets/img/posts/2026-11-07-android-studio-byoa-claude-codex.png
mermaid: true
---

안드로이드 앱을 만들 때 코딩 에이전트를 터미널에서 따로 돌리면, 빌드 오류는 복사해 붙이고 에뮬레이터 화면은 말로 설명해야 한다. 구글이 10월 28일 안정 버전으로 낸 Android Studio Rabbit 2에는 이 틈을 메우는 기능 'Bring Your Own Agent(BYOA)'가 들어갔다. 이 글을 읽으면 IDE 안에서 어떤 에이전트를 어디서 켜는지, 그리고 내 요금제로 무엇을 쓰게 되는지 판단할 수 있다.

{: .summary }
> - Rabbit 2부터 **Claude Agent·Codex·Antigravity** 등 **40개 넘는** 코딩 에이전트를 안드로이드 스튜디오 안에서 고른다.
> - 켜는 곳은 에이전트 창, 또는 **Settings > Tools > AI > Agents**다. 고른 뒤 로그인하거나 API 키를 넣는다.
> - 내장 에이전트는 **추가 요금 없이** 남는다. 다른 회사 에이전트는 **그 회사 요금제와 조건**을 따른다.

## BYOA는 에이전트와 IDE 사이에 표준 플러그를 꽂는다

BYOA의 바탕은 Agent Client Protocol(ACP)이다. ACP 공식 문서는 이 규약을 편집기·IDE와 코딩 에이전트가 주고받는 말을 맞춘 표준이라고 설명한다. 언어 서버 프로토콜(LSP)이 언어 지원을 편집기마다 따로 만들 필요를 없앤 것처럼, ACP를 지키는 에이전트는 ACP를 지원하는 편집기 어디서나 돈다.

안드로이드 스튜디오는 여기에 IDE만 아는 정보를 얹는다. 릴리스 노트에 따르면 BYOA는 프로젝트 구조 전체, 빌드 진단, 에뮬레이터 제어를 에이전트에 바로 넘긴다. 구글은 이 덕분에 에이전트가 필요한 파일만 골라 토큰을 덜 쓰고 더 빨리 움직인다고 설명한다.

일정은 두 단계였다. 9월 24일 Rabbit 2 카나리(미리보기 채널)에서 Claude Agent·Codex·Antigravity를 앞세워 미리보기로 시작했고, 10월 28일 Rabbit 2가 안정 버전이 되면서 공식 블로그는 고를 수 있는 에이전트가 40개를 넘는다고 적었다. 목록에는 Junie도 있다.

## 연결하는 법: 최신 안정 버전에서 에이전트 창부터

공식 릴리스 노트와 블로그가 적은 순서는 짧다.

1. 안드로이드 스튜디오를 최신 안정 버전(Rabbit 2 이상)으로 올린다
2. 에이전트 창을 열고 기본 목록(Claude Agent, Codex, Antigravity)에서 하나를 고른다
3. 그 에이전트 계정으로 로그인하거나 API 키를 넣는다
4. 목록에 없는 에이전트는 Settings > Tools > AI > Agents의 레지스트리에서 찾는다(맥은 File 대신 Android Studio 메뉴)
5. 첫 프롬프트를 보낸다
{: .steps }

에이전트는 여러 개를 연결해 둘 수 있다. 9월 블로그는 한 에이전트의 사용량이 바닥나거나 결과가 기대에 못 미치면 다른 에이전트가 이어받게 할 수 있다고 적었다.

## 에이전트가 IDE 안에서 쓰는 도구

연결된 에이전트는 안드로이드 에뮬레이터, 빌드 시스템, Logcat 같은 안드로이드 스튜디오 도구에 접근한다. 릴리스 노트는 여기에 안드로이드 SDK 도구, 터미널·셸 실행을 더해 적었다. 9월 블로그는 Jetpack Compose 미리보기 같은 UI 도구도 붙는다고 했다.

할 수 있는 일의 범위도 넓다. 파일 읽기·쓰기·수정, 셸 명령, 테스트 실행, 웹 검색을 하고, 코드 리뷰나 테스트 같은 하위 작업에는 서브에이전트를 띄운다. 프로젝트의 스킬, 슬래시 명령, 메모리를 자동으로 불러와 긴 세션을 이어 간다.

같은 릴리스에서 'Android 스킬' 관리 화면도 생겼다. XML 화면을 Jetpack Compose로 옮기기, AGP 9로 올리기 같은 작업 절차가 미리 들어 있다. 여는 곳은 세 군데다. 에이전트 패널의 점 세 개 메뉴(Manage Agent Skills), 채팅창에 @를 치고 Manage skills, 또는 Settings > Tools > AI > Skills Manager다.

## 요금제가 갈리는 지점

BYOA로 들어온 에이전트는 여전히 그 회사 서비스다. 9월 블로그는 기업용·개인용 AI 요금제를 모두 지원하되 "에이전트 제공사에 따른다"고 못 박았다.

| 고른 에이전트 | 로그인·요금 | 공식 문서가 적은 점 |
|---|---|---|
| 내장 에이전트 | 추가 요금 없음 | 계속 제공 |
| Google Antigravity | Google AI Pro·Ultra 또는 Gemini API 키 | 최신 Gemini 모델, 더 많은 사용량 |
| Claude Agent·Codex 등 | 각 회사 로그인 또는 API 키 | 제공사 조건을 따름 |

구글은 제미나이를 가장 잘 쓰려면 내장 에이전트보다 Antigravity를 고르라고 권한다. 회사에서 Gemini Enterprise를 쓰면 관리자가 승인된 스킬·에이전트·모델 엔드포인트를 정책으로 정할 수 있다.

~~~mermaid
flowchart TD
  A[어떤 에이전트?] --> B{추가 비용 없이?}
  B -- 예 --> C[내장 에이전트]
  B -- 아니오 --> D{쓰는 요금제는?}
  D -- Google AI --> E[Antigravity]
  D -- 다른 회사 --> F[Claude·Codex 등]
~~~

{: .warning }
연결한 에이전트는 셸 명령을 실행하고 파일을 고칠 수 있다. 구글은 위험한 작업 앞에서 멈춰 승인을 받는 세부 권한을 제공한다고 적었다. 회사 코드라면 어느 에이전트에 코드를 보내도 되는지 사내 규정부터 확인하는 편이 안전하다.

{: .interpret }
이번 변화의 핵심은 '구글이 다른 회사 AI를 들였다'보다, IDE가 에이전트를 고르는 곳이 아니라 에이전트에게 도구를 빌려주는 곳으로 바뀌었다는 데 있어 보인다. 에이전트 성능이 비슷해질수록 빌드 진단과 에뮬레이터를 얼마나 잘 넘기느냐가 IDE의 경쟁력이 된다. 다만 같은 에이전트라도 터미널과 IDE에서 결과가 얼마나 다른지는 공식 자료에 숫자가 없어, 내 프로젝트로 비교해 봐야 안다.

## 마무리

에이전트를 바꾸는 비용이 '도구를 갈아타기'에서 '목록에서 다시 고르기'로 줄었다. 그렇다면 다음에 따져 볼 것은 어느 에이전트가 똑똑한가보다, 내 요금제와 회사 규정이 어느 에이전트까지 허락하는가다.

<details markdown="1">
<summary>출처 4곳</summary>

- Android Developers Blog, Matthew Warner, 「Your favorite agents are now integrated in Android Studio」(2026-10-28): [developer.android.com](https://developer.android.com/blog/posts/ai-agents-android-studio-integration)
- Android Developers Blog, Matthew Warner, 「Build your way: Use any AI agent of your choice in Android Studio」(2026-09-24): [android-developers.googleblog.com](https://android-developers.googleblog.com/2026/09/build-your-way-use-any-ai-agent-in-android-studio.html)
- Android Developers, 「Android Studio release notes」(Rabbit 2 새 기능): [developer.android.com](https://developer.android.com/studio/releases)
- Agent Client Protocol, 「Introduction」: [agentclientprotocol.com](https://agentclientprotocol.com/)

</details>
