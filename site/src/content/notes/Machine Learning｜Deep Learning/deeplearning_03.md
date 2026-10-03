---
title: 3. 활성화 함수
slug: deep-learning/linear-nonlinear-activations
description: 비선형 활성화 함수가 필요한 이유와 선형 출력을 쓰는 경우를 살펴보고, ReLU와 Leaky ReLU, Swish, GELU를 비교합니다.
publishedAt: 2026-09-27
tags:
  - Deep learning
draft: false
featured: false
---

## 1. 비선형 활성화 함수가 필요한 이유

[2장](/notes/deep-learning/easy-deep-learning-ch02/)에서 우리는 두 가지 핵심 모델을 살펴봤습니다.

### 선형 계산만 반복하면

그림의 입력 $x_1, x_2$가 은닉 노드 세 개를 거쳐 출력으로 전달되는 과정을 식으로 써 보겠습니다. 비선형 활성화 함수가 없는 경우를 보기 위해, $f_1$과 $f_2$는 입력을 그대로 내보내는 항등 함수로 둡니다.

<img src="../../../../public/images/notes/linear-nonlinear-activations/network-linear-composition.png" alt="입력 x1과 x2에서 가중치 W1부터 W6, 바이어스 b1부터 b3를 사용하는 은닉 노드 세 개를 거쳐 출력 노드 두 개로 연결되는 신경망" width="724" loading="lazy" />

은닉 노드의 출력을 위에서부터 $h_1, h_2, h_3$라고 하면 다음과 같습니다. 그림의 $W_1\sim W_6$는 각 연결의 가중치이고, $b_1,b_2,b_3$는 각 은닉 노드에 더하는 바이어스입니다.

$$
\begin{aligned}
h_1 &= W_1x_1 + W_2x_2 + b_1 \\
h_2 &= W_3x_1 + W_4x_2 + b_2 \\
h_3 &= W_5x_1 + W_6x_2 + b_3
\end{aligned}
$$

먼저 위쪽 출력 $y_1$을 보겠습니다. 그림에 표시되지 않은 출력층 가중치를 $V_1,V_2,V_3$, 바이어스를 $c_1$이라고 두면:

$$y_1 = V_1h_1 + V_2h_2 + V_3h_3 + c_1$$

여기에 은닉 노드의 식을 대입하고 $x_1,x_2$끼리 묶으면 다음과 같습니다.

$$
\begin{aligned}
y_1 &= V_1(W_1x_1 + W_2x_2 + b_1) \\
&\quad + V_2(W_3x_1 + W_4x_2 + b_2) \\
&\quad + V_3(W_5x_1 + W_6x_2 + b_3) + c_1 \\
&= (V_1W_1 + V_2W_3 + V_3W_5)x_1 \\
&\quad + (V_1W_2 + V_2W_4 + V_3W_6)x_2 \\
&\quad + (V_1b_1 + V_2b_2 + V_3b_3 + c_1) \\
&= W'_1x_1 + W'_2x_2 + b'_1
\end{aligned}
$$

각 괄호를 새로운 가중치와 바이어스로 묶었을 뿐인데, 은닉 노드 세 개를 거친 계산이 입력 두 개에서 출력으로 바로 연결되는 식이 되었습니다. 아래쪽 출력 $y_2$도 같은 방식으로 정리됩니다.

층을 더 쌓아도 마찬가지입니다. 비선형 활성화 함수가 없으면, 전체 계산은 입력에 가중치를 곱하고 바이어스를 더하는 하나의 식으로 합쳐집니다. 엄밀히는 바이어스를 포함한 아핀 변환이며, 여기서는 선형 계산이라고 부르겠습니다.

### 선형 활성화 함수는 언제 사용할까요?

은닉층은 비선형 함수를 쓰는 것이 기본이지만, 특수한 목적으로 선형 출력을 유지하는 영역이 있습니다.

| **사용 위치**  | **사용 목적**                            | **실제 사례**                                    |
| ---------- | ------------------------------------ | -------------------------------------------- |
| **출력층**    | 출력 범위를 제한(0~1 등)하지 않고 임의의 실수를 그대로 예측 | **회귀(Regression)** 모델 (예: 주가·매출 예측)          |
| **은닉층 일부** | 비선형 변환으로 인한 과도한 정보 파괴 방지             | **MobileNetV2**의 선형 병목(Linear Bottleneck) 구간 |

## 2. ReLU(Rectified Linear Unit)

널리 쓰이는 비선형 활성화 함수입니다. 양수 입력이 들어오면 그대로 출력하고 음수 입력이 들어오면 0으로 출력합니다.

<img src="../../../../public/images/notes/easy-deep-learning-ch03/relu.jpeg" alt="음수 입력에서 0, 양수 입력에서 입력값을 그대로 출력하는 ReLU 그래프" loading="lazy" width="311" height="210" />

ReLU는 양수 구간의 기울기가 1이어서 sigmoid의 포화 구간에서 생기는 기울기 소실(Vanishing Gradient)을 줄이는 데 도움이 됩니다. 다만 음수 입력은 모두 0이 되어 정보가 사라집니다.
학습 데이터에 대해 한 뉴런의 입력이 계속 음수이면 기울기도 계속 0이 되어 학습하지 못하는 **죽은 뉴런** 문제가 생길 수 있습니다.

## 3. ReLU의 대안
### Leaky ReLU

<img src="../../../../public/images/notes/linear-nonlinear-activations/leaky-relu.png" alt="음수 구간의 기울기를 0.1로 설정한 Leaky ReLU 그래프" width="391" loading="lazy" />

음수 구간에도 작은 양의 기울기를 두는 비선형 함수입니다. 기울기는 설정에 따라 달라지며, 위 그래프에서는 0.1을 사용합니다.

생성적 적대 신경망(Generative Adversarial Network, GAN) 등에 사용합니다.

음수 구간에서도 기울기를 전달하며, 곱셈과 비교만으로 계산할 수 있습니다. 실제 실행 속도는 장치와 구현에 따라 달라집니다.

### Swish / SiLU (Sigmoid Linear Unit)
<img src="../../../../public/images/notes/linear-nonlinear-activations/silu.png" alt="입력에 sigmoid 값을 곱한 SiLU 함수 그래프" width="397" loading="lazy" />
구글이 탐색 알고리즘으로 찾아낸 함수로 입력값 $x$에 시그모이드 함수 $\sigma(\beta x)$를 곱한 형태입니다.

$x \cdot \sigma(\beta x)$
- **$x$**: 들어오는 원래 신호(입력값)
- **$\sigma(\cdot)$ (시그모이드)**: 어떤 값이든 0과 1 사이의 값으로 압축하는 함수 (0% ~ 100%)
- **$\beta$ (베타)**: 곡선의 가파른 정도를 조절하는 상수 (보통 기본값으로 1을 사용하며, $\beta=1$일 때를 **SiLU**라고 합니다)

Swish 원 논문에서는 여러 이미지 분류 실험에서 ReLU보다 좋은 결과를 보고했습니다. 성능 차이는 모델과 학습 조건에 따라 달라집니다. [Swish 원 논문](https://arxiv.org/abs/1710.05941)

### GELU (Gaussian Error Linear Unit)
<img src="../../../../public/images/notes/linear-nonlinear-activations/gelu.svg" alt="GELU 함수 그래프. 음수 입력에서 0 아래로 조금 내려갔다가 원점을 지나 양수 입력에서 거의 직선으로 증가한다" loading="lazy" width="800" height="500" />

$$GELU(x) = x \cdot \Phi(x)$$
- **$x$**: 원래 들어온 입력값
- **$\Phi(x)$**: 표준정규분포($\mathcal{N}(0, 1)$)의 **누적분포함수(CDF)**
#### 입력 크기에 따라 부드럽게 조절하기
누적확률 $\Phi(x)$는 유한한 입력에서 0과 1 사이의 값을 가집니다. GELU는 이 값을 입력에 곱하며, 무작위로 출력을 선택하는 함수는 아닙니다.

- **$x$가 큰 양수일 때 (예: $x = +3$):** $\Phi(3) \approx 0.999$이므로, $x$를 거의 100% 그대로 통과시킵니다.
- **$x$가 큰 음수일 때 (예: $x = -3$):** $\Phi(-3) \approx 0.001$이므로, 출력이 거의 0에 수렴합니다.

- **$x = 0$ 근처일 때:** $\Phi(x)$가 약 0.5이므로 출력은 약 $0.5x$입니다. $x=0$에서는 출력도 0입니다.

BERT나 Vision Transformer 같은 Transformer 모델에 사용합니다. [GELU 원 논문](https://arxiv.org/abs/1606.08415)

