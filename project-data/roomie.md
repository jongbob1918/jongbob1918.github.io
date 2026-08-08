---
slug: roomie
shortName: ROOMIE
group: key
order: 2
title: ROOMIE — 호텔 서비스 로봇
description: 룸서비스 배송과 길 안내, 엘리베이터 층간 이동을 하나의 서비스로 연결한 호텔 로봇
team: 4명
period: 2025.07.07–08.13
skills:
  - ROS 2
  - Python
  - OpenCV
  - Inverse Kinematics
  - PBVS
  - ESP32 · FreeRTOS
repository: https://github.com/jongbob1918/ROOMIE
card:
  image: assets/images/elevator-alignbutton.gif
  imageAlt: ROOMIE robot arm aligning with an elevator button
  titleEn: ROOMIE — Hotel Service Robot
  keywords:
    - ROS 2
    - 4-DOF Arm
    - PBVS
    - FreeRTOS
  descriptionKo: 카메라로 인식한 버튼을 로봇 기준 3차원 좌표로 변환하고, 4축 로봇팔과 ESP32를 제어해 엘리베이터 버튼을 직접 조작했습니다.
  descriptionEn: Built a vision-to-motion pipeline that transforms an elevator button into a robot-frame target and controls a 4-DOF arm through an ESP32.
overview: >-
  호텔에서는 룸서비스 배송과 길 안내처럼 층간 이동이 필요한 반복 업무가 발생합니다. ROOMIE는 자율주행, 물품 배송, 사용자 안내와 관리자 모니터링을 ROS 2로 연결한 호텔 서비스 로봇입니다. 엘리베이터 앞까지 이동한 뒤 버튼과 문 상태를 인식하고, 4축 로봇팔로 호출·목적층 버튼을 조작해 사람의 도움 없이 층간 임무를 이어갑니다.
demo:
  type: youtube
  src: https://www.youtube.com/embed/qIbQOql0ST0
  title: ROOMIE 호텔 실내 층간 이동 데모
---

## 엘리베이터를 스스로 이용하는 서비스 흐름

ROOMIE는 엘리베이터 앞까지 자율주행한 뒤 외부 호출 버튼을 누르고 문 열림을 확인합니다. 탑승 후에는 내부 목적층 버튼을 조작하고, 층수 표시기의 OCR 결과로 도착을 판단한 다음 하차해 기존 배송·안내 임무를 계속합니다.

<figure class="feature-media"><img src="../assets/images/roomie_elevator_flow.png" alt="엘리베이터 도착, 호출 버튼 조작, 탑승, 목적층 버튼 조작과 하차로 이어지는 ROOMIE 동작 흐름" loading="lazy"></figure>

## My Role

4명으로 구성된 팀에서 엘리베이터 버튼을 조작하는 Arm Controller를 담당했습니다. Vision Service의 버튼 검출 결과를 로봇 기준 3차원 목표로 변환하고, 4축 로봇팔의 역기구학과 PBVS 정렬, ESP32 모터 제어를 연결했습니다. 또한 HTML·CSS·JavaScript 기반 Guest GUI와 PyQt 기반 Staff GUI를 구현하고 로봇 하드웨어 제작에 참여했습니다.

## 화면 속 버튼을 로봇팔의 목표로 바꾸기

Vision Service에서 버튼의 바운딩 박스와 네 모서리 좌표를 받으면 `solvePnPRansac`으로 카메라 기준 버튼 자세를 계산합니다. 이 결과에 Hand–Eye Calibration 행렬과 현재 관절의 Forward Kinematics를 결합해 로봇 베이스 기준의 목표 좌표를 얻습니다.

<div class="formula-block">T<sub>base→button</sub> = T<sub>base→tool</sub> · T<sub>tool→camera</sub> · T<sub>camera→button</sub></div>

<figure class="feature-media"><img src="../assets/images/roomie_arm_principle.png" alt="카메라 영상의 버튼 픽셀 좌표를 추출해 위치를 추정하고 로봇팔 관절 제어로 연결하는 구조" loading="lazy"></figure>

변환된 목표 위치는 `ikpy` 기반 4관절 역기구학으로 계산합니다. 계산 결과를 Forward Kinematics로 다시 검산해 위치 오차가 1 mm를 넘거나 관절 제한을 벗어나면 모터 명령을 보내지 않도록 했습니다.

## 정렬하고 누른 뒤 안전하게 복귀하기

버튼 클릭은 하나의 ROS 2 Action으로 구성했습니다. 로봇팔이 관측 자세로 이동하면 PBVS가 버튼 정면의 준비 위치를 계산하고, 준비 위치에서 버튼 방향으로 전진해 접촉한 뒤 저장한 관절각으로 후퇴합니다. 작업 성공 여부와 관계없이 마지막에는 관측 자세로 복귀하도록 실행 흐름을 묶었습니다.

<div class="diagram" role="img" aria-label="ROOMIE 버튼 조작 제어 흐름"><div class="diagram-node">Button Pose<br>Vision Service</div><div class="diagram-arrow">→</div><div class="diagram-node owner">PnP · Hand–Eye<br>3D Target</div><div class="diagram-arrow">→</div><div class="diagram-node owner">PBVS<br>Alignment</div><div class="diagram-arrow">→</div><div class="diagram-node owner">4-DOF IK<br>Press · Retreat</div><div class="diagram-arrow">→</div><div class="diagram-node">Action Result<br>Success · Abort</div></div>

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-alignbutton.gif" alt="ROOMIE가 카메라로 엘리베이터 버튼 위치에 로봇팔을 정렬하는 과정" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/elevator-pushouterbutton2.gif" alt="ROOMIE의 4축 로봇팔이 엘리베이터 외부 호출 버튼을 누르는 동작" loading="lazy"></figure></div>

동시에 들어온 클릭 요청은 실행 잠금으로 차단하고, 같은 버튼의 반복 요청에는 쿨다운을 적용했습니다. 비전 응답이나 IK 계산, ESP32 완료 응답이 실패하면 Action을 중단해 다음 단계가 잘못 이어지지 않도록 했습니다.

## 정지 진동과 통신 지연 줄이기

초기 등속 제어에서는 목표 각도에 도달할 때 팔끝이 떨리거나 동작이 끊기는 현상이 나타났습니다. ESP32에서 Gaussian 누적함수 기반 가감속 프로파일을 적용하고 네 관절의 목표각을 6 ms 주기로 함께 갱신해 급격한 속도 변화를 줄였습니다.

<dl class="flow"><dt>모션 제어</dt><dd>FreeRTOS Motion Task를 한 코어에 고정해 6 ms 주기로 네 개의 서보 목표각을 갱신합니다.</dd><dt>명령 수신</dt><dd>Communication Task를 별도 코어에서 실행해 모터 이동 중에도 시리얼 입력 처리가 제어 주기를 막지 않도록 했습니다.</dd><dt>완료 확인</dt><dd>460800 baud로 관절 명령을 전송하고 ESP32의 완료 ACK를 받은 경우에만 다음 동작으로 전환합니다.</dd><dt>예외 처리</dt><dd>오래된 수신 버퍼를 비우고 타임아웃·IK 실패·중복 요청을 각각 실패 결과로 반환합니다.</dd></dl>

## 서비스 화면과 로봇 제어 연결하기

투숙객은 Guest GUI에서 룸서비스를 주문하거나 목적지를 선택하고, 직원은 Staff GUI에서 주문을 확인한 뒤 픽업을 요청합니다. 요청은 Roomie Main Service를 거쳐 로봇에 할당되며, ROS 2 기반 Roomie Controller가 주행·비전·로봇팔·적재함 제어 모듈의 실행을 연결합니다.

<figure class="feature-media"><img src="../assets/images/roomie_system_architecture.png" alt="Guest, Staff, Admin GUI와 Roomie Main Server, 로봇 내부 제어 모듈을 연결한 ROOMIE 시스템 구성" loading="lazy"></figure>
