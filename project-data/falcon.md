---
slug: falcon
shortName: FALCON
group: side
order: 3
title: FALCON — 활주로 위험요소 관제
description: FALCON 활주로 위험요소 탐지, 추적, 좌표변환 프로젝트
team: 4명
period: 2025.05.26–07.03
skills:
  - PyTorch
  - YOLO
  - ByteTrack
  - OpenCV
  - Homography
repository: https://github.com/jongbob1918/FALCON
card:
  image: assets/images/hawkeye_mainpage.gif
  imageAlt: FALCON runway hazard detection interface
  titleEn: FALCON — Runway Safety Monitoring System
  keywords:
    - PyTorch
    - YOLOv8
    - ByteTrack
    - Object Tracking
  descriptionKo: 활주로 위험요소 탐지 모델을 커스텀 학습해 정확도 90% 이상을 검증했습니다. ByteTrack 기반 이동 경로 추적과 위험 판단 로직을 통합했습니다.
  descriptionEn: Trained a six-class runway hazard detector and integrated detection, tracking, and map-coordinate conversion. The repository reports mAP@0.5:0.95 of 0.9005.
overview: >-
  6종 지상 위험요소를 탐지하고 객체 ID와 이동 경로를 유지한 뒤,
  영상 좌표를 실제 맵 좌표로 변환해 관제 화면에 전달했습니다.
demo:
  type: image
  src: ../assets/images/hawkeye_mainpage.gif
  alt: FALCON 위험요소 탐지 및 관제 화면
---

## CCTV 영상에서 지도 표시까지

파란 테두리는 직접 담당한 범위, 회색은 팀 통합 범위입니다.

<div class="diagram" role="img" aria-label="FALCON 지상 위험요소 처리 파이프라인"><div class="diagram-node">CCTV Frame</div><div class="diagram-arrow">→</div><div class="diagram-node owner">YOLO<br>6 Classes</div><div class="diagram-arrow">→</div><div class="diagram-node owner">ByteTrack<br>ID &amp; Trajectory</div><div class="diagram-arrow">→</div><div class="diagram-node owner">ArUco Test<br>Pixel → Map</div><div class="diagram-arrow">→</div><div class="diagram-node">Server · Dashboard</div></div>

## 학습 데이터와 좌표변환

### 실제 이미지와 합성 데이터 결합

공항 모형 촬영 이미지와 팀이 생성한 Unity 기반 합성 이미지로 재학습했습니다. Ground Model v0.3은 mAP@0.5 0.9902를 기록합니다.

### ArUco 기준점 기반 평면 좌표변환

대응점으로 Homography를 계산하고 픽셀 좌표를 맵 좌표로 변환했습니다.

<div class="formula-block">λ [x_map, y_map, 1]ᵀ = H [u_pixel, v_pixel, 1]ᵀ</div>

## 탐지·추적 시스템 구성

<div class="role-grid"><div class="info-card"><strong>Ground IDS</strong><span>조류·FOD·사람·동물·항공기·차량 탐지</span></div><div class="info-card"><strong>Model Evaluation</strong><span>커스텀 학습과 지상 객체 성능 확인</span></div><div class="info-card"><strong>Coordinate Test</strong><span>ArUco 기반 픽셀–맵 좌표변환 시험</span></div></div>

## CCTV 기반 관제 환경

고정 CCTV 시점의 프레임을 기준으로 탐지·추적하고 결과를 서버와 관제 화면으로 전달합니다. 공개 자료에서 확인되지 않는 카메라 모델, 렌즈, 추론 장치와 실제 공항 설치 사양은 성능 근거에 포함하지 않습니다.

## 실제 영상에서 발생한 탐지 성능 저하

<dl class="flow"><dt>증상</dt><dd>공개 데이터 모델이 공항 모형·CCTV 시점에서 객체를 누락하거나 ArUco Marker를 오인했습니다.</dd><dt>원인</dt><dd>학습 데이터와 배치 환경의 조명·시점·배경 차이가 컸습니다.</dd><dt>해결</dt><dd>실사와 합성 데이터를 결합하고 Negative Sample을 포함해 재학습했습니다.</dd><dt>검증</dt><dd>PR Curve, Confusion Matrix와 Ground Model v0.3 평가 지표를 저장했습니다.</dd></dl>

## 성능 및 검증 결과

<div class="metric-grid"><div class="metric-card"><span class="metric-value">0.9902</span><span class="metric-label">mAP@0.5</span></div><div class="metric-card"><span class="metric-value">0.9005</span><span class="metric-label">mAP@0.5:0.95</span></div><div class="metric-card"><span class="metric-value">0.9672</span><span class="metric-label">Recall</span></div></div>

<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">ARTIFACT</span><strong>학습 결과</strong><p>PR/F1 Curve, Confusion Matrix와 results.csv가 저장되어 있습니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>IDS 실행 코드</strong><p>Detector·Tracker·Inference 코드가 공개되어 있습니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>관제 통합</strong><p>지도 Marker와 관제 UI 연동을 확인할 수 있습니다.</p></div></div>

## 관련 코드

[Ground IDS 구현 보기 ↗](https://github.com/jongbob1918/FALCON/tree/main/src/systems/ids)

학습·평가 Script와 결과 Artifact가 공개되어 있습니다.
