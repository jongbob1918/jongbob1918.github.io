---
slug: lk-biped
category: lk
order: 3
detail: true
title: 이족 로봇의 평지·계단 내비게이션
description: 평지 주행과 계단 이동을 연계하는 경로 계획·제어 로직을 구현하고, 실기 시험으로 진입 조건과 제어 전환 동작을 확인했습니다.
role: 경로 계획·계단 제어·층간 지도 전환 연동
skills:
  - ROS 2
  - Nav2
  - Path Planning
  - Robot Control
card:
  image: assets/images/lk-robotics-emblem.svg
  imageAlt: LK ROBOTICS 로고
  imageFit: contain
overview: >-
  이족 로봇의 평지 주행과 계단 이동을 연결하는 내비게이션을 개발했습니다.
  경로 계획과 계단 제어, 층간 지도 전환 연동을 담당했습니다.
  실제 로봇 시험으로 계단 진입 조건과 주행 방식이 바뀌는 구간의 동작을 확인했습니다.
---

## 이동 구간별 동작을 연결하고 시험하기

엘케이로보틱스에서 평지와 계단을 연계하는 경로 계획·제어 로직을 구현했습니다. 로봇의 균형·보행 제어와 구분되는 상위 내비게이션을 담당했습니다.

실기 시험에서는 계단 진입, 계단 이동, 주행 방식 전환을 나누어 확인했습니다. 문제가 나타난 구간의 기록을 분석하고, 시험 조건을 구분해 후속 검증 항목을 정리했습니다.
