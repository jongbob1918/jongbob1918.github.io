---
slug: lk-biped
category: lk
order: 3
detail: true
title: 실내 다층 건물 자율주행 시스템 설계
description: 바퀴형 이족 로봇의 실내 다층 자율주행 시스템을 설계했습니다. 짐벌 스캔 시스템과 고도 지도, 층간 내비게이션을 중심으로 구성했습니다.
skills:
  - ROS 2
  - Elevation Mapping
  - Multi-floor Navigation
  - Gimbal Scan System
card:
  image: assets/images/lk-robotics-emblem.svg
  imageAlt: LK ROBOTICS 로고
  imageFit: contain
overview: >-
  바퀴형 이족 로봇이 실내 여러 층을 이동하기 위한 자율주행 시스템을 설계했습니다.
  센서의 방향을 바꾸며 주변을 측정하는 짐벌 스캔 시스템과 지면의 높이를 표현하는 고도 지도를 설계 범위에 포함했습니다.
  ROS 2를 기반으로 층간 이동을 위한 내비게이션 시스템을 구성했습니다.
---

## 짐벌 스캔과 고도 지도

센서의 방향을 조절하며 주변을 측정하는 짐벌 스캔 시스템(Gimbal Scan System)과, 주변 지형의 높이를 지도에 표현하는 Elevation Mapping을 설계에 포함했습니다. 바퀴형 이족 로봇이 이동할 공간의 높이 변화를 다루기 위한 구성입니다.

## 여러 층을 연결하는 자율주행

로봇 소프트웨어 프레임워크인 ROS(Robot Operating System) 2를 기반으로, 여러 층 사이의 이동을 다루는 Multi-floor Navigation 시스템을 설계했습니다. 짐벌 스캔과 고도 지도, 층간 내비게이션을 중심으로 실내 다층 건물의 자율주행 시스템을 구성했습니다.
