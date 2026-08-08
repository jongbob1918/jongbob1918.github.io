---
slug: falcon
title: FALCON — Runway Safety Monitoring System
description: An AI monitoring system that detects and tracks runway hazards and maps them to real-world coordinates
team: 4 members
period: May 26–Jul 3, 2025
role: Team lead · Ground hazard detection integration and validation
overview: >-
  Birds, foreign object debris, people, and vehicles can threaten aircraft operations even when they appear as small objects, while continuously watching multiple CCTV feeds is difficult for an operator. FALCON detects and tracks ground hazards in fixed-camera footage, converts pixel positions into runway coordinates and zones, and sends object ID, class, location, and confidence events to a control interface.
demo:
  type: youtube
  src: https://www.youtube.com/embed/lctXpBYrVsU
  title: FALCON ground-hazard monitoring demonstration
---

## From CCTV footage to an operator alert

Each camera frame passes through `detection → tracking → coordinate mapping → zone classification → operator display`. The pipeline turns bounding boxes into events that tell an operator where a hazard is and whether the same object is still moving.

<figure class="feature-media"><img src="../assets/images/falcon_detection_sequence.png" alt="FALCON flow from CCTV input through hazard detection and zone classification to map display" loading="lazy"></figure>

## Ground-hazard detection and coordinate validation

As the lead of a four-person team, I managed schedules and documentation and integrated the Ground IDS pipeline that turns birds, FOD, people, and vehicles into control-room information. My work covered model research, training and validation on real and synthetic data, the YOLOv8–ByteTrack pipeline, and ArUco-based coordinate-mapping tests. I collaborated with Jinhyeok Jang on synthetic data, Hyojin Park on server and mapping logic, and Jiyeon Kim on the monitoring GUI.

## Why we combined synthetic, real, and negative samples

The initial public-data model missed small objects in the fixed view of our airport model and sometimes classified background ArUco markers as hazards. The training data differed too much from the target camera angle, lighting, and background.

We combined Unity and Blender synthetic images with photos of the physical airport model and object-free negative samples. YOLOv8n-box was retrained for six classes—birds, FOD, people, animals, aircraft, and vehicles—using 960×960 inputs for 150 epochs.

<dl class="flow"><dt>Problem</dt><dd>The public-data model did not generalize to small objects and the background of the fixed CCTV view.</dd><dt>Data</dt><dd>We combined Unity and Blender images, real model-airport footage, and object-free negative samples.</dd><dt>Training</dt><dd>YOLOv8n-box was retrained for six classes at 960×960 for 150 epochs.</dd><dt>Validation</dt><dd>We checked both metrics on a held-out set and multi-object detections in real airport-model footage.</dd></dl>

<figure class="feature-media"><img src="../assets/images/falcon_synthetic_dataset.gif" alt="Building FALCON ground-hazard training data with Blender and airport-model footage" loading="lazy"></figure>

## Model validation with metrics and real footage

We compared the class-wise precision–recall curves of the original public-data segmentation model and the hybrid detection model. Precision in the baseline dropped quickly as recall increased, while the hybrid model stayed closer to the upper-right region for all six classes.

<div class="media-grid pr-comparison"><figure class="feature-media"><img src="../assets/images/falcon_baseline_pr_curve.png" alt="Class-wise precision–recall curves of the baseline FALCON segmentation model" loading="lazy"><figcaption>Before · Public Dataset Segmentation Model</figcaption></figure><figure class="feature-media"><img src="../assets/images/falcon_hybrid_pr_curve.png" alt="Class-wise precision–recall curves of the FALCON hybrid detection model" loading="lazy"><figcaption>After · Hybrid Dataset YOLOv8n-box</figcaption></figure></div>

<div class="metric-grid"><div class="metric-card"><span class="metric-value">0.9902</span><span class="metric-label">mAP@0.5</span></div><div class="metric-card"><span class="metric-value">0.9005</span><span class="metric-label">mAP@0.5:0.95</span></div><div class="metric-card"><span class="metric-value">0.9928 / 0.9672</span><span class="metric-label">Precision / Recall</span></div></div>

Ground Model v0.3 achieved these values and detected multiple classes in real airport-model footage. Because the repository does not preserve whether the baseline metrics used the identical evaluation split, I do not claim a numerical improvement percentage; the PR-curve shapes are used only as comparative evidence.

## Six-class detection and object tracking

YOLOv8 inference feeds ByteTrack with persistence enabled so the same object retains its track ID across frames. Post-processing then derives states needed by the monitoring system.

<dl class="flow"><dt>Tracking</dt><dd>ByteTrack IDs become FALCON object IDs, preserving a hazard's motion across frames.</dd><dt>Worker status</dt><dd>The fluorescent-pixel ratio in the upper 60% of a person's bounding box separates workers in safety vests from other people.</dd><dt>Service vehicle</dt><dd>Yellow and black pixel ratios distinguish service vehicles from ordinary vehicles.</dd><dt>Fall event</dt><dd>A person's bounding-box aspect ratio and its duration create a separate rescue-stage event.</dd></dl>

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/falcon_ground_detection.webp" alt="FALCON detecting six ground-hazard classes on the airport model" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/falcon_worker_classification.gif" alt="FALCON post-processing that distinguishes fluorescent-vest workers" loading="lazy"></figure></div>

## Mapping pixels to physical coordinates with ArUco markers

A bounding box only identifies a location in the image. To place it on the runway map, the system finds the centers of ArUco markers 0–3 and pairs them with four measured reference points to calculate a homography.

<div class="formula-block">λ [x<sub>map</sub>, y<sub>map</sub>, 1]ᵀ = H [u<sub>pixel</sub>, v<sub>pixel</sub>, 1]ᵀ</div>

<figure class="feature-media"><img src="../assets/images/falcon_aruco_mapping.png" alt="Correspondence between measured runway-model coordinates and ArUco pixel coordinates" loading="lazy"></figure>

The center of each detection is converted into millimeter map coordinates with `perspectiveTransform`. Calibration is generated only when all four reference markers are visible, and the mapped position is compared with runway, taxiway, and grass boundaries to assign a zone.

## Sending detection events to the monitoring server

The detector separates a calibration Map Mode from an Object Mode for hazard detection. Object ID, class, coordinate, and confidence values become JSON events sent to the main server through a TCP queue; server commands can switch between the two modes.

If the connection drops, a communication thread retries every five seconds. Newlines delimit messages so multiple JSON commands received together can be reconstructed in order. This keeps network latency out of the vision loop and lets the GUI update detections, map markers, and alert history.

<figure class="feature-media"><img src="../assets/images/falcon_software_architecture.png" alt="Software architecture connecting CCTV detection, the FALCON main server, monitoring GUI, and pilot system" loading="lazy"></figure>

## Ground-hazard detection demonstration

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/-si0u8I1h2A?list=PLCGG9KRfKwMmQqXvp43pChNMyyLSyjHp9&amp;index=4" title="FALCON ground-hazard detection demonstration" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>
