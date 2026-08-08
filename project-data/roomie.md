---
slug: roomie
shortName: ROOMIE
group: key
order: 2
title: ROOMIE — 엘리베이터 버튼 조작 로봇
description: ROOMIE 4축 로봇팔 좌표변환, IK, FreeRTOS 제어 프로젝트
team: 4명
period: 2025.07.07–08.13
skills:
  - ROS 2
  - 4-DOF Arm
  - Hand-Eye Calibration
  - IK
  - FreeRTOS
  - ESP32
repository: https://github.com/jongbob1918/ROOMIE
card:
  image: assets/images/elevator-alignbutton.gif
  imageAlt: ROOMIE robot arm aligning with an elevator button
  titleEn: ROOMIE — Hotel Room-Service Robot
  keywords:
    - ROS 2
    - 4-DOF Arm
    - Inverse Kinematics
    - FreeRTOS
  descriptionKo: 카메라로 인식한 엘리베이터 버튼 위치를 4축 로봇팔의 관절각으로 변환하고, ESP32 제어기와 연결해 실제 버튼 조작을 구현했습니다.
  descriptionEn: Built a 4-DOF arm pipeline from Hand-Eye coordinate transforms and IK to ESP32 motion control. Separated communication and 6 ms target motion-update tasks with FreeRTOS.
overview: >-
  카메라에서 얻은 버튼 위치를 로봇 기준 좌표와 4개 관절각으로 변환하고,
  통신과 모션 갱신을 분리한 ESP32 제어기로 실제 버튼 조작까지 연결했습니다.
demo:
  type: image
  src: ../assets/images/elevator-pushouterbutton2.gif
  alt: ROOMIE 로봇팔의 엘리베이터 버튼 조작
---

## 버튼 인식에서 모터 명령까지

<div class="diagram" role="img" aria-label="ROOMIE 버튼 조작 파이프라인"><div class="diagram-node">Button BBox<br>Vision</div><div class="diagram-arrow">→</div><div class="diagram-node owner">PnP · Hand-Eye<br>3D Target</div><div class="diagram-arrow">→</div><div class="diagram-node owner">IK<br>4 Joint Angles</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Serial Command<br>ESP32</div><div class="diagram-arrow">→</div><div class="diagram-node owner">FreeRTOS<br>4 Servos</div></div>

관측, 접근, 정렬, 누르기를 분리하고 IK 해가 허용 오차나 관절 범위를 벗어나면 명령을 보내지 않습니다.

## 좌표변환과 모션 프로파일

### 카메라 좌표를 로봇 기준으로 변환

solvePnPRansac과 Hand-Eye Calibration, 현재 관절의 순기구학 결과를 결합합니다.

<div class="formula-block">T_base→button = T_base→tool · T_tool→camera · T_camera→button</div>

### IK 해 검증

계산한 관절각으로 Forward Kinematics를 다시 수행하고 위치 오차와 관절 범위를 검사합니다.

<div class="formula-block">e_IK = ‖p_FK(q*) − p_target‖₂ ≤ 0.001 m</div>

### Gaussian 모션 보간

ESP32의 Motion Task는 시작각과 목표각 사이를 Gaussian 누적함수 기반으로 갱신합니다.

## 제어 시스템 구성

<div class="role-grid"><div class="info-card"><strong>Pose &amp; IK</strong><span>Hand-Eye 좌표변환과 4관절 해 계산</span></div><div class="info-card"><strong>Motion Control</strong><span>ROS 2–Serial–ESP32 명령 흐름과 보간</span></div><div class="info-card"><strong>Integration</strong><span>접근·정렬·누르기 시퀀스와 GUI 연동</span></div></div>

## 4축 로봇팔과 ESP32

4개의 서보 모터로 구성된 로봇팔을 ESP32가 구동하고, 카메라 관측값은 ROS 2 제어 노드에서 좌표변환과 IK를 거쳐 관절 명령으로 변환됩니다. Encoder나 Force Sensor 기반 접촉 피드백이 확인되지 않아 명령 기반 Open-loop Actuator Control로 설명합니다.

## 버튼 빗맞힘과 정지 진동

<dl class="flow"><dt>증상</dt><dd>정지 순간 팔끝이 흔들리고 계산된 버튼 위치와 실제 접촉점이 어긋났습니다.</dd><dt>원인</dt><dd>좌표계 장착 오차, 급격한 관절각 변화와 Blocking Serial 처리가 함께 영향을 줬습니다.</dd><dt>해결</dt><dd>Hand-Eye 변환을 적용하고 통신과 Motion Task를 서로 다른 Core에 배치했으며 Gaussian 보간을 적용했습니다.</dd><dt>검증</dt><dd>버튼 인식부터 실제 누르기까지 연속 동작을 완료했습니다.</dd></dl>

## 검증 결과

<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>4개 활성 관절</strong><p>URDF Chain의 Active Link와 4개 Servo 명령을 확인할 수 있습니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>분리된 FreeRTOS Task</strong><p>Motion과 Serial 처리를 서로 다른 Core에 고정합니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>연속 버튼 조작</strong><p>접근·정렬·누르기의 End-to-end 동작을 영상으로 확인합니다.</p></div></div>

## 관련 코드

[Arm Controller 구현 보기 ↗](https://github.com/jongbob1918/ROOMIE/tree/main/ros2_ws/src/roomie_ac)

좌표변환, IK, Serial Manager, ESP32 Firmware와 Calibration 실행 파일이 공개되어 있습니다.
