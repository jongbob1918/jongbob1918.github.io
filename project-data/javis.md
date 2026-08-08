---
slug: javis
shortName: JAVIS
group: key
order: 1
title: JAVIS — 도서관 관리 로봇
description: 자율주행, 로봇팔과 비전 AI를 통합한 ROS 2 기반 도서관 관리 로봇
team: 9명
period: 2024.09–11
skills:
  - ROS 2
  - Nav2
  - Smac Planner
  - MPPI
  - System Integration
repository: https://github.com/jongbob1918/JAVIS
card:
  image: assets/images/project_javis.png
  imageAlt: JAVIS library service robot
  titleEn: JAVIS — Library Management Robot
  keywords:
    - ROS 2
    - Nav2
    - Smac Planner
    - MPPI
    - System Integration
  descriptionKo: 자율주행, 로봇팔과 비전 AI를 ROS 2로 통합해 도서 픽업·반납과 사용자 안내를 수행하는 도서관 관리 로봇을 개발했습니다.
  descriptionEn: Built a ROS 2 library management robot that integrates autonomous navigation, manipulation, and vision AI to pick up and return books and guide visitors.
overview: >-
  도서관에서는 도서 픽업·반납과 길 안내 같은 반복 업무에 지속적인 인력이 필요합니다.
  이를 자동화하기 위해 자율주행, 로봇팔과 비전 AI를 ROS 2로 연결한 도서관 관리 로봇 JAVIS를 개발했습니다.
  사용자가 도서 픽업을 요청하면 중앙 시스템이 작업을 할당하고, JAVIS가 책장으로 이동해 도서를 인식한 뒤 로봇팔로 픽업합니다.
demo:
  type: image
  src: ../assets/images/project_javis.png
  alt: JAVIS 도서관 서비스 로봇
---

## 사용자 요청에서 로봇 동작까지

서버 요청을 Task Executor가 임무 단계로 분해하고, DMC가 Drive·Arm·AI 인터페이스의 완료·실패 응답을 다음 상태 전환 조건으로 사용합니다.

<div class="diagram" role="img" aria-label="JAVIS 중앙 제어 구조"><div class="diagram-node">사용자 요청<br>Server</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Task Executor<br>Mission</div><div class="diagram-arrow">→</div><div class="diagram-node owner">DMC<br>State &amp; Exception</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Interface<br>Real / Mock</div><div class="diagram-arrow">→</div><div class="diagram-node">Drive · Arm · AI</div></div>

## 실제 장비 없이 검증하는 인터페이스

### 하위 모듈보다 인터페이스를 먼저 고정

실제 장비와 Mock이 동일한 인터페이스를 구현하도록 분리해 하위 모듈 없이도 정상·취소·실패 경로를 반복 실행했습니다.

### Navigation 실패를 계층 문제로 분해

Planner·Controller·Costmap·Sensor Filtering을 각각 확인하고 Smac Planner Hybrid와 MPPI를 적용했습니다.

## 중앙 제어기의 역할

<div class="role-grid"><div class="info-card"><strong>중앙 제어</strong><span>임무 상태, Task Executor, 배터리 예외 흐름</span></div><div class="info-card"><strong>Interface &amp; Mock</strong><span>실제 장비와 모의 응답이 같은 계약을 사용하도록 분리</span></div><div class="info-card"><strong>Navigation</strong><span>Planner·Controller·Costmap 설정 비교 및 조정</span></div></div>

## 로봇 구성

시스템은 이동 베이스, 로봇팔, AI 모듈과 배터리 상태 입력으로 구성됩니다. 중앙 제어기는 특정 장비 구현에 직접 결합하지 않고 동일한 인터페이스를 통해 실제 장비와 Mock을 교체합니다. 공개 자료에서 확인되지 않은 센서·모터 모델과 연산 장치 사양은 기재하지 않습니다.

## 협소한 서가의 주행 문제

<dl class="flow"><dt>증상</dt><dd>좁은 서가에서 경로가 생성되지 않거나 진입 후 Recovery 과정에서 장애물과 접촉했습니다.</dd><dt>원인</dt><dd>비원형 Footprint 표현, 협로 Trajectory 탐색, Sensor Filtering과 Inflation 설정이 함께 영향을 줬습니다.</dd><dt>해결</dt><dd>Planner와 Controller를 교체하고 Footprint·Sensor Filter·Inflation 관련 값을 함께 조정했습니다.</dd><dt>검증</dt><dd>폭 60cm 테스트 통로를 통과하는 단일 시연을 완료했습니다.</dd></dl>

## 검증 결과

<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>Interface와 Mock 테스트</strong><p>하위 모듈의 정상·실패 응답을 단위 테스트로 검증합니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>배터리 예외 테스트</strong><p>충전·소모·Critical Callback과 경계값을 확인합니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>60cm 협로 통과</strong><p>영상으로 확인되는 단일 시연이며 반복 성공률은 아닙니다.</p></div></div>

## 관련 코드

[DMC 구현과 테스트 보기 ↗](https://github.com/jongbob1918/JAVIS/tree/main/javis_ros2/src/javis_dmc)

저장소에는 DMC Launch, Interface/Mock 단위 테스트와 검증 체크리스트가 있습니다.
