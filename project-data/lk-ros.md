---
slug: lk-ros
category: lk
order: 2
detail: true
title: 로봇 시스템 ROS 1 → ROS 2 전환
description: 지도 작성·위치 추정·주행 코드를 ROS 2로 포팅하고, 장시간 실행 시 위치 정보가 늦게 출력되는 문제를 수정했습니다.
role: ROS 2 포팅, 기능 테스트, 지연 원인 분석
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
  기존 ROS 1 기반 로봇 소프트웨어를 ROS 2로 포팅했습니다.
  ROS(Robot Operating System)는 센서 처리와 로봇 제어 프로그램을 개발할 때 사용하는 소프트웨어 프레임워크입니다.
  지도 작성, 위치 추정, 주행 기능이 전환 후에도 동작하는지 테스트했습니다.
---

## 포팅 후 기능 테스트

기존 코드와 포팅한 코드를 비교하며 데이터가 정상적으로 전달되고 처리되는지 확인했습니다. 빌드가 완료된 뒤에는 센서를 연결해 각 기능의 동작을 테스트했습니다.

장시간 실행 테스트에서는 위치 정보가 늦게 출력되는 문제가 있었습니다. 센서 입력과 위치 정보 출력 사이의 지연 시간을 확인해 원인을 분석하고, 코드를 수정한 뒤 같은 조건으로 다시 테스트했습니다.
