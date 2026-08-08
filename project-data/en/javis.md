---
slug: javis
title: JAVIS — Library Management Robot
description: A ROS 2 library robot integrating autonomous navigation, manipulation, and vision AI
team: 9 members
period: Sep–Nov 2024
role: Navigation stabilization · Robot state and mission control
overview: >-
  Libraries require continuous staff time for repetitive work such as book pickup, returns, and visitor guidance. JAVIS connects a VIC-PINKY mobile base, a myCobot manipulator, and vision AI through ROS 2 to automate these tasks. The mobile base navigates to the target shelf, and the manipulator identifies, picks up, and returns books with its camera.
demo:
  type: image
  src: ../assets/images/javis_robot_drive.gif
  alt: JAVIS navigating in a real library
  sequence:
    - src: ../assets/images/javis_robot_drive.gif
      alt: JAVIS navigating in a real library
      duration: 28000
    - src: ../assets/images/javis_nav_rviz.gif
      alt: JAVIS navigating a narrow aisle in RViz
      duration: 7510
---

## Book pickup service

When a user requests a book, the central system checks the robot's status and battery level before assigning the task. JAVIS travels to the target shelf, identifies the book with a camera, and picks it up with the manipulator.

<figure class="feature-media"><img src="../assets/images/javis_book_pickup_pipeline.png" alt="Service flow from book selection and authentication to JAVIS pickup and delivery" loading="lazy"></figure>

## Autonomous navigation for pickup and return

JAVIS must pass through narrow aisles and stop at a designated shelf to pick up or return a book. We created an occupancy-grid map with Cartographer and a 2D LiDAR, then removed unnecessary regions and corrected shelf boundaries with a map editor.

<figure class="feature-media"><img src="../assets/images/javis_library_map.webp" alt="Library occupancy map showing shelves, aisles, waypoints, and the robot position" loading="lazy"><figcaption>2D library occupancy map generated with Cartographer</figcaption></figure>

The first configuration used Nav2's DWB Controller. It worked in open areas, but repeatedly stopped when it could not find a feasible turning trajectory in narrow or blocked spaces. Increasing costmap inflation made aisles appear impassable, while reducing it brought the robot too close to shelves.

<figure class="feature-media"><img src="../assets/images/javis_navigation_failure.gif" alt="Early DWB navigation test in which JAVIS cannot turn in a narrow space" loading="lazy"><figcaption>Early DWB test failing to turn in a narrow aisle</figcaption></figure>

I replaced the global planner with Smac Planner Hybrid, which accounts for the rectangular footprint, turning radius, and reverse paths. I tuned the LiDAR filters and inflation values to the physical robot and applied the MPPI Controller to evaluate multiple candidate trajectories.

<figure class="feature-media"><img src="../assets/images/javis_nav_rviz.gif" alt="JAVIS following a narrow-aisle route with Smac Planner Hybrid and MPPI in RViz" loading="lazy"><figcaption>Navigating a narrow aisle after applying Smac Planner Hybrid and MPPI</figcaption></figure>

Tests in the real library confirmed that JAVIS could pass narrow shelves and low-clearance turning areas to reach its pickup and return positions.

## Robot state and mission control

I divided the top-level behavior into initialization, charging, idle, task execution, and return-to-charger states. Each mission step checks completion, failure, and cancellation responses from lower-level modules. Battery conditions or an emergency-stop request move the system from the active mission into a recovery or safe state.

<figure class="feature-media"><img src="../assets/images/javis_state_machine.png" alt="JAVIS state transitions for initialization, charging, idle, tasks, return, and emergency stop" loading="lazy"></figure>

## Robot status monitoring

During hardware integration, I developed a monitoring GUI that displays the current state, subtask, battery level, and ROS logs in one view. It helped identify the exact step where a mission stopped and trace module completion or failure responses while validating state transitions and exception handling.

<figure class="feature-media"><img src="../assets/images/javis_status_gui.png" alt="Monitoring GUI displaying JAVIS state, subtask, battery, and ROS logs" loading="lazy"></figure>

## State-transition and exception tests

We defined a shared interface so integration could continue without waiting for every AI, navigation, and manipulation module. Real and mock modules use the same command and response structure, allowing the main controller to switch implementations without code changes.

<div class="media-stack"><figure class="feature-media"><img src="../assets/images/javis_interface_mock_architecture.png" alt="JAVIS interface architecture separating real and mock modules" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/javis_mock_test_gui.gif" alt="GUI for testing JAVIS control flow with configurable mock responses" loading="lazy"></figure></div>

Mock responses reproduced successful completion, execution failure, and cancellation. This allowed repeated validation of state transitions, exception handling, and lower-level call order before connecting the physical equipment.
