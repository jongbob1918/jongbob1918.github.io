---
slug: lk-patrol
title: Royal heritage patrol robot
description: Developed autonomous navigation software for a robot that patrols Seooreung in Goyang to detect fires and fallen people. Improved obstacle perception and motion control for repeated runs along a 2 km patrol route.
role: Autonomous navigation software development for the patrol robot
overview: >-
  This project is a patrol robot that detects fires and fallen people at Seooreung in Goyang.
  I developed autonomous navigation, mission execution, and docking functions.
  I adapted localization and motion control to the site for repeated runs along a 2 km route with dirt paths and slopes.
---

## Dirt paths and slopes at Seooreung

Most of the patrol route consists of dirt paths with slopes and uneven ground. Rain can wash away soil and change the path surface and height differences. The existing fixed-height obstacle detection struggled to distinguish sloping ground from actual obstacles.

## Separating ground from obstacles

I applied ground segmentation to data from a 3D Light Detection and Ranging (LiDAR) sensor, which measures the shape of the surroundings. I replaced the existing 2D obstacle handling with terrain-aware processing, using the distinction between sloping ground, steps, and obstacles for navigation.

I also added exception handling and tuned simultaneous localization and mapping (SLAM) and map-based localization for the site.

## Improving startup acceleration and velocity commands in narrow spaces

The wheeled biped robot’s reinforcement-learning-based motion control could accelerate sharply at startup even with the same velocity command. I investigated acceleration handling in the Humble version of the Model Predictive Path Integral (MPPI) controller used in the Navigation2 (Nav2) navigation stack. MPPI evaluates candidate trajectories to produce velocity commands.

I first applied an exponential moving average (EMA) filter to smooth abrupt changes in the velocity commands. However, excessive MPPI velocity commands remained under conditions where obstacle costs left little traversable space in the map.

After analyzing the Humble implementation, I ported the Kilted MPPI controller to improve acceleration handling and excessive velocity output in narrow spaces. Its acceleration constraints can be found in the [official Kilted source code](https://api.nav2.org/nav2-kilted/html/motion__models_8hpp_source.html).

## Stopping and announcing when people approach

I changed the behavior from frequent avoidance maneuvers when people approached to stopping and playing an announcement when a person was detected within the configured safety zone. This added mission exception handling for a patrol route shared with visitors.

## Docking and undocking

I developed docking to enter the docking position and undocking to leave it.

## Repeated runs along a 2 km route

I carried out multiple runs along the 2 km patrol route at Seooreung and adjusted the algorithms to the site.

<figure class="feature-media"><a href="https://www.youtube.com/watch?v=kHgA8jEmoCw&amp;t=22s" target="_blank" rel="noopener noreferrer"><img src="../assets/images/lk-patrol-seooreung-channela.jpg" alt="Patrol robot driving along a dirt path at Seooreung — watch on Channel A YouTube" loading="lazy"></a><figcaption>Robot navigating at Seooreung · Channel A News · September 4, 2026</figcaption></figure>
