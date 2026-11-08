---
slug: ffw-auto-pick
title: FFW Auto Pick — From Robot Grasping to Policy Training
description: Connecting grasp generation, repeated execution, success evaluation and demonstration collection to GR00T policy training
overview: >-
  Training a robot grasping policy requires repeatable motions and verified demonstrations.
  This project connects grasp generation, motion execution, success evaluation and recording into an automated collection workflow for the FFW robot.
  GraspNet-based and CenterPose-based collection pipelines were compared, and their datasets were used separately to train GR00T policies.
overviewNote:
  title: Portfolio outline
  paragraphs:
    - This draft establishes the story and recorded results. Demonstrations, experimental conditions and implementation evidence will be added to each section.
    - Results cover simulation collection and recorded training completion. Trained-policy performance and physical grasping performance require separate evaluation.
---

## From grasps to training data

The goal is to turn grasp candidates into executable actions and recorded demonstrations. Existing perception models and policy frameworks provide the foundation; execution, validation and collection connect them.

<div class="role-grid"><div class="info-card"><strong>Perception and execution</strong><span>Connect candidates to approach, grasp and lift</span></div><div class="info-card"><strong>Repeated collection</strong><span>Link success decisions and recordings to episodes</span></div><div class="info-card"><strong>Policy training</strong><span>Validate collected data and train GR00T</span></div></div>

> **To add:** End-to-end demonstration, project dates, collaboration scope and individual contributions.

## Making grasping repeatable

A generated grasp may be unreachable or fail to lift the object. A completed motion command alone cannot identify a successful demonstration.

The starting point was to observe candidate selection, execution failures, object lift and recording completion separately.

> **To add:** Initial workflow, representative failures, collection process before automation and success definition.

## Two perception paths, one execution workflow

| Stage | Input and responsibility | Output |
| --- | --- | --- |
| Scene input | RGB, depth, point cloud and camera-to-robot transforms | Target position and scene information |
| Candidate generation | GraspNet or CenterPose with bottle-specific rules | Grasp position, orientation and width |
| Execution | Auto Recorder: inverse kinematics (IK) checks, approach, grasp and lift | Motion state and recordings |
| Collection | Scene reset, success evaluation and episode identification | Successful demonstrations and failure records |
| Training | Data conversion, camera validation and GR00T training | Checkpoints and training records |

> **To add:** Architecture showing both candidate servers and the shared execution path, including cancellation and cleanup.

## Connecting GraspNet candidates to executable grasps

A heuristic that moves the grasp position to the selected target point was tested at three fixed positions, with 20 attempts per condition at each position.

| Condition | Left | Center | Right | Total |
| --- | --- | --- | --- | --- |
| Heuristic ON | 14/20 | 14/20 | 18/20 | 46/60 |
| Heuristic OFF | 12/20 | 6/20 | 20/20 | 38/60 |

Total successes increased, but the right position regressed. These are simulation grasp-and-save outcomes for the tested layouts, not evidence of improvement across all layouts.

> **To add:** Candidate visualizations, matched initial-condition evidence, failure videos and measured trajectories.

## Isolating the CenterPose orientation error

An early DLA34 experiment estimated approximately 15° of tilt for an almost upright bottle. Preprocessing and camera projection were checked; 54 known 3D markers produced a mean projection error of approximately 0.66 px. The exact cause of the pose error remained unresolved.

The later collection implementation uses a FAN model, fixed object dimensions, depth correction and a fixed grasp orientation. The initial diagnostic and the current bottle-specific grasp strategy are distinct stages.

> **To add:** Predicted box visualization, projection checks, reasons for version changes and upright-bottle assumptions.

## Collecting demonstrations while recording failures

The repeated workflow connects scene reset to outcome persistence. The documented success rule requires the bottle to rise at least 3.5 cm for 0.5 seconds during the specified interval, with recording successfully saved.

Command completion, object lift and recording completion are checked separately. Failed attempts remain in the records; only successful episodes enter the training list.

> **To add:** Evaluation timeline, outcome-file race condition and resume handling, configuration and episode traceability examples.

## Collection results and policy training

The latest completion summary records 300 attempts per method. These results compare complete collection pipelines, including postprocessing and grasp rules.

| Collection method | Attempts | Successful episodes | Collection success rate |
| --- | --- | --- | --- |
| GraspNet-based | 300 | 225 | 75.0% |
| CenterPose + bottle-specific rules | 300 | 248 | 82.7% |

Each dataset uses one head camera and two wrist cameras as training inputs. Both GR00T runs have completion records at 150,000 steps. Collection success and trained-policy execution success are separate metrics.

> **To add:** Per-attempt evidence, layout conditions, failure categories, training curves and data/configuration versions. Explain the unequal training dataset sizes.

## What remains to be evaluated

| Open question | Required evaluation |
| --- | --- |
| Can the trained policy execute a grasp? | Policy rollouts on held-out layouts |
| How does collection method affect policy performance? | Matched dataset sizes and evaluation conditions |
| Where do bottle-specific rules apply? | Tests across bottle types, tilt and clutter |
| Do simulation results transfer to hardware? | Separate physical sensor, transform and gripper validation |

> **To add:** Prioritized evaluation plan and measured outcomes. Keep pending work separate from completed results.
