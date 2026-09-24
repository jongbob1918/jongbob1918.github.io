---
slug: lk-biped
title: Biped navigation on flat ground and stairs
description: Connected stair center paths to a dedicated controller and used physical entry-angle trials to examine alignment conditions and limits.
role: Path planning, stair control and floor-map transition integration
overview: >-
  The wheeled biped TRON1 needs different driving behavior on flat ground and stairs to move through a building.
  I connected segment-specific paths and controllers using stair regions and entry and exit points marked on the map.
  The robot approaches the stair entrance, aligns, and follows a center path; physical trials examined entry conditions and remaining limits.
---

## Connecting flat-ground routes to stair traversal

At LK Robotics, I worked on TRON1 path planning, stair control, and floor-map transition integration. The navigation layer generated target paths and velocity commands above the manufacturer's balance and locomotion controller.

I used Nav2, the navigation stack for Robot Operating System (ROS) 2. When a route intersects a mapped stair region, it is divided into normal and stair segments. Lower and upper anchor points define a stair center path, and the path and dedicated controller are selected when that segment executes.

> Image needed: A physical TRON1 stair trial beside a map showing the normal route, stair region, entry point, and exit point.

## Aligning before following the center path

Entry direction and lateral clearance matter on stairs, so I separated alignment, traversal, and arrival. The dedicated controller adjusts angular velocity using heading and cross-track errors, with separate speed settings for ascent and descent. It also checks lateral departure, overshoot, and timeout.

On July 16, 2026, I conducted manual entry-angle trials on four steps with a 180 mm rise and 300 mm tread depth.

| Entry angle | Successes / attempts | Observation |
| --- | --- | --- |
| 0° | 3 / 3 | Three successful straight entries |
| 10° | 1 / 2 | A failure at the same angle |
| 20° | 1 / 1 | Insufficient repeated trials |
| 30° | 0 / 1 | Lateral slipping |

The 30° trial used a different speed command, so the result cannot isolate the effect of entry angle. One success at 20° also does not establish an allowable limit. Entry alignment remains necessary, and angle and speed limits require repeated trials.

> Image needed: A plan view with stair dimensions and entry angles, plus image sequences comparing straight entry with lateral slipping at 30°.

## Updating route references when changing floors

Changing floors requires updating stair regions and anchor data along with the destination map. If a new-floor path is evaluated against the previous floor's regions, the system can select the wrong stair entry direction.

Execution connects destination-floor preparation, the map-switch request, current-floor state updates, and a wait for localization readiness. During transition diagnosis, I checked both the map data read by route analysis and the ascent or descent direction passed to the stair controller. Data updates after the map-switch response must also be verified.

> Image needed: A sequence diagram showing map, stair-anchor, and current-floor state changes during a third-to-fourth-floor transition.

## Limits observed in physical trials

Initial navigation and stopping on person detection were tested on a fixed stair setup. Deceleration around moving people was insufficient in a separate trial, and wet or reflective stairs still caused depth errors and missing measurements. The person-detection stop test does not establish dynamic obstacle-avoidance performance.

An August trial also revealed a stall before switching to the stair controller: the normal navigation controller struggled to satisfy entrance position and heading together. Follow-up work is to test entry alignment and stair traversal separately, then repeat validation with different stair geometry and obstacle conditions.
