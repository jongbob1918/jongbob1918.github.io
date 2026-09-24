---
slug: lk-ros
title: Robot system migration from ROS 1 to ROS 2
description: Migrated mapping, localization and navigation to ROS 2, then removed an accumulating map-publication path that delayed position output during extended operation.
role: Robot software migration and runtime diagnosis
overview: >-
  This project connected ROS 2 navigation while retaining the robot's mapping and localization capabilities.
  I reorganized hardware communication, map management, and navigation execution for the new version of the Robot Operating System (ROS).
  After migration, I compared live sensor input and extended runtime behavior to fix delayed position output.
---

## Connecting sensor input to motion commands

At LK Robotics, I worked on migrating mapping, localization, and hardware communication to ROS 2. I separated sensor processing, map management, and motion execution, then connected them to Nav2, the ROS 2 navigation stack.

Map saving, loading, deletion, listing, and switching were exposed as services. Designated stair regions supplied paths and selected a dedicated controller. The stair behavior is described in [biped robot navigation](lk-biped.html).

> Image needed: A diagram connecting sensors, mapping and localization, map management, Nav2, and robot communication, highlighting the migrated components.

## Position output fell behind after extended operation

The system worked initially, but position output became delayed and estimates jumped during longer runs. LiDAR and inertial sensor input remained at 10 Hz and 200 Hz, while FAST-LIO output delay grew from approximately 0.14 to 0.68 seconds.

After comparing input rates and output delay, I checked the migrated code against the ROS 1 production version. A map-publication path unused in ROS 1 was active in ROS 2. It continuously accumulated scans and converted the entire point cloud into a message every second, creating a growing processing load.

> Image needed: A common timeline showing LiDAR and inertial sensor input rates alongside FAST-LIO output delay.

## Removing accumulated map publication

In a comparison run with accumulated map publication disabled, no position divergence was observed over one hour. I then removed the one-second publication path and separated raw point-cloud saving as a debugging function.

This establishes that divergence did not recur in that trial. It is not a position-accuracy measurement against an external reference. The detailed share of time spent processing sensors and publishing data still requires instrumentation.

> Image needed: Runtime plots comparing output delay and estimated position with accumulated map publication enabled and disabled.

## What was checked after migration

July development records document real-environment ROS 2 mapping validation and localization checks on flat ground, stairs, and floor transitions. Complete multi-floor missions and repeated success rates across different environments still require separate validation.

The migration required comparing runtime behavior with the production version after the build and topic connections worked. Follow-up checks should cover changing load and state, including extended operation, simultaneous camera use, and map switching.
