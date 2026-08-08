---
title: 로봇 소프트웨어 지식 로드맵
description: 프로젝트와 개발 일지에서 추출한 SLAM, Navigation, 지형 인지, ROS 2 시스템 및 검증 학습 TODO입니다.
publishedAt: 2026-08-08
category: robotics-foundations
type: overview
tags: [Roadmap, Robotics, SLAM, Navigation, ROS2]
draft: false
featured: true
---

현재 프로젝트와 개발 일지에서 반복해서 사용한 기술을 기준으로 정리한 학습 TODO다. 단순히 용어를 읽은 상태는 완료로 표시하지 않는다.

> 완료 기준: 구조를 직접 설명하고, 관련 코드 위치를 찾고, 대표 실패 조건을 말하고, 검증 실험과 측정 지표를 설계할 수 있어야 한다.

## P0 — 좌표계와 상태 추정

- [ ] `map → odom → base_link → sensor` TF 구조를 그림으로 설명한다.
- [ ] SE(2), SE(3), SO(3)의 역할과 차이를 설명한다.
- [ ] Rotation matrix, Euler angle, quaternion의 변환과 특이점을 설명한다.
- [ ] Homogeneous transformation의 합성·역변환을 직접 계산한다.
- [ ] LiDAR–IMU와 Camera–Robot extrinsic 오차의 증상을 구분한다.
- [ ] Sensor timestamp, PTP, point deskew의 관계를 설명한다.
- [ ] Gaussian, covariance, process noise, measurement noise를 설명한다.
- [ ] Kalman Filter, EKF, ESKF의 상태와 오차 상태 차이를 설명한다.
- [ ] IMU bias random walk, observability, degeneracy를 설명한다.
- [ ] Mahalanobis distance와 measurement gating을 적용한다.

## P0 — LiDAR-Inertial SLAM

- [ ] FAST-LIO2의 `IMU propagation → deskew → scan-to-map → ESKF update` 흐름을 설명한다.
- [ ] Point-to-point와 point-to-plane residual의 차이를 설명한다.
- [ ] ikd-tree가 nearest-neighbor search와 증분 map 갱신에 필요한 이유를 설명한다.
- [ ] Voxel downsampling 크기가 정확도와 처리시간에 미치는 영향을 비교한다.
- [ ] IMU dropout, 잘못된 extrinsic, 시간 오차의 증상을 rosbag으로 구분한다.
- [ ] Mapping과 prior-map Localization의 상태 흐름 차이를 설명한다.
- [ ] `map_T_odom` 보정과 pose jump 제한의 목적을 설명한다.

## P0 — Loop Closure와 Factor Graph

- [ ] Scan Context의 ring key와 회전 정합 원리를 설명한다.
- [ ] Place recognition, global registration, local registration을 구분한다.
- [ ] ICP, GICP, Nano-GICP의 대응점과 목적함수를 비교한다.
- [ ] Quatro 또는 TEASER++가 outlier에 강한 이유를 설명한다.
- [ ] PriorFactor, BetweenFactor, loop factor를 그래프로 표현한다.
- [ ] Gauss–Newton과 Levenberg–Marquardt의 차이를 설명한다.
- [ ] iSAM2의 증분 최적화와 전체 batch optimization을 비교한다.
- [ ] False loop closure를 탐지하고 차단할 gate를 설계한다.

## P0 — Navigation과 Motion Control

- [ ] Global planner, local controller, behavior, recovery의 책임을 구분한다.
- [ ] Grid A*, Hybrid A*, route-graph A*의 상태 공간을 비교한다.
- [ ] Footprint collision checking과 inflation cost를 설명한다.
- [ ] Nav2 costmap의 obstacle, voxel, inflation, custom layer 흐름을 설명한다.
- [ ] DWB, Pure Pursuit, MPPI의 후보 경로 평가 방법을 비교한다.
- [ ] Controller frequency, command latency, acceleration limit의 관계를 측정한다.
- [ ] Goal checker와 progress checker의 실패 조건을 설계한다.
- [ ] Collision Monitor의 감속·정지 영역과 한계를 검증한다.
- [ ] 동적 장애물에 대한 정지, 반응형 회피, 경로 예측 방식을 비교한다.

## P0 — 계단·비정형 지형 인지

- [ ] Ground segmentation의 ROI, normal, slope 조건을 설명한다.
- [ ] Elevation, variance, surface normal 레이어를 시각화한다.
- [ ] Slope, roughness, step height로 traversability cost를 계산한다.
- [ ] Traversability와 Nav2 costmap 값의 방향을 올바르게 변환한다.
- [ ] `FLAT / SLOPE / STAIR` 분류와 mode transition 조건을 설계한다.
- [ ] Stair entry·exit와 route graph topology를 설계한다.
- [ ] Prior map과 live elevation의 충돌 시 안전한 우선순위를 정의한다.
- [ ] RGB-D 반사, 빗물, depth hole이 elevation map에 미치는 영향을 측정한다.
- [ ] Dynamic object removal과 unknown space 처리의 실패 사례를 정리한다.

## P0 — 검증과 실험 설계

- [ ] 기능 요구사항을 측정 가능한 acceptance criterion으로 변환한다.
- [ ] 기준 commit, 설정, seed, 환경 조건을 고정한다.
- [ ] 성공률, 수행시간, 충돌 수, 최소 안전거리를 반복 측정한다.
- [ ] 평균·표준편차·P95·최악값을 함께 보고한다.
- [ ] Open-loop odometry가 독립적인 ground truth가 아닌 이유를 설명한다.
- [ ] 명령 발행, controller 수락, 실제 움직임, 독립 관측을 분리한다.
- [ ] False PASS를 방지할 independent oracle을 설계한다.
- [ ] Sensor dropout, localization jump, 통신 단절 fault injection을 수행한다.
- [ ] rosbag, CSV, 영상, RViz 캡처를 재현 가능한 evidence로 보관한다.

## P1 — ROS 2 시스템 설계

- [ ] Topic, Service, Action의 선택 기준을 설명한다.
- [ ] Reliability, durability, history, depth QoS를 상황별로 선택한다.
- [ ] Executor, callback group, multi-threading의 race condition을 설명한다.
- [ ] Lifecycle node와 component composition의 적용 기준을 정리한다.
- [ ] Interface package와 hardware abstraction 경계를 설계한다.
- [ ] 실제 장비와 Mock이 같은 계약을 사용하도록 테스트한다.
- [ ] DDS discovery, ROS Domain, NIC, Docker network 문제를 분리 진단한다.
- [ ] Diagnostic, heartbeat, watchdog과 자동 복구 정책을 설계한다.

## P1 — Behavior Tree와 로봇 안전

- [ ] Sequence, Fallback, Decorator, Stateful Action을 설명한다.
- [ ] Action cancel, halt, timeout, retry의 동작을 테스트한다.
- [ ] Navigation과 stair·inspection 같은 특수 행동의 선점 규칙을 설계한다.
- [ ] Sensor health와 localization confidence 기반 safety gate를 구현한다.
- [ ] Emergency-stop latch와 command arbitration을 설명한다.
- [ ] Fail-safe와 fail-operational의 차이를 로봇 사례로 설명한다.
- [ ] 사람 충돌, 전복, 문화재 진입, 조용한 센서 실패의 위험을 분석한다.

## P1 — Simulation·Control·RL

- [ ] URDF, USD, MJCF의 모델 표현 차이를 설명한다.
- [ ] Joint position·velocity control과 PD gain을 튜닝한다.
- [ ] Contact model, friction, solver iteration, timestep의 영향을 비교한다.
- [ ] Gazebo, MuJoCo, Isaac Sim의 물리·센서 차이를 정리한다.
- [ ] Sim-to-Sim과 Sim-to-Real 검증 gate를 정의한다.
- [ ] MDP의 state, action, transition, reward를 현재 로봇에 대응시킨다.
- [ ] PPO와 Actor–Critic의 학습 흐름을 설명한다.
- [ ] Reward shaping으로 발생한 local optimum을 진단한다.
- [ ] Curriculum과 domain randomization의 평가 기준을 설계한다.
- [ ] High-level navigation과 low-level locomotion policy의 경계를 정의한다.

## P1 — Edge·Fleet·운영

- [ ] Jetson의 CPU·GPU·메모리 사용량과 OOM 원인을 측정한다.
- [ ] CUDA inference latency와 ROS publish rate를 분리 측정한다.
- [ ] Livox, RealSense, Gremsy의 NIC·IP·RTSP·PTP 설정을 재현한다.
- [ ] Docker device, network, volume, CycloneDDS 설정을 문서화한다.
- [ ] Topological map과 metric map의 역할을 구분한다.
- [ ] Map switching 이후 relocalization과 실패 복구를 설계한다.
- [ ] MQTT task·status·result·cancel 프로토콜을 설명한다.
- [ ] 다층 이동의 stair/elevator transition을 상태 흐름으로 표현한다.

## P2 — 과거 프로젝트 복습

### JAVIS

- [ ] 중앙 제어 상태와 subsystem interface 경계를 설명한다.
- [ ] Mock 기반 통합 테스트와 실패 응답 전달을 재현한다.
- [ ] Smac Planner·MPPI 협로 설정을 동일 조건에서 비교한다.

### ROOMIE

- [ ] PnP와 Hand-Eye calibration의 좌표변환 체인을 설명한다.
- [ ] FK, IK, joint limit, singularity와 해 검증을 설명한다.
- [ ] ESP32·FreeRTOS의 serial task와 motion task를 설명한다.
- [ ] Open-loop servo 제어와 encoder·force 기반 closed-loop 제어를 비교한다.

### FALCON

- [ ] Precision, recall, mAP와 데이터셋 split을 설명한다.
- [ ] Synthetic-to-real domain gap과 negative sample 효과를 검증한다.
- [ ] ByteTrack의 ID 유지와 ID switch를 측정한다.
- [ ] Homography의 평면 가정과 픽셀–맵 RMSE를 설명한다.

## 첫 학습 순서

1. 좌표계·TF·시간 동기화
2. EKF·ESKF와 FAST-LIO2
3. Registration·Loop Closure·Factor Graph
4. Nav2 Planner·Controller·Costmap
5. Elevation·Traversability·Terrain Graph
6. 검증 방법론과 반복 실험
7. Behavior Tree·안전·예외처리
8. Simulation·Control·RL

이 페이지는 공부한 내용을 표시하기 위한 목록이 아니라, 실험과 코드 근거가 확보됐는지 추적하기 위한 체크리스트로 유지한다.
