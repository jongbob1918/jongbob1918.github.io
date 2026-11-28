---
slug: ai-worker-auto-recorder
shortName: AI Worker Auto Recorder
category: physical-ai
order: 1
collapsibleSections: true
title: "ROBOTIS AI Worker: Autonomous Data Collection Pipeline"
description: 파지 추정 모델과 규칙 기반 모션 플래닝을 결합해, ROBOTIS AI Worker가 스스로 물체를 집고 성공한 에피소드만 저장하는 자율 데이터 수집 파이프라인입니다. Isaac Lab에서 400회 시도해 성공 데모 319개를 모았고, 이 데이터로만 학습한 VLA(Vision Language Action) 정책은 40개 위치 평가에서 62.5%의 파지 성공률을 냈습니다.
period: 2026.09–11
team: 개인 프로젝트
role: ""
skills:
  - ROS 2
  - Isaac Sim
  - GraspNet
  - CenterPose
  - GR00T
  - VLA
  - AI Worker
card:
  image: assets/images/ai-worker-card-thumbnail.webp
  video: assets/videos/ai-worker-card.mp4
  imageAlt: Autonomous Data Collection Pipeline 제목 화면 뒤로, 웹 화면에서 대상 병을 클릭해 Auto Pick이 시작되고 Isaac Lab에서 AI Worker가 여러 위치의 병을 차례로 집으러 가는 8배속 수집 장면
  imageFit: cover
overview: 최근 피지컬 AI 분야에서는 VLA 모델과 모방학습을 통해 정교한 로봇 제어가 가능해졌습니다. 하지만 고품질 학습 데이터를 수동 텔레오퍼레이션으로 확보하는 데 막대한 비용과 시간이 소모됩니다. 이 병목을 해결하기 위해, 기존 로보티즈 오픈소스 기반에 파지 추정 모델과 규칙 기반 모션 플래닝을 결합해 ROBOTIS AI Worker가 스스로 물체를 파지하고 성공한 에피소드만 선별·저장하는 자율 데이터 수집 파이프라인을 추가 구축했습니다. 약 6시간 동안 800회 시도를 수행해 629개의 성공 데모(순수 녹화 2.98시간 분량, 성공률 78.6%)를 확보했습니다. 해당 데이터만으로 학습한 VLA 정책은 40개 위치에 대한 자체 시뮬레이션 평가에서 62.5%(75/120회)의 파지 성공률을 달성했습니다.
demo:
  type: video
  src: ../assets/videos/ai-worker-auto-record-hero.mp4
  poster: ../assets/images/ai-worker-auto-record-hero-poster.webp
  autoplay: true
  alt: 2배속 자동 녹화 시연. 왼쪽 웹 화면에서 Auto Pick이 동작하는 동안 오른쪽 위 Isaac Lab에서 AI Worker가 병을 집어 들고, 오른쪽 아래 RViz에 병 점군과 GraspNet 파지 후보가 표시된다
---

## Pipeline

### Data Collection

개인 프로젝트로 ROBOTIS 오픈소스 위에 후보 선택부터 녹화 저장까지 이어지는 8단계 자동 수집 파이프라인을 구현했습니다. 데이터 수집과 관리는 Cyclo Intelligence, 경로 계획과 제어는 Cyclo Control을 사용했습니다.

브라우저에서 병을 클릭하면 주변 점군으로 파지 후보를 만들고, 접근·파지·들어 올리기·녹화를 이어서 실행합니다. 병을 3.5 cm 이상 들어 0.5초간 유지하고 녹화까지 완료된 시도만 학습용 시연으로 저장합니다.

<div class="media-grid media-grid-natural"><figure class="feature-media"><img src="../assets/images/ai-worker-cyclo-intelligence.webp" alt="ROBOTIS Cyclo 소프트웨어 구성 중 데이터 수집·정제·모델 추론을 맡는 Cyclo Intelligence를 강조한 화면" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/ai-worker-cyclo-control.webp" alt="ROBOTIS Cyclo 소프트웨어 구성 중 TCP 제어·MoveJ 관절 제어·충돌 회피를 맡는 Cyclo Control을 강조한 화면" loading="lazy"></figure></div>

![대상 선택, 파지 추론, 파지 동작 생성, 실행·리코딩의 4단계와 카메라 이미지·관절 상태가 cyclo_data를 거쳐 저장되는 자동 녹화 흐름](../assets/images/ai-worker-auto-record-pipeline.webp)
#### 상세 시스템 흐름도

![웹 화면 클릭이 cyclo_intelligence의 auto_recorder_node로 전달되고, grasp_server의 GraspNet 추론 결과로 ai_worker 컨트롤러가 8단계 파지 동작을 실행하며 cyclo_data가 센서·명령을 기록하는 상세 구조](../assets/images/ai-worker-auto-record-architecture.webp)

#### 병 파지 시연 수집

<video controls autoplay muted loop playsinline preload="metadata" aria-label="8배속 연속 자동 수집. Isaac Lab 정면 시점에서 AI Worker가 테이블 위 여러 위치에 놓인 병을 차례로 집어 드는 시도를 반복한다"><source src="../assets/videos/ai-worker-auto-recorder-8x.mp4" type="video/mp4"></video>


병 위치를 5줄 × 8열 격자로 고정하고, 각 위치에서 파지 후보 생성기마다 10회씩 반복했습니다.

![Isaac Lab에서 5줄 × 8열 격자로 놓은 병 40개를 위에서 내려다본 장면. 위치를 보여주려고 한꺼번에 놓았고, 평가는 한 번에 병 1개로 진행했다](../assets/images/ai-worker-fixed40-locations.webp)

GraspNet으로 모은 수집 결과가 고르지 않다는 피드백을 받았습니다. 클릭한 병을 어떤 자세로 잡을지 후보를 만드는 단계에 CenterPose 방식을 붙여 같은 조건에서 비교했습니다.


|       | GraspNet (GSNet)    | CenterPose + 고정 파지 규칙 |
| ----- | ------------------- | --------------------- |
| 입력    | 클릭 주변 점군            | RGB 이미지 + depth       |
| 출력    | 6자유도 파지 후보 여러 개와 점수 | 병 3D 박스 → 중심 위치       |
| 파지 방향 | 모델이 후보마다 추정         | 고정 규칙 (추정 자세는 쓰지 않음)  |
| 물체 가정 | 없음                  | 서 있는 병                |
| 충돌 검사 | 점군 기준 필터            | 없음 (IK 검증만)           |
| 연산    | GPU (CUDA)          | CPU (ONNX Runtime)    |

서 있는 병 수집에는 CenterPose의 중심 위치와 고정된 파지 방향 규칙을 사용했습니다. 추정 방향의 기울어짐과 반복 파지 편차를 확인한 결과에 따른 결정입니다.

### GR00T 학습

GraspNet 시연 310개와 CenterPose 시연 319개로 GR00T N1.7 정책을 각각 학습했습니다. 언어·영상 백본은 고정하고, 연결부와 동작 생성부만 미세 조정했습니다(약 16.2억 파라미터).

첫 학습 단계에서 GPU 메모리가 부족해 고정한 백본을 16비트(BF16)로 불러오고 fused AdamW를 적용했습니다. RTX 5090(32 GB) 한 장에서 배치 크기 8, 학습률 0.0001로 정책마다 15만 스텝을 학습했습니다.

![GraspNet 시연 310개와 CenterPose 시연 319개로 학습한 GR00T N1.7의 손실 곡선. 150,000스텝까지 두 정책의 손실이 감소하며, 세로축은 로그 스케일이고 각 점은 1,000스텝 구간 평균이다](../assets/images/ai-worker-training-loss.webp)

### Inference

GR00T는 머리와 양쪽 손목의 카메라 영상, 로봇 상태, 작업 지시를 받아 여러 시점의 동작을 한 번에 예측합니다.

<div class="policy-flow" role="img" aria-label="GR00T가 30 Hz 간격으로 예측한 관절 목표값 사이를 제어 루프가 선형 보간해 Isaac Lab의 AI Worker에 100 Hz로 명령을 보낸다.">
  <div class="policy-stage"><strong>GR00T N1.7</strong><svg viewBox="0 0 176 92" aria-hidden="true"><path d="M9 12V82H169" fill="none" stroke="#bfccd8"/><circle cx="16" cy="73" r="5" fill="white" stroke="#174674" stroke-width="2"/><circle cx="64" cy="42" r="5" fill="white" stroke="#174674" stroke-width="2"/><circle cx="112" cy="56" r="5" fill="white" stroke="#174674" stroke-width="2"/><circle cx="160" cy="20" r="5" fill="white" stroke="#174674" stroke-width="2"/></svg><span>관절 목표값 · 30 Hz</span></div>
  <i aria-hidden="true"></i>
  <div class="policy-stage"><strong>제어 루프</strong><svg viewBox="0 0 176 92" aria-hidden="true"><path d="M9 12V82H169" fill="none" stroke="#bfccd8"/><path d="M16 73 L64 42 L112 56 L160 20" fill="none" stroke="#69a9df" stroke-width="2"/><circle cx="16.0" cy="73.0" r="3" fill="#2179bc"/><circle cx="30.4" cy="63.7" r="3" fill="#2179bc"/><circle cx="44.8" cy="54.4" r="3" fill="#2179bc"/><circle cx="59.2" cy="45.1" r="3" fill="#2179bc"/><circle cx="73.6" cy="44.8" r="3" fill="#2179bc"/><circle cx="88.0" cy="49.0" r="3" fill="#2179bc"/><circle cx="102.4" cy="53.2" r="3" fill="#2179bc"/><circle cx="116.8" cy="52.4" r="3" fill="#2179bc"/><circle cx="131.2" cy="41.6" r="3" fill="#2179bc"/><circle cx="145.6" cy="30.8" r="3" fill="#2179bc"/><circle cx="160.0" cy="20.0" r="3" fill="#2179bc"/><circle cx="16" cy="73" r="4" fill="white" stroke="#174674" stroke-width="2"/><circle cx="64" cy="42" r="4" fill="white" stroke="#174674" stroke-width="2"/><circle cx="112" cy="56" r="4" fill="white" stroke="#174674" stroke-width="2"/><circle cx="160" cy="20" r="4" fill="white" stroke="#174674" stroke-width="2"/></svg><span>선형 보간 · 100 Hz</span></div>
  <i aria-hidden="true"></i>
  <div class="policy-stage"><strong>AI Worker</strong><img src="../assets/images/ai-worker-inference-scene.webp" alt="" loading="lazy"><span>Isaac Lab 시뮬레이션</span></div>
</div>

## Results and Analysis

### Data Quality: GraspNet vs CenterPose

|  | GraspNet | CenterPose |
| --- | --- | --- |
| 성공 | 310/400 (77.5%) | 319/400 (79.8%) |
| X=0.295m (가장 먼 줄) | **18/80** | 9/80 |
| X=0.340m | 53/80 | **70/80** |
| X=0.385·0.430·0.475m | 239/240 | 240/240 |
| 같은 위치 반복 시 파지 위치 편차 (중앙값 / 상위 10%) | 3.5mm / 8.5mm | **0.3mm / 0.9mm** |
| 같은 위치 반복 시 파지 방향 편차 (중앙값 / 상위 10%) | 2.6° / 8.9° | **0.0° / 0.0°** |
| 최대 들기 높이 중앙값 | 5.3cm | 5.4cm |
| 시도당 소요 시간 중앙값 | 28.6초 | 27.6초 |

편차는 성공한 시도의 Grasp 목표 자세를 위치별로 모아, 위치 표준편차와 평균 방향으로부터의 각도 차이로 계산했습니다(2회 이상 성공한 위치만: GraspNet 34곳, CenterPose 32곳).

![40개 위치별 성공 횟수를 5줄 × 8열 격자로 나타낸 두 개의 히트맵. GraspNet 310/400은 가장 먼 줄 X=0.295m에서 양 끝 위치만 6·3·9회 성공하고 X=0.340m 줄 가운데가 0~6회다. CenterPose 319/400은 가장 먼 줄에서 한 위치만 9회 성공하고 X=0.340m 줄은 한 위치를 빼고 모두 10회다. X=0.385m 이후 줄은 두 방식 모두 거의 10회다](../assets/images/ai-worker-grasp-success-grid.webp)

실패 171건 중 169건은 목표 자세에 맞는 팔 관절 각도를 구하는 역기구학(Inverse Kinematics, IK) 단계에서 후보가 모두 탈락한 경우였고, 가장 먼 줄(X=0.295m)에 몰렸습니다(성공 27/160). X=0.430·0.475m 줄은 모두 성공했습니다. 관절 한계 때문인지 충돌 때문인지는 분리하지 못했습니다.

<details class="validation-appendix">
<summary>CenterPose 상세 검증</summary>

**1. 자세가 기울어 나오고, 멀수록 더 기울어짐.** 위 실험 400회에서 서 있는 병의 추정 높이축이 수직에서 벗어난 각도를 줄별로 계산했습니다.

| 줄 | 카메라까지 거리 | 내려다보는 각도 | 기울기 중앙값 (상위 10%) | 수평 중심 오차 중앙값 | 수집 성공 |
| --- | --- | --- | --- | --- | --- |
| X=0.295m | 0.78m | 44° | 25.7° (35.4°) | 17mm | 9/80 |
| X=0.340m | 0.74m | 46° | 24.4° (33.3°) | 19mm | 70/80 |
| X=0.385m | 0.71m | 48° | 19.9° (31.9°) | 11mm | 80/80 |
| X=0.430m | 0.69m | 51° | 17.7° (24.0°) | 10mm | 80/80 |
| X=0.475m | 0.66m | 54° | 13.6° (20.9°) | 10mm | 80/80 |

![줄별 CenterPose 추정 병 축 기울기 분포. 카메라에서 가까운 X=0.475m 줄 중앙값 13.6°에서 가장 먼 X=0.295m 줄 25.7°까지 멀어질수록 커진다. 실제 병 기울기는 0°다](../assets/images/ai-worker-centerpose-tilt.webp)

![머리 카메라 영상 위에 CenterPose 추정 3D 박스를 겹친 두 장면. 가까운 줄(카메라 0.66m)은 추정 기울기 14.8°, 가장 먼 줄(0.78m)은 26.7°다. 흰 선은 시뮬레이션 정답으로 투영한 실제 수직축이고, 노란 추정 높이 방향이 이 선에서 벗어나 있다](../assets/images/ai-worker-centerpose-near-far.webp)

카메라에서 멀수록 기울기와 중심 오차가 커졌습니다. 다만 멀수록 카메라가 덜 내려다보게 되므로, 거리 때문인지 보는 각도 때문인지는 나누지 못했습니다. 표식 9개를 6프레임에서 투영해 렌더링 영상과의 평균 차이가 0.66 px임을 확인했습니다. 최종 파지 자세는 CenterPose가 추정한 중심 위치와 서 있는 병 전용 방향 규칙으로 정했습니다.

**2. 물체 종류마다 모델이 따로 필요하고, 점수로 종류를 가리지 못함.** CenterPose는 병·시리얼 상자처럼 범주별로 모델이 나뉩니다. 쇼룸 에셋 11종 × 회전 3개로 시험했을 때(추가 학습 없음, 임계값 0.3) 병 모델은 플라스틱 병뿐 아니라 커피캔 5종(15/15장)과 과자 봉지(땅콩 3/3, 군밤 2/3)에도 병으로 반응했습니다.

**3. 화면에서 작게 보이면 검출하지 못함.** 같은 시험에서 카메라 전체 화면(672×376)을 넣으면 병 9장 중 0장, 병 주변을 잘라 넣으면 9장 모두 검출했습니다. 수집 실험은 1280×720에서 병이 약 160~180px 높이로 보여 검출됐습니다.

![CenterPose 병 모델 검출 결과. 각 줄 왼쪽은 머리 카메라 전체 화면이고 오른쪽 세 칸은 물체 주변을 확대한 0°·90°·180° 입력이다. 녹차병, 커피캔 TOP 더 블랙, 땅콩 믹스 봉지 모두 확대 입력에서 bottle 점수 0.4~0.93으로 3D 박스가 그려지고, 젤리 봉지는 90°에서만 검출된다](../assets/images/ai-worker-centerpose-categories.webp)

![카메라 투영 검증. 렌더 화면의 표식 9개 중심과 CameraInfo로 투영한 위치가 0.52~0.90px 차이로 겹친다](../assets/images/ai-worker-centerpose-camera-check.webp)

</details>

### Sim-to-Sim VLA Baseline

각 데이터로 별도로 학습한 정책을 같은 40개 위치에서 위치당 3회 평가했습니다. 시도당 제한 시간은 30초이며 성공 기준은 수집과 같습니다.

| 정책 학습 데이터 | 전체 | X=0.295 | X=0.340 | X=0.385 | X=0.430 | X=0.475 |
| --- | --- | --- | --- | --- | --- | --- |
| GraspNet 시연 310개 | 75/120 | 5/24 | 11/24 | 19/24 | 22/24 | 18/24 |
| CenterPose 시연 319개 | 75/120 | 1/24 | 14/24 | 20/24 | 22/24 | 18/24 |

CenterPose 방식은 같은 위치에서 파지 자세 편차가 작았습니다. 두 정책의 전체 파지 성공 횟수는 같았고, 위치별 결과에는 차이가 있었습니다. 위치당 평가 횟수는 3회였습니다. 서 있는 병의 시연 수집에는 CenterPose 방식을 사용했습니다. GraspNet의 다른 형상 파지 성능은 추가 검증이 필요합니다.

팔 떨림이 일부 시도에 영향을 줬습니다. 정책 실패를 떨림, 도달 범위, 충돌 등 원인별로 분류하지 못해, 떨림이 성공률에 미친 영향은 아직 수치로 분리하지 못했습니다.

### Action Chunking & Jitter Reduction

Phase 2에서 청크 경계의 명령 변화와 팔 떨림을 측정하고, 청크 블렌딩·스무딩 적용 전후를 같은 평가 조건으로 비교할 계획입니다.

### Sim-to-Real Transfer

Phase 3에서 실물 AI Worker로 정책을 옮기고, 센서·좌표계·제어 주기 차이가 파지에 미치는 영향을 검증할 계획입니다.

## Next Steps

로봇 팔 떨림이 일부 시험에 영향을 줬습니다. 가장 먼 줄에 집중된 역기구학 탈락은 관절 한계와 충돌 중 어느 쪽이 원인인지 구분하지 못했습니다.

학습에 사용하지 않은 위치, 누운 병과 다른 형상, 실물 로봇은 추가 검증이 필요합니다.

다음 실험에서는 역기구학 탈락을 관절 한계와 충돌로 구분하고, 미학습 위치·다른 형상으로 평가를 확장합니다. 청크 블렌딩과 스무딩으로 떨림을 줄인 뒤 실물 AI Worker에서 전이를 검증할 계획입니다.

## Code

자동 수집 파이프라인의 기반으로 사용한 ROBOTIS 소프트웨어입니다.

[GitHub · Cyclo Intelligence](https://github.com/ROBOTIS-GIT/cyclo_intelligence)
