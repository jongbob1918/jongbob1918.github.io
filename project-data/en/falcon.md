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

## Object detection model troubleshooting

We defined six ground-object classes: birds, debris, wild animals, people, vehicles, and aircraft. The initial model was trained on roughly 15,000 public images but struggled to detect small objects in footage of the airport model.

Real airport photographs differed from our test setup in object size, shape, and background. We built training data that reflected the model environment to reduce this gap.

## Improving the model with mixed training data

The team scanned physical models in 3D and used Polycam and Blender to build a virtual airport environment. A teammate implemented the Unity environment and automatic labeling pipeline, varying camera angles and lighting while generating images and object-location labels together.

<figure class="feature-media"><img src="../assets/images/falcon_synthetic_pipeline.webp" alt="Presentation slide 60: Unity pipeline varying camera angles and lighting while automatically generating object labels" loading="lazy"></figure>

We combined 3,000 synthetic images with 1,000 photographs. We trained YOLOv8n, a lightweight model that locates and classifies objects, for 100 passes through the training data.

## Comparing detections on test data

We evaluated models trained on public, synthetic, photographed, and mixed images using test images of the airport model and objects. The public-image model was trained for 150 epochs; the other models were trained for 100. The model trained on mixed synthetic and photographed images performed best in this comparison.

The precision–recall curves below show the relationship between how many detections are correct and how many target objects are found. The mixed-data model maintained high values for both across all six classes.

<figure class="feature-media"><img src="../assets/images/falcon_dataset_evaluation.webp" alt="Presentation slide 62: class-wise precision–recall curves on test data for the four training-data configurations" loading="lazy"></figure>

The mixed-data model achieved a mean average precision (mAP) of **0.930** at a 50% overlap threshold between predicted and reference boxes, and **0.7207** averaged across thresholds from 50% to 95%. We selected this model for ground-object detection.

## Placing detected objects on the map

To display objects on the controller map, we needed to convert image pixels into coordinates on the airport model. I researched and tested coordinate mapping with square reference markers (ArUco); the backend teammate designed the transformation logic.

We measured marker-center locations on the model and found the corresponding pixel positions in camera images. These pairs define a planar transformation matrix, or homography, that maps the center of each detected object onto the map. The mapped position determines whether the object is on a runway, taxiway, or grass area.

<figure class="feature-media"><img src="../assets/images/falcon_aruco_mapping.png" alt="Measured ArUco marker locations on the airport model paired with their pixel positions in camera footage" loading="lazy"></figure>

ByteTrack associates the same object across frames as it moves. We also analyzed fluorescent vest and vehicle colors to distinguish workers and service vehicles. Sending object identifiers, classes, and positions to the server updates map markers and popup alerts on the controller interface.

## Demonstrating the integrated system

We checked object detection on the airport model and identification of workers wearing fluorescent vests. We connected these detections to the controller map and pilot voice alerts.

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/falcon_ground_detection.webp" alt="Detection of birds, debris, people, animals, aircraft, and vehicles on the airport model" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/falcon_worker_classification.gif" alt="Demonstration identifying workers by fluorescent vest color" loading="lazy"></figure></div>

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/-si0u8I1h2A" title="FALCON integrated demonstration delivering hazard information as pilot voice alerts" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>
