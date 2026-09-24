---
slug: lk-patrol
title: Seooreung patrol robot
description: Separated localization failures in forest-route logs and checked a memory-corruption fix by replaying a 55-minute recording.
role: Outdoor mapping, localization diagnosis and stabilization
overview: >-
  Patrolling Seooreung requires the robot to maintain its position among similar trees and junctions.
  I integrated range sensors and cameras on TRON2, built a site map, and tested localization and navigation.
  I separated process crashes from tracking loss, then patched and replay-tested the crash issue.
---

## Maintaining position on a forest route

At LK Robotics, I worked on outdoor mapping and localization diagnosis. The target mission was a roughly 2.88 km round trip between Daebinmyo and the management office; work began with mapping and segment trials.

TRON2 carried a depth camera and a LiDAR (Light Detection and Ranging) sensor for measuring surrounding geometry. LiDAR and an Inertial Measurement Unit (IMU) estimated motion, while matching current scans to the stored map corrected the robot's position.

> Image needed: Sensor layout on the field-test robot and a map distinguishing the target round-trip route from the segments actually tested.

## Separating position errors from process crashes

During forest trials, the robot marker on the map froze or jumped, and the localization process sometimes terminated. I compared sensor input, FAST-LIO motion estimates, and map-corrected positions on a common timeline to locate the first failing stage.

The crash backtrace showed memory corruption detected while releasing a point-cloud object. I protected shared point clouds and correction state against concurrent access, and limited executor and registration threads to two and four respectively.

I replayed approximately 55 minutes of the same sensor recording with AddressSanitizer enabled. The process passed the previous crash point and shut down normally without another reported memory error or abnormal termination.

> Image needed: The original memory-corruption backtrace beside the patched run's 55-minute replay and clean shutdown results.

## A good matching score can still give a wrong position

Large position corrections continued after the crash fix. Results reported as converged by the Nano-GICP point-cloud registration algorithm could still include corrections of several meters or more.

In two field recordings from August 14, a fitness threshold of 0.25 would have accepted 24 of 27 and 89 of 103 results previously rejected for large corrections. The score alone could not distinguish those corrections, so correction distance and consistency across successive results also needed inspection.

> Image needed: Stored-map and current-scan overlays from the same timestamp, showing the fitness score, correction distance, and misaligned physical structures.

## Results and remaining work

The crash did not recur in the replay, but automatic recovery after losing position in the forest remained unresolved. Navigation could remain enabled while localization was searching for a position, requiring changes that connect localization confidence to permission to move.

A separate return-route failure involved FAST-LIO output stopping and then resuming with a large position jump. Monitoring processing stalls and resetting estimator state remain follow-up work. An unattended round trip, ditch avoidance, and fire or fallen-person detection have not been validated.
