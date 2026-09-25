---
slug: elevator-mcu
shortName: aduino project - LED elevator
category: side
order: 5
title: aduino project - LED elevator
description: 버튼과 LED로 호출·이동·대기를 구현한 Arduino 원데이 프로젝트
team: 1명
period: 2025.07.06
skills:
  - arduino
  - state machine
  - c++
repository: https://github.com/jongbob1918/elevator-mcu
card:
  image: assets/images/elevator-mcu-demo.gif
  imageAlt: Tinkercad에서 실행한 4층 LED 엘리베이터 호출·이동 시뮬레이션
  skills:
    - arduino
    - state machine
    - c++
overview: >-
  Arduino와 버튼 4개, LED 14개로 4층 엘리베이터의 호출·이동·대기 동작을 구현했습니다. 하루 동안 혼자 진행한 프로젝트로, Tinkercad에서 회로를 구성하고 동작을 확인했습니다. 이동 중 들어오는 호출과 취소를 처리하면서 호출 우선순위를 정하는 방법을 고민했습니다.
demo:
  type: image
  src: ../assets/images/elevator-mcu-demo.gif
  alt: Tinkercad에서 실행한 LED 엘리베이터 호출 및 이동 테스트
---

## 하드웨어 구성

빨간 LED 4개는 각 층의 위치, 노란 LED 6개는 층 사이의 이동을 나타냅니다. 층마다 버튼과 초록 LED를 하나씩 두어 호출 여부를 표시했습니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-hardware.webp" alt="Arduino에 층 표시용 빨간 LED 4개, 이동 표시용 노란 LED 6개, 호출용 버튼과 초록 LED를 연결한 회로" loading="lazy"><figcaption>빨간 LED 사이에 노란 LED를 두 개씩 배치한 4층 회로</figcaption></figure></div>

시작하면 1층에서 대기합니다. 버튼을 한 번 누르면 해당 층이 호출되고, 다시 누르면 취소됩니다. 이동할 때는 0.5초 간격으로 LED를 한 칸씩 옮기며, 도착한 층의 호출 LED는 꺼집니다.

## 호출 순서를 큐에 넣으려 했지만

처음에는 버튼을 누른 순서대로 층 번호를 큐에 저장하려 했습니다. 그런데 1층에서 4층으로 가는 중에 2층 호출이 들어오면, 나중에 누른 2층을 먼저 들러야 했습니다. 호출 취소까지 처리하려니 큐 중간에 값을 넣거나 지우는 일이 많아졌습니다.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-design.webp" alt="호출된 층을 순서대로 큐에 저장하는 초기 설계" loading="lazy"><figcaption>처음 구상한 호출 큐</figcaption></figure><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-problem.webp" alt="이동 중 호출 추가와 취소로 큐 순서를 수정해야 하는 상황" loading="lazy"><figcaption>호출이 바뀔 때 큐를 수정해야 하는 문제</figcaption></figure></div>

그래서 `floorList[4]`에는 각 층의 호출 여부만 저장하고, 현재 위치와 진행 방향을 기준으로 목적층을 매번 다시 찾도록 바꿨습니다. 호출을 추가하거나 취소할 때는 해당 층의 값만 바꾸면 됩니다.

## 진행 방향의 가까운 층부터 처리

올라가는 중에는 위쪽의 가까운 호출부터 찾고, 위에 호출이 없으면 아래쪽을 찾습니다. 내려가는 중에는 반대로 처리합니다. 호출이 모두 사라지면 가장 가까운 층으로 이동해 대기합니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-direction-example.webp" alt="상승 중일 때와 하강 중일 때 호출 처리 순서가 달라지는 예시" loading="lazy"><figcaption>같은 호출이 남아 있어도 진행 방향에 따라 처리 순서가 달라집니다.</figcaption></figure></div>

`scanTop()`과 `scanBottom()`이 위·아래의 호출을 찾고, `getWantFloor()`가 마지막 이동 방향인 `upMode`에 따라 탐색 순서를 정합니다. 현재 위치는 `nowFloor`, 목적 위치는 `wantFloor`에 저장했습니다. 두 값은 층 번호가 아니라 층 사이 LED까지 포함한 0~9의 위치입니다.

## 버튼 입력과 이동 처리

버튼을 누르고 있는 동안 호출이 반복해서 등록·취소되지 않도록, 이전 입력과 현재 입력을 비교했습니다. `LOW → HIGH`로 바뀐 순간에만 호출 상태와 초록 LED를 함께 바꿉니다.

```cpp
int current = digitalRead(buttons[button]);

if (prevButtons[button] == LOW && current == HIGH) {
    floorSensing(button);
}

prevButtons[button] = current;
```

메인 루프에서는 버튼 확인과 목적층 탐색을 반복합니다. 이동은 `millis()`로 시간을 확인해 500 ms가 지났을 때만 `moveElevator()`를 호출합니다. 이동을 기다리는 동안에도 새 호출과 취소를 반영할 수 있습니다. 루프 마지막에는 `delay(10)`을 두었습니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-loop-flow.webp" alt="버튼 확인과 목적층 탐색을 반복하고 500 ms 간격으로 이동하는 메인 루프 순서도" loading="lazy"><figcaption>입력과 목적층은 매 루프 확인하고, 이동은 시간 간격에 맞춰 실행합니다.</figcaption></figure></div>

## 테스트

단일 호출, 이동 중 추가 호출, 호출 취소, 대기 상태 등을 8개 테스트 케이스로 정리했습니다. 아래 표는 각 입력에 대한 기대 동작입니다.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-test-cases.webp" alt="호출 순서와 취소 여부에 따른 기대 동작을 정리한 8개 테스트 케이스 표" loading="lazy"><figcaption>테스트 입력 순서와 예상 결과</figcaption></figure></div>

페이지 상단 데모에는 간단한 조작을 담았습니다. 다른 호출 순서는 [Tinkercad 시뮬레이션](https://www.tinkercad.com/things/1Y2Mx1cmY9a-elevatorled)에서 직접 실행할 수 있습니다.

## 남은 부분

LED로 호출과 이동 규칙을 확인하는 데까지 구현했습니다. 실제 모터 제어는 포함하지 않았습니다. 또한 버튼 접점이 튀면서 한 번의 입력이 여러 번 감지되는 현상을 걸러내는 처리가 없어, 실제 버튼으로 제작한다면 이 부분을 보완해야 합니다.

[발표 슬라이드 보기](https://docs.google.com/presentation/d/1m6TEW22ZXlsffNen36meO2qcAVfPnEL0svScLSEzju0/edit?usp=sharing) · [전체 코드](https://github.com/jongbob1918/elevator-mcu/blob/main/src/elevator.ino)
