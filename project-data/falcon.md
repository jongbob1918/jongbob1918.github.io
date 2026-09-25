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
  - Object Detection
  - Object Tracking
  - OpenCV
  - Homography
  - Python
repository: https://github.com/jongbob1918/FALCON
role: 프로젝트 총괄·지상 객체 탐지 시스템 구축·카메라 영상과 실제 구역 위치 정합
card:
  image: assets/images/hawkeye_mainpage.gif
  imageAlt: FALCON runway hazard detection interface
overview: >-
  공군 부사관으로 근무하며 활주로의 새와 동물, 나사 같은 이물질이 항공기 운항에 위험이 되는 상황을 경험했습니다. 인력 중심의 감시를 보조하기 위해 지상 위험요소 탐지, 조류 충돌 위험 분석, 음성 안내를 통합한 운항안전서비스 FALCON을 개발했습니다. 카메라에서 위험요소를 감지하면 위치와 종류를 관제 화면에 표시하고 조종사에게 음성 경보로 전달합니다.
demo:
  type: youtube
  src: https://www.youtube.com/embed/lctXpBYrVsU
  title: FALCON 지상 위험요소 관제 데모
---

## 위험요소 감지부터 경보까지의 서비스 흐름

카메라 영상에서 위험요소를 감지하면 종류와 위치를 분석해 관제 지도에 표시합니다. 관제사는 지도 마커와 팝업으로 위험요소를 확인하고, 조종사는 음성 경보로 위험정보를 전달받습니다.

<figure class="feature-media"><img src="../assets/images/falcon_detection_sequence.png" alt="카메라 입력에서 객체 탐지·추적·좌표변환을 거쳐 관제 지도와 경보를 갱신하는 처리 순서" loading="lazy"></figure>

## 시스템 설계

지상·조류 탐지 서버, 관제 PC, 조종사 PC를 메인 서버로 연결했습니다. 각 탐지 서버는 카메라 영상을 분석하고, 메인 서버는 탐지 결과와 위험정보를 관리해 관제 화면(Hawkeye)과 조종사 서비스(RedWing)로 전달합니다.

<figure class="feature-media"><img src="../assets/images/falcon_software_architecture.png" alt="지상·조류 탐지 서버가 메인 서버를 통해 관제 화면과 조종사 서비스로 정보를 전달하는 구조" loading="lazy"></figure>

## 초기 위험요소 객체탐지 모델 학습

지상 탐지 대상은 조류, 이물질, 야생동물, 사람, 차량, 항공기 6종으로 정했습니다. 처음에는 공개 이미지 약 15,000장으로 모델을 학습했지만, 공항 모형을 촬영한 영상에서는 작은 객체를 잘 찾지 못했습니다.

실제 공항 사진과 모형의 크기·형태·배경 차이를 줄이기 위해 학습 데이터를 다시 구성했습니다.

## 합성·실제 데이터를 결합한 모델 개선

팀에서 Polycam과 Blender로 모형을 가상 환경에 재현했습니다. 합성 데이터 담당 팀원은 Unity로 촬영 각도·조명을 바꾸며 이미지와 객체 위치 라벨을 자동 생성했습니다.

<figure class="feature-media"><img src="../assets/images/falcon_synthetic_pipeline.webp" alt="발표자료 60쪽: Unity에서 촬영 각도와 조명을 바꾸고 객체 위치 라벨을 자동 생성하는 과정" loading="lazy"></figure>

합성 이미지 3,000장과 실제 촬영 이미지 1,000장을 섞어 경량 객체 탐지 모델 YOLOv8n을 학습했습니다.

## 학습 데이터별 탐지 성능

<figure class="feature-media"><img src="../assets/images/falcon_dataset_evaluation.webp" alt="발표자료 62쪽: 테스트 데이터로 평가한 공개·합성·실제·혼합 데이터 모델의 클래스별 정밀도·재현율 곡선" loading="lazy"></figure>

테스트에서 가장 좋은 결과를 보인 합성·실제 혼합 데이터 모델을 지상 탐지에 사용했습니다.

## 구역별 출입등급에 따른 위험 알림

활주로에서 감지한 사람과 차량을 모두 위험으로 처리하면, 정상적인 작업에도 알림이 발생해 서비스의 신뢰도가 떨어진다고 판단했습니다. 이륙을 앞둔 활주로에는 사람과 차량이 진입하면 안 되지만, 정비 중인 구역에는 작업자와 작업 차량이 들어가야 합니다.

그래서 공항을 8개 구역으로 나누고, 관리자가 구역별 출입등급을 설정하도록 했습니다. 감지한 객체의 종류와 해당 구역의 등급을 비교해 출입 조건을 위반한 경우 알림을 보냅니다.

<figure class="feature-media"><img src="../assets/images/falcon_zone_access_settings.webp" alt="발표자료 39쪽: 공항의 8개 구역과 전체 허용·작업자 및 작업차량만 허용·전체 금지의 3단계 출입등급 설정 화면" loading="lazy"></figure>

아래는 유도로 A를 출입 금지로 설정한 뒤 차량의 출입 위반을 알리는 화면입니다.

<figure class="feature-media"><img src="../assets/images/falcon_zone_access_alert.webp" alt="발표자료 40쪽: 유도로 A의 출입등급을 3으로 설정한 뒤 일반 차량과 작업 차량을 표시하고 출입 위반 알림을 생성한 화면" loading="lazy"></figure>

## 카메라 영상에서 객체의 구역 판별

출입등급을 적용하려면 감지한 객체가 어느 구역에 있는지 알아야 했습니다. 영상에서 기준점을 식별할 수 있는 사각 마커(ArUco)를 사용해 카메라 좌표와 지도 좌표를 연결했습니다.

마커 중심의 실제 위치를 측정하고 영상에서 같은 마커의 픽셀 위치를 찾았습니다. 두 좌표의 대응 관계로 평면 좌표변환 행렬(Homography)을 구해 객체의 중심점을 지도 좌표로 옮기고, 활주로·유도로·잔디 중 어느 구역에 있는지 판단했습니다. 저는 좌표변환 조사·테스트를 맡았고, 백엔드 팀원이 변환 로직을 설계했습니다.

<figure class="feature-media"><img src="../assets/images/falcon_aruco_mapping.png" alt="공항 모형에서 측정한 ArUco 마커 위치와 카메라 영상에서 추출한 픽셀 위치의 대응 관계" loading="lazy"></figure>

추적 알고리즘 ByteTrack으로 움직이는 객체를 계속 추적하고, 형광 조끼와 차량 색상으로 작업자·작업 차량을 구분했습니다. 객체의 종류와 위치를 출입등급과 함께 판단해 관제 지도와 알림에 반영했습니다.

## 모형 환경에서 통합 시연

공항 모형에 배치한 객체를 탐지하고, 형광 조끼를 입은 작업자를 구분하는 동작을 확인했습니다. 탐지한 위치를 관제 화면에 표시하고 조종사 음성 경보로 전달하는 흐름까지 연결했습니다.

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/falcon_ground_detection.webp" alt="공항 모형의 조류·이물질·사람·동물·항공기·차량을 탐지한 화면" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/falcon_worker_classification.gif" alt="형광 조끼 색상을 분석해 작업자를 구분하는 시연" loading="lazy"></figure></div>

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/-si0u8I1h2A" title="FALCON 위험정보를 조종사 음성 경보로 전달하는 통합 시연" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>
