---
slug: lk-patrol
title: Royal heritage patrol robot at Seooreung
description: Built outdoor maps and debugged localization issues. Replayed sensor data from field tests to check the fixes.
role: Mapping and localization debugging
overview: >-
  I built maps used by the royal heritage patrol robot at Seooreung.
  I analyzed sensor data and logs to debug localization errors and problems during long runs.
  After changing the code, I replayed the same data to check whether the problems recurred.
---

## Log analysis and reproduction tests

I compared sensor-input and position-output timestamps to identify when errors occurred. I investigated incorrect position estimates separately from problems with program execution.

I replayed field data to test under the same input conditions. I compared logs before and after code changes and checked whether the original problems recurred.

## News coverage

[Channel A News · Sunrabot patrol robot at the royal tombs (Korean)](https://ichannela.com/news/detail/000000548784.do) — September 4, 2026

The report shows the robot on patrol during its trial deployment at Seooreung, including a demonstration of detecting a fallen visitor.
