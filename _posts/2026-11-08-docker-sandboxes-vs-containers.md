---
layout: post
title: "AI 코딩 에이전트 격리하는 법, 컨테이너 대신 Docker Sandboxes를 쓸 때와 아닐 때"
date: 2026-11-08 11:50:00 +0900
categories: ["DevOps"]
tags: ["도커", "DockerSandboxes", "AI코딩에이전트", "마이크로VM", "컨테이너보안"]
permalink: /posts/2026-11-08-docker-sandboxes-vs-containers/
description: "코딩 에이전트를 컨테이너에 넣으면 충분할까. 도커가 11월 5일 정리한 컨테이너와 Docker Sandboxes의 차이, 설치 조건, sbx로 시작하는 순서, 그래도 에이전트가 닿는 곳을 공식 문서로 정리했다."
image: /assets/img/posts/2026-11-08-docker-sandboxes-vs-containers.png
mermaid: true
---

코딩 에이전트에게 권한 확인을 끄고 몇 시간씩 일을 맡기려면, 먼저 "어디에 가둬 둘까"를 정해야 한다. 익숙한 답은 컨테이너지만, 도커는 11월 5일 공식 블로그에서 컨테이너와 자사 Docker Sandboxes가 아예 다른 기술이라고 선을 그었다. 이 글을 읽으면 내 에이전트 작업에 컨테이너로 충분한지, 마이크로VM 샌드박스가 필요한지 판단하고 첫 샌드박스를 띄우는 순서까지 알 수 있다.

{: .summary }
> - 컨테이너는 **호스트 커널을 함께 쓰는 프로세스**이고, Docker Sandboxes는 **자기 커널·파일시스템·네트워크·Docker Engine을 가진 마이크로VM**이다.
> - 에이전트가 **무인으로 돌거나, 이미지를 빌드하거나, 남이 쓴 입력을 읽으면** 도커는 샌드박스부터 쓰라고 권한다.
> - 시작은 `sbx run claude` 한 줄이다. sbx CLI와 로컬 샌드박스는 **상업용도 무료**, 모델 요금은 따로다.

## 컨테이너와 샌드박스는 경계가 놓인 자리가 다르다

컨테이너는 리눅스 네임스페이스로 자기만의 파일시스템·프로세스·네트워크 보기를 얻고, cgroups로 CPU·메모리를 나눠 받는 프로세스다. 같은 머신의 컨테이너는 모두 호스트 커널 하나를 함께 쓴다. 그래서 빨리 뜨고 촘촘하게 들어가지만, 경계가 곧 그 공유 커널이다.

Docker Sandboxes는 에이전트 하나마다 마이크로VM을 띄운다. 안에는 자기 리눅스 커널과 전용 Docker Engine이 있고, 에이전트는 그 안에서 sudo를 쓴다. 에이전트가 컨테이너를 탈출해도 떨어지는 곳은 버려도 되는 마이크로VM이고, 같은 머신의 다른 샌드박스에도 닿지 못한다고 도커는 설명한다.

도커가 짚은 대표 구멍은 `/var/run/docker.sock`이다. 컨테이너에 도커 권한을 주려고 이 소켓을 마운트하면 호스트 Docker 데몬을 통째로 넘기는 셈이 된다. 도커 블로그는 소켓이 마운트된 컨테이너 속 에이전트가 제로데이 없이 설정의 빈틈만으로 호스트의 비밀 파일에 닿은 시연을 소개했다. 샌드박스 안 에이전트는 VM 안의 전용 엔진을 쓰므로 호스트 소켓이 경계 밖에 남는다.

| 구분 | 컨테이너 속 에이전트 | Docker Sandboxes 속 에이전트 |
|---|---|---|
| 커널 | 호스트 커널 공유 | 마이크로VM 전용 커널 |
| 도커 사용 | 호스트 소켓이나 중첩 데몬 | VM 안 전용 Docker Engine |
| 네트워크 | 컨테이너 네트워크 + 운영자 설정 | 호스트 프록시, 기본 차단 |
| 자격 증명 | 환경 변수·파일·소켓 | 지원 HTTP 서비스는 호스트에서 주입 |
| 상태 | 이미지·볼륨에서 다시 빌드 | `sbx rm` 전까지 유지 |

## 컨테이너로 충분할 때, 샌드박스가 필요할 때

도커의 기준은 한 문장이다. 코드와 의존성을 내가 통제하면 컨테이너, 실행 중에 코드를 만들거나 받아 오면 샌드박스다. 서비스 배포, CI 작업, 짧게 돌고 사라지는 실행은 여전히 컨테이너가 맞는 도구라고 도커도 적었다.

도커가 꼽은 "샌드박스부터 시작할 신호"는 다섯 가지다. 하나라도 해당하면 샌드박스 쪽이다.

- 에이전트가 무인으로 돌거나 권한 확인을 자동 승인한다
- 에이전트가 이미지를 빌드하거나 Compose·Testcontainers를 돌린다
- 이슈, 웹 페이지, 패키지 메타데이터, MCP 출력처럼 내가 쓰지 않은 입력을 읽는다
- 에이전트 환경 안에 두고 싶지 않은 API 키가 필요하다
- 세션이 작업 하나보다 길게 이어진다

~~~mermaid
flowchart TD
  A[에이전트 작업] --> B{실행 중 코드 생성?}
  B -- 아니오 --> C[컨테이너]
  B -- 예 --> D{무인·빌드·외부입력?}
  D -- 아니오 --> C
  D -- 예 --> E[Docker Sandboxes]
~~~

## 첫 샌드박스 띄우는 순서

설치 조건은 하이퍼바이저다. 맥은 macOS 14 이상 애플 실리콘, 윈도우는 윈도우 11에서 Windows Hypervisor Platform을 켜야 하고, 리눅스는 우분투 24.04 이상에서 KVM이 켜져 있고 내 계정이 kvm 그룹에 있어야 한다. 가상 머신 안에서 돌리려면 중첩 가상화가 필요하다. 호스트에 Docker Desktop이나 Docker Engine이 없어도 된다.

1. sbx를 설치한다: 맥은 `brew install docker/tap/sbx`, 윈도우는 `winget install -h Docker.sbx`, 우분투는 도커 apt 저장소를 추가한 뒤 `sudo apt install docker-sbx`
2. `sbx login`으로 도커 계정에 로그인한다
3. 프로젝트 폴더에서 `sbx run --name my-sandbox claude`를 실행한다. 네트워크 정책을 처음 물으면 Balanced를 고른다
4. 다른 터미널에서 `sbx ls`로 샌드박스와 공유된 작업 폴더를 확인한다
5. 막힌 주소가 필요하면 `sbx policy allow network registry.npmjs.org`처럼 하나씩 연다
6. 쉬려면 `sbx stop`, 끝나면 `sbx rm`으로 지운다
{: .steps }

Claude Code를 Claude 구독(Max·Team·Enterprise)으로 쓰면 샌드박스 안에서 `/login`만 하면 되고, 세션 토큰은 호스트에 남는다고 문서는 적었다. 지원 에이전트는 Claude Code, Codex, Copilot, Cursor, Gemini, Kiro, OpenCode 등이다.

## 샌드박스 안에서도 에이전트가 닿는 곳

마이크로VM은 내가 공유한 것까지 숨겨 주지 않는다. 가장 큰 공유물은 작업 폴더다. 기본 모드에서는 현재 폴더가 읽기·쓰기로 마운트돼, 에이전트가 프로젝트 파일을 고치거나 지울 수 있다.

호스트 작업 트리를 지키려면 `sbx run --clone claude .`로 클론 모드를 쓴다. 에이전트는 VM 안의 별도 클론에서 일하고, 결과는 `git fetch sandbox-<이름>`으로 가져온다. 다만 원래 저장소는 샌드박스 안 `/run/sandbox/source`에서 읽기 전용으로 보인다. 로컬 stdio MCP 서버와 공유 스킬도 호스트 쪽에서 돌아가므로 에이전트의 손이 거기까지 닿는다.

{: .warning }
클론 모드도 원본 저장소 읽기는 막지 않는다. 저장소 안에 비밀 값이 들어 있다면 샌드박스가 그것을 가려 주지 않으며, 에이전트가 고친 코드는 실행하기 전에 diff부터 읽어야 한다고 도커도 적었다.

비용은 이렇게 나뉜다. sbx CLI와 로컬 샌드박스 컴퓨팅은 상업용을 포함해 무료다. 도커가 관리하는 클라우드 샌드박스는 사용량 과금 구독이고, 조직 단위 정책 관리는 별도 유료 구독이며, 모델 제공사 요금은 따로 든다. 팀 설정을 묶는 Kits는 얼리 액세스, 저장소에 넣는 `sbxenv.yaml`은 실험 기능이라 바뀔 수 있다.

{: .interpret }
도커의 정리는 "컨테이너가 약하다"가 아니라 "에이전트는 애플리케이션이 아니라 사람처럼 움직이는 행위자"라는 데 있다. 설정대로만 움직이는 앱에는 커널 경계로 충분했지만, 환경을 더듬어 빈틈을 찾는 것이 일인 에이전트에게는 그 에이전트가 고칠 수 없는 바깥 경계가 필요하다는 얘기다. 권한 확인을 끄는 순간 그 일을 대신할 경계가 어디 있는지가 운영의 질문이 된다.

## 마무리

도커가 글을 맺으며 단 소제목은 "에이전트는 샌드박스에, 애플리케이션은 컨테이너에"다. 둘 중 하나를 고르는 문제가 아니라, 권한 확인 창을 끄기 전에 그 자리를 무엇으로 채울지 정하는 문제에 가깝다.

<details markdown="1">
<summary>출처 5곳</summary>

- Docker Blog, Srini Sekaran·Oleg Selajev, 「Docker Sandboxes vs. Containers: Choosing the Right Isolation for AI Agents」(2026-11-05): [docker.com](https://www.docker.com/blog/docker-sandboxes-vs-containers/)
- Docker Docs, 「Docker Sandboxes」: [docs.docker.com](https://docs.docker.com/ai/sandboxes/)
- Docker Docs, 「Install Docker Sandboxes」: [docs.docker.com](https://docs.docker.com/ai/sandboxes/install/)
- Docker Docs, 「Get started with local Docker Sandboxes」: [docs.docker.com](https://docs.docker.com/ai/sandboxes/get-started/)
- Docker Docs, 「Use Git with sandboxes」·「Supported agents」: [docs.docker.com](https://docs.docker.com/ai/sandboxes/workflows/git/), [docs.docker.com](https://docs.docker.com/ai/sandboxes/agents/)

</details>
