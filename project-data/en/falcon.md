---
slug: falcon
title: FALCON — Runway Operational Safety Service
description: An AI operational safety service supporting controllers and pilots through ground-hazard detection, bird-strike risk analysis, and voice guidance
team: 4 members
period: May 26–Jul 3, 2025
context: ADDINEDU · Autonomous Robot Developer Training with ROS 2 and AI, Cohort 9
role: Project leadership · Ground-object detection system development · Camera-to-ground zone mapping
overview: >-
  While serving as a noncommissioned officer in the Republic of Korea Air Force, I encountered runway hazards such as birds, animals, and loose debris. We developed FALCON to support manual monitoring by combining ground-hazard detection, bird-strike risk analysis, and voice guidance. When a camera detects a hazard, the system displays its location and type on the controller interface and delivers a voice alert to the pilot.
demo:
  type: youtube
  src: https://www.youtube.com/embed/lctXpBYrVsU
  title: FALCON ground-hazard monitoring demonstration
---

## Service flow from hazard detection to alerts

When a camera detects a hazard, the system identifies its type and location and places it on the controller map. Controllers see map markers and popup alerts, while pilots receive the hazard information through voice alerts.

<figure class="feature-media"><img src="../assets/images/falcon_detection_sequence.png" alt="Processing sequence from camera input through detection, tracking, and coordinate mapping to map and alert updates" loading="lazy"></figure>

## System design

The ground- and bird-detection servers, controller PC, and pilot PC connect through the main server. Each detection server analyzes camera footage. The main server manages detections and risk information and forwards them to the controller interface (Hawkeye) and pilot service (RedWing).

<figure class="feature-media"><img src="../assets/images/falcon_software_architecture.png" alt="Detection servers connected through the main server to the controller interface and pilot service" loading="lazy"></figure>

## Training the initial hazard detection model

We defined six ground-object classes: birds, debris, wild animals, people, vehicles, and aircraft. The initial model was trained on roughly 15,000 public images but struggled to detect small objects in footage of the airport model.

We rebuilt the training data to reduce differences in object size, shape, and background between airport photographs and our model environment.

## Improving the model with mixed training data

The team recreated the physical models in a virtual environment using Polycam and Blender. The teammate responsible for synthetic data used Unity to vary camera angles and lighting and automatically generate images and object-location labels.

<figure class="feature-media"><img src="../assets/images/falcon_synthetic_pipeline.webp" alt="Presentation slide 60: Unity pipeline varying camera angles and lighting while automatically generating object labels" loading="lazy"></figure>

We trained the lightweight object detection model YOLOv8n on 3,000 synthetic images and 1,000 photographs.

## Detection performance by training data

<figure class="feature-media"><img src="../assets/images/falcon_dataset_evaluation.webp" alt="Presentation slide 62: class-wise precision–recall curves on test data for the four training-data configurations" loading="lazy"></figure>

We selected the model trained on mixed synthetic and photographed images, which performed best in testing, for ground detection.

## Placing detected objects on the map

We used square reference markers (ArUco) to map image positions to map coordinates. I researched and tested the mapping; the backend teammate designed the transformation logic.

Measured marker positions and their image coordinates define a planar transformation matrix, or homography. We used it to map object locations and classify them as runway, taxiway, or grass areas.

<figure class="feature-media"><img src="../assets/images/falcon_aruco_mapping.png" alt="Measured ArUco marker locations on the airport model paired with their pixel positions in camera footage" loading="lazy"></figure>

ByteTrack associates the same object across frames as it moves. We also analyzed fluorescent vest and vehicle colors to distinguish workers and service vehicles. Sending object identifiers, classes, and positions to the server updates map markers and popup alerts on the controller interface.

## Demonstrating the integrated system

We checked object detection on the airport model and identification of workers wearing fluorescent vests. We connected these detections to the controller map and pilot voice alerts.

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/falcon_ground_detection.webp" alt="Detection of birds, debris, people, animals, aircraft, and vehicles on the airport model" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/falcon_worker_classification.gif" alt="Demonstration identifying workers by fluorescent vest color" loading="lazy"></figure></div>

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/-si0u8I1h2A" title="FALCON integrated demonstration delivering hazard information as pilot voice alerts" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>
