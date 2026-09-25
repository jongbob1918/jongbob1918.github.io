---
slug: physical-ai-hackathon
shortName: PHYSICAL AI
category: side
order: 4
title: 한성대×로보시지 제1회 Physical AI 해커톤
description: ACT 모방학습으로 SO-101 양팔의 공 전달·색상 분류 미션에 도전한 해커톤 참가 기록
team: 4명
period: "2026.02.08~02.09"
skills:
  - LeRobot
  - ACT
  - Imitation Learning
  - SO-101
repository: https://github.com/TheMomentLab/physical_ai_hackathon
card:
  image: https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif
  imageAlt: 제1회 Physical AI 해커톤에서 두 대의 SO-101 로봇팔이 색상 공을 전달하고 분류하는 모습
  skills:
    - LeRobot
    - ACT
    - Imitation Learning
    - SO-101
overview: >-
  한성대학교와 로보시지가 주최한 제1회 Physical AI 해커톤에 4인 팀으로 참가했습니다.
  120만 원대 SO-101 로봇팔 두 대와 2D 카메라를 사용해 색상 공을 집어 수납함에 분류하는 미션에 도전했습니다.
  LeRobot 라이브러리와 AI 모델을 사용하여 공 5개 중 3개 분류에 성공했습니다.
demo:
  type: image
  src: https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif
  alt: 두 대의 SO-101 로봇팔이 색상 공을 전달하고 수납함에 분류하는 해커톤 시연
---

## 도전 과제: 두 팔이 공을 건네 색상별로 분류하기

<div class="role-grid"><div class="info-card"><strong>Pick & Place</strong><span>한쪽 팔로 바닥의 공 집기</span></div><div class="info-card"><strong>Transfer</strong><span>반대쪽 팔의 그리퍼로 전달</span></div><div class="info-card"><strong>Classification</strong><span>색상별 수납함에 넣기</span></div></div>

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/mission_top_view.jpg" alt="색상 공과 수납함, 두 대의 SO-101 로봇팔이 배치된 해커톤 미션 상단 모습" loading="lazy"></figure>

## 모델 선택

제한된 시간 안에 구현과 테스트를 마치기 위해 LeRobot에서 지원하는 ACT를 사용했습니다. ACT는 카메라 영상과 관절 상태를 바탕으로 여러 동작을 한 번에 예측해 집기·전달·분류 같은 연속 동작을 제어합니다.

<figure class="feature-media hackathon-act-media"><img src="../assets/images/act_architecture.png" alt="학습 단계의 CVAE 스타일 변수 인코더와 다중 카메라·관절 상태에서 행동 시퀀스를 출력하는 ACT Transformer 구조" loading="lazy"></figure>

사람이 리더 로봇팔을 움직이며 카메라 영상, 관절 상태와 동작을 에피소드로 기록했습니다.

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/teleop.jpg" alt="리더 로봇팔을 조작해 두 대의 SO-101 팔의 시연 데이터를 기록하는 텔레오퍼레이션 모습" loading="lazy"></figure>

## 1차 시도: 다섯 개의 공을 한 번에 학습시키기

다섯 공을 순서대로 집어 전달하고 분류하는 전체 동작을 하나의 에피소드로 묶어 약 200회 기록했습니다. 테스트에서는 공이나 그리퍼 위치가 조금만 달라져도 집기에 실패하거나 중간에 멈췄습니다. 긴 동작을 한꺼번에 학습하면서 단계별 시연이 부족하고, 앞 단계의 오차가 뒤로 이어진 것으로 판단했습니다.

<figure class="feature-media hackathon-act-media"><img src="../assets/images/physical-ai-first-attempt.png" alt="파랑·파랑·빨강·빨강·노랑 순서의 전체 동작을 약 200회 학습한 뒤, 위치 변화로 집기에 실패하거나 중간에 멈추는 양팔 로봇의 1차 시도를 설명한 그림" loading="lazy"></figure>

## 2차 시도: 공 하나씩 학습하고 실패 복구도 기록하기

시연을 **공 하나를 집어 전달하고, 같은 색 수납함에 넣는 동작**으로 나눴습니다. 긴 순서를 한꺼번에 익히기보다 짧은 동작을 반복해서 학습하도록 바꿨습니다.

공 위치가 달라져도 대응할 수 있도록 정면뿐 아니라 대각선으로 접근하는 시연도 기록했습니다. 일부러 공을 놓친 뒤 다시 집는 동작을 넣어, **실패한 상태에서 작업을 이어가는 과정**도 학습 데이터에 포함했습니다.

<figure class="feature-media hackathon-act-media"><img src="../assets/images/physical-ai-second-attempt.png" alt="공 하나의 집기·전달·분류를 따로 기록하고, 여러 각도로 접근하며, 놓친 공을 다시 집는 복구 동작까지 시연에 포함한 2차 학습 방법" loading="lazy"></figure>

## 심사 결과: 5개 중 3개 성공

최종적으로 공 5개를 각각 200회씩 기록해 약 1,000개의 단일 태스크 시연 데이터를 확보했습니다. 마감이 오전 9시였기 때문에 학습을 더 이어가지 못하고, 당시 15,000 step까지 학습된 체크포인트로 심사를 진행했습니다.

로봇은 다섯 개의 공 가운데 세 개를 집어 전달하고 색상별 수납함에 넣는 데 성공했습니다. 네 번째 공을 처리하는 과정에서 오른팔이 수납함을 넘어뜨렸고, 환경이 흐트러져 남은 시연은 더 이상 진행할 수 없었습니다. 완주에는 실패했지만, 데이터 전략을 바꾼 뒤 실제 심사 환경에서 세 번의 연속 성공을 확인했습니다.

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif" alt="두 SO-101 로봇팔이 공을 집어 서로 전달하고 색상별 수납함에 넣는 실제 시연" loading="lazy"></figure>

## 회고: 모방을 넘어 판단할 수 있는 구조가 필요했다

ACT는 짧은 시간 안에 정밀한 양팔 동작을 학습시키는 데 효과적이었지만, 이번 미션에서는 모방학습만으로 해결하기 어려운 한계도 확인했습니다. 정책은 카메라 영상과 현재 관절 상태로 다음 행동을 생성하지만, “현재 몇 번째 공인지”, “어느 색을 다음에 처리해야 하는지”, “수납함이 넘어졌는지”와 같은 명시적인 작업 상태나 목표를 스스로 결정하는 구조는 아니었습니다. 따라서 정해진 순서를 데이터에서 암묵적으로 모방할 뿐, 상황에 따라 다음 행동을 결정론적으로 선택하거나 작업 계획을 다시 세우는 데는 취약했습니다.

다시 설계한다면 ACT를 저수준 양팔 조작 정책으로 사용하되, 색상 인식과 공 개수·작업 진행 상태를 관리하는 상위 상태 머신을 분리하겠습니다. 여기에 수납함 전도나 집기 실패를 감지하는 조건을 추가해, 필요한 단일 태스크 정책을 선택하고 실패 시 복구 동작으로 전환하도록 구성할 수 있습니다. 이번 경험을 통해 모델 선택만큼이나 **태스크를 어떻게 나누고, 실패 상태까지 어떤 데이터로 보여주는가**가 실제 로봇의 강건성을 좌우한다는 점을 배웠습니다.

## 함께한 팀

<figure class="feature-media hackathon-team-media"><img src="https://github.com/TheMomentLab/.github/blob/main/1770642885261.jpg?raw=true" alt="한성대×로보시지 제1회 Physical AI 해커톤에 참가한 4인 팀 단체 사진" loading="lazy"></figure>
