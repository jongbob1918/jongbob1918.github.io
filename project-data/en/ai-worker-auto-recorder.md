---
slug: ai-worker-auto-recorder
title: "ROBOTIS AI Worker: Autonomous Data Collection Pipeline"
description: Replaces human teleoperation with a grasp estimation model and motion planning. One click carries a grasp through to recording, and in simulation repeated collection runs automatically.
period: 2026.09–11
team: Personal project
role: ""
card:
  imageAlt: "An Autonomous Data Collection Pipeline title card, then a click on the target bottle in the web UI that starts Auto Pick, then an 8x-speed Isaac Lab scene where the AI Worker reaches for bottles at different positions"
overview: Training a Vision-Language-Action (VLA) model by imitation learning needs many demonstrations, and collecting them by human teleoperation takes a lot of time and money. To see whether a robot could take over this collection, I added a grasp estimation model and rule-based motion planning on top of ROBOTIS open source, building a pipeline in which the AI Worker picks up a bottle on its own and keeps only successful attempts. In Isaac Lab simulation, with a single type of green tea bottle, it made 800 attempts and collected 629 successful demonstrations. A VLA policy trained only on this data succeeded in 75 of 120 grasps on a 40-position evaluation I designed.
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

The pipeline builds on two parts of Cyclo, the ROBOTIS robot software: Cyclo Intelligence for data collection and management, and Cyclo Control for motion planning and control. On top of them, I added a pipeline that runs grasp inference, motion planning and recording to the end from a single click.

<div class="media-grid media-grid-wide"><figure class="feature-media"><img src="../assets/images/ai-worker-cyclo-intelligence.webp" alt="ROBOTIS Cyclo software stack with Cyclo Intelligence highlighted, covering data collection, data curation and model inference" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/ai-worker-cyclo-control.webp" alt="ROBOTIS Cyclo software stack with Cyclo Control highlighted, covering TCP control, MoveJ joint control and collision avoidance" loading="lazy"></figure></div>

By repository records, I made 96 commits alone between September 5 and October 22, 2026, and added a new automatic collection package of about 3,700 lines.

| Provided by open source | Implemented or modified by me |
| --- | --- |
| AI Worker robot model and ROS 2 control | Collection execution from grasp candidates through approach, lift and recording |
| Isaac simulation environment and robot USD (3D scene file) | Four-camera setup, coordinate alignment and sensor topics |
| GraspNet, CenterPose and GR00T models | Connecting both candidate generators to one workflow, success evaluation and evaluation procedure |

Grasp inference runs in `grasp_server`, a separate Docker container. The auto recording node (`/auto_recorder_node`) takes grasp candidates computed from the point cloud around the clicked point, then starts recording, approaches, grasps, closes the gripper, lifts and saves the recording in order.

![Detailed architecture where a web UI click reaches auto_recorder_node in cyclo_intelligence, grasp_server returns GraspNet candidates, ai_worker controllers execute an 8-step grasp sequence and cyclo_data records sensors and commands](../assets/images/ai-worker-auto-record-architecture.webp)

## Data Collection

I loaded a break room furnished with real IKEA furniture as a simulation asset, rendered bottles into it and connected the automatic collection pipeline to the simulation. The only object so far is one green tea bottle.

### Comparing GraspNet and CenterPose

I used GraspNet first as the grasp candidate generator. Its results were uneven, so I connected CenterPose (an object pose estimation model) for comparison. CenterPose still reports an upright bottle tilted by about 14 to 15 degrees, so it is paired with a bottle-specific grasp rule that assumes the bottle is standing. Camera input and projection are not the cause: 9 markers across 6 frames matched the rendered projection to a mean of 0.66 px.

Comparing on random layouts at first led to diverging interpretations. I then fixed the bottle at 40 positions in a 5-row by 8-column grid and repeated each position 10 times per method.

![Top-down Isaac Lab view of 40 bottles in a 5-row by 8-column grid with the AI Worker body at the bottom; all bottles are shown together only to mark the positions, and evaluation used one bottle at a time](../assets/images/ai-worker-fixed40-locations.webp)

| Collection | Attempts | Successful demonstrations |
| --- | --- | --- |
| Round 1 GraspNet (random layout) | 300 | 225 (75.0%) |
| Round 1 CenterPose (random layout) | 300 | 248 (82.7%) |
| Round 2 GraspNet (40 fixed positions) | 400 | 310 (77.5%) |
| Round 2 CenterPose (40 fixed positions) | 400 | 319 (79.8%) |

The gap between the two methods shrank from 7.7 percentage points in round 1 to 2.3 in round 2. The scene setups also differ, so I cannot confirm that fixing positions caused the change.

Of the 171 round-2 failures, 169 were cases where inverse kinematics (IK, computing arm joint angles for a target pose) rejected every candidate. The farthest row (X=0.295 m) succeeded in only 27 of 160 attempts, while the X=0.430 m and 0.475 m rows succeeded every time. I did not pre-check the 40 positions with IK, so I could not separate joint limits from collisions as the cause.

## Policy & Training

I trained NVIDIA GR00T N1.7 (a VLA model that outputs actions from images, language and robot state) separately on the two round-2 datasets. Inputs are one head camera and two wrist cameras.

On one RTX 5090 (32 GB), the default configuration ran out of memory at the first optimizer step and never completed an update. Keeping the frozen language and vision parts (the backbone) in FP32 still ran out of memory even with fused AdamW; loading the backbone in BF16 (16-bit floating point) together with fused AdamW let training run.

The language model and vision encoder stayed frozen, and about 1.62 billion of roughly 3.14 billion parameters (the connector and action generator) were trained, with batch size 8 and learning rate 0.0001 for 150,000 steps.

### Simulation evaluation

Evaluation covers the same 40 positions × 3 trials × 2 models, 240 trials in total. Each trial lasts 30 seconds with the same success rule as collection. It reuses the training positions, so it does not measure generalization to new positions.

| Policy training data | Overall | X=0.295 | X=0.340 | X=0.385 | X=0.430 | X=0.475 |
| --- | --- | --- | --- | --- | --- | --- |
| 310 GraspNet demonstrations | 75/120 | 5/24 | 11/24 | 19/24 | 22/24 | 18/24 |
| 319 CenterPose demonstrations | 75/120 | 1/24 | 14/24 | 20/24 | 22/24 | 18/24 |

Overall successes were equal but differed by row. The row with the lowest policy success was the farthest row, which also had the fewest successful demonstrations during collection. With 3 trials per position, the sample is too small to generalize row-level differences.

In the first evaluation, both policies almost never succeeded. I found that the controller holding the stored pose kept sending arm commands while paused. I disabled it, confirmed before every trial that no external arm command was present, and re-evaluated; the table above is that result.

### Limitations

Arm jitter made some test results unreliable.

| Limitation | Next validation |
| --- | --- |
| All results are from simulation | Separate evaluation with physical sensors, frames and gripper |
| Evaluated only at training positions, with one training run per dataset | Evaluate at positions not used in training |
| The cause of the farthest row's weakness is not isolated | IK pre-check of all 40 positions; retrain with equal per-position counts |
| Not compared with teleoperation data quality | Compare with a policy trained on the same amount of teleoperation data |
| Success ends at a 0.5 s hold, with one green tea bottle as the only object | Add a full-carry success rule and more object types |
