---
slug: lk-ros
category: lk
order: 2
detail: true
title: 로봇 시스템 ROS 1 → ROS 2 전환
description: 지도 생성·위치추정·주행 기능의 ROS 2 전환을 담당하고, 장시간 실행 중 발생하는 위치 정보 지연 문제를 분석·개선했습니다.
role: 로봇 소프트웨어 이식 및 실행 구조 점검
skills:
  - ROS 2
  - SLAM
  - Navigation
  - C++
card:
  image: assets/images/lk-robotics-emblem.svg
  imageAlt: LK ROBOTICS 로고
  imageFit: contain
overview: >-
  로봇 소프트웨어 프레임워크 ROS(Robot Operating System)의 버전 전환을 담당했습니다.
  지도 생성·위치추정·주행 기능을 ROS 2 환경으로 옮기고 기능 간 연결을 점검했습니다.
  장시간 실행 시험에서 발견한 위치 정보 지연을 분석하고 개선했습니다.
---

## 전환 전후의 실행 동작 비교

엘케이로보틱스에서 로봇 소프트웨어 이식과 실행 구조 점검을 담당했습니다. 기존 기능이 새 환경에서도 이어지도록 데이터 전달과 실행 조건을 비교했습니다.

빌드와 연결 확인 이후에는 장시간 실행 중 처리 지연이 누적되는지 점검했습니다. 센서 입력과 처리 결과의 시간 차이를 분석해 지연 원인을 좁히고, 수정 전후를 비교 시험했습니다.
