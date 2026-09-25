---
slug: lk-patrol
category: lk
order: 1
detail: true
title: 야외 순찰 로봇
description: 실주행 기록으로 위치추정과 장시간 실행 중 발생한 문제를 분석·수정하고, 기록 데이터 재생으로 수정 사항을 검증했습니다.
role: 야외 지도 생성·위치추정 분석 및 안정화
skills:
  - ROS 2
  - FAST-LIO
  - Localization
  - C++
card:
  image: assets/images/lk-robotics-emblem.svg
  imageAlt: LK ROBOTICS 로고
  imageFit: contain
overview: >-
  야외 순찰 로봇의 지도 생성과 위치추정 분석을 담당했습니다.
  실주행 기록을 바탕으로 위치추정과 장시간 실행 중 발생한 문제를 분석하고 수정했습니다.
  수정 전후에 같은 기록 데이터를 재생해 문제의 재발 여부를 확인했습니다.
---

## 실주행 기록으로 문제 원인 좁히기

엘케이로보틱스에서 야외 지도 생성과 위치추정 분석·안정화를 담당했습니다. 센서 입력과 위치추정 결과를 시간 순서대로 비교해 문제가 발생한 단계를 좁혔습니다.

증상이 비슷해도 원인이 다를 수 있어, 위치추정 품질과 프로그램 실행 안정성을 나누어 점검했습니다. 수정 후에는 같은 기록 데이터를 재생해 변경 전후를 비교하고 재발 여부를 확인했습니다.
