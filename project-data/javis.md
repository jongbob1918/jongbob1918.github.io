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
  이를 자동화하기 위해 VIC-PINKY 모바일 로봇과 myCobot 매니퓰레이터, 비전 AI를 ROS 2로 연결한 도서관 관리 로봇 JAVIS를 개발했습니다.
  VIC-PINKY는 목표 책장까지 자율주행하고, myCobot은 카메라로 인식한 도서를 픽업·반납합니다.
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

## 도서 픽업 서비스

사용자가 도서를 요청하면 중앙 시스템이 로봇의 상태와 배터리를 확인해 작업을 할당합니다. JAVIS는 목표 책장으로 이동하고, 카메라로 도서를 인식한 뒤 로봇팔로 픽업합니다.

<figure class="feature-media"><img src="../assets/images/javis_book_pickup_pipeline.png" alt="도서 선택부터 인증, JAVIS 작업과 도서 수령까지의 서비스 흐름" loading="lazy"></figure>

## 픽업·반납 자율주행

좁은 서가 사이에서 픽업·반납 임무를 수행할 수 있도록 지도 작성부터 경로 계획, 경로 추종까지 Nav2 주행 구성을 개선했습니다.

<dl class="flow"><dt>지도 작성</dt><dd>Cartographer와 2D LiDAR로 도서관 지도를 작성하고 픽업·반납 위치를 지정했습니다.</dd><dt>초기 테스트</dt><dd>DWB로 주행을 반복하자 좁은 복도와 앞이 막힌 구간에서 탈출하지 못했습니다. Inflation 값을 높이면 통로를 막힌 공간으로 판단하고, 낮추면 벽에 지나치게 가까워졌습니다.</dd><dt>주행 개선</dt><dd>로봇의 형상과 회전 반경, 후진을 고려하는 Smac Planner Hybrid를 적용했습니다. LiDAR 필터와 Inflation 값을 조정하고, 여러 후보 궤적을 비교해 움직임을 선택하는 MPPI를 튜닝했습니다.</dd><dt>결과</dt><dd>좁은 서가와 회피 여유가 적은 구간에서도 충돌 없이 픽업·반납 위치까지 주행했습니다.</dd></dl>

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/javis_navigation_failure.gif" alt="DWB 적용 후 좁은 공간에서 회전에 실패하는 초기 주행" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/javis_nav_rviz.gif" alt="Smac Hybrid와 MPPI 적용 후 좁은 서가를 통과하는 주행" loading="lazy"></figure></div>

## 로봇 상태 및 임무 제어

로봇의 초기화, 충전, 작업 대기, 작업 수행과 충전소 이동을 상위 State로 구분했습니다. 각 임무 단계에서는 하위 모듈의 완료·실패·취소 응답을 확인해 다음 상태를 결정하고, 배터리 조건이나 긴급 정지 요청이 발생하면 현재 임무에서 복구 또는 안전 상태로 전환하도록 구성했습니다.

<figure class="feature-media"><img src="../assets/images/javis_state_machine.png" alt="JAVIS의 초기화, 충전, 대기, 작업, 복귀와 긴급 정지 상태 전이도" loading="lazy"></figure>

## 서버 요청을 주행·로봇팔 동작으로 연결하기

`DMC(Dobby Main Controller)`는 로봇 내부에서 작업 순서와 상태를 관리하는 메인 제어기입니다. 관제 서버가 임무를 보내면 DMC가 자율주행·비전·로봇팔 모듈을 순서대로 실행하고, 성공·실패 결과와 로봇 상태를 서버에 반환합니다.

<div class="diagram" role="img" aria-label="관제 서버의 임무가 DMC를 거쳐 자율주행, 비전과 로봇팔 동작으로 실행되고 결과가 반환되는 흐름"><div class="diagram-node">관제 서버<br>임무 할당</div><div class="diagram-arrow">→</div><div class="diagram-node owner">DMC<br>상태 · 작업 순서 관리</div><div class="diagram-arrow">→</div><div class="diagram-node owner">주행 · 비전 · 로봇팔<br>임무 실행</div><div class="diagram-arrow">→</div><div class="diagram-node">관제 서버<br>결과 · 상태 반환</div></div>

## 로봇 상태 모니터링

실물 로봇 통합 테스트 중 현재 State, 세부 임무, 배터리와 ROS 로그를 한 화면에서 확인하는 모니터링 GUI를 개발했습니다. 임무가 멈춘 단계와 모듈별 완료·실패 응답을 추적해 State Machine의 전이, 예외 처리와 통합 로직을 검증하는 데 사용했습니다.

<figure class="feature-media"><img src="../assets/images/javis_status_gui.png" alt="JAVIS의 메인 상태, 세부 임무, 배터리와 ROS 로그를 확인하는 모니터링 GUI" loading="lazy"></figure>

## 상태 전이 및 예외 처리 테스트

AI, 주행과 로봇팔 모듈이 모두 준비될 때까지 기다리지 않고 통합 개발을 진행할 수 있도록 공통 인터페이스를 정의했습니다. 실제 모듈과 Mock 모듈이 같은 명령과 응답 구조를 사용하므로 메인 컨트롤러를 변경하지 않고 실행 대상을 교체할 수 있습니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/javis_interface_mock_architecture.png" alt="실제 모듈과 Mock 모듈을 분리한 JAVIS 인터페이스 구조" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/javis_mock_test_gui.gif" alt="Mock 응답을 조작해 JAVIS 제어 흐름을 시험하는 GUI" loading="lazy"></figure></div>

Mock의 응답을 통해 정상 완료뿐 아니라 실행 실패와 작업 취소 상황을 재현했습니다. 이를 통해 실제 장비를 연결하기 전에 State Machine의 전이, 예외 처리와 하위 모듈 호출 순서를 반복적으로 확인했습니다.
