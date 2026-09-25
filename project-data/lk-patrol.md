---
slug: lk-patrol
category: lk
order: 1
detail: true
title: 궁능순찰로봇 서오릉
description: 야외 지도를 작성하고 위치 추정 오류를 디버깅했습니다. 주행 중 수집한 센서 데이터를 재생해 수정 결과를 확인했습니다.
role: 지도 작성, 위치 추정 디버깅
skills:
  - ROS 2
  - 3D LiDAR
  - SLAM
  - Localization
  - C++
card:
  image: assets/images/lk-patrol-seooreung-channela.jpg
  imageAlt: 서오릉 숲길을 순찰하는 궁능순찰로봇 — 채널A 뉴스 화면
  imageFit: cover
overview: >-
  서오릉 궁능순찰로봇이 주행할 때 사용하는 지도를 작성했습니다.
  센서 데이터와 로그를 분석해 위치 추정 오류와 장시간 실행 시 발생하는 문제를 디버깅했습니다.
  코드 수정 후에는 같은 데이터를 재생해 문제가 다시 발생하는지 확인했습니다.
---

## 로그 분석과 재현 테스트

센서 데이터의 수신 시각과 위치 계산 결과의 출력 시각을 비교해 오류가 발생한 시점을 찾았습니다. 위치 계산이 잘못되는 문제와 프로그램 실행 중 발생하는 문제를 구분해 원인을 분석했습니다.

현장에서 수집한 데이터를 재생해 같은 조건으로 테스트했습니다. 코드 수정 전후의 로그를 비교하고, 기존 문제가 다시 발생하는지 확인했습니다.

## 관련 보도

<figure class="feature-media"><a href="https://www.youtube.com/watch?v=kHgA8jEmoCw&amp;t=22s" target="_blank" rel="noopener noreferrer"><img src="../assets/images/lk-patrol-seooreung-channela.jpg" alt="서오릉 숲길을 주행하는 궁능순찰로봇 — 채널A 유튜브 영상 보기" loading="lazy"></a><figcaption>채널A 뉴스 · 서오릉 순라봇 · YouTube · 2026.09.04</figcaption></figure>
