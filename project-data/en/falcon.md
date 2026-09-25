---
slug: falcon
title: FALCON — Runway Operational Safety Service
description: An AI operational safety service supporting controllers and pilots through ground-hazard detection, bird-strike risk analysis, and voice guidance
team: 4 members
period: May 26–Jul 3, 2025
context: ADDINEDU · Autonomous Robot Developer Training with ROS 2 and AI, Cohort 9
role: Project leadership · Ground-object detection system development · Camera-to-ground zone mapping
overview: >-
  While serving as a noncommissioned officer in the Republic of Korea Air Force, I saw how birds, wild animals, and debris such as screws and litter on a runway can put aircraft at risk. Finding and removing these hazards requires regular inspections, but limited personnel and operating costs made that work burdensome. To address this problem, I developed a service that uses AI to detect hazards in footage from airport cameras and alert the staff responsible for managing them.
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

We defined six ground-object classes: birds, debris, wild animals, people, vehicles, and aircraft. We trained the first model on roughly 15,000 public images, mostly photographs of real airports, but its detection accuracy dropped in footage of the airport model. In some cases, it classified model animals as people.

We photographed the airport model and labeled object locations to add training images closer to the footage. Limited project time and personnel made it difficult to collect enough labeled images by hand. We therefore built a simulation pipeline to generate images and labels in larger numbers.

## Improving the model with mixed training data

The team recreated the physical models in a virtual environment using Polycam and Blender.

<figure class="feature-media"><img src="../assets/images/falcon_simulated_airport_scene.png" alt="Vehicle, bird, animal, and debris models scanned with Polycam beside the airport-model environment recreated in Blender" loading="lazy"></figure>

The teammate responsible for synthetic data used Unity to vary camera angles and lighting and automatically generate images and object-location labels.

<figure class="feature-media"><img src="../assets/images/falcon_synthetic_pipeline.webp" alt="Presentation slide 60: Unity pipeline varying camera angles and lighting while automatically generating object labels" loading="lazy"></figure>

We trained the lightweight object detection model YOLOv8n on 3,000 synthetic images and 1,000 photographs of the model that we had labeled by hand.

## Detection performance by training data

<figure class="feature-media"><img src="../assets/images/falcon_dataset_evaluation.webp" alt="Presentation slide 62: class-wise precision–recall curves on test data for the four training-data configurations" loading="lazy"></figure>

We selected the model trained on mixed synthetic and photographed images, which performed best in testing, for ground detection.

## Hazard alerts based on zone access levels

Treating every detected person or vehicle as a hazard would trigger alerts for normal work and reduce trust in the service. People and vehicles must stay clear of a runway before takeoff, while maintenance areas need to admit workers and service vehicles.

We divided the airport into eight zones and let administrators set an access level for each. The system compares the detected object type with the zone's access level and alerts on access violations.

<figure class="feature-media"><img src="../assets/images/falcon_zone_access_settings.webp" alt="Presentation slide 39: eight airport zones with three access levels allowing everyone, only workers and service vehicles, or no people or vehicles" loading="lazy"></figure>

The example below shows a vehicle access alert after Taxiway A is set to prohibit entry.

<figure class="feature-media"><img src="../assets/images/falcon_zone_access_alert.webp" alt="Presentation slide 40: Taxiway A set to access level 3, with ordinary and service vehicles marked and an access-violation alert displayed" loading="lazy"></figure>

## Identifying an object's zone from camera footage

Applying access rules requires knowing which zone contains each detected object. We used square reference markers (ArUco) to identify reference points in the image and connect camera coordinates to map coordinates.

We measured marker-center positions on the physical model and found the same points in the camera image. These pairs define a planar transformation matrix, or homography, that maps object centers to the map and identifies runway, taxiway, or grass zones.

<figure class="feature-media"><img src="../assets/images/falcon_aruco_mapping.png" alt="Measured ArUco marker locations on the airport model paired with their pixel positions in camera footage" loading="lazy"></figure>

ByteTrack follows moving objects across frames, while fluorescent vest and vehicle colors distinguish workers and service vehicles. Object types and locations are checked against access levels to update the controller map and alerts.

## Demonstrating the integrated system

We checked object detection on the airport model and identification of workers wearing fluorescent vests. We connected these detections to the controller map and pilot voice alerts.

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/falcon_ground_detection.webp" alt="Detection of birds, debris, people, animals, aircraft, and vehicles on the airport model" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/falcon_worker_classification.gif" alt="Demonstration identifying workers by fluorescent vest color" loading="lazy"></figure></div>

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/-si0u8I1h2A" title="FALCON integrated demonstration delivering hazard information as pilot voice alerts" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>
