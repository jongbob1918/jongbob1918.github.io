---
slug: physical-ai-hackathon
title: PHYSICAL AI HACKATHON — Bimanual Imitation Learning
description: A hackathon project using ACT imitation learning for bimanual ball transfer and color sorting
team: 4 members
period: Feb 8–9, 2026
overview: >-
  I joined a four-person team at the first Physical AI Hackathon hosted by Hansung University and ROBOSIZE. Using two SO-101 arms, each costing roughly KRW 1.2 million, and 2D cameras, we trained the robots to pick up colored balls, transfer them between grippers, and sort them into bins.
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

A human moved the leader arms while camera images, joint states, and actions were recorded as episodes.

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/teleop.jpg" alt="Teleoperation setup recording demonstrations for two SO-101 arms" loading="lazy"></figure>

## First attempt: learn all five balls in one sequence

We recorded about 200 episodes, each covering the full sequence of picking, transferring, and sorting all five balls. During testing, small changes in ball or gripper position caused missed grasps or mid-sequence stops. We attributed this to too few demonstrations of each stage within the long sequence and errors carrying over into later actions.

<figure class="feature-media hackathon-act-media"><img src="../assets/images/physical-ai-first-attempt.png" alt="Illustration of the first attempt: about 200 demonstrations of blue, blue, red, red, and yellow balls in one sequence, followed by missed grasps and mid-sequence stops when positions change" loading="lazy"></figure>

## Second attempt: learn one ball at a time and record recovery

We split demonstrations into **picking up one ball, passing it between arms, and placing it in the matching bin**. This let the model learn repeated short actions instead of one long sequence.

We recorded the gripper approaching the ball diagonally rather than descending vertically. We also deliberately missed a ball and picked it up again, adding **how to continue after a failed grasp** to the training data.

<figure class="feature-media hackathon-act-media"><img src="../assets/images/physical-ai-second-attempt.png" alt="Three changes to training demonstrations: record one ball at a time, approach diagonally, and include a missed grasp followed by another attempt" loading="lazy"></figure>

## Judging result

We collected about 1,000 training demonstrations, 200 for each of five balls. To meet the 9 a.m. deadline, we used the model trained to 15,000 steps for judging.

The robots picked, transferred, and sorted three balls consecutively. While handling the fourth, the right arm knocked over a bin, ending the demonstration before we could complete the full sequence. Unfortunately, we did not win an award.

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif" alt="Two SO-101 arms picking, transferring, and sorting balls into color-coded bins" loading="lazy"></figure>

## Reflection

ACT learned the two-arm motions, but the system struggled to continue when conditions changed, such as a bin falling over. It needed a separate mechanism to track progress and choose the next action.

In a redesign, ACT would control arm motion while a high-level state machine managed ball color, the number processed, and failures. The experience showed the importance of splitting tasks into short actions and including recovery demonstrations in the training data.

## Team

<figure class="feature-media hackathon-team-media"><img src="https://github.com/TheMomentLab/.github/blob/main/1770642885261.jpg?raw=true" alt="Four-person team at the first Hansung University and ROBOSIZE Physical AI Hackathon" loading="lazy"></figure>
