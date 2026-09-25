---
slug: lk-ros
title: Robot system migration from ROS 1 to ROS 2
description: Ported mapping, localization, and navigation code to ROS 2 and fixed delayed position output during long runs.
role: ROS 2 porting, functional testing and latency analysis
overview: >-
  I ported existing ROS 1 robot software to ROS 2.
  The Robot Operating System (ROS) is a software framework used to develop sensor-processing and robot-control programs.
  I tested mapping, localization, and navigation after the migration.
---

## Testing after the port

I compared the original and ported code to check data delivery and processing. After the build passed, I connected sensors and tested each function.

Long-running tests revealed delayed position output. I measured the delay between sensor input and position output to investigate the cause, then changed the code and repeated the test under the same conditions.
