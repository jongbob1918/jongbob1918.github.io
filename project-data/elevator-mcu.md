---
slug: elevator-mcu
shortName: ELEVATOR MCU
group: side
order: 5
title: ELEVATOR MCU — LED 엘리베이터 제어
description: Arduino와 LED·버튼으로 4층 엘리베이터의 호출 우선순위와 이동 상태를 구현한 원데이 프로젝트
team: 1명
period: 2025.07.06
skills:
  - Arduino
  - C++
  - Finite-State Control
  - Non-blocking Timing
  - Embedded Systems
repository: https://github.com/jongbob1918/elevator-mcu
card:
  image: https://raw.githubusercontent.com/jongbob1918/elevator-mcu/main/docs/images/test_demo.gif
  imageAlt: Arduino LED 엘리베이터 호출 및 이동 시뮬레이션
  titleEn: ELEVATOR MCU — LED Elevator Controller
  keywords:
    - Arduino
    - C++
    - State Control
    - Embedded Systems
  descriptionKo: Arduino의 버튼 입력과 LED 배열로 4층 호출을 관리하고, 진행 방향에 따라 목적층을 선택하는 엘리베이터 제어 로직을 구현했습니다.
  descriptionEn: Built a four-floor Arduino elevator controller that manages button calls and selects destinations according to its current travel direction.
overview: >-
  엘리베이터의 호출 처리와 이동 규칙을 작은 임베디드 환경에서 검증하려면 입력, 상태, 출력의 흐름을 재현할 장치가 필요합니다.
  이를 위해 4개 버튼과 14개 LED로 층별 호출 상태와 이동 위치를 표현하는 Arduino 제어기를 개발했습니다.
  사용자가 층 버튼을 누르면 호출을 등록하고 진행 방향에 맞춰 목적층을 다시 선택한 뒤 0.5초 간격으로 LED 위치를 이동합니다.
demo:
  type: image
  src: https://raw.githubusercontent.com/jongbob1918/elevator-mcu/main/docs/images/test_demo.gif
  alt: Arduino LED 엘리베이터 호출 및 이동 테스트
  caption: Tinkercad에서 확인한 호출 등록·이동·도착 동작
---

## 버튼 입력에서 층 이동까지

<div class="diagram" role="img" aria-label="LED 엘리베이터 제어 흐름"><div class="diagram-node owner">Button Edge<br>Call Toggle</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Direction Scan<br>Target Floor</div><div class="diagram-arrow">→</div><div class="diagram-node owner">500 ms Timer<br>Move One Step</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Floor · Transit LED<br>Status Output</div></div>

버튼의 상승 에지를 감지해 해당 층의 호출 상태를 토글하고, 현재 이동 방향에서 먼저 만나는 호출을 목적층으로 선택합니다. 이동은 한 번에 LED 한 칸씩 갱신하며 목적층에 도착하면 호출 표시를 해제합니다.

## 호출 우선순위와 상태 표현

### 배열로 관리하는 4개 층

`floorList`에 각 층의 호출 여부를 저장하고 `nowFloor`, `wantFloor`, `upMode`로 현재 위치, 목적 위치와 진행 방향을 관리합니다. 핀 번호와 층 수를 배열·상수로 분리해 배선이나 층 구성을 한곳에서 변경할 수 있도록 구성했습니다.

### 진행 방향을 유지하는 목적층 탐색

상승 중에는 `scanTop()`으로 위쪽 호출을 먼저 찾고, 호출이 없을 때만 아래쪽을 탐색합니다. 하강 중에는 반대 순서를 적용해 이동 방향의 요청을 우선 처리합니다.

<div class="formula-block">상승: 위쪽 호출 → 아래쪽 호출 · 하강: 아래쪽 호출 → 위쪽 호출</div>

## 타이머 기반 이동 제어

`millis()`로 이전 갱신 시각과 현재 시각의 차이를 비교해 500 ms마다 `moveElevator()`를 호출합니다. 긴 대기 함수로 이동 주기를 만들지 않기 때문에 이동 중에도 메인 루프가 버튼 입력을 반복 확인하고 새 호출을 목적층 계산에 반영할 수 있습니다.

## 하드웨어 구성

<div class="role-grid"><div class="info-card"><strong>현재 층</strong><span>RED LED 4개로 층 위치 표시</span></div><div class="info-card"><strong>층간 이동</strong><span>YELLOW LED 6개로 이동 과정 표시</span></div><div class="info-card"><strong>호출 상태</strong><span>버튼 4개와 GREEN LED 4개로 등록·취소 표시</span></div></div>

Arduino Uno 또는 Nano의 디지털·아날로그 핀을 함께 사용합니다. 실제 승강기 모터가 아닌 LED 시퀀스로 제어 로직을 시뮬레이션한 프로젝트이며, 회로와 동작은 Tinkercad에서도 실행할 수 있습니다.

## 초기 설계 개선

<dl class="flow"><dt>증상</dt><dd>초기 순차 조건문 구조에서는 호출 방향과 목적층 선택 흐름이 분산되어 동작을 추적하기 어려웠습니다.</dd><dt>원인</dt><dd>버튼 확인, 호출 탐색과 이동 처리가 하나의 흐름에 섞여 있었습니다.</dd><dt>해결</dt><dd><code>buttonPress()</code>, <code>scanTop()</code>·<code>scanBottom()</code>, <code>getWantFloor()</code>, <code>moveElevator()</code>로 역할을 분리했습니다.</dd><dt>검증</dt><dd>단일 호출, 이동 중 추가 호출, 호출 취소와 모든 호출 처리 후 대기 시나리오를 정의하고 시뮬레이션으로 동작을 확인했습니다.</dd></dl>

## 검증 결과

<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>방향별 호출 탐색</strong><p>상·하행에 따라 탐색 순서를 바꾸고 반대 방향 호출을 이어서 처리합니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>이동 중 입력 확인</strong><p>시간 차 기반 이동 갱신 사이에서 버튼 상태를 반복 확인합니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>회로 시뮬레이션</strong><p>호출 LED와 위치 LED가 입력·이동 상태에 따라 바뀌는 동작을 확인합니다.</p></div></div>
