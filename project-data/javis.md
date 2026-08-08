---
slug: javis
shortName: JAVIS
group: key
order: 1
title: JAVIS — 도서관 관리 로봇
description: 자율주행, 로봇팔과 비전 AI를 통합한 ROS 2 기반 도서관 관리 로봇
team: 9명
period: 2024.09–11
role: 자율주행 안정화 · 로봇 상태 및 임무 제어
skills:
  - ROS 2
  - Python
  - Nav2
  - 2D LiDAR SLAM
  - Path Planning
  - State Machine
repository: https://github.com/jongbob1918/JAVIS
card:
  image: assets/images/javis_robot_drive.gif
  imageAlt: 도서관 환경을 자율주행하는 JAVIS
  sequence:
    - src: assets/images/javis_robot_drive.gif
      alt: 도서관 환경을 자율주행하는 JAVIS
      duration: 28000
    - src: assets/images/javis_nav_rviz.gif
      alt: RViz에서 협소한 서가 사이를 주행하는 JAVIS
      duration: 7510
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
  src: ../assets/images/javis_robot_drive.gif
  alt: 실제 도서관 환경을 주행하는 JAVIS
  sequence:
    - src: ../assets/images/javis_robot_drive.gif
      alt: 실제 도서관 환경을 주행하는 JAVIS
      duration: 28000
    - src: ../assets/images/javis_nav_rviz.gif
      alt: RViz에서 협소한 서가 사이를 주행하는 JAVIS
      duration: 7510
---

## 도서 요청에서 픽업까지

사용자가 도서를 요청하면 중앙 시스템이 로봇의 상태와 배터리를 확인해 작업을 할당합니다. JAVIS는 목표 책장으로 이동하고, 카메라로 도서를 인식한 뒤 로봇팔로 픽업합니다.

<figure class="feature-media"><img src="../assets/images/javis_book_pickup_pipeline.png" alt="도서 선택부터 인증, JAVIS 작업과 도서 수령까지의 서비스 흐름" loading="lazy"></figure>

## 좁은 서가에서도 안정적으로 이동하기

JAVIS는 2D LiDAR로 작성한 지도에서 위치를 추정하고, Nav2를 사용해 목표 책장까지의 경로를 생성합니다. Global Planner가 전체 이동 경로를 만들고 Local Controller가 LiDAR로 감지한 장애물과 Costmap을 반영해 로봇의 속도와 회전 방향을 결정합니다.

초기 구성에서는 장애물의 Inflation 영역을 크게 설정하면 좁은 통로가 막힌 것으로 판단했고, 작게 설정하면 벽과 가까운 경로가 생성됐습니다. 회전이나 Recovery 과정에서 주변 장애물과 접촉하는 문제도 반복됐습니다.

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/javis_navigation_failure.gif" alt="협소 공간에서 회전 중 장애물과 접촉하는 초기 주행" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/javis_nav_rviz.gif" alt="개선 후 협소한 서가 사이를 주행하는 JAVIS의 RViz 화면" loading="lazy"></figure></div>

<dl class="flow"><dt>경로 계획</dt><dd>점 모델 중심의 NavFn 대신 로봇의 직사각형 형상, 회전 반경과 후진 경로를 고려하는 Smac Planner Hybrid를 적용했습니다.</dd><dt>장애물 인식</dt><dd>실제 로봇보다 넓게 설정돼 근접 장애물을 제거하던 LiDAR 필터 범위를 다시 설정하고 Costmap Inflation 가중치를 조정했습니다.</dd><dt>경로 추종</dt><dd>복잡한 공간에서 유효한 회피 궤적을 찾기 어려웠던 DWB 대신 샘플링 기반 예측 제어를 사용하는 MPPI Controller를 적용했습니다.</dd></dl>

## 서비스 서버와 로봇 모듈 연결하기

JAVIS는 서비스 서버와 로봇 내부 제어 모듈이 ROS 2 인터페이스를 통해 요청과 상태를 양방향으로 교환하는 구조입니다. JAVIS Device의 DMC는 서버에서 받은 임무를 주행·로봇팔 제어기에 전달하고, 각 모듈의 실행 결과와 로봇 상태를 다시 서버에 전달합니다. AI Image Server는 카메라 영상을 처리하고 인식 결과를 로봇에 반환합니다.

<div class="system-architecture" role="img" aria-label="JAVIS Server와 AI Image Server가 로봇 내부 JAVIS Device, Arm Controller, Drive Controller와 양방향으로 통신하는 시스템 구성"><section class="system-domain service-domain"><h3>Service</h3><div class="system-module"><strong>JAVIS Server</strong><small>작업 요청 · 로봇 상태</small></div><div class="system-module"><strong>AI Image Server</strong><small>영상 분석 · 인식 결과</small></div></section><div class="bidirectional-links" aria-hidden="true"><div><span>Task · Status</span><b>⇄</b></div><div><span>Image · Result</span><b>⇄</b></div></div><section class="system-domain robot-domain"><h3>Robot · JAVIS</h3><div class="system-module system-core"><strong>JAVIS Device · DMC</strong><small>상태 관리 · 임무 제어</small><div class="module-parts"><span>Speaker</span><span>LCD</span><span>Web Cam</span><span>Mic</span></div></div><div class="internal-links" aria-hidden="true">⇅</div><div class="robot-modules"><div class="system-module"><strong>Arm Controller · RP5</strong><small>도서 픽업 제어</small><div class="module-parts"><span>Joint Motor</span><span>Gripper</span><span>Web Cam</span></div></div><div class="system-module"><strong>Drive Controller · RP5</strong><small>자율주행 제어</small><div class="module-parts"><span>BLDC Motor</span><span>Impact Sensor</span><span>LiDAR</span><span>Temp Sensor</span></div></div></div></section></div>

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/javis_state_machine.png" alt="JAVIS의 충전, 대기, 작업과 긴급 정지 상태 전이도" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/javis_status_gui.png" alt="JAVIS의 메인 상태, 세부 임무, 배터리와 ROS 로그를 확인하는 모니터링 GUI" loading="lazy"></figure></div>

## 실제 장비 없이 제어 흐름 검증하기

AI, 주행과 로봇팔 모듈이 모두 준비될 때까지 기다리지 않고 통합 개발을 진행할 수 있도록 공통 인터페이스를 정의했습니다. 실제 모듈과 Mock 모듈이 같은 명령과 응답 구조를 사용하므로 메인 컨트롤러를 변경하지 않고 실행 대상을 교체할 수 있습니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/javis_interface_mock_architecture.png" alt="실제 모듈과 Mock 모듈을 분리한 JAVIS 인터페이스 구조" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/javis_mock_test_gui.gif" alt="Mock 응답을 조작해 JAVIS 제어 흐름을 시험하는 GUI" loading="lazy"></figure></div>

Mock의 응답을 통해 정상 완료뿐 아니라 실행 실패와 작업 취소 상황을 재현했습니다. 이를 통해 실제 장비를 연결하기 전에 State Machine의 전이, 예외 처리와 하위 모듈 호출 순서를 반복적으로 확인했습니다.
