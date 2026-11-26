---
slug: ai-worker-auto-recorder
title: "ROBOTIS AI Worker: Autonomous Data Collection Pipeline"
description: Replaces human teleoperation with a grasp estimation model and motion planning. One click carries a grasp through to recording, and in simulation repeated collection runs automatically.
period: 2026.09–11
team: Personal project
role: ""
card:
  imageAlt: "An Autonomous Data Collection Pipeline title card, then a click on the target bottle in the web UI that starts Auto Pick, then an 8x-speed Isaac Lab scene where the AI Worker reaches for bottles at different positions"
overview: Teaching a robot to pick up objects takes many demonstrations, which are time-consuming to collect by teleoperation. I extended ROBOTIS’s open-source software so a click on a bottle in the web interface makes the AI Worker pick it up and save successful attempts. In Isaac Lab, I trained and evaluated separate policies on demonstrations from two grasp candidate generators.
demo:
  type: video
  src: ../assets/videos/ai-worker-auto-record-hero.mp4
  poster: ../assets/images/ai-worker-auto-record-hero-poster.webp
  autoplay: true
  alt: Automatic recording demo at 2x speed. While Auto Pick runs in the web UI on the left, the AI Worker picks up the bottle in Isaac Lab at top right, and RViz at bottom right shows the bottle point cloud and GraspNet grasp candidates
---

## System Setup

One click on a bottle in the web UI runs grasp inference, grasp motion generation, execution and recording without further human input.

![Four-stage automatic recording flow of target selection, grasp inference, grasp motion generation and execution with recording, where camera images and joint states are saved through cyclo_data](../assets/images/ai-worker-auto-record-pipeline.webp)

A finished motion command alone does not show a successful grasp, so command completion, object lift and save completion are checked separately. Only attempts where the bottle rises at least 3.5 cm, stays up for 0.5 s and finishes saving become successful demonstrations; failed attempts are logged but excluded from training.

### Detailed system diagram

The pipeline builds on two parts of Cyclo, the ROBOTIS robot software. Cyclo Intelligence handles data collection and management. Cyclo Control handles motion planning and control. On top of them, I added a pipeline that runs grasp inference, motion planning and recording to the end from a single click.

<div class="media-grid media-grid-natural"><figure class="feature-media"><img src="../assets/images/ai-worker-cyclo-intelligence.webp" alt="ROBOTIS Cyclo software stack with Cyclo Intelligence highlighted, covering data collection, data curation and model inference" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/ai-worker-cyclo-control.webp" alt="ROBOTIS Cyclo software stack with Cyclo Control highlighted, covering TCP control, MoveJ joint control and collision avoidance" loading="lazy"></figure></div>

By repository records, I made 96 commits alone between September 5 and October 22, 2026, and added a new automatic collection package of about 3,700 lines.

| Provided by open source | Implemented or modified by me |
| --- | --- |
| AI Worker robot model and ROS 2 control | Collection execution from grasp candidates through approach, lift and recording |
| Isaac simulation environment and robot USD (3D scene file) | Four-camera setup, coordinate alignment and sensor topics |
| GraspNet, CenterPose and GR00T models | Connecting both candidate generators to one workflow, success evaluation and evaluation procedure |

Grasp inference runs in `grasp_server`, a separate Docker container. The auto recording node (`/auto_recorder_node`) takes grasp candidates computed from the point cloud around the clicked point, then starts recording, approaches, grasps, closes the gripper, lifts and saves the recording in order.

![Detailed architecture where a web UI click reaches auto_recorder_node in cyclo_intelligence, grasp_server returns GraspNet candidates, ai_worker controllers execute an 8-step grasp sequence and cyclo_data records sensors and commands](../assets/images/ai-worker-auto-record-architecture.webp)

### Collecting bottle grasps

I loaded a break room furnished with real IKEA furniture as a simulation asset, rendered bottles into it and connected the automatic collection pipeline to the simulation. The only object so far is one green tea bottle.

Comparing on random layouts at first led to diverging interpretations. I then fixed the bottle at 40 positions in a 5-row by 8-column grid and repeated each position 10 times per method.

<video controls autoplay muted loop playsinline preload="metadata" aria-label="Automatic collection at 8x speed. The AI Worker repeatedly picks up bottles placed at different positions on the table in Isaac Lab"><source src="../assets/videos/ai-worker-auto-recorder-8x.mp4" type="video/mp4"></video>

![Top-down Isaac Lab view of 40 bottles in a 5-row by 8-column grid with the AI Worker body at the bottom; all bottles are shown together only to mark the positions, and evaluation used one bottle at a time](../assets/images/ai-worker-fixed40-locations.webp)

## Result

In Isaac Lab, I collected grasp demonstrations using one type of upright green tea bottle placed at 40 fixed positions. CenterPose with a bottle-specific grasp rule saved 319 successful demonstrations in 400 attempts (79.8%). GraspNet saved 310 in 400 attempts (77.5%).

I trained a separate Vision-Language-Action (VLA) policy on each dataset. Both policies succeeded in 75 of 120 grasps (62.5%) in simulation, using the same 40 positions as collection.

## Challenge 1: Comparing grasp candidate generators

### Problem

I used GraspNet first as the grasp candidate generator. Its results were uneven, so I connected CenterPose (an object pose estimation model) for comparison. CenterPose estimated the bottle’s tilt at a median of 13.6° in the nearest row and 25.7° in the farthest row. I used its estimated center and set the grasp direction with a rule for upright bottles. As a projection check, 9 markers across 6 frames differed from their rendered positions by 0.66 px on average.

### Collection comparison

| Collection | Attempts | Successful demonstrations |
| --- | --- | --- |
| Round 1 GraspNet (random layout) | 300 | 225 (75.0%) |
| Round 1 CenterPose (random layout) | 300 | 248 (82.7%) |
| Round 2 GraspNet (40 fixed positions) | 400 | 310 (77.5%) |
| Round 2 CenterPose (40 fixed positions) | 400 | 319 (79.8%) |

The gap between the two methods shrank from 7.7 percentage points in round 1 to 2.3 in round 2. The scene setups also differ, so I cannot confirm that fixing positions caused the change.

Of the 171 round-2 failures, 169 were cases where inverse kinematics (IK, computing arm joint angles for a target pose) rejected every candidate. The farthest row (X=0.295 m) succeeded in only 27 of 160 attempts, while the X=0.430 m and 0.475 m rows succeeded every time. I did not pre-check the 40 positions with IK, so I could not separate joint limits from collisions as the cause.

### Policy evaluation

I trained NVIDIA GR00T N1.7 (a VLA model that outputs actions from images, language and robot state) separately on the two round-2 datasets. Inputs are one head camera and two wrist cameras.

I evaluated each policy in three trials per position. Each trial lasted 30 seconds and used the same success rule as collection.

| Policy training data | Overall | X=0.295 | X=0.340 | X=0.385 | X=0.430 | X=0.475 |
| --- | --- | --- | --- | --- | --- | --- |
| 310 GraspNet demonstrations | 75/120 | 5/24 | 11/24 | 19/24 | 22/24 | 18/24 |
| 319 CenterPose demonstrations | 75/120 | 1/24 | 14/24 | 20/24 | 22/24 | 18/24 |

Overall successes were equal but differed by row. The row with the lowest policy success was the farthest row, which also had the fewest successful demonstrations during collection. With 3 trials per position, the sample is too small to generalize row-level differences.

## Challenge 2: Training memory limits

### Problem

On one RTX 5090 (32 GB), the default configuration ran out of memory at the first optimizer step. Using fused AdamW still exceeded the memory limit with the frozen language and vision backbone in 32-bit floating point (FP32).

### Solution

I loaded the frozen backbone in 16-bit floating point (BF16) and used fused AdamW. I trained approximately 1.62 billion of 3.14 billion parameters in the connector and action generator.

### Result

Training completed 150,000 steps with batch size 8 and a learning rate of 0.0001.

## Challenge 3: Arm command interference during evaluation

In the first evaluation, both policies almost never succeeded. I found that the controller holding the stored pose kept sending arm commands while paused. I disabled it, confirmed before every trial that no external arm command was present, and re-evaluated; the table above is that result.

## Limitations

Arm jitter made some test results unreliable.

| Limitation | Next validation |
| --- | --- |
| All results are from simulation | Separate evaluation with physical sensors, frames and gripper |
| Evaluated only at training positions, with one training run per dataset | Evaluate at positions not used in training |
| The cause of the farthest row's weakness is not isolated | IK pre-check of all 40 positions; retrain with equal per-position counts |
| Not compared with teleoperation data quality | Compare with a policy trained on the same amount of teleoperation data |
| Success ends at a 0.5 s hold, with one green tea bottle as the only object | Add a full-carry success rule and more object types |
