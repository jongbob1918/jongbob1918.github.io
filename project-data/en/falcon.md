---
slug: falcon
title: FALCON — Runway Operational Safety Service
description: An AI operational safety service supporting controllers and pilots through ground-hazard detection, bird-strike risk analysis, and voice guidance
team: 4 members
period: May 26–Jul 3, 2025
context: ADDINEDU · Autonomous Robot Developer Training with ROS 2 and AI, Cohort 9
role: Project leadership · Ground-object detection system development · Camera-to-ground zone mapping
overview: >-
  While serving as a noncommissioned officer in the Republic of Korea Air Force, I experienced how birds, animals, and debris such as screws and litter on runways can pose a critical risk to aircraft operations. I started this project to automate hazard monitoring with AI and help reduce the staffing shortages and costs associated with manual runway safety management. FALCON supports controllers and pilots in safe aircraft operations through ground-hazard detection, bird-strike risk analysis, and voice guidance. It delivers hazard information detected in CCTV footage through the control interface and voice alerts for pilots.
demo:
  type: youtube
  src: https://www.youtube.com/embed/lctXpBYrVsU
  title: FALCON ground-hazard monitoring demonstration
---

## Software architecture

The ground- and bird-detection servers, controller PC, and pilot PC connect through the main server. The main server manages detections and risk information and delivers them to the controller interface (Hawkeye) and pilot service (RedWing).

<figure class="feature-media"><img src="../assets/images/falcon_software_architecture.png" alt="Software architecture connecting CCTV detection, the FALCON main server, monitoring GUI, and pilot system" loading="lazy"><figcaption>Connections between detection servers, the main server and database, the controller PC, and the pilot PC</figcaption></figure>

## Building the ground-hazard detection system

As the lead of a four-person team, I managed schedules and documentation and was responsible for the ground-object detection system, model research, and training. Synthetic-data generation and ground-detection model development were collaborative work.

<figure class="feature-media"><img src="../assets/images/falcon_detection_sequence.png" alt="FALCON flow from CCTV input through hazard detection and zone classification to map display" loading="lazy"><figcaption>CCTV input, hazard detection, and zone-state assessment leading to status updates, popup alerts, and map display</figcaption></figure>

The initial model trained on public data missed small objects in airport-model footage and sometimes mistook ArUco markers for hazards. Training data needed to reflect the fixed camera view and model background.

We combined synthetic images produced by the team in Unity and Blender with photographs of the airport model and background images without target objects (negative samples). YOLOv8n-box was retrained with 960×960 inputs for 150 epochs and a batch size of 8 to detect six classes: birds, debris, people, animals, aircraft, and vehicles.

<figure class="feature-media"><img src="../assets/images/falcon_synthetic_dataset.gif" alt="Building FALCON ground-hazard training data with Blender and airport-model footage" loading="lazy"></figure>

## Tracking objects and locating them in physical zones

Detection results feed ByteTrack to follow the same object across frames. Post-processing uses safety-vest and vehicle colors to distinguish workers from other people and service vehicles from ordinary vehicles.

To place detections on the monitoring map, image pixels must be matched to physical zone coordinates. I researched and tested ArUco-based coordinate mapping; the backend team member designed the transformation logic.

Image coordinates and measured positions of four reference markers define a planar transformation matrix (homography). OpenCV’s `perspectiveTransform` maps detection-box centers to model-map coordinates, which are then checked against runway, taxiway, and grass zones.

<figure class="feature-media"><img src="../assets/images/falcon_aruco_mapping.png" alt="Correspondence between measured runway-model coordinates and ArUco pixel coordinates" loading="lazy"></figure>

Object identifiers, classes, coordinates, and confidence scores are sent to the monitoring server. The server and monitoring interface were implemented by their respective team members and use these results to update map markers and popup alerts.

## Model evaluation and airport-model demonstrations

These Ground Model v0.3 results are recorded in the project README. The dataset combines synthetic images and photographs of the airport model, with approximately 69.4% allocated to training, 20.9% to validation, and 9.8% to testing. The README does not specify whether the metrics below come from the validation or test split.

<div class="metric-grid"><div class="metric-card"><span class="metric-value">0.9902</span><span class="metric-label">mAP@0.5</span></div><div class="metric-card"><span class="metric-value">0.9005</span><span class="metric-label">mAP@0.5:0.95</span></div><div class="metric-card"><span class="metric-value">0.9928 / 0.9672</span><span class="metric-label">Precision / Recall</span></div></div>

The precision–recall curves below show the initial model trained on public data and the model retrained on mixed data. Matching evaluation conditions have not been established, so these curves are not used to calculate a percentage improvement.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/falcon_baseline_pr_curve.png" alt="Class-wise precision–recall curves of the baseline FALCON segmentation model" loading="lazy"><figcaption>Before · Public Dataset Segmentation Model</figcaption></figure><figure class="feature-media"><img src="../assets/images/falcon_hybrid_pr_curve.png" alt="Class-wise precision–recall curves of the FALCON hybrid detection model" loading="lazy"><figcaption>After · Hybrid Dataset YOLOv8n-box</figcaption></figure></div>

Airport-model footage demonstrated detection of multiple object classes and identification of workers by safety-vest color. The following video shows ground-hazard detection in operation.

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/falcon_ground_detection.webp" alt="FALCON detecting six ground-hazard classes on the airport model" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/falcon_worker_classification.gif" alt="FALCON post-processing that distinguishes fluorescent-vest workers" loading="lazy"></figure></div>

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/-si0u8I1h2A?list=PLCGG9KRfKwMmQqXvp43pChNMyyLSyjHp9&amp;index=4" title="FALCON ground-hazard detection demonstration" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>

## Limitations and next steps

**From a model to an airport:** The results presented here come from synthetic data and airport-model footage. Deployment at an actual airport requires further evaluation across camera distances, lighting, and weather conditions.

**Coordinate-mapping validation:** My work included mapping research and tests, but this page does not present measured position errors or their test conditions. Further validation should compare mapped positions with known reference locations and measure errors and zone-classification accuracy near boundaries.

**Operational evaluation:** Detection metrics alone do not establish the impact on monitoring work. Next steps include measuring the delay from video input to displayed alerts, false-alarm frequency, and missed hazards.
