---
layout: post
title: "GitHub Agentic Workflows 쓰는 법, 마크다운 한 장이 Actions 워크플로가 된다"
date: 2026-11-01 11:50:00 +0900
categories: ["DevOps"]
tags: ["깃허브액션", "AgenticWorkflows", "AI에이전트", "CI자동화", "gh-aw"]
permalink: /posts/2026-11-01-github-agentic-workflows-quickstart/
description: "10월 28일 정식 출시된 GitHub Agentic Workflows를 저장소에 처음 붙이는 순서와, 에이전트에게 쓰기 권한을 주지 않는 safe outputs 구조, 비용을 보는 명령까지 정리했다."
image: /assets/img/posts/2026-11-01-github-agentic-workflows-quickstart.png
mermaid: true
---

이슈 분류, 실패한 CI 원인 찾기, 문서 손보기처럼 매번 사람이 읽고 판단해야 했던 저장소 일은 YAML 스크립트로 자동화하기 어려웠다. GitHub가 10월 28일 이런 일을 AI 코딩 에이전트에게 맡기는 GitHub Agentic Workflows를 정식 출시했다. 이 글을 읽으면 내 저장소에 첫 에이전트 워크플로를 붙이는 순서와, 에이전트가 무엇을 할 수 있고 무엇은 못 하게 막혀 있는지를 판단할 수 있다.

{: .summary }
> - 자동화 내용을 **마크다운 파일**로 쓰면 `gh aw compile`이 표준 GitHub Actions YAML(`.lock.yml`)로 바꿔 준다.
> - 에이전트는 기본적으로 **읽기 권한**만 갖고, 이슈·PR 생성은 별도 job이 **safe outputs**로 대신 처리한다.
> - 공식 빠른 시작은 **약 10분**, 확장 설치 → `gh aw add-wizard` → 실행 확인 세 단계다.

## 무엇이 달라졌나: 자연어 지시서가 워크플로가 된다

GitHub 체인지로그에 따르면 Agentic Workflows는 GitHub Next의 오픈소스 프로젝트이고, 10월 28일 github.com의 Free·Team·Enterprise 요금제에서 정식으로 쓸 수 있게 됐다. 워크플로 파일 하나는 두 부분으로 나뉜다. 맨 위 `---` 사이의 YAML 머리말에는 언제 돌지(트리거), 무엇에 접근할지(권한), 어떤 도구를 쓸지를 적고, 그 아래에는 에이전트에게 시킬 일을 평범한 문장으로 쓴다.

~~~markdown
---
on: daily
safe-outputs:
  create-issue:
---
어제 올라온 이슈를 요약하고, 답이 필요한 것을 표시해 줘.
~~~

이 파일을 컴파일하면 일반 Actions 워크플로가 나오므로, 이미 쓰고 있는 러너 그룹과 정책 제약이 그대로 적용된다. 에이전트 엔진은 GitHub Copilot이 기본이고 Claude Code, OpenAI Codex, Google Gemini, Pi 중에서 고를 수 있다.

{: .interpret }
"AI가 Actions를 대신 짠다"가 아니라 "Actions 안에서 AI가 판단만 맡는다"에 가깝다. 빌드·테스트·배포처럼 같은 입력에 같은 결과가 나와야 하는 일은 공식 문서도 기존 Actions에 그대로 두라고 권한다.

## 처음 붙이는 순서: 확장 설치부터 첫 보고서까지

공식 빠른 시작은 GitHub Next가 공개한 예제 `repo-status`(저장소 활동을 모아 매일 보고서 이슈를 여는 워크플로)를 붙이는 것으로 시작한다. 준비물은 쓰기 권한이 있는 저장소, Settings → Actions에서 켜 둔 Actions, `gh` CLI 2.0.0 이상, 그리고 Copilot·Claude·Codex·Gemini 중 하나의 AI 계정이다.

1. `gh extension install github/gh-aw`로 확장을 설치한다
2. 저장소 루트에서 `gh aw add-wizard githubnext/agentics/repo-status`를 실행한다
3. 마법사에서 AI 엔진을 고르고, 엔진별 키를 저장소 시크릿으로 넣는다
4. 워크플로 `.md`와 생성된 `.lock.yml`이 `.github/workflows/`에 추가된다(직접 푸시 또는 PR)
5. 첫 실행은 2~3분쯤 걸린다. `gh aw status`나 Actions 탭에서 확인한다
6. 성공하면 Issues 탭에 "Daily Repo Report" 이슈가 생긴다
{: .steps }

내용을 고치려면 `.github/workflows/repo-status.md`의 "What to include" 부분을 내 저장소 사정에 맞게 바꾸면 된다. 머리말을 바꿨다면 `gh aw compile`로 다시 컴파일하고, `.md`와 `.lock.yml` 두 파일을 함께 커밋한 뒤 `gh aw run repo-status`로 다시 돌린다.

| 엔진 | 필요한 인증 |
|---|---|
| GitHub Copilot(기본) | 조직 결제의 `copilot-requests: write` 또는 `COPILOT_GITHUB_TOKEN` |
| Claude Code | `ANTHROPIC_API_KEY` 또는 Anthropic WIF |
| OpenAI Codex | `CODEX_API_KEY` 또는 `OPENAI_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` 또는 Google WIF |

Claude를 쓸 때 `claude login`으로 받은 구독 토큰(`CLAUDE_CODE_OAUTH_TOKEN`)은 지원하지 않는다. 넣으면 CLI가 오류를 내고 API 키나 WIF를 쓰라고 안내한다. 기본 엔진인 Copilot CLI로 돌리려면 Copilot 라이선스가 필요하다.

## 에이전트는 왜 직접 이슈를 못 여나: safe outputs

이 도구에서 가장 눈여겨볼 부분은 권한 구조다. 에이전트 job은 기본적으로 읽기 권한만 갖고, Agent Workflow Firewall 뒤의 샌드박스 컨테이너에서 실행된다. 에이전트가 "이슈를 만들고 싶다"고 구조화된 출력으로 요청하면, 쓰기 권한을 가진 별도 job이 그 요청을 검증한 뒤에 실행한다.

~~~mermaid
flowchart LR
  A[트리거] --> B[에이전트 job<br/>읽기 전용]
  B --> C[위협 탐지 job]
  C --> D[safe outputs job<br/>쓰기 권한]
  D --> E[이슈·PR·댓글]
~~~

머리말에 `safe-outputs:`를 따로 적지 않으면 `create-issue` 하나만 최대 1개로 자동으로 켜진다. 이슈 생성·댓글·라벨·PR 생성 같은 동작은 각각 키로 열어 줘야 하고, 대부분 한 번 실행에 최대 개수가 정해져 있다. 체인지로그는 여기에 더해 변경 사항을 적용하기 전에 모든 제안을 검사하는 위협 탐지 job이 따로 돈다고 설명한다.

{: .warning }
공식 빠른 시작은 `pull_request_target` 대신 `pull_request` 트리거를 쓰라고 경고한다. `pull_request_target`은 기준 저장소의 권한으로 돌기 때문에, 외부 PR 코드를 체크아웃해 실행하면 시크릿이나 쓰기 권한이 새어 나갈 수 있다.

## 비용은 두 갈래로 나간다

비용 관리 문서에 따르면 한 번 실행에 드는 돈은 GitHub Actions 사용 시간과 AI 제공사의 추론 요금을 더한 값이다. 보통 실행 한 번은 10~30초짜리 사전 job과 1~15분짜리 에이전트 job으로 이뤄지고, job마다 러너 준비에 약 1.5분이 더 붙는다.

<div class="stat-row">
  <div class="stat"><b>1 AIC = $0.01</b><span>gh-aw가 추론 비용을 세는 단위</span></div>
  <div class="stat"><b>1~15분</b><span>에이전트 job 한 번의 보통 길이</span></div>
  <div class="stat"><b>약 1.5분</b><span>job마다 붙는 러너 준비 시간</span></div>
</div>

`gh aw logs`를 실행하면 워크플로별 실행 시간, 토큰 사용량, AIC(AI Credits)를 표로 볼 수 있고, `gh aw audit <run-id>`로 실행 한 번을 자세히 뜯어볼 수 있다. 이번 정식 출시에서 실험 기능이던 `gh aw forecast`가 정식 기능이 됐고, 위협 탐지에 드는 크레딧과 월별 범위까지 함께 보여 준다. 다만 AIC는 models.dev 가격표로 추정한 값이라 실제 청구액은 각 제공사 결제 화면에서 확인하라고 문서는 적고 있다.

## 정식 출시에서 새로 생긴 것

체인지로그가 공개 프리뷰 이후 추가됐다고 밝힌 기능은 다섯 가지다.

| 기능 | 내용 |
|---|---|
| ARC·Docker-in-Docker | 자체 호스팅 ARC 러너에서 실행 |
| 예산 예측 | `gh aw forecast` 정식화, 월별 범위 표시 |
| 엔진·모델 선택 | 워크플로마다 모델 제공사 지정, 새 템플릿 |
| 모델 라우팅 | 작업 종류·난이도에 맞춰 모델 선택 |
| 격리 강화 | 마이크로 VM 실행, 저장소 간 데이터 유출을 막는 enclave |

{: .tip }
> - [ ] 첫 워크플로는 결과가 이슈 1개로 끝나는 보고서형부터 붙인다
> - [ ] `safe-outputs:`에 꼭 필요한 동작만 연다
> - [ ] 일주일 뒤 `gh aw logs`로 실행 시간과 AIC를 확인한다

## 마무리

비용 관리 문서의 첫 문장은 "결정적인 도구로 풀 수 있는 일이면 결정적인 도구를 쓰라"는 것이다. 에이전트 워크플로는 기존 CI를 갈아엎는 도구가 아니라, 사람이 읽고 판단하던 틈에만 끼워 넣는 도구로 설계됐다. 그러니 처음 고를 일도 "우리 팀이 매주 손으로 읽고 정리하는 것"에서 찾는 편이 빠르다.

<details markdown="1">
<summary>출처 5곳</summary>

- GitHub Changelog, 「GitHub Agentic Workflows generally available」(2026-10-28): [github.blog](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available)
- GitHub Agentic Workflows 문서, 「Quick Start」: [github.github.com](https://github.github.com/gh-aw/setup/quick-start/)
- GitHub Agentic Workflows 문서, 「How Agentic Workflows Work」: [github.github.com](https://github.github.com/gh-aw/introduction/how-they-work/)
- GitHub Agentic Workflows 문서, 「Safe Outputs」: [github.github.com](https://github.github.com/gh-aw/reference/safe-outputs/)
- GitHub Agentic Workflows 문서, 「Cost Management」: [github.github.com](https://github.github.com/gh-aw/reference/cost-management/)

</details>
