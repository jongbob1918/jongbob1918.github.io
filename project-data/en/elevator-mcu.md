---
slug: elevator-mcu
title: aduino project - LED elevator
description: A one-day Arduino project simulating elevator calls, movement, and idle behavior with buttons and LEDs
team: Solo project
period: Jul 6, 2025
overview: >-
  I built a four-floor elevator simulation with an Arduino, four buttons, and fourteen LEDs in a solo, one-day project. I assembled and checked the circuit in Tinkercad. Handling new calls and cancellations during movement led me to rethink how to choose the next floor.
demo:
  type: image
  src: ../assets/images/elevator-mcu-demo.gif
  alt: Four-floor LED elevator call and movement test running in Tinkercad
---

## Hardware

Four red LEDs mark the floors, and six yellow LEDs show movement between them. Each floor has a button and a green LED to indicate an active call.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-hardware.webp" alt="Arduino circuit with four red floor LEDs, six yellow movement LEDs, and a button and green call LED for each floor" loading="lazy"><figcaption>Four floors with two yellow LEDs between each pair of red LEDs</figcaption></figure></div>

The elevator starts at floor 1. Pressing a button registers a call; pressing it again cancels it. The position advances one LED every 0.5 seconds, and the call LED turns off when the elevator reaches that floor.

## Why I moved away from a queue

My first idea was to queue floor numbers in the order the buttons were pressed. But if a call for floor 2 arrived while traveling from floor 1 to floor 4, floor 2 should be served first. Supporting this and cancellations meant inserting and removing entries in the middle of the queue.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-design.webp" alt="Initial design storing called floors in a queue" loading="lazy"><figcaption>The initial call queue</figcaption></figure><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-problem.webp" alt="New calls and cancellations requiring changes to the queue during movement" loading="lazy"><figcaption>Changes needed when calls are added or canceled</figcaption></figure></div>

I changed `floorList[4]` to store only whether each floor has an active call. The target is recalculated from the current position and direction on each loop. Adding or canceling a call only changes that floor's value.

## Serving nearby floors in the travel direction

While moving up, the elevator looks for the nearest call above it, then searches below if none remain above. While moving down, it searches in the reverse order. With no calls left, it moves to the nearest floor and waits.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-direction-example.webp" alt="Examples showing different call orders during upward and downward travel" loading="lazy"><figcaption>The same active calls are served in a different order depending on direction.</figcaption></figure></div>

`scanTop()` and `scanBottom()` find calls above and below. `getWantFloor()` chooses their search order using `upMode`, which stores the last travel direction. `nowFloor` and `wantFloor` hold the current and target positions. These are LED positions from 0 to 9, including the spaces between floors.

## Button input and movement

I compare the previous and current button readings so holding a button does not repeatedly register and cancel its call. The call state and green LED change only when the input switches from `LOW` to `HIGH`.

```cpp
int current = digitalRead(buttons[button]);

if (prevButtons[button] == LOW && current == HIGH) {
    floorSensing(button);
}

prevButtons[button] = current;
```

The main loop checks buttons and recalculates the target. It uses `millis()` to call `moveElevator()` only after 500 ms have elapsed, allowing new calls and cancellations between movement steps. Each loop ends with `delay(10)`.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-loop-flow.webp" alt="Main loop checking buttons and the target repeatedly while moving at 500 ms intervals" loading="lazy"><figcaption>Input and target checks run each loop; movement runs at timed intervals.</figcaption></figure></div>

## Tests

I defined eight test cases covering single calls, new calls during movement, cancellations, and idle behavior. The table lists the expected behavior for each input sequence.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-test-cases.webp" alt="Eight test cases listing expected behavior for call sequences and cancellations" loading="lazy"><figcaption>Test inputs and expected results</figcaption></figure></div>

The demo at the top shows a short interaction. Other call sequences can be tried in the [Tinkercad simulation](https://www.tinkercad.com/things/1Y2Mx1cmY9a-elevatorled).

## Remaining work

The implementation covers call and movement rules using LEDs. Motor control is outside its scope. It also lacks filtering for mechanical button bounce, which can register a single press multiple times. This would need attention before building it with physical buttons.

[View presentation](https://docs.google.com/presentation/d/1m6TEW22ZXlsffNen36meO2qcAVfPnEL0svScLSEzju0/edit?usp=sharing) · [Full source](https://github.com/jongbob1918/elevator-mcu/blob/main/src/elevator.ino)
