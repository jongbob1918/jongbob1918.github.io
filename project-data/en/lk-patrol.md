---
slug: lk-patrol
title: Royal heritage patrol robot
description: Developed autonomous navigation software for a robot that patrols Seooreung in Goyang to detect fires and fallen people. Improved obstacle perception and motion control for repeated runs along a 2 km patrol route.
role: Autonomous navigation software development for the patrol robot
overview: >-
  I contributed autonomous navigation software to the development of a royal heritage patrol robot in collaboration with the Korea Heritage Service. Built on a wheeled biped platform, the robot detects fires and fallen people at Seooreung in Goyang.
---

## Localization errors in woodland and grass-covered areas

Seooreung in Goyang is a [heritage site covering approximately 1.87 million m²](https://heritage.go.kr/heri/cul/culSelectDetail.do?ccbaAsno=0001980000000&ccbaCpno=1333101980000&ccbaCtcd=31&ccbaKdcd=13&pageNo=1_1_1_0), with extensive woodland, undergrowth, and lawns. Parts of the patrol area lacked distinctive features for localization. Local matching, which aligns sensor data with a prebuilt map, could incorrectly place the robot several meters ahead or fail to find a match.

The existing system responded to local matching failures by searching the entire map through global localization. On a large prebuilt map, identifying the correct candidate position was difficult and computational load increased.

### Splitting maps and linking transition points

I divided the patrol area and mapped each section separately. I connected the maps with waypoints and loaded the relevant map when the robot reached a transition point. This reduced the map area processed at once and resource usage.

### Building a replay-based experiment workflow

Weather and battery constraints made it difficult to revisit the site for every algorithm or parameter change. There was no existing workflow for recording, replaying, and comparing sensor data. I collected field data over a week using rosbag, a ROS message recording tool, and used it for repeatable experiments.

I defined acceptance criteria, candidate algorithms, and parameter combinations, then used agents to run replay experiments in parallel. I identified settings that avoided localization jumps across multiple recordings and restricted acceptance of local matching results to a configured tolerance.

I also visualized and compared intervals where incorrect matching candidates were selected. This let me check mismatches the agents could miss and refine the algorithms and parameters.

## Incorrect initial poses after map transitions

I implemented navigation so that a goal in another map led the robot through the required transition waypoints, switched maps, and continued to the goal. However, localization could shift if the initial pose in the new map was not specified accurately.

I aligned the prebuilt maps using Iterative Closest Point (ICP), a point-cloud registration algorithm, and stored the resulting inter-map coordinate transforms in a shared interface. I linked transition waypoints to the same physical location in both maps and used this correspondence to set the initial pose after switching. This reduced inconsistencies caused by specifying transition positions separately in each map.

## Obstacle perception on slopes and uneven ground

Most of the patrol route consists of dirt paths. Even apparently flat sections differ in elevation, and rain can wash away soil and change the surface and height differences.

The existing indoor navigation system detected obstacles using z-axis height in the robot’s reference frame. Outdoors, elevation changes on slopes and uneven sections caused traversable ground to be classified as obstacles.

I applied ground segmentation to data from a 3D Light Detection and Ranging (LiDAR) sensor, which measures the shape of the surroundings. Navigation used the distinction between ground and obstacles rather than a fixed height threshold, allowing obstacle avoidance to account for changes in terrain height.

## Improving startup acceleration and velocity commands in narrow spaces

The wheeled biped robot’s reinforcement-learning-based motion control could accelerate sharply at startup even with the same velocity command. I investigated acceleration handling in the Humble version of the Model Predictive Path Integral (MPPI) controller used in the Navigation2 (Nav2) navigation stack. MPPI evaluates candidate trajectories to produce velocity commands.

I first applied an exponential moving average (EMA) filter to smooth abrupt changes in the velocity commands. However, excessive MPPI velocity commands remained under conditions where obstacle costs left little traversable space in the map.

After analyzing the Humble implementation, I ported the Kilted MPPI controller to improve acceleration handling and excessive velocity output in narrow spaces. Its acceleration constraints can be found in the [official Kilted source code](https://api.nav2.org/nav2-kilted/html/motion__models_8hpp_source.html).

## Stopping and announcing when people approach

I changed the behavior from frequent avoidance maneuvers when people approached to stopping and playing an announcement when a person was detected within the configured safety zone. This added mission exception handling for a patrol route shared with visitors.

## Docking and undocking

I developed docking to enter the docking position and undocking to leave it.

## Repeated runs along a 2 km route

After checking localization settings and matching results on recorded data, I completed multiple round trips along the patrol route at Seooreung. I used both replay experiments and field runs to improve localization stability.

<figure class="feature-media"><a href="https://www.youtube.com/watch?v=kHgA8jEmoCw&amp;t=22s" target="_blank" rel="noopener noreferrer"><img src="../assets/images/lk-patrol-seooreung-channela.jpg" alt="Patrol robot driving along a dirt path at Seooreung — watch on Channel A YouTube" loading="lazy"></a><figcaption>Robot navigating at Seooreung · Channel A News · September 4, 2026</figcaption></figure>
