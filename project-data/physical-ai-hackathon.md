---
slug: physical-ai-hackathon
shortName: PHYSICAL AI
group: side
order: 4
title: PHYSICAL AI — 양팔 모방학습 조작
description: LeRobot과 ACT를 이용한 SO-101 양팔 공 전달·분류 프로젝트
team: 4명
period: 2026.02
skills:
  - LeRobot
  - ACT
  - Imitation Learning
  - Bimanual Manipulation
  - SO-101
repository: https://github.com/TheMomentLab/physical_ai_hackathon
card:
  image: https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif
  imageAlt: Two SO-101 robot arms manipulating colored balls during the Physical AI Hackathon
  titleEn: PHYSICAL AI — Bimanual Imitation Learning
  keywords:
    - LeRobot
    - ACT
    - Imitation Learning
    - Bimanual Manipulation
    - SO-101
  descriptionKo: 3개 카메라와 12차원 양팔 상태를 입력으로 하는 ACT 정책을 50,000 step 학습했습니다. 두 SO-101 로봇팔의 공 집기·팔 간 전달·색상별 분류 미션과 실제 공 조작을 시연했습니다.
  descriptionEn: Trained a bimanual ACT policy for 50,000 steps using three camera views and a 12-dimensional robot state. Demonstrated colored-ball manipulation with two SO-101 arms for a grasp, handover, and sorting mission.
overview: >-
  제1회 Physical AI 해커톤의 과제는 한쪽 팔로 공을 집고 반대쪽 그리퍼로 전달한 뒤 색상별 수납함에 분류하는 양팔 조작이었습니다.
  4인 팀에서 LeRobot 기반 텔레오퍼레이션 데이터 수집부터 ACT 정책 학습과 실제 로봇 추론까지 연결했습니다.
  공개 체크포인트는 3개 카메라 영상과 12차원 로봇 상태를 입력받아 두 SO-101 팔의 12차원 행동을 100-step chunk로 출력합니다.
demo:
  type: image
  src: https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif
  alt: Physical AI Hackathon dual-arm colored-ball manipulation demo
---

## 공 집기에서 색상 분류까지

대회 미션은 공을 한쪽 팔로 집은 뒤 반대쪽 그리퍼로 전달하고, 전달받은 팔이 색상에 맞는 수납함으로 옮기는 순서로 구성됩니다.

<div class="diagram" role="img" aria-label="Physical AI 양팔 조작 파이프라인"><div class="diagram-node">3 Camera Views<br>640 × 480</div><div class="diagram-arrow">→</div><div class="diagram-node owner">ACT Policy<br>Visual · State</div><div class="diagram-arrow">→</div><div class="diagram-node owner">100-step<br>Action Chunk</div><div class="diagram-arrow">→</div><div class="diagram-node">Dual SO-101<br>12-DoF Action</div><div class="diagram-arrow">→</div><div class="diagram-node">Grasp · Handover<br>Color Sorting</div></div>

## 텔레오퍼레이션 데이터와 ACT 정책

### 양팔 시연 데이터 구성

LeRobot의 `bi_so_leader`와 `bi_so_follower` 구성을 사용해 좌·우 팔을 텔레오퍼레이션하고, 상단과 전방 카메라 영상 및 관절 상태를 행동 명령과 함께 기록하는 파이프라인을 구성했습니다.

### 3개 시점에서 12차원 행동 예측

공개된 최종 정책은 `left_top`, `left_front`, `right_front`의 3개 RGB 영상과 12차원 로봇 상태를 입력으로 사용합니다. ResNet-18 시각 백본과 ACT Transformer가 두 팔의 12차원 행동을 100-step chunk로 예측합니다.

<div class="metric-grid"><div class="metric-card"><span class="metric-value">3</span><span class="metric-label">640 × 480 Camera Views</span></div><div class="metric-card"><span class="metric-value">12 → 12</span><span class="metric-label">State · Action Dimensions</span></div><div class="metric-card"><span class="metric-value">50K</span><span class="metric-label">Training Steps</span></div></div>

## 양팔 조작 시스템

<div class="role-grid"><div class="info-card"><strong>Dual SO-101</strong><span>좌·우 팔로 공 집기, 그리퍼 간 전달과 분류 동작 수행</span></div><div class="info-card"><strong>LeRobot Dataset</strong><span>카메라 관측, 관절 상태와 텔레오퍼레이션 행동을 에피소드로 기록</span></div><div class="info-card"><strong>ACT Inference</strong><span>시각·상태 입력을 정규화하고 연속 행동 chunk를 실제 팔 명령으로 변환</span></div></div>

## 카메라와 USB 장치 매핑

<dl class="flow"><dt>증상</dt><dd>카메라 연결 순서가 바뀌거나 첫 프레임 읽기가 실패하면 학습과 추론의 관측 키가 달라질 수 있습니다.</dd><dt>원인</dt><dd>동적으로 할당되는 video·serial 장치 경로와 카메라 포맷 설정이 실행 환경마다 달라졌습니다.</dd><dt>해결</dt><dd>udev 규칙으로 팔과 카메라에 고정 심볼릭 링크를 부여하고 OpenCV 입력을 640×480, 30 FPS, MJPG로 통일했습니다.</dd><dt>검증</dt><dd>장치 매핑 문서와 텔레오퍼레이션 노트북에서 동일한 카메라 이름과 로봇 ID를 사용하도록 구성했습니다.</dd></dl>

## 공개 결과와 검증 범위

<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">MODEL</span><strong>ACT 최종 체크포인트</strong><p>50,000-step 학습 설정과 모델 가중치, 전처리·후처리 설정이 Hugging Face에 공개되어 있습니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>실제 공 조작</strong><p>두 SO-101 팔과 색상 공을 사용한 실제 조작 장면을 저장소 GIF에서 확인할 수 있습니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">SCOPE</span><strong>4인 팀 프로젝트</strong><p>공개 README에는 김종명을 포함한 4명의 팀원이 명시되어 있으며 세부 개인 담당 범위는 별도로 공개되어 있지 않습니다.</p></div></div>

## 관련 코드와 모델

[프로젝트 저장소 보기 ↗](https://github.com/TheMomentLab/physical_ai_hackathon)

[ACT 최종 모델 보기 ↗](https://huggingface.co/Moment-Lab/act_hackathon_roboseasy_final)
