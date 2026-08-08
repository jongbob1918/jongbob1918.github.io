---
slug: physical-ai-hackathon
shortName: PHYSICAL AI
group: side
order: 4
title: 한성대×로보시지 제1회 Physical AI 해커톤
description: ACT 모방학습으로 SO-101 양팔의 공 전달·색상 분류 미션에 도전한 해커톤 참가 기록
team: 4명
period: 2026.02
skills:
  - LeRobot
  - ACT
  - Imitation Learning
  - Bimanual Manipulation
  - SO-101
repository: https://github.com/TheMomentLab/physical_ai_hackathon
card:
  image: https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif
  imageAlt: 제1회 Physical AI 해커톤에서 두 대의 SO-101 로봇팔이 색상 공을 전달하고 분류하는 모습
  titleEn: PHYSICAL AI HACKATHON — Bimanual Imitation Learning
  keywords:
    - LeRobot
    - ACT
    - Imitation Learning
    - Bimanual Manipulation
    - SO-101
  descriptionKo: 5개 연속 동작을 색상별 단일 태스크로 재구성하고 복구 시연을 더해, 심사에서 5개 공 중 3개 분류에 성공했습니다.
  descriptionEn: Reframed one five-ball sequence as per-color tasks, added recovery demonstrations, and sorted three of five balls during judging.
overview: >-
  한성대학교와 로보시지가 주최한 제1회 Physical AI 해커톤에 4인 팀으로 참가했습니다.
  두 대의 SO-101 로봇팔로 공을 전달하고 색상별 수납함에 분류하는 미션을 수행했습니다.
  제한된 시간 안에 텔레오퍼레이션으로 양팔 동작 데이터를 수집하고 LeRobot과 ACT로 학습해 실제 로봇 심사를 진행했습니다.
demo:
  type: image
  src: https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif
  alt: 두 대의 SO-101 로봇팔이 색상 공을 전달하고 수납함에 분류하는 해커톤 시연
---

## 도전 과제: 두 팔이 공을 건네 색상별로 분류하기

<div class="role-grid"><div class="info-card"><strong>Pick & Place</strong><span>한쪽 팔로 바닥의 공 집기</span></div><div class="info-card"><strong>Transfer</strong><span>반대쪽 팔의 그리퍼로 전달</span></div><div class="info-card"><strong>Classification</strong><span>색상별 수납함에 넣기</span></div></div>

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/mission_top_view.jpg" alt="색상 공과 수납함, 두 대의 SO-101 로봇팔이 배치된 해커톤 미션 상단 모습" loading="lazy"></figure>

## 모델 선택

[ACT(Action Chunking with Transformers)](https://arxiv.org/abs/2304.13705)는 카메라 영상과 로봇의 관절 상태를 입력받아 여러 미래 행동을 하나의 **action chunk**로 예측하는 모방학습 모델입니다.

<dl class="flow"><dt>개발 환경</dt><dd>LeRobot에서 ACT 학습과 추론을 바로 구성할 수 있어 제한된 준비 시간을 데이터 수집과 태스크 개선에 사용할 수 있었습니다.</dd><dt>연속 동작</dt><dd>여러 시점의 행동을 묶어 예측하므로 집기·전달·분류로 이어지는 양팔 동작을 끊김 없이 제어하는 데 적합했습니다.</dd><dt>입력 정보</dt><dd>카메라 영상과 관절 상태를 함께 사용해 공의 위치와 두 로봇팔의 움직임을 하나의 정책으로 학습할 수 있었습니다.</dd></dl>

별도의 모델 비교 실험은 진행하지 않았으며, 해커톤의 개발 시간과 양팔 연속 제어 조건을 기준으로 ACT를 선택했습니다.

<figure class="feature-media hackathon-act-media"><img src="../assets/images/act_architecture.png" alt="학습 단계의 CVAE 스타일 변수 인코더와 다중 카메라·관절 상태에서 행동 시퀀스를 출력하는 ACT Transformer 구조" loading="lazy"></figure>

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/teleop.jpg" alt="리더 로봇팔을 조작해 두 대의 SO-101 팔의 시연 데이터를 기록하는 텔레오퍼레이션 모습" loading="lazy"><figcaption>텔레오퍼레이션 · 사람이 리더 팔을 움직이며 카메라 영상, 관절 상태와 행동을 에피소드로 기록</figcaption></figure>

## 1차 시도: 다섯 개의 공을 한 번에 학습시키기

처음에는 실제 심사 순서와 동일하게 파란 공 2개, 빨간 공 2개, 노란 공 1개를 연속으로 집어 전달하고 분류하는 전체 과정을 하나의 에피소드로 기록했습니다. 이 방식으로 약 200개의 시연 데이터를 수집해 첫 학습을 진행했습니다.

그러나 1차 테스트에서는 로봇이 동작 중 갑자기 멈추거나, 공과 그리퍼의 위치가 조금만 달라져도 집기 정확도가 크게 떨어졌습니다. 하나의 긴 에피소드 안에 공의 위치, 색상, 순서와 양팔 전달 단계가 모두 섞이면서 각 단계에 필요한 시연 밀도가 부족했고, 앞 단계의 작은 오차가 뒤 동작까지 누적됐습니다.

<dl class="flow"><dt>데이터</dt><dd>파랑 → 파랑 → 빨강 → 빨강 → 노랑의 다섯 공 전체 과정을 약 200개 에피소드로 기록</dd><dt>학습 단위</dt><dd>집기·전달·색상 분류를 하나의 긴 행동 시퀀스로 모방</dd><dt>관찰 결과</dt><dd>중간 정지와 불안정한 집기가 발생하고, 공 위치 변화에 대한 정확도가 기대에 미치지 못함</dd></dl>

## 2차 시도: 태스크를 나누고 실패까지 데이터로 만들기

추가 기술 조사를 거쳐 다섯 공을 한 번에 학습시키는 대신, **공 하나를 집어 색상에 맞는 수납함에 넣는 태스크**로 시연을 나눴습니다. 색상별 단일 태스크를 반복하면 모델이 한 번의 성공 동작을 더 조밀하게 관찰할 수 있고, 긴 시퀀스에서 발생하던 오차 누적도 줄일 수 있다고 판단했습니다.

또한 사용한 카메라는 2D 영상만 제공하므로, 화면 속 위치가 같아 보여도 실제 깊이와 크기 차이로 스케일 왜곡이 생길 수밖에 없었습니다. 정면으로만 접근하는 동일한 궤적 대신 그리퍼가 공을 **대각선 방향으로 진입하도록** 시연 각도를 다양화해 위치 오차에 대한 대응 범위를 넓혔습니다.

성공 궤적만 기록하지도 않았습니다. 텔레오퍼레이션 중 일부러 공을 놓친 뒤 다시 접근해 집는 복구 동작을 추가했습니다. 실제 추론에서 공이 미끄러지거나 예상 위치를 벗어나더라도 다음 행동으로 이어갈 수 있도록 실패 이후의 상태와 복구 과정을 데이터에 포함했습니다.

<div class="metric-grid"><div class="metric-card"><span class="metric-value">1 task</span><span class="metric-label">공 하나·색상별 수납함 단위로 분리</span></div><div class="metric-card"><span class="metric-value">≈ 1,000</span><span class="metric-label">공 5개 × 각 200회 시연</span></div><div class="metric-card"><span class="metric-value">15K</span><span class="metric-label">심사 시점 Training Steps</span></div></div>

## 심사 결과: 5개 중 3개 성공

최종적으로 공 5개를 각각 200회씩 기록해 약 1,000개의 단일 태스크 시연 데이터를 확보했습니다. 마감이 오전 9시였기 때문에 학습을 더 이어가지 못하고, 당시 15,000 step까지 학습된 체크포인트로 심사를 진행했습니다.

로봇은 다섯 개의 공 가운데 세 개를 집어 전달하고 색상별 수납함에 넣는 데 성공했습니다. 네 번째 공을 처리하는 과정에서 오른팔이 수납함을 넘어뜨렸고, 환경이 흐트러져 남은 시연은 더 이상 진행할 수 없었습니다. 완주에는 실패했지만, 데이터 전략을 바꾼 뒤 실제 심사 환경에서 세 번의 연속 성공을 확인했습니다.

<figure class="feature-media hackathon-wide-media"><img src="https://raw.githubusercontent.com/TheMomentLab/physical_ai_hackathon/main/assets/demo.gif" alt="두 SO-101 로봇팔이 공을 집어 서로 전달하고 색상별 수납함에 넣는 실제 시연" loading="lazy"><figcaption>실제 양팔 조작 · 공 집기, 그리퍼 간 전달, 색상별 수납함 분류</figcaption></figure>

## 회고: 모방을 넘어 판단할 수 있는 구조가 필요했다

ACT는 짧은 시간 안에 정밀한 양팔 동작을 학습시키는 데 효과적이었지만, 이번 미션에서는 모방학습만으로 해결하기 어려운 한계도 확인했습니다. 정책은 카메라 영상과 현재 관절 상태로 다음 행동을 생성하지만, “현재 몇 번째 공인지”, “어느 색을 다음에 처리해야 하는지”, “수납함이 넘어졌는지”와 같은 명시적인 작업 상태나 목표를 스스로 결정하는 구조는 아니었습니다. 따라서 정해진 순서를 데이터에서 암묵적으로 모방할 뿐, 상황에 따라 다음 행동을 결정론적으로 선택하거나 작업 계획을 다시 세우는 데는 취약했습니다.

다시 설계한다면 ACT를 저수준 양팔 조작 정책으로 사용하되, 색상 인식과 공 개수·작업 진행 상태를 관리하는 상위 상태 머신을 분리하겠습니다. 여기에 수납함 전도나 집기 실패를 감지하는 조건을 추가해, 필요한 단일 태스크 정책을 선택하고 실패 시 복구 동작으로 전환하도록 구성할 수 있습니다. 이번 경험을 통해 모델 선택만큼이나 **태스크를 어떻게 나누고, 실패 상태까지 어떤 데이터로 보여주는가**가 실제 로봇의 강건성을 좌우한다는 점을 배웠습니다.

## 함께한 팀

<figure class="feature-media hackathon-team-media"><img src="https://github.com/TheMomentLab/.github/blob/main/1770642885261.jpg?raw=true" alt="한성대×로보시지 제1회 Physical AI 해커톤에 참가한 4인 팀 단체 사진" loading="lazy"></figure>
