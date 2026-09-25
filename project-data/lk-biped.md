---
slug: lk-biped
category: lk
order: 3
detail: true
title: 이족 로봇의 평지·계단 내비게이션
description: 평지와 계단을 이동하는 로봇의 경로 계획과 주행 제어를 개발하고, 실제 로봇으로 계단 진입과 주행 모드 전환을 테스트했습니다.
role: 경로 계획, 계단 주행 제어, 층별 지도 전환
skills:
  - ROS 2
  - Navigation
  - Path Planning
  - Robot Control
card:
  image: assets/images/lk-robotics-emblem.svg
  imageAlt: LK ROBOTICS 로고
  imageFit: contain
overview: >-
  평지와 계단을 이동하는 이족 로봇의 자율주행 기능을 개발했습니다.
  로봇이 따라갈 경로와 속도 명령을 만드는 소프트웨어를 담당했습니다.
  계단 주행 제어와 층별 지도 전환을 구현하고 실제 로봇에서 테스트했습니다.
---

## 계단 주행 테스트

계단 진입 각도를 바꿔가며 로봇의 움직임을 확인했습니다. 평지에서 계단으로 진입할 때 주행 모드가 전환되는지도 테스트했습니다.

문제가 발생하면 주행 로그를 분석해 계단에 접근하는 과정과 계단을 오르내리는 과정 중 어디에서 발생했는지 확인했습니다. 테스트 조건과 결과를 기록하고 추가로 확인할 항목을 정리했습니다.
