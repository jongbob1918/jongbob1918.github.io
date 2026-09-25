---
slug: lk-biped
title: Indoor multi-floor navigation system design
description: Designed an indoor multi-floor navigation system for a wheeled biped robot, centered on gimbal scanning, elevation mapping, and navigation between floors.
overview: >-
  I designed an indoor multi-floor navigation system and developed gimbal scanning for a wheeled biped robot.
---

## Problem Statement

Patrolling multiple indoor floors required connecting flat-ground navigation, stair entry and traversal, map switching, and navigation on the destination floor. Stair traversal also needed to account for terrain height and robot posture, while observation tasks required operating a gimbal after reaching a destination.

The engineering tasks were to coordinate floor transitions, incorporate terrain height into stair navigation, and connect navigation with observation tasks.

## System Setup

The TRON1 wheeled biped robot used the Robot Operating System (ROS) 2 Humble framework and Navigation2 (Nav2) for path planning and motion control.

| Component | Role |
| --- | --- |
| 3D Light Detection and Ranging (LiDAR) sensor | Prior mapping and localization |
| Color and depth (RGB-D) camera | Near-field geometry and depth observation |
| Elevation map | Grid representation of ground height for stair navigation |
| Behavior tree | Execution flow for navigation, map switching, and observation |
| Gremsy VIO gimbal camera | Camera orientation and visible-light/thermal observation |

## Challenge 1: Connecting floor transitions and map switching

### Problem

Navigation within a single floor could not take the robot to a destination on another floor. The system needed to reach a stair entry, traverse the stairs, and prepare the destination map and localization state.

### Solution

I designed a graph of key locations and traversable connections, using A* search to plan routes between floors. Planning and execution were separated so that a route could be converted into navigation, stair traversal, and map-switching tasks.

In ROS 2, a behavior tree connected navigation to the stair entry, distance-controlled entry motion, destination map activation, and a wait for localization readiness. The next navigation task depended on localization being ready for the new map.

### Remaining Problem

A map switch could leave a stair-analysis module using information from the previous floor, causing incorrect entry-direction or ascent/descent decisions. Map data, zone information, and the current floor state all needed consistent updates.

I separated map-switch requests, zone metadata updates, and localization readiness into individual checks to trace this issue.

## Challenge 2: Incorporating stair height into navigation

### Problem

Stair navigation needed to account for height changes, landings, and turns. Some passages also overlapped at the same horizontal position, so a map storing one height per position could not represent the entire building.

### Solution

I separated route planning across floors from the local elevation map around the robot. I implemented a controller that follows stair paths using elevation data and checks for obstacles ahead. It applies ascent/descent speed and alignment policies, prioritizing a stop when dynamic obstacles are detected.

I also investigated dividing prior point-cloud maps into height layers to represent overlapping surfaces. Combining prior terrain with live elevation observations was documented as a follow-up design.

### Remaining Problem

Missing depth data could distort stair geometry in the elevation map and mark traversable areas as blocked. Further diagnosis needed to distinguish failures in raw sensor data, coordinate transforms, and map integration.

Beyond controller implementation, real-stair validation remained for coordinate alignment, obstacle stop/resume behavior, and repeated runs.

## Challenge 3: Gimbal scanning and task interruption after navigation

### Problem

Scanning at a destination still needed to respond to cancellation, emergency stops, and new tasks. An independent scan could continue after the parent task ended, so task state and gimbal motion needed coordinated handling.

### Solution

I connected navigation followed by gimbal scanning in a behavior tree. Cancellation, emergency stops, and preemption by a new task stop the scan and trigger a return motion.

I implemented sector, bowtie, and look-around patterns with configurable scan limits. Mounted-hardware trials exposed vibration and speed issues, leading to stepwise yaw/pitch motion and adjustments to movement and pause durations.

### Result

The gimbal scanning feature underwent build checks and automated tests. I also tested patterns on the mounted hardware and adjusted the motion.

## Validation & Next Steps

Field checks covered localization on flat ground, stairs, and floor-transition segments, as well as gimbal communication and camera control. Inspection start, save, and stop operations were also checked on the robot.

Repeated end-to-end multi-floor runs and hardware validation of the elevation-based stair controller remained follow-up work. Test cases were organized around stair ascent/descent, static obstacles, and people crossing the route.
