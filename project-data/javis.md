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
  - Python
  - Nav2
  - 2D LiDAR SLAM
  - Path Planning
  - State Machine
repository: https://github.com/jongbob1918/JAVIS
card:
  image: https://github.com/user-attachments/assets/ce7e6dba-8987-49cb-96f2-9ed3a3f76779
  imageAlt: JAVIS navigating between library shelves in RViz
  titleEn: JAVIS — Library Management Robot
  keywords:
    - ROS 2
    - Python
    - Nav2
    - 2D LiDAR SLAM
    - Path Planning
    - State Machine
  descriptionKo: 자율주행, 로봇팔과 비전 AI를 ROS 2로 통합해 도서 픽업·반납과 사용자 안내를 수행하는 도서관 관리 로봇을 개발했습니다.
  descriptionEn: Built a ROS 2 library management robot that integrates autonomous navigation, manipulation, and vision AI to pick up and return books and guide visitors.
overview: >-
  도서관에서는 도서 픽업·반납과 길 안내 같은 반복 업무에 지속적인 인력이 필요합니다.
  이를 자동화하기 위해 자율주행, 로봇팔과 비전 AI를 ROS 2로 연결한 도서관 관리 로봇 JAVIS를 개발했습니다.
  사용자가 도서 픽업을 요청하면 중앙 시스템이 작업을 할당하고, JAVIS가 책장으로 이동해 도서를 인식한 뒤 로봇팔로 픽업합니다.
demo:
  type: image
  src: https://github.com/user-attachments/assets/ce7e6dba-8987-49cb-96f2-9ed3a3f76779
  alt: RViz에서 협소한 서가 사이를 주행하는 JAVIS
  caption: 2D LiDAR와 Nav2를 사용한 서가 환경 자율주행
---

## 도서 요청에서 픽업까지

사용자가 도서를 요청하면 중앙 시스템이 로봇의 상태와 배터리를 확인해 작업을 할당합니다. JAVIS는 목표 책장으로 이동하고, 카메라로 도서를 인식한 뒤 로봇팔로 픽업합니다. 각 단계의 진행 상태와 작업 결과는 다시 중앙 시스템으로 전달됩니다.

<div class="diagram" role="img" aria-label="JAVIS 도서 픽업 작동 파이프라인"><div class="diagram-node">도서 요청</div><div class="diagram-arrow">→</div><div class="diagram-node">작업 할당</div><div class="diagram-arrow">→</div><div class="diagram-node owner">책장까지<br>자율주행</div><div class="diagram-arrow">→</div><div class="diagram-node owner">도서 인식</div><div class="diagram-arrow">→</div><div class="diagram-node owner">로봇팔 픽업</div><div class="diagram-arrow">→</div><div class="diagram-node">결과 반환</div></div>

## 여러 기능을 하나의 작업으로 연결하기

주행, 비전과 로봇팔 모듈은 서로 독립적으로 동작합니다. 메인 컨트롤러는 ROS 2와 State Machine을 기반으로 각 모듈의 실행 순서를 관리하고, 완료·실패 응답을 다음 상태로 전환하는 조건으로 사용합니다.

<div class="diagram" role="img" aria-label="JAVIS 중앙 제어 구조"><div class="diagram-node">중앙 시스템<br>작업 요청</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Task Executor<br>임무 실행</div><div class="diagram-arrow">→</div><div class="diagram-node owner">DMC<br>상태 · 예외</div><div class="diagram-arrow">→</div><div class="diagram-node owner">공통 Interface</div><div class="diagram-arrow">→</div><div class="diagram-node">Drive · Arm · AI</div></div>

메인 컨트롤러는 임무 상태와 배터리 상태를 함께 확인하고, 충돌이나 하위 모듈 응답 실패처럼 정상적으로 작업을 이어갈 수 없는 상황을 별도의 상태 전이로 처리합니다.

## 실제 장비 없이 통합 흐름 검증하기

실제 주행 장치, 카메라와 로봇팔이 모두 준비될 때까지 기다리지 않고 통합 개발을 진행할 수 있도록 실제 모듈과 동일한 인터페이스를 사용하는 Mock 환경을 구현했습니다.

<div class="role-grid"><div class="info-card"><strong>같은 명령 구조</strong><span>실제 모듈과 Mock이 동일한 인터페이스로 명령을 수신</span></div><div class="info-card"><strong>상태 전이 확인</strong><span>하위 모듈의 완료·실패 응답에 따른 다음 동작 검증</span></div><div class="info-card"><strong>독립적인 통합 개발</strong><span>장비 연결 전에도 전체 임무 흐름을 반복 실행</span></div></div>

Mock의 응답을 바꿔 정상 완료뿐 아니라 실패와 작업 취소 상황을 재현했습니다. 이를 통해 실제 로봇을 연결하기 전에 State Machine의 전이와 예외 처리 흐름을 반복적으로 확인했습니다.

## 좁은 서가를 통과하지 못했던 이유

초기 Nav2 구성에서는 좁은 서가에 진입하지 못하거나 회전 과정에서 주변 장애물과 접촉하는 문제가 발생했습니다. 장애물의 Inflation 영역을 크게 설정하면 통로가 막힌 것으로 판단했고, 작게 설정하면 벽과 가까운 경로가 생성됐습니다.

<dl class="flow"><dt>문제</dt><dd>경로 생성 실패, Recovery 반복과 회전 중 장애물 접촉이 발생했습니다.</dd><dt>원인</dt><dd>로봇의 비원형 Footprint와 회전 반경, LiDAR Sensor Filtering, Costmap Inflation과 협로 Trajectory 탐색이 함께 영향을 줬습니다.</dd><dt>개선</dt><dd>NavFn·DWB 구성과 비교해 Smac Planner Hybrid와 MPPI를 적용하고, Footprint·Sensor Filter·Inflation 값을 함께 조정했습니다.</dd><dt>확인</dt><dd>실제 테스트 통로에서 경로 생성과 진입, 회전 동작을 시연 영상으로 확인했습니다.</dd></dl>

## JAVIS를 구성하는 장비와 모듈

JAVIS는 이동 베이스, 2D LiDAR, 카메라, 로봇팔과 온보드 제어 모듈로 구성됩니다. 2D LiDAR와 Nav2는 지도 작성, 위치 추정과 장애물 회피를 담당하고, 카메라와 AI 모듈은 목표 도서를 인식합니다. 이동이 완료되면 로봇팔이 인식 결과를 바탕으로 픽업 작업을 수행합니다.

## 구현 결과 확인하기

<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>Interface와 Mock 테스트</strong><p>하위 모듈의 정상·실패 응답과 상태 전이를 단위 테스트로 확인합니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>배터리 예외 테스트</strong><p>충전·소모·Critical Callback과 경계값 처리 코드를 확인할 수 있습니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>협소 공간 주행</strong><p>경로 생성부터 통로 진입과 회전까지의 동작을 시연 영상으로 확인합니다.</p></div></div>

## 코드에서 확인하기

[DMC 구현과 테스트 보기 ↗](https://github.com/jongbob1918/JAVIS/tree/main/javis_ros2/src/javis_dmc)

저장소에는 DMC Launch, Interface/Mock 단위 테스트와 검증 체크리스트가 있습니다.
