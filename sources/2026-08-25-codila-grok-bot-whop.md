---
layout: default
title: "Grok Bot × Whop — 원문 번역"
permalink: /sources/2026-08-25-codila-grok-bot-whop/
nav_exclude: true
search_exclude: false
---

# Grok Bot Agents × Whop: 프롬프트 하나로 비즈니스를 자동화하는 24/7 AI 에이전트 팀 만들기

다들 GrokBot 이야기를 하지만, 정작 **그걸로 어떻게 돈을 만드느냐**는 잘 묻지 않는다.

진짜 기회는 또 하나의 챗봇(chatbot)으로 쓰는 데 있지 않다.

GrokBot을 **24/7 비즈니스 오퍼레이터(business operator)** 로 바꾸는 일이다.

당신이 결과(outcome)를 주면, GrokBot이 Whop을 통해 상품을 만들고, 가격을 설정하고, 체크아웃(checkout)을 생성하고, 앱을 배포하고, 성과(performance)를 모니터링한다.

모든 행동은 기록되고 → 되돌리기 어려운(irreversible) 결정은 승인(approval)이 필요하며 → 노트북을 닫아도 워크플로(workflow)는 계속 돌아간다.

> 그러니 에이전트에게 어디를 클릭할지 가르치지 마라. 비즈니스 목표(objective), 명령 계층(command layer), 증명 기준(proof standard)을 줘라.
>
> 알파(alpha) 전에 — 더 신선한 알파를 받으려면 내 서브스택을 구독하라 — https://substack.com/@0xcodila

---

## 1. 대시보드 열 개 대신 프롬프트 하나

이런 메시지를 보낸다고 상상해 보라.

```
Build a $49 product called Creator Ops Kit. Create its pricing and checkout link, deploy the companion app as a preview, draft a $50 ad campaign, and return a launch report with every ID, URL, cost, and action that still needs my approval.
```

(번역: Creator Ops Kit이라는 $49 상품을 만들어라. 가격과 체크아웃 링크를 만들고, 동반 앱을 프리뷰(preview)로 배포하고, $50 광고 캠페인 초안을 잡은 뒤, 모든 ID·URL·비용·아직 내 승인이 필요한 액션이 담긴 런치 리포트(launch report)를 돌려줘라.)

그 프롬프트에는 **결과(outcome)는 하나**지만 **잡(job)은 여러 개**가 들어 있다. Whop CLI는 상품(products), 플랜(plans), 체크아웃 설정(checkout configurations), 호스팅 앱(hosted apps), 통계(stats), 내보내기(exports), 광고(ads)를 다룰 수 있다. 모든 명령은 JSON을 반환할 수 있어, 에이전트에게 **기계가 읽을 수 있는 상태(machine-readable state)** 를 준다.

봇은 경로를 준비하고, 되돌릴 수 있는(reversible) 단계는 실행하며, 게시(publishing)·지출(spending)·환불(refunding)·자금 이동(moving money) 앞에서는 멈춘다.

---

## 2. 시스템이 돌아가는 방식

아키텍처(architecture)는 세 층이다.

1. **Grok Bot은 오퍼레이터(operator)** 다. 목표를 해석하고, 일을 이어 붙이며(sequences work), 예외를 다루고, 판단(judgment)이 필요할 때 묻는다.

2. **Whop CLI는 액션 레이어(action layer)** 다. 결정을 부서지기 쉬운 대시보드 클릭 대신 **명시적 명령(explicit commands)** 으로 바꾼다.

3. **JSON은 비즈니스 원장(business ledger)** 이다. 상품 ID, 플랜 ID, 체크아웃 URL, 캠페인 상태, 지출(spend), 에러를 대화(conversation) 밖에 저장한다.

이 분리가 중요하다. 대화는 맥락(context)을 잃을 수 있지만, 명령 결과는 다시 확인할 수 있다.

단계마다 `business-state.json`을 유지하라. 필드 다섯 개다. `status`, `resource_id`, `artifact`, `evidence`, `next_action`. 모든 명령은 이것을 **먼저** 읽어, 중복 상품이나 중복 캠페인을 막는다.

**대화는 일을 설명하고, 상태(state)가 일을 통제한다.**  
(Conversation explains the work. State controls the work.)

---

## 3. Grok Bot을 Whop에 연결하기

Grok Bot의 클라우드 컴퓨터(cloud computer)에 CLI를 설치한다.

```
curl -fsSL https://whop.com/install.sh | sh
whop --version
whop
```

마지막 명령이 브라우저 로그인(sign-in)을 열고 비즈니스를 고르게 한다. 비밀번호, 패스키(passkeys), 2단계 인증(two-factor authentication)은 **secure takeover** 로 처리하라. 자격증명(credentials)을 채팅에 붙여 넣지 마라.

그다음 봇에게 CLI 자체의 **기계 가독 맵(machine-readable map)** 을 준다.

```
whop --llms
whop skills add
whop --help
```

무인 작업(unattended work)에는 Whop이 `WHOP_API_KEY`를 지원한다. 보호된 시크릿(protected secret)으로 저장하고, 이 워크플로에 필요한 권한만 부여하라.

실제 결제에 손대기 전에는 Whop **sandbox** 로 상품·결제 테스트를 하라. 앱은 sandbox에서 지원되지 않으니, `--skip_promote`로 프리뷰 빌드(preview builds)를 배포하고, 프로모션(promotion) 전에 승인을 요구하라.

---

## 4. 상품 런칭하기

바뀔 수 있는 플래그(flags)를 하드코딩하지 마라. 봇이 먼저 **살아 있는 명령 스키마(live command schema)** 를 보게 하라.

```
whop products create --help
whop plans create --help
whop checkout-configurations create --help
```

한 스테이지(stage)씩 `--format json`으로 실행하고, 돌아온 ID마다 원장(ledger)에 적어라.

최소 런치 체인(launch chain)은 이렇다.

Product → Plan → Checkout Configuration → Preview App → Verification → Approval → Production  
(상품 → 플랜 → 체크아웃 설정 → 프리뷰 앱 → 검증 → 승인 → 프로덕션)

Whop 문서의 체크아웃 생성 예시는 다음과 같다.

```
whop checkout-configurations create --plan_id plan_xxx --format json
```

앱은 `whop apps deploy --skip_promote`가 프리뷰를 만든다. Grok Bot이 체크아웃을 테스트하고, 프리뷰를 점검하고, 증거(evidence)를 모은 뒤, 승인용 **런치 패킷(launch packet)** 하나를 돌려준다.

---

## 5. 매출 루프를 닫기

상품이 팔리기 시작하면, 운영 시스템(operating system)은 **측정 가능(measurable)** 해진다.

Whop은 광고 성과(ad performance)를 판매 데이터 옆에 둘 수 있고, 자격이 되는 머천트(merchants)는 기존 Whop 잔고(balance)로 캠페인에 자금을 댈 수 있다. 그러면 루프가 짧아진다.

Sale → Whop Balance → Ad Spend → New Sale → Updated Decision  
(판매 → Whop 잔고 → 광고비 → 새 판매 → 갱신된 결정)

중요한 것은 자동 지출(automatic spending)이 아니다. **자동 대사(automatic reconciliation)** 다.

> 매일 아침 Grok Bot이 매출(revenue), 지출(spend), 전환(conversion), 환불(refunds), 예산(budget)을 비교한 뒤 hold / increase / decrease / pause를 권고한다. 변경은 승인 뒤에 남는다.

Whop Ads는 현재 베타(beta)이며 접근이 제한적이다. 그래서 광고 스테이지는 먼저 선택 계정이 쓸 수 있는지 확인해야 한다. 안 되면 다른 계정으로 즉흥 대응(improvising)하지 말고 `BLOCKED: ADS_ACCESS`를 반환하라.

---

## 6. 비즈니스를 24/7로 돌리기

수동으로 **세 번** 성공한 뒤, 그 워크플로를 **Skill** 로 저장하라. Skill에는 입력(inputs), 명령(commands), 기대 산출물(expected artifacts), 검증 규칙(validation rules), 실패 처리(failure handling), 승인 경계(approval boundaries)를 정의한다.

그다음 **Routine** 으로 만든다.

```
Every weekday at 8:00 AM, read the current business state, pull revenue, members, churn, payments, disputes, and ad performance, compare the last seven days with the previous seven, and post a linked exception report. Do not change budgets, issue refunds, send messages, or move money.
```

(번역: 평일 아침 8시에 현재 비즈니스 상태를 읽고, 매출·멤버·이탈(churn)·결제·분쟁(disputes)·광고 성과를 가져와 최근 7일과 직전 7일을 비교한 뒤, 링크가 달린 예외 리포트(exception report)를 올려라. 예산 변경, 환불, 메시지 발송, 자금 이동은 하지 마라.)

Grok Bot Routine은 노트북이 꺼져 있어도 돌아갈 수 있다. 봇은 메트릭에 `whop stats time_series --format json`을, 구조화된 대시보드 데이터에는 exports를 쓸 수 있다.

리포트는 임계값(threshold)이 깨지거나, 데이터가 오래되었거나(stale), 승인이 필요할 때만 시끄러워진다.

---

## 7. 승인과 안전

24/7 오퍼레이터에게 필요한 것은 무한 권한이 아니라 **좁은 권한(narrow authority)** 이다.

다섯 가지 하드 룰(hard rules)을 써라.

- 일일·평생 광고비 상한(daily and lifetime ad-spend ceiling)을 둬라.
- 에스컬레이션(escalation) 전 재시도(retries)는 두 번을 넘기지 마라.
- 쓰기 명령(write command)을 재시도하기 전에 현재 상태를 확인해라.
- 모든 액션에 대해 명령, 대상(target), 결과, 증거(evidence)를 로그로 남겨라.
- 광고, 지급(payouts), 환불, 게시, 삭제, 프로덕션 승격(production promotion), 권한 변경, 법률 서류(legal filings)에는 승인을 요구하라.

공식 Grok Bot 보안 가이드는 구매, 자금 이체(financial transfers), 삭제, 게시, 프로덕션 변경에 대해 **최소 권한(least privilege)** 과 **명시적 승인(explicit approval)** 을 권한다.

자동화는 일상 업무(routine work)를 줄여야지, 책임(accountability)을 지우면 안 된다.

---

## 8. 복붙용 운영 프롬프트 (Copy-Paste Operating Prompt)

```
You are the operator of my Whop business. Use the Whop CLI as the source of action and JSON output as the source of state. First run whop --llms and inspect --help for every command you plan to use. Never invent a flag.
Objective: [DESCRIBE THE BUSINESS OUTCOME].
Account: [BUSINESS NAME OR BIZ_ID].
Budget: [LIMIT].
Deadline: [DATE AND TIME ZONE].
You may read data, create drafts, create products and plans, generate checkout configurations, and deploy preview builds. Require my approval before spending money, activating ads, promoting an app to production, publishing, issuing refunds, moving funds, deleting data, changing permissions, accepting legal terms, or making legal filings.
Maintain business-state.json with the status, resource ID, artifact, evidence, and next action for every stage. Before any write, check whether the resource already exists. Use JSON output whenever available. Stop after two failed attempts.
Return one report containing: completed actions, created IDs and links, verification evidence, current metrics, blocked steps, proposed next actions, and approvals required. Never mark a stage complete without independent evidence.
```

(요지 번역: 너는 내 Whop 비즈니스의 오퍼레이터다. 액션의 소스는 Whop CLI, 상태의 소스는 JSON 출력이다. 쓰려는 명령마다 먼저 `whop --llms`와 `--help`를 보고, 플래그를 지어내지 마라. 목표·계정·예산·마감을 채운다. 읽기·초안·상품·플랜·체크아웃·프리뷰 배포는 허용한다. 지출·광고 활성화·프로덕션 승격·게시·환불·자금 이동·삭제·권한 변경·약관 수락·법률 서류는 내 승인이 필요하다. 단계마다 `business-state.json`을 유지하고, 쓰기 전 존재 여부를 확인하며, 가능하면 JSON을 쓰고, 실패 두 번이면 멈춰라. 보고에는 완료 액션, 생성 ID·링크, 검증 증거, 현재 지표, 막힌 단계, 다음 제안, 필요 승인을 담아라. 독립 evidence 없이 단계를 완료 처리하지 마라.)

Grok Bot과 Whop을 짝짓는 진짜 이점은 여기 있다. 대시보드를 더 긴 채팅으로 바꾸는 게 아니다. **흩어진 클릭을 검증 가능한 운영 시스템(verifiable operating system)** 으로 바꾸는 일이다.

목표(objective) 하나가 들어가고, 상품·결제·성장·리포팅이 **하나의 통제된 루프(controlled loop)** 를 통과한다.

---

## 9. 결론

당신은 더 이상 대시보드에서 대시보드로 일을 나르는 사람이 아니게 된다.

지금까지 AI는 *무엇을 할지* 말해 줄 수 있었지만, 상품 설정, 결제, 배포, 광고, 리포팅은 여전히 손으로 밀어야 했다.

> Whop에 연결된 Grok Bot이 그걸 바꾼다.

봇이 워크플로를 조율(coordinate)한다. Whop이 비즈니스 액션을 실행한다. 구조화된 상태(structured state)가 모든 결과를 기록한다. 예산, 승인, 예외에 대한 책임은 당신에게 남는다.

지렛대(leverage)는 더 빠른 클릭이 아니다. 상품이 런칭되고, 판매가 데이터를 만들고, 데이터가 성장을 알려 주며, 완료된 모든 액션이 증거와 함께 돌아오는 **하나의 통제된 루프**다.

> 기술(skill)은 더 이상 “다음에 어떤 대시보드를 열까?”가 아니다.

> “무엇을 위임할까, 완료를 무엇으로 증명할까, 시스템이 어디서 나를 위해 멈춰야 할까?”가 된다.

그건 프롬프팅 질문이 아니다.

당신 비즈니스의 **새로운 운영 모델(operating model)** 이다.

@0xCodila
