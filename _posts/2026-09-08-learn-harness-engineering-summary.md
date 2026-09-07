---
layout: post
title: "Learn Harness Engineering 무료 코스 (요약본)"
date: 2026-09-08 00:00:00 +0900
categories: ["Notes"]
permalink: /posts/2026-09-08-learn-harness-engineering-summary/
---

santi(`@santtiagom_`)가 [로드맵을 실습으로 옮기려면 이 레포를 보라](https://x.com/santtiagom_/status/2092751908922446181)고 추천한 **Harness Engineering** 무료 코스를 Notes용 라이브러리로 요약해 둔다. 따라 하기 절차서가 아니라, **무엇이 있는지·어디를 보면 되는지** 한눈에 두는 메모다.

- 포스트: [https://x.com/santtiagom_/status/2092751908922446181](https://x.com/santtiagom_/status/2092751908922446181)
- 레포: [walkinglabs/learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering)
- 문서 사이트: [walkinglabs.github.io/learn-harness-engineering](https://walkinglabs.github.io/learn-harness-engineering/)
- 작성 추천: santi (`@santtiagom_`) · 코스: Walking Labs
- 수집: 2026-09-08

## 한 줄 요약

AI 코딩 에이전트가 **안정적으로** 일하게 만드는 환경·상태·검증·제어(하니스)를, 강의 14 + 실습 프로젝트 8로 배우는 **무료·프로젝트 기반** 코스다. 한국어 포함 다국어 README/문서가 있다.

트윗이 짚은 키워드: 에이전트용 레포 구조, 세션 간 상태 유지, 스코프 통제, 결과 검증.

## 코스가 말하는 것

- 벤치마크에 강한 모델도 실제 엔지니어링 작업에서는 깨진다 → **능력 공백**을 하니스로 메운다.
- 하니스는 대충 “프롬프트 더 쓰기”가 아니라, 대략 **지시(instructions) · 상태(state) · 검증(verification) · 범위(scope) · 수명주기(lifecycle)** 같은 서브시스템으로 본다. (코스 L02 프레임)
- 레포가 **단일 기록 시스템(system of record)** 이 되어야 한다. 에이전트가 못 보면 없는 것과 같다.
- 긴 작업은 디스크에 진행을 남기고, 초기화·완료 정의·기능 목록·E2E 검증·관측·세션 정리를 하니스로 묶는다.
- 이후 확장: **루프 엔지니어링**(프롬프트를 그만 붙잡고 자동 루프) → **그래프 엔지니어링**(단일 루프가 전문화·병렬·공유 상태·복구를 필요로 하면 그래프).

## 구성 (수집 시점)

| 구분 | 내용 |
|---|---|
| 강의 | L01–L14 (왜 실패하는가 → 하니스란 → 레포 SoR → 지시 파일 → 연속성 → init → 스코프 → 기능 목록 → 조기 승리 → E2E → 관측 → 클린 상태 → 루프 → 그래프) |
| 프로젝트 | P01–P08 (최소 하니스 비교 → 읽기 쉬운 워크스페이스 → 멀티세션 → 증분/스코프 → 검증 → 캡스톤 관측 → 첫 루프 → 첫 그래프) |
| 캡스톤 축 | Electron 기반 개인 지식 베이스 앱 — 프로젝트가 같은 제품 위에서 단계적으로 진화 |
| 빠른 시작 | `skills/harness-creator/` 로 AGENTS.md · 기능 목록 · init.sh · 검증 워크플로 스캐폴딩 |
| 참고 원문 | OpenAI harness engineering, Anthropic long-running harness 글, Awesome Harness Engineering |

## 라이브러리로 쓰는 법

이 글은 강의를 대신 요약·강의하지 않는다. **북마크용 입구**다.

- 이론만 → 문서 사이트 강의 목록
- 손대보기 → P01(프롬프트만 vs 최소 하니스)부터
- 자기 레포에 바로 → `harness-creator` 스킬
- 루프/그래프까지 → L13–L14 · P07–P08

*레포·강의 구성은 수집 시점(2026-09-08) 기준. 트윗은 스페인어 추천 한 줄 + 레포 링크. 요약·라이브러리 정리. AI 보조 작성.*
