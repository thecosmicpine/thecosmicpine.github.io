---
layout: post
title: "CloudWatch 로그 보존 기간 한 번에 정하는 법, 계정 단위 보존 정책과 dry run 먼저 쓰기"
date: 2026-11-12 11:50:00 +0900
categories: ["DevOps"]
tags: ["CloudWatch", "AWS", "로그보존", "클라우드비용", "관측성"]
permalink: /posts/2026-11-12-cloudwatch-logs-account-retention-policy/
description: "CloudWatch Logs 계정 단위 보존 정책으로 로그 그룹 보존 기간을 한 번에 맞추는 법. 30일 최소값, 가장 긴 정책 우선, 24시간 뒤 적용, dry run으로 줄어드는 그룹 먼저 확인하는 순서까지."
image: /assets/img/posts/2026-11-12-cloudwatch-logs-account-retention-policy.png
mermaid: true
---

AWS 계정의 CloudWatch Logs 목록을 열면 보존 기간이 "Never expire"인 로그 그룹이 줄줄이 나오곤 한다. 로그 그룹을 만들 때 기간을 정하지 않으면 기본값이 '무기한 보관'이라서다. AWS는 11월 9일 계정 전체나 이름 앞부분이 같은 로그 그룹에 보존 기간을 한 번에 거는 '계정 단위 보존 정책'을 내놨다. 이 글을 읽으면 정책 하나로 기본 보존 기간을 정하고, 감사용 로그는 더 길게 남기며, 적용 전에 어떤 로그가 지워질지 미리 확인할 수 있다.

{: .summary }
> - 정책 하나로 계정 전체 또는 **이름 접두어**(예: `/aws/lambda`)가 같은 로그 그룹의 보존 기간을 정한다. 리전마다 **최대 20개**, 추가 요금 없음.
> - 정책끼리 겹치면 **가장 긴 기간**이 이긴다. 대신 정책은 로그 그룹 자체 설정을 **덮어쓴다**. 10년짜리 그룹도 90일 정책에 걸리면 90일이 된다.
> - 만들기 전에 `--dry-run`으로 **보존 기간이 줄어드는 그룹 수**부터 본다. 정책은 만든 뒤 **24시간** 지나야 적용된다.

## 무엇이 바뀌었나: 로그 그룹마다 하던 일을 정책 하나로

지금까지 보존 기간은 로그 그룹마다 따로 정했다. 콘솔에서 그룹의 Retention 칸을 눌러 바꾸거나, 그룹을 만드는 코드에 기간을 넣어야 했다. 서비스와 함수가 늘수록 로그 그룹도 늘어나니, 누군가 챙기지 않으면 무기한 보관 그룹이 계속 쌓인다.

계정 단위 보존 정책은 이 일을 계정 쪽으로 옮긴다. 정책에는 두 값이 들어간다. 하나는 보존 일수(30·60·90·120·150·180·365·400·545·731·1096·1827·2192·2557·2922·3288·3653일 또는 `NEVER_EXPIRE`), 다른 하나는 적용 방식이다. `RETROACTIVE`는 이미 있는 로그 그룹까지, `NEW_ONLY`는 정책을 만든 뒤 새로 생기는 그룹에만 건다.

<div class="stat-row">
  <div class="stat"><b>20개</b><span>계정·리전당 만들 수 있는 보존 정책 수</span></div>
  <div class="stat"><b>30일</b><span>계정 단위 정책의 최소 보존 기간</span></div>
  <div class="stat"><b>24시간</b><span>정책을 만들거나 바꾼 뒤 적용까지</span></div>
</div>

범위는 접두어로만 고른다. 접두어를 비우면 계정 전체, `/aws/lambda`를 넣으면 이름이 그렇게 시작하는 그룹만이다. 정책은 리전 단위라서, 여러 리전을 쓰면 리전마다 따로 만들어야 한다. 바레인·UAE 두 중동 리전을 뺀 모든 상용 리전에서 쓸 수 있다.

## 겹치면 긴 쪽이 이긴다, 그런데 그룹 설정은 진다

정책끼리는 겹쳐도 된다. 한 로그 그룹에 정책이 여러 개 걸리면 가장 긴 기간이 쓰이고, `NEVER_EXPIRE`는 가장 긴 것으로 친다. 그래서 "계정 전체 90일, `/security`로 시작하는 그룹은 1년" 같은 구성이 된다. AWS 발표문이 든 예시도 이 조합이다.

정책과 로그 그룹 자체 설정 사이는 다르다. 문서는 계정 단위 정책이 로그 그룹의 보존 설정을 "덮어쓴다"고 적는다. 그룹에 10년을 걸어 뒀어도 90일 정책 범위에 들어가면 90일보다 오래된 로그는 지워진다.

{: .warning }
반대 방향도 있다. 계정 단위 정책은 30일보다 짧게 정할 수 없다. 비용을 줄이려고 7일이나 14일로 걸어 둔 그룹이 30일 계정 정책 범위에 들어가면 보존 기간이 30일로 늘어난다. dry run 결과의 '늘어나는 그룹 수'도 함께 봐야 하는 이유다.

## 정책 거는 순서: dry run → 생성 → 24시간 뒤 확인

공식 문서에 나온 AWS CLI 명령으로 순서를 정리하면 아래와 같다. 권한은 만들기·고치기에 `logs:PutAccountPolicy`와 `logs:PutRetentionPolicy`, 보기에 `logs:DescribeAccountPolicies`가 필요하다. dry run도 같은 권한이 필요하다.

1. 정책 문서를 정한다. 기간(`retentionInDays`)과 적용 방식(`enforcementMode`)을 고르고, 범위를 접두어로 좁힐지 정한다.
2. 같은 명령에 `--dry-run`을 붙여 미리 본다. 정책은 저장되지 않고 결과만 돌아온다.
3. 결과에서 줄어드는 그룹 수(`decreasedRetentionLogGroupCount`)와 저장량이 큰 상위 20개 그룹(`topLogGroupsImpacted`)을 확인한다.
4. 문제가 없으면 `--dry-run`을 빼고 다시 실행해 정책을 만든다.
5. 24시간 뒤 로그 그룹 정보를 조회해 `retentionPolicyName`에 정책 이름이 찍혔는지 본다.
{: .steps }

문서의 예시 명령은 이렇다. 람다 로그 그룹 전체를 90일로, 이미 있는 그룹까지 맞춘다.

~~~bash
aws logs put-account-policy \
  --policy-name LambdaRetentionPolicy \
  --policy-type RETENTION_POLICY \
  --policy-document '{ "retentionInDays": 90, "enforcementMode": "RETROACTIVE"}' \
  --selection-criteria 'LogGroupNamePrefix="/aws/lambda"' \
  --dry-run
~~~

만든 정책은 `aws logs describe-account-policies --policy-type RETENTION_POLICY`로 보고, 지울 때는 `aws logs delete-account-policy --policy-name LambdaRetentionPolicy --policy-type RETENTION_POLICY`를 쓴다. 지우기에도 `--dry-run`을 붙일 수 있다. 한 계정에서 dry run은 한 번에 하나만 돌릴 수 있다.

## 언제 RETROACTIVE, 언제 NEW_ONLY인가

판단은 "지금 쌓인 로그를 정리해도 되나"에서 갈린다. 아래 흐름도는 문서에 나온 동작을 기준으로 고르는 순서를 정리한 것이다.

~~~mermaid
flowchart TD
  A[보존 정책 만들기] --> B{기존 그룹도 맞출까?}
  B -- 아니오 --> C[NEW_ONLY]
  B -- 예 --> D[dry run 실행]
  D --> E{줄어드는 그룹 있음?}
  E -- 없음 --> F[기존까지 적용]
  E -- 있음 --> G[긴 정책 먼저 추가]
  G --> D
~~~

줄어드는 그룹 중 감사·보안 로그가 있으면, 그 접두어에 더 긴 정책(예: 365일이나 `NEVER_EXPIRE`)을 먼저 만들고 dry run을 다시 돌린다. 겹치면 긴 쪽이 이기므로, 긴 정책이 먼저 있으면 계정 기본 정책이 그 그룹을 줄이지 못한다.

| 상황 | 고를 것 | 이유 |
|---|---|---|
| 새로 생길 그룹만 관리 | `NEW_ONLY` | 기존 로그는 그대로 둔다 |
| 무기한 그룹 정리 | `RETROACTIVE` | 기존 그룹까지 기간이 걸린다 |
| 감사 로그는 길게 | 접두어 정책 추가 | 겹치면 긴 기간이 이긴다 |

{: .interpret }
보존 기간을 줄여도 비용이 바로 줄지는 않는다. 문서에 따르면 기간이 지난 로그는 보통 72시간 안에 실제로 지워지지만, 삭제 표시가 된 시점부터 보관 요금에서 빠진다. 여기에 정책 적용까지 걸리는 24시간을 더하면, 바꾼 뒤 이틀에서 나흘쯤 지나 저장량(`storedBytes`)을 확인하는 편이 정확하다.

## 마무리

계정 단위 보존 정책은 "새 로그 그룹이 생길 때마다 누가 기간을 챙기나"라는 질문을 계정 설정 하나로 바꾼다. 다만 정책이 그룹 설정을 이긴다는 점 때문에, 정책을 거는 순간 오래 남겨야 할 로그가 지워질 수도, 짧게 두던 로그가 길어질 수도 있다. 기본 정책보다 긴 정책을 먼저 만들고, dry run 숫자가 예상과 맞을 때 기본 정책을 거는 순서가 가장 안전하다.

<details markdown="1">
<summary>출처 5곳</summary>

- AWS, 「Amazon CloudWatch Logs announces account-level retention policies」(2026-11-09): [aws.amazon.com](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-cloudwatch-log-retention/)
- AWS 문서, 「Working with log groups and log streams」 중 Account-level retention policies·Change log data retention: [docs.aws.amazon.com](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#account-level-retention-policies)
- AWS API 문서, 「PutAccountPolicy」: [docs.aws.amazon.com](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutAccountPolicy.html)
- AWS API 문서, 「DryRunResult」: [docs.aws.amazon.com](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DryRunResult.html)
- AWS API 문서, 「LogGroup」(retentionInDays·retentionPolicyName): [docs.aws.amazon.com](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_LogGroup.html)

</details>
