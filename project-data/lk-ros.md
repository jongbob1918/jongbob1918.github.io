---
slug: lk-ros
category: lk
order: 2
detail: true
title: 로봇 소프트웨어 ROS 2 전환
description: 회사 로봇의 기존 ROS 1 Noetic 소프트웨어를 ROS 2 Humble로 포팅하고, ROS 2와 Nav2 기반으로 시스템을 재설계했습니다.
skills:
  - ROS 2
  - Nav2
  - System Redesign
card:
  image: assets/images/ros1-noetic-to-ros2-humble.png
  imageAlt: 왼쪽 ROS 1 Noetic에서 오른쪽 ROS 2 Humble로 전환하는 방향을 나타낸 그림
  imageFit: cover
demo:
  type: image
  src: ../assets/images/ros1-noetic-to-ros2-humble.png
  alt: ROS 1 Noetic에서 ROS 2 Humble로의 소프트웨어 전환 방향

overview: >-
  회사 로봇에서 사용하던 ROS 1 Noetic 기반 소프트웨어를 ROS 2 Humble로 전환했습니다.
  기존 코드를 포팅하고 자율주행 시스템을 ROS 2와 Nav2 기반으로 재설계했습니다.
  새 환경에서 제공하는 기능을 활용할 수 있도록 로봇 소프트웨어의 기반을 변경했습니다.
---

## ROS 1 Noetic에서 ROS 2 Humble로

센서 처리와 로봇 제어 프로그램을 연결하는 소프트웨어 프레임워크인 ROS(Robot Operating System)를 전환했습니다. 기존 ROS 1 Noetic 기반 코드를 ROS 2 Humble 환경으로 포팅했습니다.

## 자율주행 시스템 재설계

경로 계획과 주행 제어를 제공하는 Nav2(Navigation2)를 중심으로 자율주행 시스템을 재설계했습니다. 기존 코드를 옮기는 작업과 함께, ROS 2와 Nav2의 기능을 활용할 수 있도록 시스템 구성을 변경했습니다.
