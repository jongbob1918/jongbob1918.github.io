---
slug: lk-ros
title: Robot software migration to ROS 2
description: Ported the company’s robot software from ROS 1 Noetic to ROS 2 Humble and redesigned the system around ROS 2 and Nav2.
overview: >-
  I migrated the company’s robot software from ROS 1 Noetic to ROS 2 Humble.
  I ported the existing code and redesigned the autonomous navigation system around ROS 2 and Nav2.
  This changed the software foundation so the robot could use features available in the new environment.
demo:
  type: image
  src: ../assets/images/ros1-noetic-to-ros2-humble.png
  alt: Software migration from ROS 1 Noetic on the left to ROS 2 Humble on the right
---

## From ROS 1 Noetic to ROS 2 Humble

I migrated the Robot Operating System (ROS), the software framework that connects sensor-processing and robot-control programs. I ported the existing ROS 1 Noetic code to the ROS 2 Humble environment.

## Redesigning the navigation system

I redesigned autonomous navigation around Navigation2 (Nav2), which provides path planning and motion control. Alongside porting the existing code, I changed the system structure to use ROS 2 and Nav2 features.
