---
slug: elevator-mcu
title: ELEVATOR MCU — Direction-Aware LED Controller
description: A one-day Arduino project replacing a queue-first design with direction- and state-based request scanning
team: Solo project
period: Jul 6, 2025
overview: >-
  This solo, one-day project models elevator calls, movement, and idle behavior with four buttons and fourteen LEDs. A queue-based first design became complicated when calls were added or canceled in transit. I replaced call order with per-floor request state and recompute the next target on every loop according to the last travel direction. The project validates scheduling logic in Arduino and Tinkercad rather than controlling a physical elevator motor.
demo:
  type: image
  src: ../assets/images/elevator-mcu-demo.gif
  alt: Four-floor LED elevator call and movement test running in Tinkercad
---

## Turning requirements into LED control rules

The requirements called for at least three floors, red LEDs for the current floor, yellow LEDs for movement between floors, and a button and green call-status LED at each floor. I implemented a four-floor layout.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-requirements.webp" alt="Requirements for floors, position indicators, inter-floor movement, and call buttons" loading="lazy"><figcaption>User requirements for display, movement, and call functions</figcaption></figure></div>

<div class="role-grid"><div class="info-card"><strong>Current floor</strong><span>Four red LEDs indicate floor arrival</span></div><div class="info-card"><strong>Inter-floor motion</strong><span>Six yellow LEDs show movement</span></div><div class="info-card"><strong>Call state</strong><span>Four buttons and green LEDs register and cancel calls</span></div></div>

Each LED position represents motion instead of a physical motor. One floor interval is `RED → YELLOW → YELLOW`; moving `nowFloor` from 0 to 9 visualizes both floors and the spaces between them.

## Initial design — storing calls in a queue

The first design queued floor numbers in button-press order and served the earliest request first.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-design.webp" alt="Initial design storing called floors in a queue" loading="lazy"><figcaption>Initial design · Preserve call order</figcaption></figure><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-problem.webp" alt="Queue complexity caused by cancellation, insertion, and direction changes" loading="lazy"><figcaption>Problem · Cancellation, insertion, and direction changes complicate the queue</figcaption></figure></div>

It handled simple calls but required continual queue edits when:

- a registered call was pressed again to cancel it;
- a second-floor request arrived while moving from floor 1 to floor 4;
- a nearby request in the current direction should take priority; or
- remaining calls in the opposite direction should be served after arrival.

The next target therefore needed to depend on active calls and travel direction, not event order.

## Improvement — recomputing targets from calls and direction

Instead of a queue, `floorList[4]` stores only whether each floor is active. `upMode` stores direction, `nowFloor` stores the current LED position, and `wantFloor` stores the selected target. Every main-loop iteration scans active calls again to choose the next target.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-state-design.webp" alt="Improved design using call, upward, downward, and stop behavior" loading="lazy"><figcaption>Moving from stored call order to state- and direction-aware scanning</figcaption></figure></div>

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-direction-example.webp" alt="Examples of choosing the next call while moving upward or downward" loading="lazy"><figcaption>The same call list produces a different target based on current direction</figcaption></figure></div>

The presentation described stop, upward, and downward states, but the code does not use an explicit FSM enum. `upMode` records the last direction, while `wantFloor == nowFloor` represents idle behavior. It is therefore more accurate to describe the implementation as direction-aware scheduling than as an explicit three-state FSM.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-variables.webp" alt="Variables storing current position, target position, direction, and floor calls" loading="lazy"><figcaption>State variables separate position, target, direction, and active calls</figcaption></figure></div>

<div class="diagram" role="img" aria-label="Direction-aware call scheduling flow"><div class="diagram-node owner">Button Edge<br>Call Toggle</div><div class="diagram-arrow">→</div><div class="diagram-node owner">floorList<br>Active Calls</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Direction Scan<br>Target Floor</div><div class="diagram-arrow">→</div><div class="diagram-node owner">500 ms Tick<br>Move One LED</div></div>

## Registering and canceling calls on the rising edge

The previous and current button values are compared so a held button does not toggle its call state on every loop. `floorSensing()` runs only on the `LOW → HIGH` transition.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/elevator-mcu-button-flow.webp" alt="buttonPress flow comparing previous and current button values" loading="lazy"><figcaption>buttonPress() · Detect only the LOW → HIGH edge</figcaption></figure><figure class="feature-media"><img src="../assets/images/elevator-mcu-call-toggle-flow.webp" alt="floorSensing flow toggling call state and the green LED" loading="lazy"><figcaption>floorSensing() · Update the call and green LED together</figcaption></figure></div>

```cpp
int current = digitalRead(buttons[button]);

if (prevButtons[button] == LOW && current == HIGH) {
    floorSensing(button);
}

prevButtons[button] = current;
```

`floorSensing()` inverts the selected `floorList` entry and updates its green LED. The first click registers a call and the next click cancels it.

This detects a rising edge but has no software debounce interval or hardware filter. Only the main loop's 10 ms delay remains, so a physical mechanical button could still bounce and toggle more than once.

## Scanning the nearest call in the current direction

While moving upward, `scanTop()` searches active calls above the current position from nearest to farthest. If none exist, `scanBottom()` searches the other direction. Downward travel applies the reverse order.

<div class="formula-block">Upward: nearest call above → calls below &nbsp;·&nbsp; Downward: nearest call below → calls above</div>

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-target-flow.webp" alt="getWantFloor flow choosing scanTop or scanBottom from the current direction" loading="lazy"><figcaption>getWantFloor() · Search the current direction first, then reverse</figcaption></figure></div>

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/elevator-mcu-scan-bottom.webp" alt="scanBottom flow finding the nearest call below" loading="lazy"><figcaption>scanBottom() · Find the nearest call below</figcaption></figure><figure class="feature-media"><img src="../assets/images/elevator-mcu-scan-top.webp" alt="scanTop flow finding the nearest call above" loading="lazy"><figcaption>scanTop() · Find the nearest call above</figcaption></figure></div>

With no active calls, the current LED position is rounded to the nearest physical floor for idle. This is a simple single-elevator direction-priority scheduler, not a production multi-elevator dispatch algorithm.

## Checking calls between 500 ms movement ticks

Movement calls `moveElevator()` only when the elapsed `millis()` time exceeds 500 ms, advancing one LED. Because the full motion is not blocked by `delay(500)`, button state and new calls can be checked between movement ticks.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/elevator-mcu-move-flow.webp" alt="moveElevator flow advancing one LED toward the target" loading="lazy"><figcaption>moveElevator() · Advance one LED toward the target</figcaption></figure><figure class="feature-media"><img src="../assets/images/elevator-mcu-loop-flow.webp" alt="Main loop checking buttons, selecting a target, and moving every 500 milliseconds" loading="lazy"><figcaption>loop() · Keep checking input while movement runs every 500 ms</figcaption></figure></div>

The loop still ends with `delay(10)`, so the program is not completely free of blocking calls. More precisely, it combines a short polling interval with `millis()`-based cooperative timing.

## Hardware and position representation

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-hardware.webp" alt="Elevator circuit with an Arduino Uno, four buttons, and fourteen LEDs" loading="lazy"><figcaption>Arduino Uno/Nano with 4 buttons, 4 red, 6 yellow, and 4 green LEDs</figcaption></figure></div>

Pin numbers are grouped in the `leds`, `ledGreens`, and `buttons` arrays. Adding floors requires updating the pin arrays as well as `totalfloor`, `floorHeight`, the call-state array, and total position LEDs. `moveTime` controls the speed.

## Separating input, scanning, and movement

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-flow.webp" alt="Overall function flow from button detection and call management to target scanning and movement" loading="lazy"><figcaption>Overall function flow from the project presentation</figcaption></figure></div>

<dl class="flow"><dt>buttonPress()</dt><dd>Detects a rising edge and requests a call-state change.</dd><dt>floorSensing()</dt><dd>Toggles the call and updates that floor's green LED.</dd><dt>scanTop() / scanBottom()</dt><dd>Finds the nearest active call relative to position and direction.</dd><dt>getWantFloor()</dt><dd>Selects the target with direction priority and reversal.</dd><dt>moveElevator()</dt><dd>Moves the current position by one step and updates the LEDs.</dd></dl>

## Eight defined test scenarios

The presentation defines eight input sequences and expected behaviors covering a single call, calls during movement, cancellation, and idle state.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-test-cases.webp" alt="Eight elevator test cases covering calls, in-motion requests, cancellation, and idle behavior" loading="lazy"><figcaption>TC01–08 · Defined input sequences and expected behavior</figcaption></figure></div>

[View presentation](https://docs.google.com/presentation/d/1m6TEW22ZXlsffNen36meO2qcAVfPnEL0svScLSEzju0/edit?usp=sharing) · [Tinkercad simulation](https://www.tinkercad.com/things/1Y2Mx1cmY9a-elevatorled) · [Full source](https://github.com/jongbob1918/elevator-mcu/blob/main/src/elevator.ino)
