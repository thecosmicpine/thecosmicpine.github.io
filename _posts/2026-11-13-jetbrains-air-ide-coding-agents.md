---
layout: post
title: "젯브레인 IDE 2026.3 Air 쓰는 법, AI 코딩 에이전트 여러 개 돌리고 Code Notes로 리뷰한다"
date: 2026-11-13 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["JetBrains", "AI코딩에이전트", "코드리뷰", "IntelliJ", "Junie"]
permalink: /posts/2026-11-13-jetbrains-air-ide-coding-agents/
description: "IntelliJ 등 젯브레인 IDE 2026.3에 들어간 Air로 Claude·Codex·Copilot·Junie 에이전트를 한곳에서 돌리는 법. 구독 연결, 임시 worktree로 병렬 작업, Code Notes 리뷰, AI Assistant에서 넘어올 때 달라지는 점까지."
image: /assets/img/posts/2026-11-13-jetbrains-air-ide-coding-agents.png
mermaid: true
---

IntelliJ IDEA나 PyCharm을 쓰면서 AI 코딩 에이전트는 터미널 창에 따로 띄워 두는 사람이 많다. 에이전트가 무엇을 바꿨는지 보려면 다시 IDE로 돌아와 diff를 뒤져야 한다. 젯브레인은 11월 11일 블로그에서 2026.3 버전부터 'Air in JetBrains IDEs'를 IDE에 정식으로 넣었다고 밝혔다. 이 글을 읽으면 이미 쓰는 Claude·Codex·Copilot 구독을 IDE 안에 연결하고, 에이전트 여러 개를 서로 부딪치지 않게 돌리고, 결과를 줄 단위 메모로 되돌려 보내는 순서를 알 수 있다.

{: .summary }
> - Air는 AI 모델이 아니라 **에이전트 작업대**다. Codex·Claude·GitHub Copilot·Junie 등을 IDE 안에서 돌리고, **JetBrains AI 유료 구독은 필요 없다**.
> - 2026.3부터 IDE에 **기본으로 들어 있다**. 툴바의 **New Session**이나 **Ctrl 두 번**(전역 프롬프트)으로 세션을 연다.
> - 에이전트가 끝나면 **Review Code**로 바뀐 파일을 보고, 줄 옆에 **Code Notes**를 달아 에이전트에게 돌려보낸다.

## Air는 무엇이고, 무엇이 아닌가

공식 문서는 Air를 "코딩 에이전트를 돌리는 작업 공간"이라고 설명하고, 스스로 AI 서비스가 아니라고 못 박는다. 모델은 내가 고른 에이전트와 그 공급자에서 온다. PC에 이미 설치된 Codex나 Junie 같은 에이전트는 IDE가 SDK를 찾듯 자동으로 잡히고, 없으면 레지스트리에서 설치한다. 그 밖의 에이전트는 ACP(Agent Client Protocol)라는 공통 규격으로 붙는다. 젯브레인 FAQ가 꼽은 지원 목록에는 Codex, Claude Agent, Claude Code, Gemini, GitHub Copilot, DeepSeek, OpenCode, Cursor, Grok, Kimi 등이 있다.

비용 구조도 여기서 갈린다. 다른 회사 구독을 쓰면 코드는 젯브레인을 거치지 않고 그 공급자로 바로 간다. 젯브레인 계정으로 로그인하면 자체 에이전트 Junie를 'Lite' 구성으로 무료로 쓸 수 있다(공정 사용 조건). IDE의 일반 코드 자동 완성은 그대로 동작하고 JetBrains AI 사용량에 잡히지 않는다.

{: .note }
Air는 에이전트를 저절로 켜거나 코드를 보내지 않는다. 내가 에이전트를 고르고 인증해야 시작된다. 조직은 JetBrains Console에서 쓸 수 있는 에이전트·공급자·모델·MCP 서버를 정할 수 있다.

## 켜는 순서: 업데이트하고, 세션 열고, 인증한다

2026.3 이상이면 Air 플러그인이 IDE에 기본으로 들어 있다. 2026.2는 설정의 Plugins > Marketplace에서 'Air'를 찾아 설치한다. 플러그인 자체는 무료다.

1. IDE를 2026.3으로 올리고, 에이전트를 맡길 프로젝트를 연다.
2. 메인 툴바의 **New Session**을 누르거나 옆 화살표에서 에이전트 프리셋을 고른다. IDE 어디서든 **Ctrl을 두 번**(윈도우 단축키 기준) 누르면 전역 프롬프트가 열린다.
3. 첫 메시지를 보내면 에이전트가 기존 로그인을 찾는다. 없으면 'Choose a sign-in method' 목록에서 에이전트 로그인, JetBrains AI, 'Add an AI provider'(API 키) 중 하나를 고른다.
4. 모델, 추론 강도(effort), 확인 없이 할 수 있는 작업 범위(operation mode)를 정한다.
5. 할 일을 쓰고 `@file:`, `@folder:`로 파일을, `$`로 스킬을 붙여 보낸다.
6. 끝나면 세션 탭 위쪽의 **Review Code**를 눌러 바뀐 내용을 본다.
{: .steps }

자주 쓰는 조합은 프리셋으로 저장해 둔다. 프리셋은 에이전트·모델·effort·operation mode를 묶은 것으로, 문서는 "작은 수정용과 여러 단계 작업용을 따로 두라"고 예를 든다.

## 여러 에이전트를 동시에 돌릴 때는 임시 worktree

에이전트 두 개가 같은 폴더를 동시에 고치면 서로의 변경을 덮어쓸 수 있다. Air는 세션마다 별도의 Git worktree를 줄 수 있다. worktree는 같은 저장소의 Git 기록을 공유하면서 파일과 체크아웃만 따로 갖는 작업 사본이다.

새 세션을 열 때 프롬프트 위의 실행 방식 목록에서 **Temporary Worktree**를 고르고 기준 브랜치를 정하면 된다. 진행 중인 세션에서 다른 접근을 시험하고 싶으면 Agent Sessions 창에서 세션을 오른쪽 클릭해 **Fork Session > Fork in new temporary worktree**를 고른다. 원래 세션은 그대로 남고, 갈라진 세션은 자기 사본에서 일한다. 어느 세션이 일하는지, 어느 세션이 내 입력을 기다리는지, 읽지 않은 결과가 있는지는 Agent Sessions 창에 프로젝트별로 모인다.

{: .warning }
젯브레인 발표문에 따르면 에이전트가 스스로 만든 worktree는 아직 Air가 추적하지 않는다. 병렬 작업은 Air 쪽에서 Temporary Worktree로 시작해야 리뷰와 변경 옮기기가 한곳에서 된다.

## 리뷰는 Code Notes로 돌려보낸다

Air가 가장 공들인 부분은 리뷰다. 젯브레인은 발표문에서 "에이전트가 코드를 더 많이 쓸수록 병목은 리뷰로 옮겨 간다"고 쓰고, 개발자 49%가 AI 출력 검토와 프롬프트 수정에 주 4시간 이상을 쓴다는 아틀라시안 조사를 인용했다.

리뷰는 이렇게 흘러간다. **Review Code**에서 범위를 고른다. 커밋 전 변경만 보려면 Local changes, 이미 만든 커밋까지 보려면 그 커밋을 누른다. 바뀐 파일이 Review in progress 탭에 뜨면 diff를 보며 고칠 줄 옆 여백을 눌러 질문이나 수정 요청을 적는다. 다 봤으면 **Finish & Attach Comments**를 눌러 메모를 세션에 붙이고 보낸다. 에이전트는 메모가 달린 줄의 맥락과 함께 받아 답하거나 코드를 고친다.

| 할 일 | 누르는 곳 | 알아 둘 점 |
|---|---|---|
| 변경 검토 시작 | 세션 탭 Review Code | Git 저장소 필요 |
| 줄 단위 요청 | diff 줄 옆 여백 | 한 번에 세션 하나만 리뷰 |
| 커밋 메시지 | Commit 창 Generate Commit Message | AGENTS.md 형식을 따른다 |

터미널 화면에서 도는 에이전트(예: Claude Code)는 이 리뷰 모드를 쓸 수 없다. 대신 메모를 프롬프트 칸에 직접 붙여 보낸다.

## 내 구독은 어떻게 붙나

구독마다 연결하는 자리가 다르다. 아래 흐름도는 공식 문서와 발표문에 나온 경로만 정리한 것이다.

~~~mermaid
flowchart TD
  A[Air 세션 시작] --> B{쓰는 구독은?}
  B -- Claude Pro·Max --> C[터미널로 Claude]
  B -- Copilot --> D[Copilot 고르고 로그인]
  B -- API 키 --> E[AI provider 추가]
  B -- 없음 --> F[Junie Lite 무료]
~~~

Claude Pro·Max 구독은 Air의 채팅 화면에서 쓸 수 없다. 문서는 채팅이 SDK 연동이라 앤트로픽 약관상 구독을 그렇게 쓸 수 없다고 설명한다. Agent Sessions 창에서 New Session 옆 화살표 > **Manage Agents**로 가서 Claude 카드를 **Terminal**로 바꾸면, Claude Code가 IDE 탭 안에서 열리고 구독으로 로그인할 수 있다. 채팅 화면의 Claude Agent는 JetBrains AI 구독이나 앤트로픽 API 키가 있어야 한다.

GitHub Copilot은 에이전트 목록에서 고르고 GitHub로 로그인하면 내 프로젝트에서 바로 돈다. 사용량은 Air가 아니라 GitHub가 관리하므로 남은 한도도 GitHub에서 확인해야 한다. 클라우드에서 돌리는 기능은 회사가 Air Teams를 쓸 때만 된다.

{: .interpret }
Air의 계산은 "새 구독을 하나 더 파는 것"보다 "이미 낸 구독을 IDE 안으로 끌어오는 것"에 가깝다. 에이전트를 바꿔도 리뷰·worktree·커밋 흐름은 같으니, 팀이 에이전트를 섞어 써도 검토 방식은 하나로 맞출 수 있다. 다만 공식 문서도 Air가 활발히 개발 중이라 화면이 자주 바뀔 수 있다고 적어 두었다.

## AI Assistant를 쓰던 사람이 알아 둘 것

Air로 넘어오면 기존 AI Chat 대화는 Junie 세션으로 자동으로 옮겨진다. 짧은 질문은 Junie를 Lite나 Luna 모델에 effort를 Off로 두고 쓰라는 게 젯브레인 안내다. 오른쪽 도구 창 배치가 익숙하면 Air 왼쪽 아래 Settings > Show Chat > In Toolwindow를 고른다.

AI Chat 배너에서 'Switch to Air'를 눌렀다면 AI Assistant는 숨겨진다. 다시 쓰려면 Shift를 두 번 눌러 'Open AI Assistant' 액션을 실행한다. AI Assistant는 2027년 초까지 별도 플러그인으로 지원된다. Air를 아예 끄려면 설정의 Plugins에서 비활성화하고 IDE를 다시 시작한다.

## 마무리

Air를 켜도 에이전트가 하는 일 자체는 터미널에서와 같다. 달라지는 것은 그 결과를 내가 받아 드는 방식이다. 에이전트가 쓴 코드를 IDE의 디버거·검사·테스트로 확인하고 줄마다 메모로 돌려보내는 습관이 생기면, 어느 에이전트를 쓰든 "내가 이해한 코드만 커밋한다"는 기준을 지키기가 쉬워진다.

<details markdown="1">
<summary>출처 6곳</summary>

- JetBrains AI 블로그, 「JetBrains IDEs Transformed for the Agentic Era of Development – With Air」(2026-11-11): [blog.jetbrains.com](https://blog.jetbrains.com/ai/2026/11/air-in-jetbrains-ides-ga/)
- JetBrains 문서, 「Air in IDEs」 개요: [jetbrains.com](https://www.jetbrains.com/help/air-ides/air-overview.html)
- JetBrains 문서, 「Quickstart guide」: [jetbrains.com](https://www.jetbrains.com/help/air-ides/air-in-ides-quickstart.html)
- JetBrains 문서, 「Start, continue, or fork a session」: [jetbrains.com](https://www.jetbrains.com/help/air-ides/air-in-ides-start-a-session.html)
- JetBrains 문서, 「Review and commit changes」·「Use Claude subscription」: [jetbrains.com](https://www.jetbrains.com/help/air-ides/air-in-ides-review-changes.html), [jetbrains.com](https://www.jetbrains.com/help/air-ides/air-in-ides-claude-subscription.html)
- JetBrains Air 블로그, 「Use Your GitHub Copilot Plan in JetBrains Air」 및 AI Assistant 문서 「Switch to JetBrains Air in IDEs」: [blog.jetbrains.com](https://blog.jetbrains.com/air/2026/11/github-copilot-in-air/), [jetbrains.com](https://www.jetbrains.com/help/ai-assistant/switch-to-air.html)

</details>
