---
slug: roomie
title: ROOMIE — Autonomous Hotel Service Robot
description: A ROS 2 hotel service robot integrating navigation, delivery, guidance, and elevator interaction
period: Jul 7–Aug 13, 2025
overview: >-
  Hotels have repetitive cross-floor work such as room-service delivery and guest guidance. ROOMIE connects autonomous navigation, delivery, guidance, and staff monitoring through ROS 2. At an elevator, it recognizes buttons and door state, operates the call and destination buttons with a four-axis arm, and continues its mission on another floor without human assistance.
demo:
  type: youtube
  src: https://www.youtube.com/embed/CqO3OH661Os
  title: ROOMIE project demonstration
---

## An end-to-end elevator service flow

ROOMIE navigates to the elevator, presses the external call button, and checks that the door has opened. After boarding, it presses the destination-floor button, uses OCR on the floor indicator to determine arrival, exits, and resumes the delivery or guidance mission.

<figure class="feature-media"><img src="../assets/images/roomie_elevator_flow.png" alt="ROOMIE flow covering elevator arrival, call-button operation, boarding, destination selection, and exit" loading="lazy"></figure>

## System design

Guests order room service or select a destination in the Guest GUI, while staff confirm an order and request pickup in the Staff GUI. The Roomie Main Service assigns the request to a robot, and the ROS 2 Roomie Controller coordinates navigation, vision, manipulator, and cargo-box modules.

<figure class="feature-media"><img src="../assets/images/roomie_system_architecture.png" alt="ROOMIE architecture connecting guest, staff, and admin GUIs with the main server and robot modules" loading="lazy"></figure>

## Arm controller hardware

We used an educational four-axis arm costing roughly KRW 50,000 for the bare mechanism. A standard 2D camera and button-contact tip were mounted at the end effector, and an ESP32 controlled four servo motors.

<figure class="feature-media"><img src="../assets/images/roomie_arm_hardware.webp" alt="ROOMIE four-axis arm with a 2D camera, button-contact tip, and servo motors" loading="lazy"></figure>

## Estimating a button target from a 2D camera

The input consists of the detected button center `(u, v)` and bounding-box width `Wpx`. With the physical button diameter set to `D = 35 mm`, the camera intrinsics `(fx, fy, cx, cy)` estimate its distance and direction.

<figure class="feature-media portrait-evidence"><img src="../assets/images/roomie-button-detection-cropped.webp" alt="Elevator button and bounding box detected in the 2D camera image" loading="lazy"><figcaption>The button center and bounding-box size are used for position estimation</figcaption></figure>

<div class="formula-block">Z ≈ f<sub>x</sub>D / W<sub>px</sub> &nbsp;·&nbsp; X = (u-c<sub>x</sub>)Z/f<sub>x</sub> &nbsp;·&nbsp; Y = (v-c<sub>y</sub>)Z/f<sub>y</sub></div>

The pinhole model approximates depth `Z` from the ratio between the physical diameter and its image size. Back-projecting the center pixel gives the camera-frame position `p_camera = (X, Y, Z)`.

<div class="formula-block">p<sub>base</sub> = T<sub>base←tool</sub>(q) · T<sub>tool←camera</sub> · p<sub>camera</sub></div>

Forward kinematics at joint state `q` provides `Tbase←tool`, and hand–eye calibration provides the fixed `Ttool←camera`. Their composition converts the camera-frame button location into the base-frame target `p_base` used by the four-axis inverse kinematics solver.

<figure class="feature-media"><img src="../assets/images/roomie_arm_principle.png" alt="Transformation from an image-space button coordinate through camera, tool, and base frames to arm control" loading="lazy"><figcaption>Converting image coordinates into a base-frame target for the manipulator</figcaption></figure>

## Validating four-axis IK targets

The target position is solved with `ikpy` for four joints. The current joint angles initialize the solver, and forward kinematics checks the result. A numerical residual above 1 mm or a joint-limit violation marks the motion as failed.

<figure class="feature-media evidence-video"><video controls playsinline preload="metadata" poster="../assets/images/roomie-ik-target-control-poster.jpg"><source src="../assets/videos/roomie-ik-target-control.mp4" type="video/mp4">Your browser does not support MP4 video.</video><figcaption>IK target-control test comparing physical arm motion with the RViz joint model</figcaption></figure>

The 1 mm value is the numerical IK tolerance, not the absolute end-effector accuracy of the physical arm.

## Pressing from a repeatable observation pose

The first implementation estimated the button from an arbitrary pose, so the reached position changed with the arm's starting configuration. I changed the sequence so every `ClickButton` request first moves to a fixed observation pose and then estimates the target under the same conditions.

The arm's total link length is about 33.5 cm, which limits its independent workspace. The ROOMIE base first performs a precise approach to the button, after which the arm executes the click from the observation pose.

<div class="diagram" role="img" aria-label="Sequence from ROOMIE base approach to button press"><div class="diagram-node">Precise base approach</div><div class="diagram-arrow">→</div><div class="diagram-node owner">OBSERVE_POSE</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Estimate button</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Standby<br>80 mm</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Press<br>100 mm</div><div class="diagram-arrow">→</div><div class="diagram-node">Retreat</div></div>

<figure class="feature-media evidence-video"><video controls playsinline preload="metadata" poster="../assets/images/roomie-button-click-poster.jpg"><source src="../assets/videos/roomie-button-click.mp4" type="video/mp4">Your browser does not support MP4 video.</video><figcaption>Development test of the observation pose and button approach</figcaption></figure>

<div class="media-grid"><figure class="feature-media"><img src="../assets/images/elevator-alignbutton.gif" alt="ROOMIE approaching and aligning near an elevator button" loading="lazy"></figure><figure class="feature-media"><img src="../assets/images/elevator-pushouterbutton2.gif" alt="ROOMIE arm pressing an external elevator call button" loading="lazy"></figure></div>

## Gaussian-profile motion control

To reduce end-effector jitter from constant-speed motion, I applied a Gaussian profile for smoother acceleration and deceleration. The ESP32 updates all four servo targets every 6 ms and returns a completion acknowledgment when the motion ends.

<figure class="feature-media"><img src="../assets/images/roomie_gaussian_motion.webp" alt="Gaussian velocity and acceleration profiles used to smooth ROOMIE arm motion" loading="lazy"></figure>

## Full demonstration

<figure class="feature-media"><div class="video-embed"><iframe src="https://www.youtube.com/embed/qIbQOql0ST0" title="Full ROOMIE demonstration" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></figure>

## Result

<div class="metric-grid"><div class="metric-card"><span class="metric-value">10</span><span class="metric-label">Button-approach trials</span></div><div class="metric-card"><span class="metric-value">3</span><span class="metric-label">Successful contacts</span></div><div class="metric-card"><span class="metric-value">30%</span><span class="metric-label">Contact success rate</span></div></div>

## Limitations

The end effector contacted the button accurately in three of ten trials. The remaining seven missed the target.

<div class="evidence-grid constraint-grid"><div class="evidence-card"><span class="status-tag warning">PERCEPTION</span><strong>2D depth estimate</strong><p>Distance was inferred from button size and was sensitive to detection scale and viewing angle.</p></div><div class="evidence-card"><span class="status-tag warning">MECHANISM</span><strong>Backlash and frame flex</strong><p>Physical end-effector error remained even with a fixed observation pose.</p></div><div class="evidence-card"><span class="status-tag warning">ACTUATION</span><strong>Limited pressing force</strong><p>Torque and frame stiffness were limited when the arm was extended.</p></div><div class="evidence-card"><span class="status-tag warning">FEEDBACK</span><strong>No sensor feedback</strong><p>Without encoders or a force sensor, actual tip position and contact force could not be measured quantitatively.</p></div></div>
