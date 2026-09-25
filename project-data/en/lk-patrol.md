---
slug: lk-patrol
title: Outdoor patrol robot
description: Built outdoor maps and debugged localization issues. Replayed sensor data from field tests to check the fixes.
role: Mapping and localization debugging
overview: >-
  I built maps used by an outdoor patrol robot.
  I analyzed sensor data and logs to debug localization errors and problems during long runs.
  After changing the code, I replayed the same data to check whether the problems recurred.
---

## Log analysis and reproduction tests

I compared sensor-input and position-output timestamps to identify when errors occurred. I investigated incorrect position estimates separately from problems with program execution.

I replayed field data to test under the same input conditions. I compared logs before and after code changes and checked whether the original problems recurred.
