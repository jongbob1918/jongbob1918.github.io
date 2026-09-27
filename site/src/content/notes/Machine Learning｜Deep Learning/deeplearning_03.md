---
title: 3. 활성화 함수
slug: deep-learning/linear-nonlinear-activations
description: 비선형 활성화 함수가 필요한 이유와 선형 출력을 쓰는 경우를 살펴보고, ReLU의 정보 손실을 MobileNetV2 사례에 연결합니다.
publishedAt: 2026-09-27
tags:
  - Deep learning
draft: false
featured: false
---



## 1. 비선형 활성화 함수가 필요한 이유

![[Pasted image 20260927161552.png|515]]

### 선형 계산만 반복하면

x입력층에서 나온 값들이 만약 선형 활성화함수 f1를 통과한다면 값들은 선형성이 유지됩니다.

층을 깊게 쌓으면 더 복잡한 관계를 표현할 수 있을까요? 

활성화 함수를 입력을 그대로 내보내는 항등 함수 $f(x)=x$로 둘 경우:

$$\begin{aligned} \hat{y} &= w_2(w_1x + b_1) + b_2 \\ &= \underbrace{(w_2 w_1)}_{W'}x + \underbrace{(w_2 b_1 + b_2)}_{B'} \\ &= W'x + B' \end{aligned}$$

- **결과:** 100개 층을 쌓아도 단 1개 층($W'x + B'$)과 수학적으로 완전히 같습니다.
    
- **해결책:** 층 사이에 **비선형 활성화 함수**를 넣어야 연산이 하나로 합쳐지지 않고 복잡한 고차원 패턴을 표현할 수 있습니다.
    

##### 선형 활성화 함수는 언제 쓸까?

은닉층은 비선형 함수를 쓰는 것이 기본이지만, 특수한 목적으로 선형 출력을 유지하는 영역이 있습니다.

| **사용 위치**  | **사용 목적**                            | **실제 사례**                                    |
| ---------- | ------------------------------------ | -------------------------------------------- |
| **출력층**    | 출력 범위를 제한(0~1 등)하지 않고 임의의 실수를 그대로 예측 | **회귀(Regression)** 모델 (예: 주가·매출 예측)          |
| **은닉층 일부** | 비선형 변환으로 인한 과도한 정보 파괴 방지             | **MobileNetV2**의 선형 병목(Linear Bottleneck) 구간 |

## 2. ReLU(Rectified Linear Unit)

널리 쓰이는 비선형 활성화 함수입니다. 양수입력이 들어오면 그대로 출력하고 음수입력이 들어오면 0으로 출력합니다. 

<img src="../../../../public/images/notes/easy-deep-learning-ch03/relu.jpeg" alt="음수 입력에서 0, 양수 입력에서 입력값을 그대로 출력하는 ReLU 그래프" loading="lazy" width="311" height="210" />



ReLU는 연산이 빠르고 기울기 소실(Vanishing Gradient)을 줄여주지만, 정보 손실이 발생합니다.
은닉층이 층이 적을경우 기울기 소실이 일어나지만 층이 많을경우 기울기 손실을 줄여줍니다.
이런 현상은 음수를 0으로 만들어버려 죽은뉴런 문제를 만들기 때문이다.

## 3. RELU의 대안책
###  Leaky ReLU

![[Pasted image 20260927171402.png]]

음수영역에서 기울기가 0이 아닌 0.01로 설정한 비선형 함수입니다.

GAN(Generative Adversarial Network)과 경량 CNN에서 많이 사용합니다.

지수 함수($e^x$)나 시그모이드처럼 복잡한 초월함수 연산이 전혀 없어, NPU/엣지 디바이스나 실시간 처리가 중요한 **경량 모델**에서 압도적인 속도를 냅니다.


### Swish / SiLU (Sigmoid Linear Unit)
![[Pasted image 20260927171844.png|397]]
구글이 탐색 알고리즘으로 찾아낸 함수로 입력값 $x$에 시그모이드 함수 $\sigma(\beta x)$를 곱한 형태입니다

$x \cdot \sigma(\beta x)$
- **$x$**: 들어오는 원래 신호(입력값)
- **$\sigma(\cdot)$ (시그모이드)**: 어떤 값이든 0과 1 사이의 값으로 압축하는 함수 (0% ~ 100%)
- **$\beta$ (베타)**: 곡선의 가파른 정도를 조절하는 상수 (보통 기본값으로 1을 사용하며, $\beta=1$일 때를 **SiLU**라고 부름)

Efficient Net이나, Mamba에 활용되어 Relu보다 좋은 성능을 보인다고 나옴
### GELU (Gaussian Error Linear Unit)
<img src="../../../../public/images/notes/linear-nonlinear-activations/gelu.svg" alt="GELU 함수 그래프. 음수 입력에서 0 아래로 조금 내려갔다가 원점을 지나 양수 입력에서 거의 직선으로 증가한다" loading="lazy" width="800" height="500" />

$$GELU(x) = x \cdot \Phi(x)$$
- **$x$**: 원래 들어온 입력값
- **$\Phi(x)$**: 표준정규분포($\mathcal{N}(0, 1)$)의 **누적분포함수(CDF)**
#### 의미: "확률적으로 살려두기"
정규분포 확률 $\Phi(x)$는 항상 0과 1 사이의 값(확률)을 가집니다.

- **$x$가 큰 양수일 때 (예: $x = +3$):** $\Phi(3) \approx 0.999$이므로, $x$를 거의 100% 그대로 통과시킵니다.
- **$x$가 큰 음수일 때 (예: $x = -3$):** $\Phi(-3) \approx 0.001$이므로, 출력이 거의 0에 수렴합니다.
    
- **$x = 0$ 근처일 때:** $\Phi(0) = 0.5$이므로, 절반($0.5x = 0$)만 통과시키며 부드러운 곡선을 만듭니다.

LLM / Transformer / Vision Transformer에서 많이 사용합니다.

