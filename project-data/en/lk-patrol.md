---
slug: lk-patrol
title: Royal heritage patrol robot
description: Developed autonomous navigation software for a robot that patrols Seooreung in Goyang to detect fires and fallen people. Improved obstacle perception and motion control for repeated runs along a 2 km patrol route.
role: Autonomous navigation software development for the patrol robot
introduction: >-
  I developed autonomous navigation software for an outdoor patrol robot that detects fires and fallen people at Seooreung in Goyang. My work covered localization, motion control, mission execution, and docking.
---

## Dirt paths and slopes at Seooreung

Most of the 2 km patrol route at Seooreung consists of dirt paths with slopes and uneven ground. Rain can wash away soil and change the path surface and height differences. Since visitors share the route, navigation had to account for both terrain and approaching people.

<figure class="feature-media"><a href="https://www.youtube.com/watch?v=kHgA8jEmoCw&amp;t=22s" target="_blank" rel="noopener noreferrer"><img src="../assets/images/lk-patrol-seooreung-channela.jpg" alt="Patrol robot driving along a dirt path at Seooreung — watch on Channel A YouTube" loading="lazy"></a><figcaption>Robot navigating at Seooreung · Channel A News · September 4, 2026</figcaption></figure>

## Distinguishing slopes from obstacles

The existing fixed-height obstacle detection struggled to distinguish sloping ground from actual obstacles.

I applied ground segmentation to data from a 3D Light Detection and Ranging (LiDAR) sensor, which measures the shape of the surroundings. I replaced the existing 2D obstacle handling with terrain-aware processing, using the distinction between sloping ground, steps, and obstacles for navigation.

## Reducing abrupt acceleration and excessive velocity commands

### Abrupt acceleration at startup

The wheeled biped robot’s reinforcement-learning-based motion control could accelerate sharply at startup even with the same velocity command. I investigated acceleration handling in the Humble version of the Model Predictive Path Integral (MPPI) controller used in the Navigation2 (Nav2) navigation stack. MPPI evaluates candidate trajectories to produce velocity commands.

### Filtering velocity commands

I first applied an exponential moving average (EMA) filter to smooth abrupt changes in the velocity commands. However, excessive MPPI velocity commands remained under conditions where obstacle costs left little traversable space in the map.

### Remaining issues in narrow spaces and porting MPPI

After analyzing the Humble implementation, I ported the Kilted MPPI controller to improve acceleration handling and excessive velocity output in narrow spaces. Its acceleration constraints can be found in the [official Kilted source code](https://api.nav2.org/nav2-kilted/html/motion__models_8hpp_source.html).

## Stopping and announcing when people approach

I changed the behavior from frequent avoidance maneuvers when people approached to stopping and playing an announcement when a person was detected within the configured safety zone. This added mission exception handling for a patrol route shared with visitors.

## Field integration and repeated runs

I also added exception handling and tuned simultaneous localization and mapping (SLAM) and map-based localization for the site. I also developed docking and undocking to enter and leave the docking position.

I carried out multiple runs along the 2 km patrol route at Seooreung and adjusted the algorithms to the site.
