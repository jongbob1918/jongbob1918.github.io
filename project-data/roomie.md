---
slug: roomie
shortName: ROOMIE
group: key
order: 2
title: ROOMIE — 저비용 로봇팔의 엘리베이터 버튼 조작
description: 약 5만 원대 4축 로봇팔과 2D 카메라로 엘리베이터 버튼 조작에 도전한 Arm Controller
team: 4명
period: 2025.07.07–08.13
skills:
  - ROS 2
  - Python · OpenCV
  - 4-DOF Inverse Kinematics
  - Vision-Guided Control
  - ESP32 · FreeRTOS
repository: https://github.com/jongbob1918/ROOMIE
card:
  image: assets/images/elevator-alignbutton.gif
  imageAlt: 2D 카메라의 관측 결과로 엘리베이터 버튼 앞에 정렬하는 ROOMIE 로봇팔
  titleEn: ROOMIE — Vision-Guided Low-Cost Robot Arm
  keywords:
    - ROS 2
    - 4-DOF Arm
    - Arm Control
    - FreeRTOS
  descriptionKo: 약 5만 원대 4축 로봇팔과 2D 카메라로 엘리베이터 버튼의 위치 계산부터 누르기까지 구현했습니다.
  descriptionEn: Built an elevator-button manipulation pipeline using a low-cost 4-DOF arm and a standard 2D camera.
overview: >-
  호텔에서는 룸서비스 배송과 길 안내처럼 층간 이동이 필요한 반복 업무가 발생합니다. ROOMIE는 자율주행, 물품 배송, 사용자 안내와 관리자 모니터링을 ROS 2로 연결한 호텔 서비스 로봇입니다. 엘리베이터 앞까지 이동한 뒤 버튼과 문 상태를 인식하고, 4축 로봇팔로 호출·목적층 버튼을 조작해 사람의 도움 없이 층간 임무를 이어갑니다.
demo:
  type: youtube
  src: https://www.youtube.com/embed/CqO3OH661Os
  title: ROOMIE 프로젝트 시연 영상
---

## 엘리베이터를 스스로 이용하는 서비스 흐름

ROOMIE는 엘리베이터 앞까지 자율주행한 뒤 외부 호출 버튼을 누르고 문 열림을 확인합니다. 탑승 후에는 내부 목적층 버튼을 조작하고, 층수 표시기의 OCR 결과로 도착을 판단한 다음 하차해 기존 배송·안내 임무를 계속합니다.

<figure class="feature-media"><img src="../assets/images/roomie_elevator_flow.png" alt="엘리베이터 도착, 호출 버튼 조작, 탑승, 목적층 버튼 조작과 하차로 이어지는 ROOMIE 동작 흐름" loading="lazy"></figure>

## 시스템 설계

투숙객은 Guest GUI에서 룸서비스를 주문하거나 목적지를 선택하고, 직원은 Staff GUI에서 주문을 확인한 뒤 픽업을 요청합니다. 요청은 Roomie Main Service를 거쳐 로봇에 할당되며, ROS 2 기반 Roomie Controller가 주행·비전·로봇팔·적재함 제어 모듈의 실행을 연결합니다.

<figure class="feature-media"><img src="../assets/images/roomie_system_architecture.png" alt="Guest, Staff, Admin GUI와 Roomie Main Server, 로봇 내부 제어 모듈을 연결한 ROOMIE 시스템 구성" loading="lazy"></figure>

## 인식 결과를 물리 동작으로 연결한 Arm Controller

4명으로 구성된 팀에서 Vision Service가 버튼을 검출한 이후부터 로봇팔이 조작 명령을 마치고 ROS 2 Action 결과를 반환할 때까지의 Arm Controller를 담당했습니다.

<div class="diagram" role="img" aria-label="Arm Controller 담당 범위"><div class="diagram-node">Vision Service<br>버튼 검출</div><div class="diagram-arrow">→</div><div class="diagram-node owner">3D 위치 추정<br>좌표계 변환</div><div class="diagram-arrow">→</div><div class="diagram-node owner">관측 자세<br>4-DOF IK</div><div class="diagram-arrow">→</div><div class="diagram-node owner">ESP32 제어<br>ACK · 예외 처리</div><div class="diagram-arrow">→</div><div class="diagram-node">Action Result<br>Success · Abort</div></div>

담당 범위에는 버튼 중심과 크기를 이용한 거리 추정, Forward Kinematics와 Hand–Eye Calibration을 이용한 좌표계 변환, 4축 역기구학, 관측 자세 기반 동작 계획, ESP32 모터 제어와 오류 처리가 포함됩니다. GUI와 팀 전체 기능을 나열하기보다 저비용 로봇팔의 불확실성을 실제 동작으로 연결한 과정에 집중했습니다.

## Arm Controller 하드웨어 구성

본체 기준 약 5만 원대의 교육용 4축 로봇팔을 사용했습니다. 팔끝에는 일반 2D 카메라와 버튼 접촉부를 장착하고, 네 개의 서보모터를 ESP32에서 제어하도록 구성했습니다.

<figure class="feature-media"><img src="../assets/images/roomie_arm_hardware.webp" alt="2D 카메라와 팔끝 버튼 클릭부, 서보모터로 구성된 ROOMIE의 4축 로봇팔" loading="lazy"></figure>

## 2D 검출 결과를 로봇 기준 3차원 목표로 바꾸기

Vision Service는 엘리베이터 버튼의 검출 박스와 중심 위치를 제공합니다. 기본 실행 경로인 `normal` 모드에서는 실험 대상 버튼의 대표 지름을 35 mm로 설정하고, 화면상 버튼 크기와 카메라 내부 파라미터를 이용해 깊이를 근사했습니다.

<figure class="feature-media portrait-evidence"><img src="../assets/images/roomie-button-detection.webp" alt="2D 카메라 영상에서 여러 엘리베이터 버튼을 검출한 결과" loading="lazy"><figcaption>실제 2D 카메라 입력에서 검출한 엘리베이터 버튼. 검출 박스의 중심과 크기가 Arm Controller의 위치 추정 입력이 됩니다.</figcaption></figure>

<div class="formula-block">Z ≈ f<sub>x</sub>D / W<sub>px</sub> &nbsp;·&nbsp; X = (u-c<sub>x</sub>)Z/f<sub>x</sub> &nbsp;·&nbsp; Y = (v-c<sub>y</sub>)Z/f<sub>y</sub></div>

버튼의 실제 지름 `D`, 영상에서의 버튼 너비 `Wpx`와 초점거리 `fx`로 깊이 `Z`를 근사하고, 버튼 중심 픽셀 `(u, v)`를 카메라 기준 `(X, Y, Z)`로 변환합니다.

네 기준점이 제공되는 경우에는 `solvePnPRansac`으로 카메라 기준 Pose를 구하는 `corner` 경로도 구현했습니다. 다만 공개 저장소의 기본 설정은 중심과 크기를 이용하는 `normal` 모드이며, PnP를 기본 시연 결과로 설명하지 않습니다.

<div class="formula-block">T<sub>base→button</sub> = T<sub>base→tool</sub> · T<sub>tool→camera</sub> · T<sub>camera→button</sub></div>

현재 명령 관절각의 Forward Kinematics, Hand–Eye Calibration과 OpenCV–로봇 좌표축 보정을 적용해 카메라 기준 버튼 위치를 로봇 베이스 기준 목표로 변환했습니다.

<figure class="feature-media"><img src="../assets/images/roomie_arm_principle.png" alt="카메라 영상의 버튼 좌표를 로봇 베이스 기준 목표와 관절 제어로 연결하는 원리" loading="lazy"><figcaption>버튼의 영상 좌표를 카메라·Tool·Base 좌표계를 거쳐 로봇팔의 목표로 변환하는 구조</figcaption></figure>

## 4축 IK 목표 검증

변환된 목표 위치는 `ikpy` 기반 4관절 역기구학으로 계산했습니다. 현재 관절각을 초기값으로 사용하고, 계산 결과를 Forward Kinematics로 다시 검산해 수치 잔차가 1 mm를 넘거나 관절 제한을 벗어나면 이동을 실패 처리했습니다.

<figure class="feature-media evidence-video"><video controls playsinline preload="metadata" poster="../assets/images/roomie-ik-target-control-poster.jpg"><source src="../assets/videos/roomie-ik-target-control.mp4" type="video/mp4">브라우저가 MP4 영상을 지원하지 않습니다.</video><figcaption>IK 목표 제어 실험. 실제 로봇팔의 이동과 RViz 관절 모델을 함께 확인했습니다.</figcaption></figure>

여기서 1 mm는 IK 수치해의 허용 잔차이며 실제 로봇팔 끝단의 절대 정확도를 의미하지는 않습니다.

## 관측 자세에서 버튼 누르기

초기에는 임의의 자세에서 버튼 위치를 계산해 시작 자세에 따라 팔끝의 도달 위치가 달라졌습니다. 이후 `ClickButton` 요청을 받으면 먼저 정해진 관측 자세로 이동하고, 같은 조건에서 버튼 위치를 계산하도록 순서를 고정했습니다.

로봇팔 링크의 전체 길이는 약 33.5 cm이므로 팔만으로 확보할 수 있는 작업 범위가 제한적이었습니다. ROOMIE 본체가 버튼 가까이 정밀하게 접근한 뒤, 로봇팔이 관측 자세에서 클릭 동작을 실행하도록 구성했습니다.

<div class="diagram" role="img" aria-label="ROOMIE 본체 접근부터 버튼 클릭까지의 순서"><div class="diagram-node">본체 정밀 접근</div><div class="diagram-arrow">→</div><div class="diagram-node owner">OBSERVE_POSE</div><div class="diagram-arrow">→</div><div class="diagram-node owner">버튼 위치 계산</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Standby<br>80 mm</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Press<br>100 mm</div><div class="diagram-arrow">→</div><div class="diagram-node">Retreat</div></div>

<figure class="feature-media evidence-video"><video controls playsinline preload="metadata" poster="../assets/images/roomie-button-click-poster.jpg"><source src="../assets/videos/roomie-button-click.mp4" type="video/mp4">브라우저가 MP4 영상을 지원하지 않습니다.</video><figcaption>개발 환경에서 관측 자세와 버튼 접근 동작을 확인한 실험</figcaption></figure>

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/elevator-alignbutton.gif" alt="ROOMIE가 엘리베이터 버튼 가까이 정밀하게 접근하는 과정" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/elevator-pushouterbutton2.gif" alt="ROOMIE 로봇팔이 엘리베이터 외부 호출 버튼을 누르는 과정" loading="lazy"></figure></div>

## ESP32 모션 제어

초기 등속 제어에서 발생한 급격한 시작과 정지를 줄이기 위해, 오차함수 기반 누적 프로파일로 시작각과 목표각 사이를 부드럽게 보간했습니다. 모터 갱신과 명령 수신은 FreeRTOS의 서로 다른 태스크로 분리했습니다.

<div class="role-grid"><div class="info-card"><strong>6 ms 모션 갱신</strong><span>네 개 서보의 목표각을 일정한 주기로 갱신</span></div><div class="info-card"><strong>통신 태스크 분리</strong><span>팔이 움직이는 동안에도 새 명령과 오류를 처리</span></div><div class="info-card"><strong>완료·실패 반환</strong><span>완료 ACK를 확인하고 IK·통신 오류를 Action 결과로 반환</span></div></div>

## 전체 시연

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/qIbQOql0ST0" title="ROOMIE 전체 시연 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>

## 최종 결과와 한계

10회의 버튼 조작 시도 중 실제 입력이 확인된 경우는 3회였습니다. 나머지 시도에는 위치 정렬 오차와 버튼을 누르는 힘이 부족했던 경우가 함께 포함돼 있으며, 두 원인을 별도로 집계하지는 못했습니다.

<div class="metric-grid"><div class="metric-card"><span class="metric-value">10회</span><span class="metric-label">버튼 조작 시도</span></div><div class="metric-card"><span class="metric-value">3회</span><span class="metric-label">실제 버튼 입력 성공</span></div><div class="metric-card"><span class="metric-value">30%</span><span class="metric-label">입력 성공률</span></div></div>

<div class="evidence-grid constraint-grid"><div class="evidence-card"><span class="status-tag warning">PERCEPTION</span><strong>2D 깊이 추정</strong><p>버튼 크기로 거리를 근사했지만 검출 크기와 촬영 각도에 민감했습니다.</p></div><div class="evidence-card"><span class="status-tag warning">MECHANISM</span><strong>백래시·프레임 변형</strong><p>관측 자세를 통일해도 실제 팔끝 위치에는 오차가 남았습니다.</p></div><div class="evidence-card"><span class="status-tag warning">ACTUATION</span><strong>부족한 누름 힘</strong><p>버튼에 도달해도 토크와 프레임 강성 부족으로 입력되지 않았습니다.</p></div><div class="evidence-card"><span class="status-tag warning">FEEDBACK</span><strong>센서 피드백 부재</strong><p>Encoder와 Force Sensor가 없어 실패 원인을 직접 측정하지 못했습니다.</p></div></div>
