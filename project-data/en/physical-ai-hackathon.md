---
slug: physical-ai-hackathon
title: PHYSICAL AI HACKATHON — Bimanual Imitation Learning
description: A hackathon project using ACT imitation learning for bimanual ball transfer and color sorting
team: 4 members
period: Feb 2026
overview: >-
  I joined a four-person team at the first Physical AI Hackathon hosted by Hansung University and ROBOSIZE. Using two SO-101 arms, each costing roughly KRW 1.2 million, and 2D cameras, we trained the robots to pick up colored balls, transfer them between grippers, and sort them into bins. The LeRobot-based system successfully sorted three of five balls during judging.
demo:
  type: image
  src: https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif
  alt: Two SO-101 arms transferring colored balls and sorting them into bins
---

## Challenge: transfer and sort balls with two arms

<div class="role-grid"><div class="info-card"><strong>Pick & Place</strong><span>Pick a ball from the floor with one arm</span></div><div class="info-card"><strong>Transfer</strong><span>Pass it to the opposite gripper</span></div><div class="info-card"><strong>Classification</strong><span>Place it in the color-matched bin</span></div></div>

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/mission_top_view.jpg" alt="Top view of the hackathon setup with colored balls, bins, and two SO-101 arms" loading="lazy"></figure>

## Model selection

We chose ACT, supported by LeRobot, to finish implementation and testing within the limited event time. ACT predicts a chunk of actions from camera images and joint states, enabling continuous pick, transfer, and sorting motion.

<figure class="feature-media hackathon-act-media"><img src="../assets/images/act_architecture.png" alt="ACT Transformer with a CVAE-style latent encoder and action-sequence output from cameras and joint state" loading="lazy"></figure>

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/teleop.jpg" alt="Teleoperation setup recording demonstrations for two SO-101 arms" loading="lazy"><figcaption>Teleoperation · A human moves the leader arms while camera images, joint states, and actions are recorded as episodes</figcaption></figure>

## First attempt: learn all five balls in one sequence

Our first dataset copied the judging order: two blue balls, two red balls, and one yellow ball were picked, transferred, and sorted in a single episode. We recorded about 200 demonstrations and trained the first policy.

In initial tests, the robot sometimes stopped mid-motion, and small changes in ball or gripper position sharply reduced grasp accuracy. Position, color, ordering, and the bimanual handoff were mixed into one long episode, leaving too few examples for each stage and allowing early errors to accumulate.

<dl class="flow"><dt>Data</dt><dd>About 200 episodes covering blue → blue → red → red → yellow</dd><dt>Training unit</dt><dd>Imitate grasping, transfer, and color sorting as one long action sequence</dd><dt>Observation</dt><dd>Mid-sequence stops, unstable grasps, and weak tolerance to ball-position changes</dd></dl>

## Second attempt: split tasks and include recovery data

After additional research, we replaced the five-ball sequence with a single-ball task: pick one ball and place it in the matching bin. Repeating each color-specific task gave the model denser examples of a successful action and reduced error accumulation.

Because the cameras only provided 2D images, similar image positions could still represent different depths and scales. We varied the demonstrations so the gripper approached diagonally instead of always following one frontal trajectory.

We also recorded recovery rather than only successful trajectories. During teleoperation, we intentionally missed a ball and then approached it again, adding the states and actions needed to continue after slippage or a displaced target.

<div class="metric-grid"><div class="metric-card"><span class="metric-value">1 task</span><span class="metric-label">One ball and one color-matched bin</span></div><div class="metric-card"><span class="metric-value">≈ 1,000</span><span class="metric-label">5 balls × 200 demonstrations</span></div><div class="metric-card"><span class="metric-value">15K</span><span class="metric-label">Training steps at judging</span></div></div>

## Judging result: three of five balls

We ultimately recorded about 1,000 single-task demonstrations, 200 for each of five balls. The 9 a.m. deadline prevented further training, so judging used the checkpoint at 15,000 steps.

The robots successfully picked, transferred, and sorted three balls. While processing the fourth, the right arm knocked over a bin and disrupted the environment, ending the run. Although the full sequence was not completed, the revised data strategy produced three consecutive successes in the judging setup.

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif" alt="Two SO-101 arms picking, transferring, and sorting balls into color-coded bins" loading="lazy"><figcaption>Physical bimanual manipulation · grasp, gripper-to-gripper transfer, and color sorting</figcaption></figure>

## Reflection: the system needed decisions beyond imitation

ACT learned precise bimanual motion quickly, but the mission exposed limits of imitation learning alone. The policy generated actions from camera images and joint state, but did not explicitly represent which ball was current, which color should come next, or whether a bin had fallen. It imitated the sequence embedded in the data and was weak at deterministic replanning when conditions changed.

In a redesign, I would use ACT as the low-level manipulation policy and add a high-level state machine for color recognition, ball count, and task progress. Conditions for a fallen bin or failed grasp could select the required single-task policy or trigger recovery. The project showed that task decomposition and failure-state demonstrations matter as much as model choice for real-robot robustness.

## Team

<figure class="feature-media hackathon-team-media"><img src="https://github.com/TheMomentLab/.github/blob/main/1770642885261.jpg?raw=true" alt="Four-person team at the first Hansung University and ROBOSIZE Physical AI Hackathon" loading="lazy"></figure>
