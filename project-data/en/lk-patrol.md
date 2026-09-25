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

<figure class="feature-media"><a href="https://www.youtube.com/watch?v=kHgA8jEmoCw&amp;t=22s" target="_blank" rel="noopener noreferrer"><img src="../assets/images/lk-patrol-seooreung-channela.jpg" alt="Patrol robot on a forest path at Seooreung — watch on Channel A YouTube" loading="lazy"></a><figcaption>Channel A News · Seooreung patrol robot · YouTube · 2026.09.04</figcaption></figure>
