---
slug: lk-ros
title: Robot system migration from ROS 1 to ROS 2
description: Migrated mapping, localization, and navigation to ROS 2, and investigated and reduced position-output delays during extended operation.
role: Robot software migration and runtime diagnosis
overview: >-
  I worked on migrating robot software between versions of the Robot Operating System (ROS).
  I moved mapping, localization, and navigation functions to ROS 2 and checked their connections.
  Extended-runtime tests revealed position-output delays that I investigated and addressed.
---

## Comparing behavior before and after migration

At LK Robotics, I worked on software migration and runtime checks. I compared data delivery and execution conditions to preserve existing functionality in the new environment.

After checking builds and connections, I examined whether processing delays accumulated during extended operation. Comparing sensor-input and output timestamps helped narrow down the cause, followed by comparison tests before and after the changes.
