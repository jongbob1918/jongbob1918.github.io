---
slug: lk-ros
title: Robot software migration to ROS 2
description: Migrated a ROS 1 Noetic system to ROS 2 Humble, ported selected algorithms, and introduced behavior-tree decision-making and functional modules designed for reuse across robots.
overview: >-
  I was responsible for migrating the company’s robot software to ROS 2 Humble.
demo:
  type: image
  src: ../assets/images/ros1-noetic-to-ros2-humble.png
  alt: Software migration from ROS 1 Noetic on the left to ROS 2 Humble on the right
---

## Problem Statement

The existing system used the Robot Operating System (ROS) 1 Noetic framework and the move_base navigation package. A state machine managed robot behavior by selecting the next action based on the current state and transition conditions.

[Official support for ROS 1 Noetic ended on May 31, 2025](https://www.ros.org/blog/noetic-eol/). The algorithms available in the existing move_base configuration and its system structure also limited further service development. I migrated the system to ROS 2 Humble and redesigned navigation and decision-making.

## Porting selected algorithms to ROS 2

I selected the components needed by the new system rather than porting the entire codebase. These included simultaneous localization and mapping (SLAM) using a 3D Light Detection and Ranging (LiDAR) sensor, and localization against prebuilt maps. I ported these components to ROS 2 Humble.

Path planning and motion control were organized around Navigation2 (Nav2).

## Behavior trees and functional modules

I replaced the state-machine-based decision structure with a behavior tree, which organizes condition checks and action execution into a tree.

<figure class="feature-media"><a href="https://docs.nav2.org/rolling/getting_started/nav2_behavior_trees/detailed_behavior_tree_walkthrough/detailed_behavior_tree_walkthrough/" target="_blank" rel="noopener noreferrer"><img src="../assets/images/nav2-navigation-behavior-tree.png" alt="Official Nav2 behavior tree example connecting ComputePathToPose and FollowPath under NavigateWithReplanning" loading="lazy"></a></figure>

I separated decision-making from individual functions and organized the system into four modules.

| Module | Responsibility |
| --- | --- |
| Mapping and localization | 3D LiDAR SLAM and localization against prebuilt maps |
| Navigation | Nav2-based path planning and motion control |
| Control-center communication | Communication between the robot and the control-center system |
| Decision-making | Behavior-tree condition checks and action execution flow |

The modular structure was designed to support reuse across multiple robots.
