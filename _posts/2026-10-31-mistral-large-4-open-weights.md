---
layout: post
title: "Mistral Large 4 공개 가중치, 직접 돌릴까 API로 쓸까: 1조 파라미터 모델 고르는 법"
date: 2026-10-31 11:50:00 +0900
categories: ["AI와 기술"]
tags: ["미스트랄", "MistralLarge4", "오픈웨이트", "온프레미스AI", "AI라이선스"]
permalink: /posts/2026-10-31-mistral-large-4-open-weights/
description: "미스트랄이 1조 파라미터 모델 Mistral Large 4의 가중치를 풀었다. 내려받아 직접 돌릴 때 필요한 GPU와 용량, 라이선스 조건, API 요금을 비교해 우리 팀에 맞는 쓰는 방식을 고를 수 있다."
image: /assets/img/posts/2026-10-31-mistral-large-4-open-weights.png
mermaid: true
---

미스트랄이 10월 29일(미국 시간) 자사 최대 모델 Mistral Large 4(별명 Le Chonk)의 가중치를 허깅페이스에 올렸다. 가중치가 공개됐다는 말은 회사 서버에 내려받아 인터넷과 끊어 놓고도 돌릴 수 있다는 뜻이다. 그런데 파라미터가 약 1조 개인 모델을 정말 우리 서버에서 돌릴 수 있을까, 돌려도 되는 걸까. 이 글을 읽으면 직접 배포, 클라우드·API 사용, 상업 라이선스 문의 가운데 우리 상황에 맞는 길을 고를 수 있다.

{: .summary }
> - 전체 **약 1조** 파라미터 중 토큰마다 **49B(임베딩 포함 52B)**만 쓰는 MoE 모델이고, 컨텍스트는 **1M 토큰**이다.
> - 기본 FP8 가중치는 **약 1.06TB**라서 vLLM 검증 구성은 **Blackwell GPU 4~8장, H200이면 16장**이다.
> - 사내에서 쓰는 건 자유지만, 남에게 **API로 모델을 빌려주는 사업**이면 미스트랄과 **별도 상업 계약**이 필요하다.

## 무엇이 공개됐나: 1조 개 중 49B만 움직이는 모델

Mistral Large 4는 전문가 혼합(MoE) 구조다. 전문가 128개 가운데 토큰마다 4개와 공유 전문가 1개만 계산에 참여한다. 그래서 전체 파라미터는 약 1조 개지만 한 토큰에 실제로 쓰는 양은 49B, 임베딩·출력층까지 치면 52B다. 미스트랄은 이 모델을 유럽에 있는 자사 데이터센터의 NVIDIA Grace Blackwell GPU 3,800장으로 처음부터 학습했다고 밝혔다.

| 항목 | 내용 |
|---|---|
| 입력·출력 | 텍스트와 이미지 입력, 텍스트 출력 |
| 컨텍스트 | 1M 토큰(vLLM 레시피 검증은 256k까지) |
| 추론 모드 | low·medium·high 세 단계, 기본값 high |
| 에이전트 기능 | 함수 호출, JSON 출력, 엄격한 JSON 스키마 |
| 언어 | 160개 이상(EU 공식 언어 전부 포함) |

이 모델은 10월 6일 공개 미리보기로 먼저 나왔다. 이번 공개는 그 뒤 3주 동안 강화학습을 더 한 개선판의 가중치다.

## 직접 돌리려면 무엇이 필요한가

내려받을 파일부터 크다. 허깅페이스 저장소 파일을 합치면 약 1,061GB다. vLLM 레시피 기준으로 FP8 판은 8장에 나눠 담을 때 GPU 한 장마다 가중치만 약 128GiB가 필요하고, Blackwell용 NVFP4 판(약 610GB)은 약 76GiB가 필요하다.

<div class="stat-row">
  <div class="stat"><b>약 1.06TB</b><span>기본 FP8 가중치 크기</span></div>
  <div class="stat"><b>약 610GB</b><span>Blackwell용 NVFP4 가중치</span></div>
  <div class="stat"><b>최대 1.9배</b><span>DSpark 켰을 때 처리량(회사 측정)</span></div>
</div>

vLLM이 검증했다고 밝힌 하드웨어는 NVIDIA GB300(NVFP4면 4-GPU 트레이 하나), B300 8장, B200 8장(NVFP4), H200 8장 두 묶음(FP8, 총 16장), AMD Instinct MI350X 8장이다. 서빙은 미스트랄이 권하는 vLLM 전용 도커 이미지(`vllm/vllm-openai:mistral-large-4`)로 한다. vLLM 레시피는 아직 정식 vLLM 릴리스나 나이틀리 휠에는 이 모델 지원이 들어 있지 않다고 적었다.

1. `docker pull vllm/vllm-openai:mistral-large-4`로 전용 이미지를 받는다
2. `--tensor-parallel-size 8`로 GPU 8장에 모델을 나눠 띄운다
3. 도구 호출을 쓰려면 `--tool-call-parser mistral`, `--reasoning-parser mistral`을 붙인다
4. 메모리가 모자라면 `--max-model-len`이나 동시 요청 수(`--max-num-seqs`)를 줄인다
{: .steps }

체크포인트에는 DSpark라는 추측 디코딩용 초안 헤드가 함께 들어 있다. 서빙 명령에 `--speculative-config`를 더하면 출력은 그대로 두고 처리량을 최대 1.9배까지 올렸다고 미스트랄은 밝혔다. 모델 카드에는 "자체 서빙 성능이 기대에 못 미치면 Mistral API를 권한다"는 문장도 있다.

## 라이선스: 사내 사용은 자유, 모델을 빌려주는 사업은 따로 계약

라이선스 이름은 Mistral Ecosystem Open-Weight License다. 허깅페이스 화면에는 'License: other'로 표시된다. MIT 라이선스를 고친 형태로, 상업·비상업 사용과 수정·재배포·추가 학습을 모두 허락한다.

조건은 하나가 붙는다. 사용자나 그 계열사가 '모델 서비스(Model as a Service)' 사업을 하면 상업 목적으로 쓰기 전에 미스트랄과 별도 상업 라이선스를 맺어야 한다. 라이선스는 이를 API나 호스팅 엔드포인트처럼 제3자가 입력·파라미터·학습 데이터를 실질적으로 다룰 수 있게 모델을 내주는 것으로 정의한다.

{: .warning }
제품의 특정 기능 안에만 모델을 넣은 경우, 다른 곳에 호스팅된 모델로 요청을 넘기기만 하는 경우, 제3자에게 모델을 내주지 않는 사내 사용은 이 조건에서 빠진다. 반대로 고객이 프롬프트와 파라미터를 직접 넣는 추론 API를 팔 계획이라면 배포 전에 계약부터 확인해야 한다.

## API로 쓰면 얼마인가, 성능 숫자는 어디까지 믿을까

직접 돌리지 않는다면 Mistral API에서 `mistral-large-4`로 부를 수 있다. 공식 문서 요금은 입력 100만 토큰당 0.7달러, 캐시된 입력 0.07달러, 출력 2.1달러다. 미스트랄은 Mistral Studio, OpenRouter, Microsoft Foundry, NVIDIA 호스팅 엔드포인트에서도 쓸 수 있다고 밝혔다.

성능은 모두 회사 발표 숫자다. 미스트랄에 따르면 Artificial Analysis 코딩 에이전트 지수에서 48%로 공개 가중치 1위권인 GLM-5.3과 비슷하면서 작업당 토큰은 평균 47% 적게 썼다. Terminal-Bench 4.0은 41%, Artificial Analysis 사이버 지수는 51%이고, 악성 사이버 요청 거절률은 평균 96.6%라고 했다.

{: .interpret }
토큰을 47% 덜 쓴다는 주장이 맞다면, 출력 토큰 요금이 비용 대부분을 차지하는 코딩 에이전트에서 체감 차이가 클 수 있다. 다만 자체 배포는 GPU 4~16장을 상시로 묶어 두는 일이라, 사용량이 적은 팀은 API로 품질과 토큰 사용량을 먼저 재 보는 편이 순서상 맞아 보인다.

## 우리 팀은 어느 쪽인가

~~~mermaid
flowchart TD
  A[ML4를 써 보고 싶다] --> B{남에게 API로 제공?}
  B -- 예 --> C[상업 라이선스 문의]
  B -- 아니오 --> D{데이터 반출 불가?}
  D -- 아니오 --> E[API로 시작]
  D -- 예 --> F{B200급 8장 있나?}
  F -- 있다 --> G[vLLM 자체 배포]
  F -- 없다 --> H[장비부터 확보]
~~~

{: .note }
미스트랄은 기술 보고서를 곧 낼 예정이라고 밝혔다. 벤치마크의 세부 조건은 그 보고서가 나온 뒤 다시 확인하는 것이 좋다.

이번 공개로 '보안 담당자가 회사 밖으로 코드를 내보내지 않고 쓸 수 있는 최상위급 모델'이라는 선택지가 생겼다. 다만 그 선택지를 실제로 잡으려면 1TB짜리 파일을 담을 GPU와 라이선스 조항 한 줄을 먼저 확인해야 한다. 결정은 모델 성능이 아니라 우리 데이터가 어디까지 나갈 수 있는지에서 시작하면 된다.

<details markdown="1">
<summary>출처 5곳</summary>

- Mistral AI, 「Mistral Large 4 (Le Chonk) is now open weight」: [mistral.ai](https://mistral.ai/news/mistral-large-4-oss/)
- Hugging Face, 「mistralai/Mistral-Large-4-1T-A52B」 모델 카드와 LICENSE: [huggingface.co](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B)
- Mistral Docs, 「Mistral Large 4」 모델·요금 페이지: [docs.mistral.ai](https://docs.mistral.ai/models/mistral-large-4-0)
- vLLM Recipes, 「mistralai/Mistral-Large-4-1T-A52B」: [recipes.vllm.ai](https://recipes.vllm.ai/mistralai/Mistral-Large-4-1T-A52B)
- TechCrunch, 「Mistral releases weights for its trillion-parameter AI model targeting cybersecurity」(2026-10-29): [techcrunch.com](https://techcrunch.com/2026/10/29/mistral-releases-weights-for-its-trillion-parameter-ai-model-targeting-cybersecurity/)

</details>
