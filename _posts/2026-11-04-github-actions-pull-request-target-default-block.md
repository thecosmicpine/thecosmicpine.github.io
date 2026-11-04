---
layout: post
title: "GitHub Actions pull_request_target, 12월 2일부터 공개 저장소에서 막힌다: 확인하는 곳과 허용하는 법"
date: 2026-11-04 11:50:00 +0900
categories: ["DevOps"]
tags: ["GitHubActions", "CI보안", "공개저장소", "워크플로정책", "공급망보안"]
permalink: /posts/2026-11-04-github-actions-pull-request-target-default-block/
description: "12월 2일부터 공개 저장소의 pull_request_target 워크플로가 기본 차단된다. 어떤 워크플로가 걸리는지 확인하는 곳, pull_request로 바꿀지 정책으로 허용할지 고르는 기준을 정리했다."
image: /assets/img/posts/2026-11-04-github-actions-pull-request-target-default-block.png
mermaid: true
---

오픈소스 저장소에서 외부 기여자의 PR에 라벨을 붙이거나 댓글을 다는 자동화는 대개 `pull_request_target` 이벤트로 돈다. GitHub는 11월 2일 이 이벤트를 2026년 12월 2일부터 모든 공개 저장소에서 기본으로 막는다고 알렸다. 이 글을 읽으면 내 저장소에서 어떤 워크플로가 멈출지 어디서 확인하는지, 그 워크플로를 `pull_request`로 바꿀지 정책으로 허용할지 판단할 수 있다.

{: .summary }
> - **12월 2일**부터 공개 저장소의 `pull_request_target` 워크플로는 허용 정책이 없으면 실행되지 않는다. 비공개·내부 저장소는 해당 없다.
> - 그 전에 **11월 9일·16일** 두 차례, 한국 시각 다음 날 새벽 1시~3시에 미리 막아 보는 시험 차단이 있다.
> - 확인은 저장소 **Settings → Actions → Policies**의 Policy insights에서, 계속 써야 하면 이벤트 정책에서 명시적으로 허용한다.

## 무엇이 바뀌나: 기본 정책 하나가 생겼다

GitHub Actions에는 '워크플로 실행 보호(workflow execution protections)'라는 정책이 있다. 누가 워크플로를 실행할 수 있는지(actor 규칙), 어떤 이벤트가 워크플로를 깨울 수 있는지(event 규칙)를 허용 목록으로 정하는 기능이다. 이번 변경은 이 기능 위에 GitHub가 직접 만든 기본 이벤트 정책 하나를 얹는 것이다.

이 기본 정책은 이미 적용 가능한 이벤트 정책이 있는 저장소에서는 그 정책을 대신하지 않는다. 지금은 '평가(evaluate)' 모드라 워크플로가 그대로 돌고, 막혔을 실행만 기록된다. 원래 집행일은 11월 2일이었는데 12월 2일로 한 달 미뤄졌다. 적용 대상은 GitHub Free·Team·Enterprise Cloud의 공개 저장소이고, GitHub Enterprise Server는 빠진다.

| 날짜 | 시간(UTC) | 한국 시각 |
|---|---|---|
| 11월 9일 | 16:00~18:00 | 11월 10일 01:00~03:00 |
| 11월 16일 | 16:00~18:00 | 11월 17일 01:00~03:00 |
| 12월 2일 | 상시 | 이후 계속 차단 |

시험 차단 시간에 막힌 실행은 오류 주석이 달린 실패 실행으로 남고, 워크플로는 실행되지 않는다. 시간이 끝나면 다시 평가 모드로 돌아가 경고만 남긴다.

## 왜 막나: 포크 코드가 비밀값 옆에서 돈다

`pull_request`와 `pull_request_target`은 같은 PR 활동에 반응하지만 믿는 정도가 다르다. GitHub 문서에 따르면 차이는 다음과 같다.

| 구분 | pull_request | pull_request_target |
|---|---|---|
| 실행하는 워크플로 파일 | PR 병합 커밋 | 기본 브랜치 |
| 토큰·비밀값 | 읽기 전용, 비밀값 없음 | 읽기·쓰기 토큰, 비밀값 접근 |
| 기본 checkout 대상 | PR 병합 커밋 | 기본 브랜치 |

`pull_request_target` 자체는 기본 브랜치의 믿을 수 있는 코드만 돌리므로 안전하다. 문제는 포크 PR을 테스트하려고 `actions/checkout`에 {% raw %}`ref: ${{ github.event.pull_request.head.sha }}`{% endraw %}를 주고, 이어서 `make test`나 `npm install`처럼 그 코드를 실행할 때다. 공격자는 PR의 Makefile이나 빌드 스크립트에 명령을 숨겨 두기만 하면 저장소의 비밀값과 쓰기 토큰을 쓸 수 있다. GitHub Security Lab은 이 형태를 'pwn request'라고 부르고, 여러 공급망 침해의 원인이었다고 설명한다.

{: .interpret }
GitHub는 지금까지 문서와 보안 가이드로 "PR 코드를 실행하지 말라"고 안내해 왔다. 이번에는 이벤트 정책을 따로 두지 않은 공개 저장소에서 이벤트 자체를 꺼 두는 쪽을 택했다. 필요한 저장소만 스스로 이유를 확인하고 켜라는, 기본값을 뒤집는 방식이다.

## 내 저장소에서 확인하는 곳

먼저 어떤 워크플로가 걸리는지 본다. 저장소나 조직의 **Settings** 탭에서 왼쪽 메뉴 Actions 아래 **Policies**를 누르면, 그 아래에 **Policy insights** 페이지가 있다. 활성 정책이면 막힌 실행이, 평가 정책이면 막혔을 실행이 여기 나온다. 엔터프라이즈는 **Policies** 탭에서 Actions → Policies로 들어간다.

~~~mermaid
flowchart TD
  A[걸리는 워크플로] --> B{비밀값이 필요?}
  B -- 아니오 --> C[pull_request로 교체]
  B -- 예 --> D{PR 코드를 실행?}
  D -- 예 --> E[워크플로 구조 변경]
  D -- 아니오 --> F[이벤트 정책 허용]
~~~

확인부터 결정까지 순서는 다음과 같다.

1. Policy insights에서 `pull_request_target`으로 막혔거나 막혔을 워크플로를 찾는다
2. 비밀값이 필요 없는 워크플로는 `on: pull_request`로 바꾼다
3. 계속 써야 하는 워크플로는 Actions 정책에서 이벤트 정책을 만들고 `pull_request_target`을 허용하며, 워크플로 파일 경로로 대상을 좁힌다
4. 쓸 이유가 없으면 아무것도 하지 않는다. 12월 2일부터 기본 정책이 막는다
{: .steps }

정책 화면에서 이름과 적용 상태, 대상 워크플로·저장소를 고른 뒤 event 규칙을 설정한다. 직접 만드는 정책을 '평가' 상태로 시험하는 기능은 GitHub Enterprise Cloud에서만 된다. 정책은 REST API로도 관리할 수 있다.

## 계속 써야 한다면 먼저 줄일 것

GitHub 문서는 `pull_request_target`을 허용하기 전에 두 가지를 묻는다. `pull_request`로 대신할 수 있는지, 그리고 checkout한 PR 코드가 어디서든 실행되는지다. 실행은 내가 적은 단계만이 아니라 의존성 설치, 설정 파일, 빌드 스크립트에서도 일어난다. PR 코드를 데이터로 읽기만 하는 게 아니라면 허용하지 않는 편이 맞다.

허용하기로 했다면 문서가 권하는 보강은 다음과 같다. `GITHUB_TOKEN` 권한과 비밀값을 꼭 필요한 만큼으로 줄인다. 이 이벤트로 도는 워크플로는 기본 브랜치 캐시를 읽기만 할 수 있으니, 캐시를 채우는 일은 `push` 같은 믿을 수 있는 트리거로 옮긴다. 셀프 호스티드 러너라면 내부망과 분리하고 실행마다 새로 만든다.

{: .warning }
`actions/checkout`에는 포크 PR의 head를 받아오지 못하게 막는 보호가 있고, `allow-unsafe-pr-checkout: true`를 줘야 풀린다. 이 입력은 정책 허용과 별개다. checkout한 코드가 절대 실행되지 않는다고 확인한 경우에만 쓴다. `git fetch`나 `gh pr checkout`, 내려받은 아티팩트 실행은 이 보호가 잡지 못한다.

## 마무리

이번 변경으로 "아무도 손대지 않은 공개 저장소의 위험한 기본값"은 사라진다. 반대로 꼭 필요한 자동화를 가진 저장소는 허용 정책이라는 기록을 남기게 된다. 12월 2일까지 기다릴 필요 없이, 11월 9일 첫 시험 차단 전에 Policy insights를 한 번 열어 보는 것만으로 무엇이 멈출지 알 수 있다.

<details markdown="1">
<summary>출처 5곳</summary>

- GitHub Changelog, 「pull_request_target blocked by default December 2」(2026-11-02): [github.blog](https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2)
- GitHub Docs, 「Securely using pull_request_target」: [docs.github.com](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
- GitHub Docs, 「Governing execution of GitHub Actions workflows」: [docs.github.com](https://docs.github.com/en/actions/how-tos/administer/control-workflow-execution)
- GitHub Docs, 「About Actions policies」: [docs.github.com](https://docs.github.com/en/actions/concepts/about-actions-policies)
- GitHub Security Lab, 「Keeping your GitHub Actions and workflows secure Part 1: Preventing pwn requests」: [securitylab.github.com](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)

</details>
