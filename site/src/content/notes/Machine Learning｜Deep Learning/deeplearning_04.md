---
title: 4. 역전파 알고리즘
slug: deep-learning/easy-deep-learning-ch03
description: 예측값에서 손실까지 이어지는 계산 경로를 거슬러 올라가며 가중치의 미분을 구하고, 그 값으로 가중치를 갱신합니다.
publishedAt: 2026-09-13
updatedAt: 2026-10-03
tags:
  - Deep learning
draft: false
featured: false
---
## 역전파 알고리즘

**역전파**(Backpropagation)는 손실에 대한 모든 가중치의 기울기를 구하는 알고리즘입니다.

경사하강법([2장](/notes/deep-learning/easy-deep-learning-ch02/))으로 가중치를 갱신하려면 매번 이 기울기를 구해야 합니다.

출력층 가중치는 예측값을 직접 바꾸므로 기울기를 바로 구할 수 있습니다.
은닉층 가중치는 은닉 노드 → 예측값 → 손실 순서로 영향을 주므로, 거쳐 가는 단계마다 미분해야 합니다.

역전파의 핵심은 [연쇄 법칙](/notes/deep-learning/easy-deep-learning-ch02/)과 계산 결과의 재사용입니다.
손실 쪽부터 미분을 거꾸로 곱해 올라가면서, 뒤에서 먼저 구한 미분과 순전파에서 구한 값을 다시 씁니다.

## 예측값과 손실 계산하기

아래  신경망을 통해 계산 과정을 보여드리겠습니다.

<img src="../../../../public/images/notes/backpropagation/example-network.png" alt="입력 두 개, 은닉 노드 세 개와 출력 노드 두 개를 연결한 신경망. 첫 은닉 노드와 두 출력의 경로에만 가중치 w, 편향 b, 활성화 전 값 z와 출력값 a를 표시하고, 윗첨자로 층 번호를 구분한다." width="960" loading="lazy" />
가중치 : $w$
편향 :  $b$
노드 입력값 : $z$
노드 출력값 : $a$
윗첨자는 층 번호
아랫첨자는 노드 번호

**첫 은닉 노드에 들어가는 값.** 입력값에 각각 가중치를 곱해 더하고, 편향을 더합니다.

$$
z^1_1=x_1w^1_1+x_2w^1_2+b^1_1
$$

**첫 은닉 노드에서 나오는 값.** $z^1_1$에 ReLU를 적용합니다. 나머지 은닉 노드도 같은 순서로 계산합니다.

$$
a^1_1=\operatorname{ReLU}(z^1_1)
$$

**첫 출력 노드에 들어가는 값.** 은닉 노드 세 개의 출력에 각각 가중치를 곱해 더하고, 출력층 편향을 더합니다.

$$
z^2_1=a^1_1w^2_1+a^1_2w^2_3+a^1_3w^2_5+b^2_1
$$

**첫 출력 노드에서 나오는 값.** 그림의 출력층은 들어온 값을 그대로 내보냅니다. 이 값이 예측값입니다.

$$
a^2_1=z^2_1,\qquad \hat y_1=a^2_1
$$

두 번째 출력도 같은 방식으로 계산하되, 가중치는 $w^2_2$, $w^2_4$, $w^2_6$, 편향은 $b^2_2$를 씁니다.

이렇게 입력에서 출력 쪽으로 차례로 계산하는 과정을 **순전파**(Forward Propagation)라고 합니다.

이후 미분과 숫자 예제는 출력 하나만 둔 경우로 단순화해 첫 출력 $\hat y_1$을 따라갑니다.

마지막으로 예측 $\hat y_1$과 정답 $y$를 비교해 손실을 구합니다. 손실은 MSE를 쓰고, 데이터가 하나라 평균은 생략합니다. $1/2$은 미분할 때 나오는 2를 없애 줍니다.

$$
L=\frac12(\hat y_1-y)^2
$$

## 손실에서 거꾸로 미분하기

출력 하나로 단순화한 그림에서 $w^1_1$이 영향을 주는 길만 강조했습니다. $w^1_1\to z^1_1\to a^1_1\to\hat y_1$로 이어지고, $\hat y_1$에서 손실 $L$이 계산됩니다.

<img src="../../../../public/images/notes/backpropagation/path-w11.png" alt="출력 하나를 둔 신경망에서 1층 가중치 w1, 활성화 전 값 z와 출력 a, 2층 가중치 w1을 거쳐 예측값으로 이어지는 경로를 주황색으로 강조한 그림" width="640" loading="lazy" />

연쇄 법칙에 따라 이 경로의 구간마다 변화율을 곱합니다. 인수는 손실 쪽 구간부터 차례로 $\hat y_1\to L$, $a^1_1\to\hat y_1$, $z^1_1\to a^1_1$, $w^1_1\to z^1_1$의 변화율입니다.

$$
\frac{\partial L}{\partial w^1_1}
=\underbrace{\frac{\partial L}{\partial\hat y_1}}_{\hat y_1-y}
\underbrace{\frac{\partial\hat y_1}{\partial a^1_1}}_{w^2_1}
\underbrace{\frac{\partial a^1_1}{\partial z^1_1}}_{\operatorname{ReLU}'(z^1_1)}
\underbrace{\frac{\partial z^1_1}{\partial w^1_1}}_{x_1}
$$

ReLU의 기울기는 입력이 양수이면 1, 음수이면 0입니다. 0에서는 정의되지 않아 구현에서는 보통 0으로 처리합니다.

### 뒤에서 구한 값 재사용하기

$w^1_2$의 경로도 $w^1_1$과 같은 길 $z^1_1\to a^1_1\to\hat y_1\to L$을 지납니다. 처음 세 인수 $(\hat y_1-y)\,w^2_1\operatorname{ReLU}'(z^1_1)$이 같으므로, $z^1_1$에서의 미분 $\delta_1$ 하나로 묶어 두고 $a^1_1$을 계산하는 두 입력선이 함께 씁니다.

<img src="../../../../public/images/notes/backpropagation/shared-delta.png" alt="첫 은닉 노드로 들어오는 1층 가중치 w1과 w2를 주황색으로 강조하고 활성화 전 값 z에 대한 미분 델타1을 표시한 그림" width="640" loading="lazy" />

$$
\delta_1=\frac{\partial L}{\partial z^1_1}=(\hat y_1-y)\,w^2_1\operatorname{ReLU}'(z^1_1),\qquad
\frac{\partial L}{\partial w^1_1}=x_1\delta_1,\quad
\frac{\partial L}{\partial w^1_2}=x_2\delta_1,\quad
\frac{\partial L}{\partial b^1_1}=\delta_1
$$

모든 은닉 노드 $j$에 같은 식이 적용됩니다.

$$
\delta_j=(\hat y_1-y)\,w^2_{2j-1}\operatorname{ReLU}'(z^1_j),\qquad
\frac{\partial L}{\partial w^1_{2j-2+i}}=x_i\delta_j
$$

출력층 가중치는 손실과 바로 이어져 더 짧습니다. $\partial L/\partial w^2_{2j-1}=a^1_j(\hat y_1-y)$, $\partial L/\partial b^2_1=\hat y_1-y$입니다.

이 식들에 들어가는 $\hat y_1$, $z^1_j$, $a^1_j$는 순전파에서 이미 구한 값이라 다시 계산하지 않고 그대로 씁니다.

그래서 학습은 **순전파 → 손실 계산 → 역전파 → 파라미터 갱신** 순서로 진행됩니다.

## 숫자로 한 번 따라가기

$x_1=1$, $x_2=2$, 정답 $y=4$로 두겠습니다(설명용 값입니다). 처음 값은 다음과 같고, $b^1_j$와 $b^2_1$은 0입니다.

| 은닉 노드 $j$ | $w^1_{2j-1}$ | $w^1_{2j}$ | $w^2_{2j-1}$ |
| --- | ---: | ---: | ---: |
| 1 | 1 | 0 | 1 |
| 2 | 0 | 1 | 1 |
| 3 | −1 | 0 | 1 |

**순전파.** $z^1=(1,\,2,\,-1)$이므로 $a^1=(1,\,2,\,0)$, 예측은 $\hat y_1=3$, 손실은 $L=\frac12(3-4)^2=0.5$입니다.

**역전파.** $\hat y_1-y=-1$이고 ReLU 기울기는 $(1,\,1,\,0)$이므로 $\delta=(-1,\,-1,\,0)$입니다. 노드 3은 ReLU의 음수 구간이라 이 노드를 지나는 미분은 모두 0입니다.

| 파라미터 | 노드 1 | 노드 2 | 노드 3 |
| --- | ---: | ---: | ---: |
| $\partial L/\partial w^1_{2j-1}=x_1\delta_j$ | −1 | −1 | 0 |
| $\partial L/\partial w^1_{2j}=x_2\delta_j$ | −2 | −2 | 0 |
| $\partial L/\partial w^2_{2j-1}=a^1_j(\hat y_1-y)$ | −1 | −2 | 0 |

$\partial L/\partial b^1_j$는 $\delta_j$와 같고, $\partial L/\partial b^2_1=-1$입니다.

**갱신.** 학습률 $\eta=0.01$로 모든 파라미터를 $\text{값}-\eta\times\text{미분}$으로 바꿉니다. 예를 들어 $w^1_1$은 $1-0.01(-1)=1.01$입니다. 갱신한 값으로 다시 순전파하면 $a^1=(1.06,\,2.06,\,0)$이고, $(w^2_1,\,w^2_3,\,w^2_5)=(1.01,\,1.02,\,1)$, $b^2_1=0.01$이므로

$$
\hat y_1=1.06(1.01)+2.06(1.02)+0.01=3.1818
$$

손실은 0.5에서 약 0.3347로 줄었습니다.

## 참고 자료

- 혁펜하임, 『이지 딥러닝』, 챕터 3.
- [Stanford CS231n · 연쇄 법칙과 역전파](https://cs231n.github.io/optimization-2/).
