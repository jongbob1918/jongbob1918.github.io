---
slug: ai-worker-auto-recorder
title: "ROBOTIS AI Worker: Autonomous Data Collection Pipeline"
description: I combined grasp estimation with rule-based motion planning so the ROBOTIS AI Worker can pick up objects and save successful episodes automatically. I collected 319 successful demonstrations in 400 attempts in Isaac Lab. A Vision-Language-Action (VLA) policy trained on that dataset achieved a 62.5% grasp success rate in a 40-position evaluation.
period: 2026.09–11
team: Personal project
role: ""
card:
  imageAlt: "An Autonomous Data Collection Pipeline title card, then a click on the target bottle in the web UI that starts Auto Pick, then an 8x-speed Isaac Lab scene where the AI Worker reaches for bottles at different positions"
overview: Vision-Language-Action (VLA) models and imitation learning have made precise robot control possible, but collecting high-quality training data through manual teleoperation takes considerable time and money. I extended ROBOTIS's open-source software with a grasp estimation model and rule-based motion planning so the AI Worker could pick up objects on its own and save only successful episodes. In about six hours, the pipeline logged 800 attempts and saved 629 successful demonstrations (2.98 hours of recorded footage, a 78.6% success rate). I trained a separate VLA policy on each of the two datasets, and both achieved a 62.5% grasp success rate (75 of 120 attempts) in a custom simulation evaluation across 40 positions.
demo:
  type: video
  src: ../assets/videos/ai-worker-auto-record-hero.mp4
  poster: ../assets/images/ai-worker-auto-record-hero-poster.webp
  autoplay: true
  alt: Automatic recording demo at 2x speed. While Auto Pick runs in the web UI on the left, the AI Worker picks up the bottle in Isaac Lab at top right, and RViz at bottom right shows the bottle point cloud and GraspNet grasp candidates
---

## Pipeline

### Data Collection

I built an eight-stage automatic collection pipeline, from grasp candidate selection through recording, as a personal project on top of ROBOTIS's open-source software. Cyclo Intelligence handles data collection and management, and Cyclo Control handles motion planning and control.

Clicking a bottle in the browser generates grasp candidates from the surrounding point cloud, then triggers the approach, grasp, lift and recording sequence. An attempt is saved as a training demonstration only if the bottle is lifted at least 3.5 cm, held for 0.5 seconds and the recording is saved.

<div class="media-grid media-grid-natural"><figure class="feature-media"><img src="../assets/images/ai-worker-cyclo-intelligence.webp" alt="ROBOTIS Cyclo software stack with Cyclo Intelligence highlighted, covering data collection, data curation and model inference" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/ai-worker-cyclo-control.webp" alt="ROBOTIS Cyclo software stack with Cyclo Control highlighted, covering tool center point control, MoveJ joint control and collision avoidance" loading="lazy"></figure></div>

![Four stages of automatic recording: target selection, grasp inference, motion generation, and execution with recording. Camera images and joint states are saved through cyclo_data](../assets/images/ai-worker-auto-record-pipeline.webp)

#### Detailed system diagram

![A browser click reaches auto_recorder_node in cyclo_intelligence. GraspNet candidates from grasp_server trigger an eight-step sequence in the AI Worker controllers, while cyclo_data records sensor data and commands](../assets/images/ai-worker-auto-record-architecture.webp)

#### Collecting bottle grasps

<video controls autoplay muted loop playsinline preload="metadata" aria-label="Automatic collection at 8x speed. The AI Worker repeatedly attempts to pick up the bottle at different table positions in Isaac Lab"><source src="../assets/videos/ai-worker-auto-recorder-8x.mp4" type="video/mp4"></video>

I fixed the bottle positions in a five-row, eight-column grid and ran ten attempts per position for each grasp candidate generator.

![Top-down view of the 40 test positions in Isaac Lab. All bottles are visible to show the grid, and each trial used one bottle](../assets/images/ai-worker-fixed40-locations.webp)

I received feedback that GraspNet produced inconsistent grasps. I added CenterPose as a second way to generate a grasp pose for the selected bottle and compared the two under the same conditions.

| | GraspNet (GSNet) | CenterPose with a fixed grasp rule |
| --- | --- | --- |
| Input | Point cloud around the selected point | Color and depth images |
| Output | Multiple six-degree-of-freedom grasp poses with scores | Bottle's 3D bounding box, used to find its center |
| Grasp orientation | Estimated for each candidate | Fixed rule for upright bottles |
| Object assumption | No bottle-specific assumption | Upright bottle |
| Collision check | Point-cloud filter | Inverse kinematics (IK) validation only |
| Inference | GPU (CUDA) | CPU (ONNX Runtime) |

For upright-bottle collection, I used the center estimated by CenterPose with a fixed grasp orientation. This decision followed checks of estimated tilt and repeated grasp variation.

### Training

Training NVIDIA GR00T N1.7 on one RTX 5090 (32 GB) ran out of memory at the first optimizer step. Fused AdamW still exceeded available memory with the frozen language and vision backbone in 32-bit floating point (FP32).

I loaded the frozen backbone in 16-bit floating point (BF16) and used fused AdamW. Of the model's 3.14 billion parameters, I trained about 1.62 billion in the connector and action generator.

Training completed 150,000 steps with a batch size of 8 and a learning rate of 0.0001.

The curves show training loss averaged over 1,000-step intervals for the policies trained on 310 GraspNet demonstrations and 319 CenterPose demonstrations. Mean loss over the final 10,000 steps was 0.00241 and 0.00224, respectively. These are training losses; grasp performance is measured in the evaluation below.

![GR00T N1.7 training loss for 310 GraspNet demonstrations and 319 CenterPose demonstrations. Both curves decrease through 150,000 steps; each point is a 1,000-step mean on a logarithmic vertical axis](../assets/images/ai-worker-training-loss.webp)

### Inference & Evaluation

Policy inference ran at 30 Hz and the robot control loop at 100 Hz. Each policy was evaluated three times at each of the same 40 collection positions, giving 120 trials per policy. Each trial lasted up to 30 seconds. Success required lifting the bottle at least 3.5 cm and holding it for 0.5 seconds.

In the first evaluation, both policies rarely succeeded. The controller that held the arm at a stored pose kept sending commands while paused. I disabled it, verified before each attempt that the arm was receiving no external commands, and ran the evaluation again.

## Results and Analysis

### Data Quality: GraspNet vs CenterPose

| | GraspNet | CenterPose |
| --- | --- | --- |
| Successful grasps | 310/400 (77.5%) | 319/400 (79.8%) |
| X = 0.295 m (farthest row) | **18/80** | 9/80 |
| X = 0.340 m | 53/80 | **70/80** |
| X = 0.385, 0.430 and 0.475 m | 239/240 | 240/240 |
| Grasp position variation at the same location (median / 90th percentile) | 3.5 mm / 8.5 mm | **0.3 mm / 0.9 mm** |
| Grasp orientation variation at the same location (median / 90th percentile) | 2.6° / 8.9° | **0.0° / 0.0°** |
| Median maximum lift height | 5.3 cm | 5.4 cm |
| Median time per attempt | 28.6 s | 27.6 s |

I grouped the target grasp poses from successful attempts by location. I measured position variation using standard deviation and orientation variation as the angular deviation from the mean orientation. The analysis used locations with at least two successes, covering 34 for GraspNet and 32 for CenterPose.

![Two heatmaps compare successful grasps across 40 positions. GraspNet does better in the farthest row at X = 0.295 m, CenterPose does better at X = 0.340 m, and both are nearly perfect across the three closest rows](../assets/images/ai-worker-grasp-success-grid.webp)

In 169 of the 171 failed attempts, inverse kinematics rejected every candidate while computing arm joint angles for the target pose. Failures clustered in the farthest row (27 successes in 160 attempts). Every attempt at X = 0.430 m and X = 0.475 m succeeded. I could not isolate joint limits from collisions as the cause.

<details class="validation-appendix">
<summary>Detailed CenterPose validation</summary>

**Estimated tilt increased at farther positions.** Across the 400 CenterPose attempts, I measured the angle between the estimated vertical axis and the true upright axis for each row.

| Row | Distance to camera | Downward viewing angle | Tilt (median / 90th percentile) | Median horizontal center error | Successful grasps |
| --- | --- | --- | --- | --- | --- |
| X = 0.295 m | 0.78 m | 44° | 25.7° / 35.4° | 17 mm | 9/80 |
| X = 0.340 m | 0.74 m | 46° | 24.4° / 33.3° | 19 mm | 70/80 |
| X = 0.385 m | 0.71 m | 48° | 19.9° / 31.9° | 11 mm | 80/80 |
| X = 0.430 m | 0.69 m | 51° | 17.7° / 24.0° | 10 mm | 80/80 |
| X = 0.475 m | 0.66 m | 54° | 13.6° / 20.9° | 10 mm | 80/80 |

![Distribution of estimated bottle tilt by row. Median tilt rises from 13.6° in the closest row to 25.7° in the farthest row. The bottle was upright throughout](../assets/images/ai-worker-centerpose-tilt.webp)

![CenterPose bounding boxes overlaid on two head-camera views. The yellow estimated vertical axis departs from the white ground-truth axis by 14.8° at 0.66 m and 26.7° at 0.78 m](../assets/images/ai-worker-centerpose-near-far.webp)

The farther rows generally showed larger tilt and center errors. As the bottle moved farther away, the camera also viewed it from a shallower angle, so the effects of distance and angle could not be separated. I checked the projection by comparing nine markers over six frames with the rendered positions. The mean difference was 0.66 px. I used CenterPose's estimated center and set the grasp orientation with a rule for upright bottles.

**The bottle model also responded to cans and bags.** CenterPose uses separate models for different object categories. At a threshold of 0.3, I tested 11 showroom assets at three rotations each without additional training. The bottle model detected five coffee can designs as bottles in all 15 views. It also responded to a peanut snack bag in three of three views and a chestnut snack bag in two of three.

**Small bottles in the image were missed.** With the full 672 × 376 image as input, the bottle model detected zero of nine bottle views. Cropping around the bottle raised detection to nine of nine. During collection at 1280 × 720, the bottle was approximately 160–180 px tall and was detected.

![Head-camera images and crops at three rotations show the bottle model drawing 3D boxes around green tea bottles, coffee cans and snack bags](../assets/images/ai-worker-centerpose-categories.webp)

![The projected centers of nine markers align with the rendered positions within 0.52–0.90 px](../assets/images/ai-worker-centerpose-camera-check.webp)

</details>

### Sim-to-Sim VLA Baseline

I evaluated each policy three times at each of the same 40 positions. Each trial lasted up to 30 seconds and used the same success criterion as collection.

| Policy training data | Overall | X = 0.295 | X = 0.340 | X = 0.385 | X = 0.430 | X = 0.475 |
| --- | --- | --- | --- | --- | --- | --- |
| 310 GraspNet demonstrations | 75/120 | 5/24 | 11/24 | 19/24 | 22/24 | 18/24 |
| 319 CenterPose demonstrations | 75/120 | 1/24 | 14/24 | 20/24 | 22/24 | 18/24 |

CenterPose produced more consistent grasp poses at the same position. The two policies achieved the same total number of successful grasps, with differences across rows based on three trials per position. I used CenterPose to collect demonstrations for upright bottles. GraspNet still needs evaluation on objects with other shapes.

Arm jitter affected some trials. Policy failures have yet to be classified by jitter, reachability and collisions, so the effect of jitter on success rate has not been quantified.

### Action Chunking & Jitter Reduction

Phase 2 will measure command changes at action chunk boundaries and arm jitter, then compare chunk blending and smoothing against the baseline under the same evaluation conditions.

### Sim-to-Real Transfer

Phase 3 will transfer the policy to a physical AI Worker and evaluate the effects of sensor, coordinate frame and control timing differences.

## Next Steps

Arm jitter affected some trials. I could not determine whether joint limits or collisions caused the inverse kinematics rejections concentrated in the farthest row.

Positions outside the training set, bottles lying on their sides, other object shapes and a physical robot still need testing.

The next experiments will separate joint-limit failures from collisions and extend evaluation to unseen positions and other object shapes. I plan to evaluate chunk blending and smoothing before testing transfer to a physical AI Worker.

## Code

ROBOTIS software used as the foundation for the automatic collection pipeline.

[GitHub · Cyclo Intelligence](https://github.com/ROBOTIS-GIT/cyclo_intelligence)
