---
slug: falcon
shortName: FALCON
category: addinedu
order: 3
title: FALCON — 활주로 운항안전서비스
description: 지상 위험요소 탐지와 조류 충돌 위험 분석, 음성 안내로 관제사와 조종사를 지원하는 AI 운항안전서비스
team: 4명
period: 2025.05.26–07.03
context: ADDINEDU · ROS2와 인공지능을 활용한 자율주행 로봇 개발자 양성과정 9기
skills:
  - PyTorch
  - YOLOv8
  - ByteTrack
  - OpenCV
  - Homography
  - TCP
repository: https://github.com/jongbob1918/FALCON
role: 프로젝트 총괄·지상 객체 탐지 시스템 구축·카메라 영상과 실제 구역 위치 정합
card:
  image: assets/images/hawkeye_mainpage.gif
  imageAlt: FALCON runway hazard detection interface
  skills:
    - YOLOv8
    - ByteTrack
    - Homography
    - OpenCV
overview: >-
  공군 부사관으로 근무하며 활주로의 새와 동물, 나사와 쓰레기 같은 이물질이 항공기 운항에 치명적인 위험이 될 수 있음을 경험했습니다. 인력 중심의 활주로 안전관리에서 발생하는 인력 부족과 비용 부담을 줄이고자 AI로 위험요소 감시를 자동화하는 프로젝트를 시작했습니다. FALCON은 지상 위험요소 탐지와 조류 충돌 위험 분석, 음성 안내로 관제사와 조종사의 안전한 항공기 운항을 지원하는 AI 서비스입니다. CCTV에서 감지한 위험정보를 관제 화면과 조종사 음성 경보로 전달합니다. 저는 프로젝트 총괄과 지상 객체 탐지 시스템 구축, 카메라 영상과 실제 구역 위치 정합을 담당했습니다.
demo:
  type: youtube
  src: https://www.youtube.com/embed/lctXpBYrVsU
  title: FALCON 지상 위험요소 관제 데모
---

## 위험 감지부터 관제·조종사 안내까지

관제사 서비스(Hawkeye)는 지상 위험요소의 위치와 경보를 화면에 표시합니다. 조종사 서비스(RedWing)는 운항 위험을 음성으로 알리고, 위험도 질의에 대한 응답과 지상 유도사의 수신호 안내를 제공합니다. 지상 탐지와 조류 충돌 위험 분석 결과는 서버를 거쳐 각 서비스로 전달됩니다.

<figure class="feature-media"><img src="../assets/images/falcon_software_architecture.png" alt="CCTV 탐지 서버, FALCON Main Server, 관제 GUI와 조종사 시스템을 연결한 전체 소프트웨어 구조" loading="lazy"></figure>

이 중 제가 맡은 지상 탐지 시스템은 위험요소의 위치를 관제 지도에 표시해, 관제사가 어느 구역에서 위험이 발생했는지 확인하도록 합니다.

<figure class="feature-media"><img src="../assets/images/falcon_detection_sequence.png" alt="CCTV 영상 수신부터 위험요소 탐지, 구역 판단과 관제 GUI 지도 표시까지 이어지는 FALCON 흐름" loading="lazy"></figure>

## 지상 위험요소 탐지 시스템 구축

4명으로 구성된 팀의 팀장으로 일정과 문서를 관리하고, 지상 객체 탐지 시스템 구축과 모델 기술조사·학습을 담당했습니다. 합성 데이터 생성과 지상 탐지 모델 제작은 팀원과 협업했습니다.

공개 데이터로 학습한 초기 모델은 공항 모형 영상에서 작은 객체를 놓치거나 배경의 ArUco 마커를 위험요소로 오인했습니다. 고정 카메라의 시점과 모형 배경에 맞는 학습 데이터가 필요했습니다.

팀이 Unity와 Blender로 만든 합성 이미지에 실제 모형 촬영 이미지와 객체가 없는 배경 이미지(Negative Sample)를 결합했습니다. YOLOv8n-box를 960×960 입력, 150 epoch, 배치 크기 8로 재학습해 조류·이물질·사람·동물·항공기·차량 6개 클래스를 탐지했습니다.

<figure class="feature-media"><img src="../assets/images/falcon_synthetic_dataset.gif" alt="Blender와 공항 모형을 활용해 지상 위험요소 학습 데이터를 구성하는 과정" loading="lazy"></figure>

## 탐지한 객체를 추적하고 실제 구역에 표시

매 프레임에서 같은 객체를 이어서 추적하도록 탐지 결과를 ByteTrack에 연결했습니다. 탐지 후에는 형광 조끼와 차량 색상을 분석해 작업자와 일반인, 작업 차량과 일반 차량을 구분했습니다.

카메라 영상의 위치를 관제 지도에 표시하려면 픽셀 좌표와 실제 구역의 좌표를 대응시켜야 합니다. 저는 ArUco 마커를 이용한 좌표변환 기술조사와 테스트를 맡았고, 변환 로직은 백엔드 담당 팀원이 설계했습니다.

네 기준 마커의 영상 좌표와 실측 좌표를 대응시켜 평면 좌표변환 행렬(Homography)을 구합니다. 이 행렬과 OpenCV의 `perspectiveTransform`으로 탐지 영역 중심을 모형 지도 좌표로 변환하고, 활주로·유도로·잔디 구역 중 어디에 있는지 판단합니다.

<figure class="feature-media"><img src="../assets/images/falcon_aruco_mapping.png" alt="활주로 모형의 ArUco Marker 실측 좌표와 OpenCV로 추출한 픽셀 좌표의 대응 관계" loading="lazy"></figure>

객체 식별번호·종류·좌표·신뢰도는 관제 서버로 전달됩니다. 서버와 관제 화면은 각 담당 팀원이 구현했으며, 탐지 결과를 받아 지도 마커와 팝업 경보를 갱신합니다.

## 모델 평가와 모형 환경 시연

프로젝트 README에 기록한 Ground Model v0.3의 평가 결과입니다. 합성 이미지와 실제 공항 모형 촬영 이미지를 결합한 데이터셋을 사용했으며, 학습·검증·테스트 분할 비율은 각각 약 69.4%·20.9%·9.8%입니다. 아래 수치가 검증·테스트 중 어느 분할에서 산출됐는지는 README에 명시돼 있지 않습니다.

<div class="metric-grid"><div class="metric-card"><span class="metric-value">0.9902</span><span class="metric-label">mAP@0.5</span></div><div class="metric-card"><span class="metric-value">0.9005</span><span class="metric-label">mAP@0.5:0.95</span></div><div class="metric-card"><span class="metric-value">0.9928 / 0.9672</span><span class="metric-label">Precision / Recall</span></div></div>

아래는 공개 데이터로 학습한 초기 모델과 혼합 데이터로 재학습한 모델의 정밀도·재현율 곡선(PR Curve)입니다. 두 모델의 평가 조건이 동일한지 확인되지 않아 개선율을 계산하는 근거로 삼지는 않았습니다.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/falcon_baseline_pr_curve.png" alt="공개 데이터로 학습한 기존 FALCON Segmentation 모델의 클래스별 PR Curve" loading="lazy"><figcaption>Before · Public Dataset Segmentation Model</figcaption></figure><figure class="feature-media"><img src="../assets/images/falcon_hybrid_pr_curve.png" alt="실사와 합성 데이터를 결합한 FALCON Hybrid Detection 모델의 클래스별 PR Curve" loading="lazy"><figcaption>After · Hybrid Dataset YOLOv8n-box</figcaption></figure></div>

모형 촬영 영상에서는 여러 종류의 객체 탐지와 형광 조끼를 이용한 작업자 구분을 확인했습니다. 이어지는 영상은 지상 위험요소 탐지 시연입니다.

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/falcon_ground_detection.webp" alt="FALCON이 공항 모형에서 여섯 종류의 지상 위험요소를 탐지하는 화면" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/falcon_worker_classification.gif" alt="형광 조끼 색상을 이용해 작업자와 일반인을 구분하는 FALCON 후처리" loading="lazy"></figure></div>

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/-si0u8I1h2A?list=PLCGG9KRfKwMmQqXvp43pChNMyyLSyjHp9&amp;index=4" title="FALCON 지상 위험요소 탐지 시연 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>

## 한계와 개선 방향

**모형과 실제 공항의 차이:** 여기서 제시한 결과는 합성 데이터와 공항 모형 촬영 환경에서 얻었습니다. 실제 공항에 적용하려면 카메라 거리·조명·날씨가 달라지는 조건에서 탐지 성능을 추가로 평가해야 합니다.

**좌표 정합의 검증 범위:** 좌표변환 기술조사와 테스트를 수행했지만, 위치 오차를 측정한 조건과 결과는 이 페이지에 제시하지 않았습니다. 후속 검증에서는 알려진 기준 위치와 변환 결과를 비교해 위치별 오차와 구역 경계에서의 판정 정확도를 확인해야 합니다.

**운영 성능 평가:** 모델의 탐지 지표만으로 관제 업무의 효과를 판단하기는 어렵습니다. 영상 입력부터 경보 표시까지의 지연, 오경보 빈도, 위험요소 누락을 함께 측정하는 것이 다음 과제입니다.
