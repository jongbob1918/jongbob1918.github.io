---
slug: lk-patrol
title: Royal heritage patrol robot
description: Developed autonomous navigation software for a robot that patrols Seooreung in Goyang to detect fires and fallen people. Improved obstacle perception and motion control for repeated runs along a 2 km patrol route.
role: Autonomous navigation software development for the patrol robot
overview: >-
  I contributed autonomous navigation software to the development of a royal heritage patrol robot in collaboration with the Korea Heritage Service. Built on a wheeled biped platform, the robot detects fires and fallen people at Seooreung in Goyang.
demo:
  type: image
  src: ../assets/images/lk-patrol-seooreung-channela.jpg
  alt: Patrol robot driving along a dirt path at Seooreung — watch on Channel A YouTube
  href: https://www.youtube.com/watch?v=kHgA8jEmoCw&t=22s
  caption: Robot navigating at Seooreung · Channel A News · September 4, 2026
---

## Problem Statement

Seooreung in Goyang is a [heritage site covering approximately 1.87 million m²](https://heritage.go.kr/heri/cul/culSelectDetail.do?ccbaAsno=0001980000000&ccbaCpno=1333101980000&ccbaCtcd=31&ccbaKdcd=13&pageNo=1_1_1_0), with extensive woodland, undergrowth, and lawns. Most of the patrol route consists of dirt paths with slopes and uneven ground. Rain can wash away soil and change the terrain.

The task was to maintain localization and repeatedly navigate a 2 km patrol route in this environment. The main issues were incorrect localization matches, initial-pose errors after map transitions, ground misclassified as obstacles, and abrupt acceleration or excessive velocity commands.

## System Setup

The wheeled biped robot used the Robot Operating System (ROS) 2 framework and the Navigation2 (Nav2) navigation stack. Data from a 3D Light Detection and Ranging (LiDAR) sensor supported localization against prebuilt maps and ground–obstacle separation.

I also developed mission execution, docking, and undocking. When people approached, I replaced frequent avoidance maneuvers with stopping and playing an announcement when a person was detected within the configured safety zone.

## Challenge 1: Localization in woodland and grass-covered areas

### Problem

Local matching, which aligns sensor data with a prebuilt map, could incorrectly place the robot several meters ahead or fail entirely. The fallback global localization searched the entire map, but struggled to find the correct candidate and increased computational load.

### Root Cause

Some woodland and grass-covered sections lacked distinctive features for localization. Searching a large prebuilt map made candidate positions difficult to distinguish and increased the area to process.

### Solution

I mapped each section separately and connected the maps with waypoints. Given a goal, the robot travels through the required transition points, loads the relevant map, and continues to the destination.

This reduced the map area processed at once. I also restricted acceptance of local matching results to a configured tolerance.

Weather and battery constraints made it difficult to revisit the site for every algorithm or parameter change. I collected field sensor data over a week using rosbag, a ROS message recording tool, and built a workflow for replaying and comparing data.

I defined acceptance criteria, candidate algorithms, and parameter combinations, then used agents to run replay experiments in parallel. I visualized and compared intervals with incorrect matching candidates to check mismatches the automated experiments could miss.

### Result

Map splitting reduced the processing area and resource usage. I identified settings that avoided localization jumps across multiple recordings and applied them to field navigation.

## Challenge 2: Initial-pose errors after map transitions

### Problem

After splitting the maps, localization could shift if the initial pose was not specified accurately when switching maps.

### Root Cause

Transition positions specified separately in each map were not aligned to the same physical location. The initial pose needed to be set in the new map’s coordinate frame.

### Solution

I aligned the prebuilt maps using Iterative Closest Point (ICP), a point-cloud registration algorithm, and stored the resulting inter-map coordinate transforms in a shared interface. I linked transition waypoints to the same physical location in both maps and used this correspondence to set the initial pose after switching.

### Result

This reduced inconsistencies between independently specified transition positions. Initial poses were set using the coordinate relationship between the maps.

## Challenge 3: Obstacle perception on slopes and uneven ground

### Problem

Traversable ground was classified as an obstacle on slopes and uneven sections.

### Root Cause

The existing indoor navigation system detected obstacles using z-axis height in the robot’s reference frame. At Seooreung, even apparently flat sections differ in elevation, and rain changes the surface. A fixed height threshold could not reliably distinguish ground from obstacles.

### Solution

I applied ground segmentation to 3D LiDAR data. Navigation used the distinction between ground and obstacles so that obstacle avoidance accounted for changes in terrain height.

## Challenge 4: Startup acceleration and velocity output in narrow spaces

### Problem

The reinforcement-learning-based motion control could accelerate sharply at startup even with the same velocity command. I investigated acceleration handling in the Humble version of the Model Predictive Path Integral (MPPI) controller, which evaluates candidate trajectories to produce velocity commands.

### First Approach

I applied an exponential moving average (EMA) filter to smooth abrupt changes in velocity commands.

### Remaining Problem

Excessive MPPI velocity commands remained when obstacle costs left little traversable space in the map. Filtering the output alone was insufficient, so I investigated the controller implementation.

### Solution

After analyzing the Humble implementation, I ported the Kilted MPPI controller. Its acceleration constraints can be found in the [official source code](https://api.nav2.org/nav2-kilted/html/motion__models_8hpp_source.html).

### Result

I improved startup acceleration handling and excessive velocity output in narrow spaces.

## Field Validation

After checking localization settings and matching results on recorded data, I completed multiple round trips along the patrol route at Seooreung. I used both replay experiments and field runs to improve localization stability.
