---
title: " 01. AI·ML·DL과 네 가지 학습 방식"
description: 인공지능, 머신러닝, 딥러닝의 관계와 지도·비지도·자기지도·강화학습의 차이를 정리한다.
publishedAt: 2026-09-13
tags:
  - Deeplearning
draft: false
featured: false
---

## 1. AI, ML, DL의 차이

### 인공지능(Artificial Intelligence)

인공지능은 컴퓨터가 사람처럼 인식하고 판단하도록 만드는 기술을 아우르는 넓은 개념이다.

사람이 규칙을 직접 정하는 방식부터, 데이터를 통해 학습하는 머신러닝과 딥러닝까지 포함한다.

<img src="/images/notes/easy-deep-learning-ch01/ai-ml-dl-overview.png" alt="인공지능 안에 머신러닝과 딥러닝을 배치한 포함 관계와 알고리즘 예시" width="500" loading="lazy" />

### 머신러닝(Machine Learning)

**머신러닝**은 사람이 모든 판단 규칙을 직접 정하는 대신, 데이터에서 판단에 필요한 패턴을 학습하는 방법이다.

규칙 기반 알고리즘으로 강아지와 고양이를 구분하려면 사람이 직접 구별 규칙을 만들어야 한다.
하지만 같은 동물도 생김새와 자세가 달라 모든 경우에 맞는 규칙을 작성하기는 어렵다.


<img src="/images/notes/easy-deep-learning-ch01/rule-based-classification.png" alt="강아지와 고양이 사진 옆에 사람이 작성한 구별 규칙을 나열한 예시" width="700" loading="lazy" />


머신러닝에서는 데이터를 이용해 모델이 패턴을 학습하도록 한다.

<img src="/images/notes/easy-deep-learning-ch01/data-based-learning.png" alt="강아지와 고양이 사진을 컴퓨터에 입력하는 데이터 기반 학습 흐름" width="700" loading="lazy" />


다양한 상황의 사진을 구분하려면 학습 데이터도 그 상황을 충분히 담고 있어야 한다.

예를 들어, 누워 있거나 뒤돌아 있는 모습, 흐릿하거나 노이즈가 있는 사진을 포함하면 다양한 입력에 대응하는 데 도움이 된다.

다만 데이터가 많고 다양하다는 이유만으로 높은 성능이 보장되지는 않는다.


이렇게 데이터로 모델을 조정하는 과정을 **훈련**이라고 한다. 훈련 후에는 **학습에 사용하지 않은 사진**으로 강아지와 고양이를 얼마나 잘 구분하는지 평가한다.


### 딥러닝(Deep Learning)

**딥러닝**은 머신러닝의 한 종류이다. **깊은 인공 신경망(Deep Neural Network)** 을 이용해 데이터에서 패턴을 학습한다.

<img src="/images/notes/easy-deep-learning-ch01/deep-learning-classification.png" alt="강아지와 고양이 이미지를 입력층, 은닉층, 출력층으로 처리하는 심층 신경망" loading="lazy" />

#### 인공 신경망이란?
위와 같은 여러 층의 인공 신경 다발로 이루어진 수학적 모델이다.

인공 신경은 뇌의 신경세포와 그 연결 방식에서 영감을 얻어 만들었다.

인공 신경망은 데이터 입력을 받는 입력층, 특징을 추출하고 계산하는 은닉층, 결과를 출력하는 출력층이 있다.
깊은 인공 신경망은 매우 많은 층(최소 두 개 이상의 은닉층)을 가진 인공 신경망이다.

<img src="/images/notes/easy-deep-learning-ch01/biological-neuron.png" alt="신경세포의 구조와 신호 입력 및 출력 방향" width="388" loading="lazy" />
<img src="/images/notes/easy-deep-learning-ch01/artificial-neuron-labeled.png" alt="입력 신호가 연결을 통해 인공신경 노드로 들어가 출력되는 구조" loading="lazy" />

#### 비 딥러닝 ML과 DL의 차이
**특징 추출**은 데이터에서 주어진 작업에 필요한 정보를 뽑아내는 과정이다.

전통적인 이미지 분류에서는 사람이 어떤 특징을 사용할지 정하고, 머신러닝 모델은 그 특징을 이용해 이미지를 분류하는 방법을 학습하는 경우가 많았다.

반면 **딥러닝 기반 이미지 분류 모델은 일반적으로 데이터에서 유용한 특징을 추출하는 방법과, 그 특징을 이용해 이미지를 분류하는 방법을 함께 학습한다.**

<img src="/images/notes/easy-deep-learning-ch01/ml-dl-comparison.png" alt="머신러닝과 딥러닝의 특징 추출 및 분류 과정 비교" loading="lazy" />

## 2. 머신러닝의 학습 방식

학습 방식에는 크게 네 가지로 지도학습, 비지도학습, 자기지도학습, 강화학습이 있다.

### 2.1 지도학습(supervised learning)

**지도학습**은 입력 데이터에 정답을 붙이고, 예측과 정답의 차이를 줄이도록 학습하는 방식이다.

입력 데이터에 정답을 붙이는 작업을 **데이터 레이블링**(Data Labeling)이라고 한다.
<img src="/images/notes/easy-deep-learning-ch01/data-labeling.png" alt="지도학습을 위한 데이터 레이블링 예시" width="480" loading="lazy" />

#### 지도학습의 종류
#### 분류와 위치 추정
사진에 무엇이 있는지만 알면 되는지, 어디에 몇 개 있는지도 알아야 하는지에 따라 작업이 달라진다.

- **분류(classification):** 이미지가 무엇을 나타내는지 클래스를 예측한다.

- **객체 위치 추정(localization):** 대상 객체의 위치를 예측한다. 보통 경계 상자로 표시한다.

- **객체 탐지(object detection):** 한 이미지에 있는 여러 객체의 종류와 위치를 함께 예측한다.
<img src="/images/notes/easy-deep-learning-ch01/classification-localization-detection.png" alt="이미지 분류와 객체 위치 추정 및 탐지 비교" loading="lazy" />

#### 분할

경계 상자만으로는 물체의 정확한 모양을 표현하기 어렵다. **분할**은 픽셀 단위로 영역을 구분한다.

- **의미 분할(semantic segmentation):** 모든 픽셀에 대해 어떤 클래스에 속하는지 판단한다.

- **인스턴스 분할(instance segmentation):** 같은 클래스라도 개별 객체를 구분한다. 사람 두 명이 있으면 각각 다른 영역으로 표시한다.

구현 예시: 객체 탐지 → 각 객체 영역의 픽셀 분할
<img src="/images/notes/easy-deep-learning-ch01/image-segmentation.png" alt="이미지의 픽셀 영역을 구분하는 분할 예시" loading="lazy" />
#### 자세 추정과 얼굴 랜드마크 탐지

- **자세 추정(Pose Estimation):** 어깨·팔꿈치·무릎 등 주요 신체 부위의 좌표를 예측한다.

 <img src="/images/notes/easy-deep-learning-ch01/pose-estimation.png" alt="신체 주요 부위의 위치를 찾는 자세 추정 예시" width="347" loading="lazy" />


- **얼굴 랜드마크 탐지:** 눈·코·입 등 얼굴의 주요 특징점 좌표를 예측한다.
<img src="/images/notes/easy-deep-learning-ch01/face-landmarks.png" alt="얼굴 주요 특징점의 위치를 찾는 랜드마크 탐지 예시" width="200" loading="lazy" />



사람이 직접 정답(레이블)을 붙이는 데에는 많은 시간과 비용이 든다.

### 2.2 자기지도학습(self-supervised learning)

지도학습의 한계를 개선하기 위해 나온 학습 방식이다.
별도로 사람이 만든 레이블 없이, 데이터 자체에서 학습에 필요한 정답이나 목표를 자동으로 만들어 학습하는 방식이다.

넓은 의미에서는 비지도학습의 한 종류로 볼 수 있지만, 데이터로부터 입력과 정답에 해당하는 학습 신호를 만든 뒤 지도학습과 유사한 방식으로 모델을 학습한다는 특징이 있어 별도로 구분하기도 한다.

이때 대표적으로 사용하는 방법이 **사전학습(Pre-training)과 미세조정(Fine-tuning)​**이다.

먼저 레이블이 없는 대량의 데이터를 이용해 가짜 목표를 만들고 모델을 사전학습한 뒤, 실제로 하려는 작업의 레이블이 있는 소량의 데이터를 이용해 모델을 미세조정한다.

이를 통해 적은 양의 레이블 데이터만으로도 특정 작업에 적합한 모델을 만들 수 있다.

<img src="/images/notes/easy-deep-learning-ch01/pretraining-finetuning.png" alt="프리텍스트 작업으로 사전학습한 모델을 다운스트림 작업으로 전이하고 미세조정하는 과정" width="578" loading="lazy" />

| 단계                | 학습 내용                                                                                                              | 사용하는 데이터           |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------ |
| 사전학습(Pretraining) | 가짜 연습 문제(Pretext Task)를 풀며 특징 학습<br>Predictor : 가짜 연습 문제(Pretext Task)를 풀기 위한 **임시 채점기**                           | 레이블이 없는 대량의 데이터    |
| 미세조정(Fine-tuning) | 실제로 풀려는 다운스트림 작업(Downstream Task)에 맞게 모델 조정<br> Predictor : 우리가 진짜 풀고 싶은 실전 문제(Downstream Task)를 위한 **실전용 최종 출력기** | 해당 작업의 레이블이 있는 데이터 |

사전학습 방식은 대표적으로 두 가지로 나뉜다.
#### 자가예측 방식 (Self-Prediction)

하나의 data sample 내에서 한 파트를 통해서 다른 파트를 예측하는 task를 말한다.

<img src="/images/notes/easy-deep-learning-ch01/self-prediction-diagram.png" alt="하나의 데이터에서 일부를 보고 나머지 부분을 예측하는 자가예측 방식" width="308" loading="lazy" />



##### 이미지에서 예시

- **Context Prediction · 위치 관계 예측**
	이미지에 정답 레이블이 없어도 어디에서 잘라낸 조각인지는 알 수 있다. 이 위치 정보를 학습 목표로 사용하는 방법이 **Context Prediction**이다. 작은 이미지 영역인 패치 사이의 상대 위치를 예측한다.
	순서

	1. 이미지에서 기준 패치를 무작위로 선택한다.
	2. 기준 패치 주변에서 같은 크기의 패치를 선택한다.
	3. 두 패치를 입력하고, 주변 패치가 기준 패치의 어느 방향에 있었는지 예측한다.

<figure>
  <img src="/images/notes/easy-deep-learning-ch01/context-prediction.jpg" alt="고양이 코의 기준 패치와 귀 패치로 상대 위치 3번을 예측하는 Context Prediction 원 저자 그림" width="1024" loading="lazy" />
  <figcaption>출처: Doersch · Gupta · Efros, <a href="https://graphics.cs.cmu.edu/projects/deepContext/">ICCV 2015 프로젝트 페이지</a>.</figcaption>
</figure>

패치의 위치는 추출 과정에서 알 수 있으므로 별도 레이블링 없이 여러 학습 쌍을 만들 수 있다. 이미지의 픽셀과 물체의 부분이 일정한 구조를 가진다는 점을 활용한다. [원 논문](https://arxiv.org/abs/1505.05192)

##### 자연어에서 예시

- **GPT:** 앞선 토큰을 보고 다음 토큰을 예측한다(Next Token Prediction).
- **BERT:** 문장의 일부를 가리고 해당 토큰을 예측한다(Masked Token Prediction). 원래 BERT는 두 문장 구간이 연속된 것인지 예측하는 작업(Next Sentence Prediction)도 사용했다.

두 방식 모두 원문으로부터 학습 목표를 만든다. [BERT 공식 설명](https://github.com/google-research/bert#what-is-bert)

#### 대조학습 방식 (Contrastive Learning)

이미지 사이의 관계를 예측하는 task를 말한다.

<img src="/images/notes/easy-deep-learning-ch01/contrastive-learning-diagram.png" alt="서로 다른 두 데이터 사이의 관계를 비교하는 대조학습 개념도" width="385" loading="lazy" />

##### 이미지에서 예시: SimCLR

1. 하나의 이미지에 서로 다른 변형을 적용한다. 예: 일부 자르기, 밝기·색상 조절.
2. 변형된 이미지를 모델에 넣어 각각 숫자 벡터로 표현한다.
3. 같은 원본의 벡터는 가까워지고, 다른 원본의 벡터는 멀어지도록 모델을 조정한다.


<figure>
  <img src="/images/notes/easy-deep-learning-ch01/simclr.png" alt="강아지와 의자 사진을 각각 두 번 변형해 같은 원본의 표현은 당기고 다른 원본은 밀어내는 SimCLR 그림" width="640" loading="lazy" />
  <figcaption>출처: Chen et al., <a href="https://simclr.github.io/">SimCLR 공식 프로젝트 페이지</a>.</figcaption>
</figure>

두 변형의 표현이 가까워지도록 모델을 조정하면서, 변형 전후에도 유지되는 핵심 특징을 학습한다. [SimCLR 원 논문](https://arxiv.org/abs/2002.05709)

### 2.3 비지도학습

**레이블이 없는 데이터에서 패턴이나 구조를 찾는 방식이다.**

대표 예시: 군집화, 차원 축소

#### 군집화

정답 분류가 없는 데이터에서 비슷한 특징이 있는 데이터끼리 묶는 방식이다.

주요 활용
	데이터에서 이상치 탐지
	 이미지 분할
	 취향이 비슷한 유저 그룹을 찾아 맞춤형 콘텐츠 추천

주요 알고리즘
- **K-means:** 군집 수 K를 정하고, 가까운 중심에 데이터를 배정한 뒤 중심을 갱신하는 과정을 반복한다.
- **DBSCAN:** 데이터가 밀집한 영역을 그룹으로 묶는 밀도 기반 방법이다.

<img src="/images/notes/easy-deep-learning-ch01/clustering-groups.png" alt="흩어진 데이터를 유사성에 따라 보라색, 초록색, 노란색의 세 그룹으로 묶는 군집화 예시" width="507" loading="lazy" />

#### 차원 축소

데이터의 특징이 많으면 계산량이 늘고, 분포를 눈으로 확인하기도 어렵다. **차원 축소**는 중요한 특징을 가능한 한 유지하면서 특징 수를 줄이는 방법이다.

<img src="/images/notes/easy-deep-learning-ch01/pca-dimensionality-reduction.png" alt="3차원 데이터를 PCA로 두 주성분 PC1과 PC2의 2차원 공간에 나타낸 차원 축소 예시" width="573" loading="lazy" />

활용 예시: 고차원 데이터 시각화, 계산량 감소

- **PCA(Principal Component Analysis):** 데이터의 분산을 최대로 보존하는 축으로 투영해 차원을 축소하는 기법이다.
	- 분산이 사라지면 데이터들이 다 똑같아 보여서 구별하지 못하기 때문이다.

- **SVD(Singular Value Decomposition):** 복잡한 직사각형 숫자 표(행렬)를 3개의 단순한 부품 표로 쪼개는 기술이다. 일부 성분을 남기는 근사나 PCA 계산에 활용할 수 있다.

[군집화·차원 축소 참고 문서](https://scikit-learn.org/stable/unsupervised_learning.html)

### 2.4 강화학습

**강화학습(Reinforcement Learning)** 은 원하는 행동에 대해서 보상과 벌을 설계하여 그 환경 안에서 시행착오를 하며 상을 받고 벌을 피하는 방식으로 최적의 행동을 스스로 학습하는 방식이다.

기존의 신경망들이 라벨(정답)이 있는 데이터를 통해서 가중치와 편향을 학습하는 것과 비슷하게 보상(Reward)이라는 개념을 사용하여 가중치와 편향을 학습한다. 목적은 최적의 행동 양식 또는 정책을 학습하는 것이다.

출처: [https://davinci-ai.tistory.com/31](https://davinci-ai.tistory.com/31) [DAVINCI - AI:티스토리]


<img src="/images/notes/easy-deep-learning-ch01/reinforcement-learning-grid-feedback.png" alt="첫 번째 시도에서 로봇이 −10점 칸으로 이동하고, 두 번째 시도에서는 그 방향을 피하는 격자 예시. 오른쪽 위에는 +100점 칸이 있다." width="624" loading="lazy" />

#### 강화학습에 나오는 용어 정리

Agent : 학습을 통해 의사 결정을 내리는 주체 (예: 훈련하는 개, 로봇, 게임 캐릭터)
Action : Agents가 그 순간 하는 행동
Reward : Agents가 Action을 따라 받는 보상
Environment : 강화학습을 하는 환경, 보상 설계
state : Agents가 현재 환경이 처한 상황이나 정보. (현재 위치, 관절값, 승점)
Policy : 상태에 따른 행동을 선택하는 전략
가치함수 : Policy에서 미래 보상의 기댓값



## 참고 자료

- [NeurIPS 2021 · Self-Supervised Learning: Self-Prediction and Contrastive Learning](https://nips.cc/media/neurips-2021/Slides/21895.pdf).

- 혁펜하임, 『이지 딥러닝』, 챕터 1.
- Doersch et al., [Context Prediction](https://arxiv.org/abs/1505.05192), 2015.
- Chen et al., [SimCLR](https://arxiv.org/abs/2002.05709), 2020.
- [BERT 공식 설명](https://github.com/google-research/bert#what-is-bert).
- [scikit-learn 비지도학습 문서](https://scikit-learn.org/stable/unsupervised_learning.html).
- [Spinning Up 강화학습 기본 개념](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html).
