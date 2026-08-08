---
slug: elevator-mcu
shortName: ELEVATOR MCU
group: side
order: 5
title: ELEVATOR MCU — LED 엘리베이터 제어
description: Arduino와 LED·버튼으로 4층 호출 스케줄링과 Non-blocking 이동 제어를 구현한 원데이 프로젝트
team: 1명
period: 2025.07.06
skills:
  - Arduino
  - C++
  - State-Based Control
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
    - Non-blocking Timing
    - Embedded Systems
  descriptionKo: 버튼 상승 엣지로 4층 호출을 등록하고, 진행 방향을 우선해 목적층을 선택하며 500 ms 주기로 LED 위치를 갱신했습니다.
  descriptionEn: Built a four-floor Arduino controller that registers rising-edge button calls, prioritizes destinations in the current direction, and updates the LED position every 500 ms.
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

## 동작 시나리오 — 버튼 호출에서 도착까지

<div class="diagram" role="img" aria-label="LED 엘리베이터 제어 흐름"><div class="diagram-node owner">Button Edge<br>Call Toggle</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Direction Scan<br>Target Floor</div><div class="diagram-arrow">→</div><div class="diagram-node owner">500 ms Timer<br>Move One Step</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Floor · Transit LED<br>Status Output</div></div>

버튼의 상승 엣지를 감지해 해당 층의 호출 상태를 토글하고, 현재 이동 방향에서 먼저 만나는 호출을 목적층으로 선택합니다. 500 ms마다 위치 LED를 한 칸씩 이동시키고, 목적층에 도착하면 해당 호출과 GREEN LED를 해제합니다.

## 호출 입력 — 상승 엣지와 토글 상태

이전 버튼 값과 현재 값을 비교해 `LOW → HIGH`가 발생한 순간에만 호출을 등록합니다. 같은 버튼을 다시 누르면 `floorList` 상태를 반전시켜 호출을 취소하고 GREEN LED를 끄도록 구성했습니다.

`floorList`에 각 층의 호출 여부를 저장하고 `nowFloor`, `wantFloor`, `upMode`로 현재 위치, 목적 위치와 진행 방향을 관리합니다. 핀 번호와 층 수를 배열·상수로 분리해 배선이나 층 구성을 한곳에서 변경할 수 있도록 구성했습니다.

## 호출 스케줄링 — 진행 방향 우선 탐색

상승 중에는 `scanTop()`으로 위쪽 호출을 먼저 찾고, 호출이 없을 때만 아래쪽을 탐색합니다. 하강 중에는 반대 순서를 적용해 이동 방향의 요청을 우선 처리합니다.

<div class="formula-block">상승: 위쪽 호출 → 아래쪽 호출 · 하강: 아래쪽 호출 → 위쪽 호출</div>

## Non-blocking Timing — 이동 중 추가 입력 처리

`millis()`로 이전 갱신 시각과 현재 시각의 차이를 비교해 500 ms마다 `moveElevator()`를 호출합니다. 이동 주기를 긴 `delay()`로 대기하지 않아, LED 위치 갱신 사이에도 메인 루프가 버튼을 계속 확인하고 추가 호출을 다음 목적층 계산에 반영합니다.

## 입력과 출력 — 4개 버튼과 14개 LED

<div class="role-grid"><div class="info-card"><strong>현재 층</strong><span>RED LED 4개로 층 위치 표시</span></div><div class="info-card"><strong>층간 이동</strong><span>YELLOW LED 6개로 이동 과정 표시</span></div><div class="info-card"><strong>호출 상태</strong><span>버튼 4개와 GREEN LED 4개로 등록·취소 표시</span></div></div>

Arduino Uno 또는 Nano의 디지털·아날로그 핀을 함께 사용합니다. 4개 RED LED는 현재 층, 6개 YELLOW LED는 층간 이동, 4개 GREEN LED는 호출 등록 상태를 표시합니다. 실제 승강기 모터 대신 LED 시퀀스로 제어 로직을 시뮬레이션한 프로젝트입니다.

## 제어 로직 분리 — 입력·탐색·이동

<dl class="flow"><dt>증상</dt><dd>초기 순차 조건문 구조에서는 호출 방향과 목적층 선택 흐름이 분산되어 동작을 추적하기 어려웠습니다.</dd><dt>원인</dt><dd>버튼 확인, 호출 탐색과 이동 처리가 하나의 흐름에 섞여 있었습니다.</dd><dt>해결</dt><dd><code>buttonPress()</code>, <code>scanTop()</code>·<code>scanBottom()</code>, <code>getWantFloor()</code>, <code>moveElevator()</code>로 역할을 분리했습니다.</dd><dt>검증</dt><dd>단일 호출, 이동 중 추가 호출, 호출 취소와 모든 호출 처리 후 대기 시나리오를 정의하고 시뮬레이션으로 동작을 확인했습니다.</dd></dl>

## 검증 결과와 한계

<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>방향별 호출 탐색</strong><p>상·하행에 따라 탐색 순서를 바꾸고 반대 방향 호출을 이어서 처리합니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>이동 중 입력 확인</strong><p>시간 차 기반 이동 갱신 사이에서 버튼 상태를 반복 확인합니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>회로 시뮬레이션</strong><p>호출 LED와 위치 LED가 입력·이동 상태에 따라 바뀌는 동작을 확인합니다.</p></div></div>

<div class="limitation"><strong>한계</strong> 실제 승강기의 모터, 문 센서와 안전 인터락은 연결하지 않았으며, 공개 저장소에는 정의된 8개 시나리오의 자동 테스 로그가 포함되어 있지 않습니다.</div>
