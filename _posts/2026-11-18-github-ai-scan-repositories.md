---
layout: post
title: "GitHub AI Scan 켜는 법, PR 검사와 저장소 전체 검사의 차이와 먼저 걸어 둘 예산"
date: 2026-11-18 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["GitHub", "AI보안스캔", "코드스캐닝", "CodeQL", "데브섹옵스"]
permalink: /posts/2026-11-18-github-ai-scan-repositories/
description: "GitHub 코드 스캐닝의 AI Scan이 PR 검사(정식)와 저장소 전체 검사(미리보기) 두 갈래가 됐다. 둘의 차이, 쓸 수 있는 저장소, 켜는 순서, 켜기 전에 정할 AI 크레딧 예산을 공식 문서로 정리했다."
image: /assets/img/posts/2026-11-18-github-ai-scan-repositories.png
mermaid: true
---

CodeQL을 켜 둔 저장소라도 PHP 화면, 셸 스크립트, Terraform 설정, Dockerfile에서는 보안 경고가 거의 올라오지 않는다. CodeQL이 그 언어를 분석하지 않기 때문이다. GitHub은 이 빈칸을 AI가 맡는 'AI Scan'을 10월 15일 PR 검사로 정식 출시했고, 10월 28일에는 저장소 전체를 훑는 검사를 공개 미리보기로 냈다. 11월에는 REST API 관리(13일)와 최대 20개 저장소 일괄 시작(16일)이 붙었다. 이 글을 읽으면 두 검사 중 무엇을 켤지 고르고, 켜기 전에 예산과 권한을 어디서 정해야 하는지 판단할 수 있다.

{: .summary }
> - AI Scan은 **두 갈래**다. PR이 열릴 때마다 자동으로 도는 **PR 검사(정식)**와, 사람이 버튼을 눌러 기본 브랜치 전체를 훑는 **저장소 검사(미리보기)**.
> - **Copilot 라이선스는 필요 없다.** 조직의 비공개 저장소는 **Code Security나 Advanced Security**가 있어야 하고, 개인 계정의 비공개 저장소는 쓸 수 없다.
> - 검사마다 **Code Security AI 크레딧**이 나간다. 저장소 검사는 한 번에 **30분·15만 크레딧**이 상한이니 켜기 전에 **하드 예산**부터 건다.

## 무엇이 나왔나: CodeQL 옆에 붙는 AI 검사기 두 개

AI Scan은 GitHub 코드 스캐닝 안의 기능 묶음이다. 경고는 CodeQL 경고와 같은 목록에 쌓이고, 담당자 지정·이슈 연결·보안 캠페인·자동 수정(agentic autofix) 같은 기존 처리 흐름을 그대로 탄다. 두 검사는 설정이 따로라 하나만 켤 수도 있다.

| 구분 | PR 검사 | 저장소 검사 |
|---|---|---|
| 상태 | 정식(10월 15일) | 공개 미리보기(10월 28일) |
| 언제 도나 | PR 생성·새 커밋마다 자동 | 쓰기 권한자가 직접 시작 |
| 무엇을 보나 | CodeQL이 안 보는 언어의 변경분 | 기본 브랜치 최신 커밋, 모든 언어 |
| 결과 위치 | PR 대화·변경 파일 탭("AI" 표시) | 코드 스캐닝 경고 목록 |

PR 검사가 보는 언어의 예로 공식 문서는 PHP, Shell/Bash, Terraform 설정(HCL), Dockerfile, 자바의 JSP, C#의 Blazor를 든다. 저장소 검사는 언어 제한이 없어서 CodeQL이 이미 분석하는 언어에서도 규칙 기반 분석이 놓친 문제를 찾는 것을 목표로 한다.

## 어느 쪽을 켤까: 막을 것인지, 쌓인 것을 찾을 것인지

두 검사는 성격이 다르다. PR 검사의 결과는 권고일 뿐이라 코드 스캐닝 검사를 실패시키지 않고, 규칙 세트로 병합을 막는 데도 쓸 수 없다. 포크에서 온 PR과 Dependabot이 만든 PR에서는 돌지 않는다. 저장소 검사는 이미 쌓인 코드를 한 번에 훑는 용도이고, 예약 실행이나 푸시마다 자동 실행은 아직 없다.

~~~mermaid
flowchart TD
  A[AI Scan 도입] --> B{CodeQL 밖 언어?}
  B -- 예 --> C[PR 검사부터]
  B -- 아니오 --> D{기존 코드 점검?}
  C --> D
  D -- 예 --> E[저장소 검사 수동]
  D -- 아니오 --> F[CodeQL만 유지]
~~~

PR 검사는 CodeQL 기본 설정이 없어도 돌고, CodeQL 분석이 실패하거나 대기 중이어도 따로 실행된다. 검사 엔진은 빌드 없이 PR 코드를 읽고 필요하면 코드 검색으로 맥락을 더 모은다. 저장소에 둔 `.github/copilot-instructions.md`나 `CLAUDE.md` 같은 지시 파일은 읽지 않고 GitHub이 만든 전용 프롬프트를 쓴다.

저장소 검사는 에이전트가 저장소를 돌며 취약점이 있을 만한 파일과 함수를 골라 들여다본다. 모든 파일을 끝까지 읽지 않고 정해진 시간 안에서 멈추므로, 한 번 돌렸다고 모든 취약점을 찾았다는 뜻은 아니다. CodeQL 경고와 겹치는 결과는 건너뛰지만 짝 맞추기가 최선 노력 수준이라 중복 경고가 생길 수 있다.

## 누가 쓸 수 있나: 저장소 주인과 공개 범위로 갈린다

두 검사 모두 Copilot 라이선스 없이 쓴다. 대신 저장소 주인과 공개 여부에 따라 조건이 붙는다.

| 저장소 | 공개 | 비공개·내부 |
|---|---|---|
| 조직 소유 | 사용 가능(활성 커미터 라이선스 불필요) | Code Security 또는 Advanced Security 필요 |
| 개인 계정 소유 | 사용 가능 | 사용 불가 |

저장소 검사는 github.com과 데이터 상주(data residency)형 GitHub Enterprise Cloud에서 쓸 수 있고, GitHub Enterprise Server는 지원하지 않는다. 자체 호스팅 러너도 두 검사 모두 지원하지 않는다.

## 켜는 순서: 엔터프라이즈 정책부터 저장소 버튼까지

엔터프라이즈 계정 아래 조직이라면 맨 위 정책이 기본값 '허용 안 함'이다. 이 정책 하나가 PR 검사와 저장소 검사를 함께 묶는다. 허용해도 자동으로 켜지지는 않는다.

1. 결제 관리자가 Code Security AI 크레딧의 포함량을 확인하고, 초과 사용을 막는 하드 예산을 건다
2. 엔터프라이즈 소유자가 코드 보안 정책에서 AI Scan을 '허용'으로 바꾼다
3. 조직 소유자나 보안 관리자가 조직 설정에서 AI Scan for repositories(필요하면 PR 검사도)를 켠다. 저장소는 조직 설정을 물려받고, 저장소 관리자는 개별로 끌 수 있다
4. 저장소에서 Security and quality 탭 → 왼쪽 Code scanning → 오른쪽 위 AI Scan 메뉴 → Standard scan 오른쪽 버튼으로 검사를 시작한다
5. 끝나면 경고 목록을 AI Scan 도구로 걸러 보고, 수정을 병합한 뒤에는 검사를 다시 돌려 닫힌 경고를 확인한다
{: .steps }

개인 계정의 공개 저장소는 저장소 설정에서 직접 켠다. 조직 설정을 끈 상태에서는 저장소 관리자가 따로 켤 수 없다. 저장소에서 끄는 곳은 Settings → Advanced Security → Code Security의 AI Scan for repositories 스위치다.

여러 조직을 스크립트나 IaC로 관리한다면 11월 13일 나온 REST API를 쓴다. `PATCH /orgs/{org}/code-scanning/ai-scan`과 `PATCH /repos/{owner}/{repo}/code-scanning/ai-scan`에 `repository_scan`을 `enabled`나 `disabled`로 보내고, PR 검사 설정 `pr_scan`도 같은 요청에 넣을 수 있다. 둘 중 하나라도 막히면 422 오류와 함께 둘 다 바뀌지 않는다. 설정을 켜는 것만으로 검사가 시작되지는 않는다.

{: .warning }
검사 비용은 활성 커미터 라이선스와 별도로 Code Security AI 크레딧에서 나간다. 공개 저장소라 라이선스가 필요 없는 경우도 마찬가지다. Copilot 이용권에 딸린 포함 크레딧이 있으면 그것부터 쓰고, 다 쓰면 종량 과금으로 넘어간다. 저장소 검사의 탐지 단계는 한 번에 30분, 15만 크레딧이 상한이다. 하드 예산이 바닥나면 검사가 결과를 내지 못하고, 예산을 올리거나 새 결제 주기가 시작돼야 다시 돈다.

## 결과를 다룰 때 알아 둘 것

저장소 검사 경고는 수정을 병합해도 저절로 닫히지 않는다. 병합 뒤 검사를 다시 시작해야 하고, 미리보기 기간에는 수정이 경고를 낸 바로 그 줄을 바꿨을 때만 재검사에서 자동으로 닫힌다. 다른 줄을 고쳐 문제를 없앴다면 사람이 직접 닫아야 한다. 재검사에서 같은 문제가 다시 나오면 기존 경고는 열린 채로 두고 새 문제만 추가한다.

문서는 AI가 만든 결과가 틀릴 수 있으니 하나씩 검토하라고 적는다. PR 검사 결과에는 엄지 위·아래 버튼이 있어 오탐을 알릴 수 있다. 조직 단위로는 보안 개요(security overview)에서 PR 검사가 켜진 저장소 수와 발견·해결 건수, 자동 수정 적용 빈도를 볼 수 있다.

{: .interpret }
PR 검사는 병합을 막지 못하는 '두 번째 리뷰어'에 가깝고, 저장소 검사는 비용 상한이 걸린 '일회성 감사'에 가깝다. 그래서 처음에는 CodeQL이 못 보는 언어가 많은 저장소 몇 개에 PR 검사를 켜고, 저장소 검사는 예산을 걸어 둔 채 중요한 저장소부터 한 번씩 돌려 보며 경고 품질과 크레딧 소모를 재 보는 순서가 무리가 적다.

## 마무리

AI Scan을 켜기 전에 정할 것은 "무슨 언어를 검사하나"보다 "누가 버튼을 누르고, 한 달에 얼마까지 쓰나"다. 조직 설정을 켜면 쓰기 권한이 있는 사람 누구나 저장소 검사를 시작할 수 있으므로, 예산 알림 받는 사람과 재검사 담당자를 먼저 정해 두면 미리보기 기간의 시행착오가 줄어든다.

<details markdown="1">
<summary>출처 10곳</summary>

- GitHub Changelog, 「AI Scan for pull requests generally available」(2026-10-15): [github.blog](https://github.blog/changelog/2026-10-15-ai-scan-for-pull-requests-generally-available)
- GitHub Changelog, 「AI Scan for repositories in public preview」(2026-10-28): [github.blog](https://github.blog/changelog/2026-10-28-ai-scan-for-repositories-in-public-preview)
- GitHub Changelog, 「Manage AI Scan for repositories using the REST API」(2026-11-13): [github.blog](https://github.blog/changelog/2026-11-13-manage-ai-scan-for-repositories-using-the-rest-api)
- GitHub Changelog, 「Bulk start AI Scan for repositories」(2026-11-16): [github.blog](https://github.blog/changelog/2026-11-16-bulk-start-ai-scan-for-repositories)
- GitHub Changelog, 「Code scanning AI Scan enablement status in security overview」(2026-10-06)·「Code scanning AI Scan metrics in security overview」(2026-10-13): [github.blog](https://github.blog/changelog/2026-10-06-code-scanning-ai-scan-enablement-status-in-security-overview), [github.blog](https://github.blog/changelog/2026-10-13-code-scanning-ai-scan-metrics-in-security-overview)
- GitHub Docs, 「AI Scan for a repository's backlog」: [docs.github.com](https://docs.github.com/en/code-security/concepts/code-scanning/ai-scan-for-repositories)
- GitHub Docs, 「Viewing and managing AI Scan alerts on your repository's default branch」: [docs.github.com](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/viewing-and-managing-ai-scan-alerts)
- GitHub Docs, 「AI Scan for pull requests」·「GitHub Advanced Security license billing」: [docs.github.com](https://docs.github.com/en/code-security/concepts/code-scanning/ai-powered-security-detections), [docs.github.com](https://docs.github.com/en/billing/concepts/product-billing/github-advanced-security)

</details>
