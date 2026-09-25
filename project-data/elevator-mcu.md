---
slug: elevator-mcu
shortName: Arduino Project - LED Elevator
category: side
order: 5
title: Arduino Project - LED Elevator
description: 버튼과 LED로 호출·이동·대기를 구현한 Arduino 원데이 프로젝트
team: 1명
period: 2025.07.06
skills:
  - Arduino
  - State Machine
  - C++
repository: https://github.com/jongbob1918/elevator-mcu
card:
  image: assets/images/elevator-mcu-demo.gif
  imageAlt: Tinkercad에서 실행한 4층 LED 엘리베이터 호출·이동 시뮬레이션
  skills:
    - Arduino
    - State Machine
    - C++
links:
  - label: 시뮬레이션
    href: https://www.tinkercad.com/things/1Y2Mx1cmY9a-elevatorled
  - label: 코드
    href: https://github.com/jongbob1918/elevator-mcu/blob/main/src/elevator.ino
overview: >-
  Arduino와 버튼·LED로 4층 엘리베이터의 호출, 이동, 대기 동작을 구현한 1인 원데이 프로젝트입니다. 이동 중 호출을 추가하거나 취소할 수 있으며, 진행 방향에서 가까운 층부터 처리합니다.
demo:
  type: image
  src: ../assets/images/elevator-mcu-demo.gif
  alt: Tinkercad에서 실행한 LED 엘리베이터 호출 및 이동 테스트
---

## 하드웨어 구성

빨간 LED 4개는 각 층의 위치, 노란 LED 6개는 층 사이의 이동을 나타냅니다. 층마다 버튼과 초록 LED를 하나씩 두어 호출 여부를 표시했습니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-hardware.webp" alt="Arduino에 층 표시용 빨간 LED 4개, 이동 표시용 노란 LED 6개, 호출용 버튼과 초록 LED를 연결한 회로" loading="lazy"></figure></div>

시작하면 1층에서 대기합니다. 버튼을 한 번 누르면 해당 층이 호출되고, 다시 누르면 취소됩니다. 이동할 때는 0.5초 간격으로 LED를 한 칸씩 옮기며, 도착한 층의 호출 LED는 꺼집니다.

## 초기 설계 방법론

처음에는 먼저 들어온 호출부터 처리하는 큐 방식으로 설계했습니다. 하지만 1층에서 4층으로 이동하다가 2층을 지나기 전에 2층 호출이 들어오면, 나중에 들어온 호출을 먼저 처리해야 했습니다. 이동 중 호출 추가와 취소를 반영하려면 큐 중간에 층 번호를 넣거나 지우고, 처리 순서도 다시 정해야 했습니다.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-design.webp" alt="호출된 층을 순서대로 큐에 저장하는 초기 설계" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-problem.webp" alt="이동 중 호출 추가와 취소로 큐 순서를 수정해야 하는 상황" loading="lazy"></figure></div>

## 개선 방법론

각 층에 호출이 있는지를 따로 기록하고, 현재 위치와 이동 방향에 따라 다음 목적층을 정하도록 바꿨습니다. 예를 들어 2층과 4층이 호출된 상태에서 2층 호출을 취소하면, 4층 호출만 남습니다. 호출 순서를 따로 수정할 필요 없이 남은 호출 중에서 목적층을 다시 선택합니다.

올라가는 중에는 위쪽의 가까운 호출부터 찾고, 위에 호출이 없으면 아래쪽을 찾습니다. 내려가는 중에는 반대로 처리합니다. 호출이 모두 사라지면 가장 가까운 층으로 이동해 대기합니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-direction-example.webp" alt="상승 중일 때와 하강 중일 때 호출 처리 순서가 달라지는 예시" loading="lazy"></figure></div>

## 버튼 입력과 이동 처리

버튼을 계속 누르고 있어도 호출 상태가 한 번만 바뀌도록, 누르지 않은 상태에서 누른 상태로 바뀌는 순간을 감지했습니다. 같은 버튼을 다시 누르면 호출이 취소되고 초록 LED가 꺼집니다.

버튼 확인과 목적층 선택은 반복해서 수행하고, 이동은 경과 시간을 확인해 0.5초마다 LED를 한 칸씩 옮기도록 했습니다. 다음 이동 시점까지 기다리는 동안에도 버튼을 확인하므로 새 호출과 취소를 반영할 수 있습니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-loop-flow.webp" alt="버튼 확인과 목적층 탐색을 반복하고 500 ms 간격으로 이동하는 메인 루프 순서도" loading="lazy"></figure></div>

## 테스트

단일 호출, 이동 중 추가 호출, 호출 취소, 대기 상태 등을 8개 테스트 케이스로 정리했습니다. 아래 표는 각 입력에 대한 기대 동작입니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-test-cases.webp" alt="호출 순서와 취소 여부에 따른 기대 동작을 정리한 8개 테스트 케이스 표" loading="lazy"></figure></div>
