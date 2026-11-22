---
slug: ai-worker-auto-recorder
title: AI Worker Auto Recorder — Collecting Training Data Without Teleoperation
description: An AI Worker that grasps bottles on its own to collect 629 demonstrations, then trains and evaluates GR00T policies on them in simulation
period: "2026.09–11"
team: 1 person (personal project)
role: Built the automatic collection pipeline on ROBOTIS open source, then trained and evaluated policies
card:
  imageAlt: Top-down Isaac Lab scene with 40 bottles in a 5-row by 8-column grid and the robot body at the bottom
overview: >-
  Collecting robot demonstrations by teleoperation turns a person's working time directly into cost.
  On top of ROBOTIS open source, I built a pipeline in which the AI Worker grasps bottles on its own and saves only the successful episodes.
  Running with no human involvement for about 6 hours, it made 800 attempts and collected 629 successful demonstrations (2.98 hours of recording); a policy trained on each dataset succeeded in 75 of 120 simulated evaluation trials across 40 positions.
---

## Without spending teleoperator hours on every demonstration

While collecting AI Worker data at ROBOTIS, I found that the largest cost was a person having to stay with the robot for every demonstration. In my own work, an 8-hour day produced about 3 hours of recorded demonstrations without breaks, or about 1.5 hours with regular breaks.

For a simple task like picking a bottle, I let the robot grasp and record by itself. The table compares both in the same unit.

| Collection method | Person | Elapsed time | Recorded duration |
| --- | --- | --- | --- |
| Teleoperation (no breaks) | Required | 8 hours | About 3 hours |
| Teleoperation (regular breaks) | Required | 8 hours | About 1.5 hours |
| Automatic collection | Not required | About 6 hours (from logs) | 2.98 hours (629 episodes) |

The teleoperation figures come from my own work experience; the automatic figure comes from logged start and end times. I did not compare data quality. No policy was trained on teleoperation data, so I cannot claim that automatic collection replaces teleoperation.

## What I built on top of the open source

I modified and implemented this alone on ROBOTIS open source: the AI Worker control software, the `cyclo_intelligence` training server and the `cyclo_lab` simulation environment. By repository records, I made 96 commits between September 5 and October 22, 2026, and added a new automatic collection package of about 3,700 lines.

| Provided by open source | Implemented or modified by me |
| --- | --- |
| AI Worker robot model and ROS 2 control | Collection execution from grasp candidates through approach, lift and recording |
| Isaac simulation environment and robot USD (3D scene file) | Four-camera setup, coordinate alignment and sensor topics |
| GraspNet, CenterPose and GR00T models | Connecting both candidate generators to one workflow, success evaluation and evaluation procedure |

## From one attempt to one demonstration

| Stage | Input and responsibility | Passed on |
| --- | --- | --- |
| Scene input | RGB and depth images, point cloud, camera-to-robot transforms | Target bottle position and scene information |
| Candidate generation | GraspNet or CenterPose (with bottle-specific rules) | Grasp position, orientation and width |
| Execution | Inverse kinematics (IK, computing arm joint angles) pre-check, approach, grasp and lift | Motion state and recording |
| Success evaluation | Did the bottle rise at least 3.5 cm, stay up for 0.5 s and finish saving? | Successful demonstration list, failure records |
| Training | Convert successful demonstrations only; one head and two wrist cameras as input | GR00T checkpoint |

A finished motion command alone does not show success, so command completion, object lift and save completion are checked separately. Failed attempts stay in the records and only successful demonstrations are used for training. When no candidate passes the IK pre-check, the attempt ends after one candidate-generation try.

## Connecting two candidate generators to one workflow

I used GraspNet first. Its results were uneven, so I received CenterPose (an object pose estimation model) to compare. The two have different inputs and assumptions, so a comparison criterion had to come first.

For GraspNet, I switched a heuristic that shifts the grasp toward the selected target point on and off, 20 trials each at three fixed positions. All 60 pairs of initial conditions across the 120 trials were confirmed to match.

| Condition | Left | Center | Right | Total |
| --- | --- | --- | --- | --- |
| Heuristic ON | 14/20 | 14/20 | 18/20 | 46/60 |
| Heuristic OFF | 12/20 | 6/20 | 20/20 | 38/60 |

The total rose but the right position fell. This is a simulation result for one layout, so I did not conclude whether to keep or remove the heuristic.

For CenterPose, a bottle standing upright came out tilted by about 14 to 15 degrees, and I did not resolve it. To test whether the camera input conversion was the cause, I compared 9 markers across 6 frames against the rendered projection and they matched to a mean of 0.66 px (maximum 0.90 px). That rules out the input and projection. As of the October 28 record, I had not found the stage that produces the error. Current collection uses the FAN model with a bottle-specific grasp rule that assumes the bottle is standing.

## Fixing conditions at 40 positions

At first there was no "consistency" criterion for comparing the two methods, so interpretations diverged. I fixed the bottle at 40 positions in a 5-row by 8-column grid and repeated each position 10 times per method.

![Top-down Isaac Lab view of 40 bottles placed in a 5-row by 8-column grid, with the AI Worker body at the bottom](../assets/images/ai-worker-fixed40-locations.webp)

The scene above places all 40 bottles together only to show the positions; evaluation used one bottle at a time.

| Collection | Attempts | Successful demonstrations |
| --- | --- | --- |
| Round 1 GraspNet (random initial layout) | 300 | 225 (75.0%) |
| Round 1 CenterPose (random initial layout) | 300 | 248 (82.7%) |
| Round 2 GraspNet (40 fixed positions) | 400 | 310 (77.5%) |
| Round 2 CenterPose (40 fixed positions) | 400 | 319 (79.8%) |

In round 1, CenterPose was 7.7 percentage points higher; in round 2, the gap shrank to 2.3 points. The scene setups differ, so I cannot confirm that fixing positions caused the change.

## Failures clustered in the farthest row

Of the 171 failures in the 800 round-2 attempts, 169 were IK candidate rejections, 1 was a recording initialization error and 1 was an interruption. In the farthest row (X=0.295 m), 133 of 160 attempts failed, leaving 27 successes, while the X=0.430 m and 0.475 m rows succeeded in all 160 attempts each.

I suspect distance and grasp direction, but I have not confirmed joint limits, collisions or the rejection stage. I did not pre-check all 40 positions with IK, which made isolating the cause harder.

## Evaluating the trained policies on the same 40 positions

I trained NVIDIA GR00T N1.7 (a Vision-Language-Action model that outputs actions from images, language and robot state) for 150,000 steps on each dataset. The language model and vision encoder stayed frozen, and about 1.62 billion of roughly 3.14 billion parameters (the connector and action generator) were trained. Batch size was 8 and the learning rate 0.0001.

Evaluation covers 40 positions × 3 trials × 2 models, 240 trials in total. Each trial lasts 30 seconds with the same success rule as collection. It reuses the positions seen in training, so it does not measure generalization to new positions.

| Policy training data | Overall | X=0.295 | X=0.340 | X=0.385 | X=0.430 | X=0.475 |
| --- | --- | --- | --- | --- | --- | --- |
| 310 GraspNet demonstrations | 75/120 | 5/24 | 11/24 | 19/24 | 22/24 | 18/24 |
| 319 CenterPose demonstrations | 75/120 | 1/24 | 14/24 | 20/24 | 22/24 | 18/24 |

Overall successes were equal but differed by row. At 22 of 40 positions the two models had the same success count; 7 positions failed all three trials for both, and 14 succeeded all three for both. The farthest row had the lowest policy success and also the fewest successes during collection. Too little training data there may be the cause, but I have not tested it. With 3 trials per position and 24 per row, the sample is small, so I do not generalize row-level differences.

## When the evaluation itself was wrong

In the first evaluation, the policy trained on GraspNet demonstrations succeeded once in 120 trials, and the CenterPose policy succeeded in 0 of 39 trials before stopping on a save error. Before concluding the models were bad, I checked and found the controller holding the stored pose was still sending arm commands while paused. They may have competed with the trained policy's commands, so the result could not be read as pure model performance.

I disabled that controller, confirmed before every trial that no external arm command existed, and re-evaluated; the table above is that result. I do not use the first evaluation as model performance.

## When training could not even start for lack of memory

On one RTX 5090 (32 GB), the default configuration ran out of memory at the first Adam optimizer step for batch sizes 1, 2 and 4, so no update completed. Loading the frozen parts in BF16 (16-bit floating point) and using fused AdamW, just those two changes, let all three batch sizes finish 10 minutes of training and save a checkpoint.

| Actual batch | Steps in 10 minutes | Samples per second | Peak GPU use |
| --- | --- | --- | --- |
| 1 | 5,142 | 8.57 | 30.12 GiB |
| 2 | 4,679 | 15.60 | 30.23 GiB |
| 4 | 3,939 | 26.26 | 30.68 GiB |

This measurement uses the official demo data (two cameras, six-dimensional actions), not AI Worker data. Batch 4 left only about 1.2 GiB free, so adding cameras could run out again; the actual AI Worker training (three camera inputs) finished with the same settings at batch 8. Keeping the backbone in FP32 still ran out of memory even with fused AdamW.

## What I cannot claim yet

- All results are from simulation. I did not evaluate on a physical robot.
- There is one evaluated policy per dataset (no training repeats), and evaluation reuses the training positions.
- The success rule ends at a 3.5 cm lift held for 0.5 seconds; I did not check whether the bottle stays lifted afterwards.
- The only object is one green tea bottle.

| Open question | Required evaluation |
| --- | --- |
| Does the trained policy also grasp at new positions? | Evaluate at positions not used in training |
| Is the farthest row weak because of too little data? | IK pre-check of all 40 positions; retrain with equal per-position counts |
| Is automatic data as good as teleoperation data? | Compare with a policy trained on the same amount of teleoperation data |
| Do simulation results hold on the real robot? | Separate evaluation with physical sensors, frames and gripper |
