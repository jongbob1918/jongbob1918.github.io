---
slug: elevator-mcu
title: Arduino Project - LED Elevator
description: A one-day Arduino project simulating elevator calls, movement, and idle behavior with buttons and LEDs
team: Solo project
period: Jul 6, 2025
links:
  - label: Simulation
    href: https://www.tinkercad.com/things/1Y2Mx1cmY9a-elevatorled
  - label: Code
    href: https://github.com/jongbob1918/elevator-mcu/blob/main/src/elevator.ino
overview: >-
  A solo, one-day project simulating calls, movement, and idle behavior for a four-floor elevator with an Arduino, buttons, and LEDs. Calls can be added or canceled during movement, and the nearest requested floor in the travel direction is served first.
demo:
  type: image
  src: ../assets/images/elevator-mcu-demo.gif
  alt: Four-floor LED elevator call and movement test running in Tinkercad
---

## Hardware

Four red LEDs mark the floors, and six yellow LEDs show movement between them. Each floor has a button and a green LED to indicate an active call.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-hardware.webp" alt="Arduino circuit with four red floor LEDs, six yellow movement LEDs, and a button and green call LED for each floor" loading="lazy"></figure></div>

The elevator starts at floor 1. Pressing a button registers a call; pressing it again cancels it. The position advances one LED every 0.5 seconds, and the call LED turns off when the elevator reaches that floor.

## Initial design approach

The initial design used a queue to serve calls in the order they arrived. But if a call for floor 2 arrived before the elevator passed it on the way from floor 1 to floor 4, that later call should be served first. Handling new calls and cancellations during movement meant inserting or removing floor numbers and adjusting the queue order.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-design.webp" alt="Initial design storing called floors in a queue" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/elevator-mcu-queue-problem.webp" alt="New calls and cancellations requiring changes to the queue during movement" loading="lazy"></figure></div>

## Improved design approach

I recorded whether each floor had an active call and selected the next target using the current position and travel direction. For example, canceling floor 2 when floors 2 and 4 are requested leaves only the call for floor 4. The next target is selected from the remaining calls without editing a stored call order.

While moving up, the elevator looks for the nearest call above it, then searches below if none remain above. While moving down, it searches in the reverse order. With no calls left, it moves to the nearest floor and waits.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-direction-example.webp" alt="Examples showing different call orders during upward and downward travel" loading="lazy"></figure></div>

## Button input and movement

To change the call state only once when a button is held down, I detect the transition from released to pressed. Pressing the same button again cancels the call and turns off its green LED.

The program repeatedly checks buttons and selects the target, while elapsed time determines when to advance one LED every 0.5 seconds. Button checks continue between movement steps, allowing new calls and cancellations to be handled.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-loop-flow.webp" alt="Main loop checking buttons and the target repeatedly while moving at 500 ms intervals" loading="lazy"></figure></div>

## Tests

I defined eight test cases covering single calls, new calls during movement, cancellations, and idle behavior. The table lists the expected behavior for each input sequence.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/elevator-mcu-test-cases.webp" alt="Eight test cases listing expected behavior for call sequences and cancellations" loading="lazy"></figure></div>
