---
layout: post
title: "GitHub Copilot Fusion 쓰는 법, 모델 대신 Standard·High·Max 중 하나를 고른다"
date: 2026-10-30 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["깃허브코파일럿", "CopilotFusion", "AI코딩", "모델라우팅", "AI요금"]
permalink: /posts/2026-10-30-github-copilot-fusion-effort-levels/
description: "GitHub Copilot Fusion은 모델 하나를 고르는 대신 노력 수준을 고르면 Copilot이 작업마다 모델을 나눠 쓰는 기능이다. 켜는 곳, 요금제별 차이, 과금 방식과 주의점을 공식 문서 기준으로 정리했다."
image: /assets/img/posts/2026-10-30-github-copilot-fusion-effort-levels.png
mermaid: true
---

Copilot 채팅창 아래 모델 목록은 갈수록 길어졌다. 간단한 수정에도 가장 비싼 모델을 그대로 쓰고 있었다면, 같은 결과를 더 적은 크레딧으로 받을 수 있었던 셈이다. GitHub는 2026년 10월 28일 이 고민을 대신 맡는 Copilot Fusion을 정식 출시했다. 이 글을 읽으면 Fusion이 무엇을 대신 결정하는지, 내 요금제에서 어떤 단계를 고를 수 있는지, 언제 직접 모델을 고르는 편이 나은지 판단할 수 있다.

{: .summary }
> - 모델 목록에서 **Copilot Fusion**을 고르고 노력 수준(**Standard·High·Max**)만 정하면, Copilot이 요청마다 쓸 모델과 일하는 방식을 정한다.
> - Standard는 무료 요금제를 포함한 **모든 요금제**에서, High·Max는 **Pro+ 이상**과 Business·Enterprise에서 쓸 수 있다.
> - 별도 요금은 없고 실제로 쓴 모델마다 원래 단가로 과금된다. 유료 요금제는 **2026년 11월 30일까지 30% 할인**을 받는다.

## Fusion은 모델이 아니라 모델을 고르는 장치다

공식 문서는 Copilot Fusion을 "실행 중에 모델을 고르고 엮는 라우터이자 오케스트레이터"라고 설명한다. 모델 목록에서 Fusion을 고르는 것은 특정 모델을 고르는 일이 아니다. 요청이 들어올 때마다 Fusion이 어떤 모델을 몇 개 쓸지, 어떤 순서로 쓸지 정하고 마지막 답 하나만 보여 준다.

Fusion이 고르는 작업 방식은 세 가지다.

| 방식 | 하는 일 |
|---|---|
| Single | 모델 하나가 바로 처리한다 |
| Cascade | 가벼운 모델이 초안을 쓰고, 판정 단계에서 통과시키거나 더 강한 모델로 넘긴다 |
| Critique | 한 모델이 초안을 쓰고 여러 모델이 동시에 검토한 뒤 처음 모델이 고친다 |

방식은 프롬프트마다 다시 정해지기 때문에, 같은 대화 안에서도 질문마다 다른 방식이 쓰일 수 있다. 중간 초안은 사용자에게 보이지 않는다.

## 세 단계는 비용과 깊이의 손잡이다

사용자가 고르는 것은 노력 수준뿐이다. 문서 설명을 그대로 옮기면 Standard는 일상 작업용으로 비용·품질·속도의 균형을 잡고 보통 작업 하나에 모델 하나를 쓴다. High는 범위가 분명한 큰 코딩 작업용, Max는 가장 깊은 추론과 분석이 필요한 작업용이다.

GitHub는 독립 평가 기관 Artificial Analysis의 코딩 에이전트 지수에서 Fusion Max가 60점을 받아 Claude Code(Opus 5.5 Max 설정)와 2점 안쪽 차이였다고 밝혔다. 같은 발표에서 작업당 평균 API 비용은 약 절반, 토큰은 약 절반, 시간은 약 40% 적었다고 했다. 이 수치는 GitHub가 발표한 값이다.

{: .interpret }
Fusion이 아끼는 지점은 '쉬운 일에 비싼 모델을 쓰는 낭비'다. 그래서 효과는 하루 작업 중 단순 수정이나 질문이 얼마나 많은지에 따라 달라진다. 어려운 작업만 몰아서 맡기는 사람에게는 절감 폭이 작을 수 있다.

## 켜는 법과 요금제별 차이

Fusion은 Visual Studio Code, GitHub Copilot 앱, Copilot CLI, JetBrains IDE에서 정식 지원된다. 클라이언트를 최신 버전으로 올린 뒤 다음 순서로 켠다.

1. 클라이언트(VS Code·Copilot 앱·Copilot CLI·JetBrains)를 최신 버전으로 업데이트한다
2. 채팅창의 모델 선택 메뉴를 연다
3. Copilot Fusion을 고른다
4. 노력 수준을 Standard·High·Max 중에서 정한다
{: .steps }

| 노력 수준 | 쓸 수 있는 요금제 |
|---|---|
| Standard | Free, Student, Pro, Pro+, Max, Business, Enterprise |
| High·Max | Pro+, Max, Business, Enterprise |

조직에서 쓰는 경우 Fusion은 관리자가 정책으로 허용한 모델 안에서만 고른다. 관리자는 특정 모델을 다른 용도로는 남겨 둔 채 Fusion에서만 빼거나, Fusion을 조직의 기본 모델로 지정할 수 있다. 쓸 수 있는 모델이 하나도 없으면 Fusion은 모델 목록에 나타나지 않는다.

연구 미리보기 때 auto, HydraFusion, HydraFusion Max를 쓰던 사람은 따로 손댈 필요가 없다. 기존 선택이 대응하는 Fusion 노력 수준으로 자동으로 옮겨진다.

## 요금과 주의할 점

Fusion 자체에는 별도 요금이 없다. 대신 Fusion이 쓴 모델마다 원래 단가로 과금되고, High와 Max는 여러 모델을 함께 쓸 수 있어 Standard보다 AI 크레딧을 더 쓸 수 있다. 유료 요금제는 2026년 11월 30일까지 Fusion을 통해 쓴 모델 비용을 30% 할인받는다.

{: .warning }
Fusion이 버린 초안이 이미 파일을 고쳤다면 그 변경은 자동으로 되돌려지지 않는다. 커밋 전에 바뀐 파일을 직접 확인해야 한다.

그 밖에 문서가 밝힌 제약은 이렇다. Fusion은 서브에이전트를 띄우지 않고 별도로 움직인다. 화면에 보이는 컨텍스트 창 크기는 Fusion이 쓰는 모델 중 가장 작은 값을 기준으로 잡은 보수적인 숫자다. 쓰는 모델 묶음과 작업 방식은 앞으로 바뀔 수 있다.

로컬 모델 연결은 아직 실험 단계다. Standard에서 Windows에 설치한 MAI Code 1.1 Flash나, Ollama 같은 로컬 서버로 돌리는 Qwen3.8 Flash Next를 섞어 쓸 수 있다. 다만 어떤 모델을 쓸지 정하는 판단은 여전히 클라우드에서 이뤄지므로, 로컬 모델을 써도 오프라인 작업이 되지는 않는다.

언제 Fusion을 쓰고 언제 직접 모델을 고를지는 이렇게 나눠 볼 수 있다.

~~~mermaid
flowchart TD
  A[새 작업 시작] --> B{특정 모델이 꼭 필요?}
  B -- 예 --> C[그 모델 직접 선택]
  B -- 아니오 --> D{작업 크기는?}
  D -- 일상 수정 --> E[Fusion Standard]
  D -- 큰 기능 --> F[Fusion High]
  D -- 깊은 분석 --> G[Fusion Max]
~~~

## 마무리

Fusion으로 바뀌는 것은 '어떤 모델이 제일 좋은가'라는 질문이 '이 일에 얼마나 공을 들일까'로 옮겨 간다는 점이다. 할인이 끝나는 11월 30일 전까지 Standard를 기본으로 두고 크레딧 사용량을 지켜보면, 내 작업에서 직접 고르는 편이 나은지 맡기는 편이 나은지 숫자로 판단할 수 있다.

<details markdown="1">
<summary>출처 3곳</summary>

- GitHub Changelog, 「Route and orchestrate models with GitHub Copilot Fusion」, 2026-10-28: [github.blog](https://github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion)
- GitHub Docs, 「About GitHub Copilot Fusion」: [docs.github.com](https://docs.github.com/copilot/concepts/models/copilot-fusion)
- GitHub Changelog, 「GitHub Copilot Fusion now supports selection of local models」, 2026-10-28: [github.blog](https://github.blog/changelog/2026-10-28-github-copilot-fusion-now-supports-selection-of-local-models)

</details>
