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

아래 그림은 입력 두 개, 은닉 노드 세 개, 출력 두 개로 구성한 신경망입니다. $z_j$와 $s_k$는 각 노드의 가중합, $h_j$와 $\hat y_k$는 출력값입니다. 가중치의 첫 첨자는 출발 노드, 둘째 첨자는 도착 노드를 뜻합니다.

이후 계산은 출력 하나만 둔 경우로 단순화해 $v_{j1}$을 $v_j$, $c_1$을 $b_{\mathrm{out}}$, $\hat y_1$을 $\hat y$로 씁니다.

<img src="../../../../public/images/notes/backpropagation/example-network.png" alt="입력 x1·x2, 은닉 노드 세 개와 출력 노드 두 개를 연결한 신경망. 첫 은닉 노드의 입력 가중치 w11·w21, 편향 b1, 가중합 z1과 출력 h1, 두 출력으로 이어지는 가중치 v11·v12와 출력층 편향 c1·c2, 가중합 s1·s2와 예측값을 표시한다. 나머지 은닉 노드와 연결선의 라벨은 생략한다." width="960" loading="lazy" />

은닉 노드는 입력을 가중치로 합한 $z_j$에 ReLU를 씌워 $h_j$를 냅니다. 출력 노드는 $h_j$를 다시 가중치로 합해 $\hat y$를 냅니다.

$$
z_j=x_1w_{1j}+x_2w_{2j}+b_j,\qquad h_j=\operatorname{ReLU}(z_j)
$$

$$
\hat y=h_1v_1+h_2v_2+h_3v_3+b_{\mathrm{out}}
$$

이렇게 입력에서 출력 쪽으로 차례로 계산하는 과정을 **순전파**(Forward Propagation)라고 합니다.

마지막으로 예측 $\hat y$와 정답 $y$를 비교해 손실을 구합니다. 손실은 MSE를 쓰고, 데이터가 하나라 평균은 생략합니다. $1/2$은 미분할 때 나오는 2를 없애 줍니다.

$$
L=\frac12(\hat y-y)^2
$$

## 손실에서 거꾸로 미분하기

같은 그림에서 $w_{11}$이 영향을 주는 길만 강조했습니다. $w_{11}\to z_1\to h_1\to\hat y$로 이어지고, $\hat y$에서 손실 $L$이 계산됩니다.

<img src="../../../../public/images/notes/backpropagation/path-w11.png" alt="예시 신경망에서 w11, h1, v1, y-hat으로 이어지는 경로만 주황색으로 강조한 그림" width="640" loading="lazy" />

연쇄 법칙에 따라 이 경로의 구간마다 변화율을 곱합니다. 인수는 손실 쪽 구간부터 차례로 $\hat y\to L$, $h_1\to\hat y$, $z_1\to h_1$, $w_{11}\to z_1$의 변화율입니다.

$$
\frac{\partial L}{\partial w_{11}}
=\underbrace{\frac{\partial L}{\partial\hat y}}_{\hat y-y}
\underbrace{\frac{\partial\hat y}{\partial h_1}}_{v_1}
\underbrace{\frac{\partial h_1}{\partial z_1}}_{\operatorname{ReLU}'(z_1)}
\underbrace{\frac{\partial z_1}{\partial w_{11}}}_{x_1}
$$

ReLU의 기울기는 입력이 양수이면 1, 음수이면 0입니다. 0에서는 정의되지 않아 구현에서는 보통 0으로 처리합니다.

### 뒤에서 구한 값 재사용하기

$w_{21}$의 경로도 $w_{11}$과 같은 길 $z_1\to h_1\to\hat y\to L$을 지납니다. 처음 세 인수 $(\hat y-y)\,v_1\operatorname{ReLU}'(z_1)$이 같으므로, $z_1$에서의 미분 $\delta_1$ 하나로 묶어 두고 $h_1$으로 들어오는 선이 함께 씁니다.

<img src="../../../../public/images/notes/backpropagation/shared-delta.png" alt="h1으로 들어오는 두 선 w11, w21을 주황색으로 강조하고 h1 옆에 델타1을 표시한 그림" width="640" loading="lazy" />

$$
\delta_1=\frac{\partial L}{\partial z_1}=(\hat y-y)\,v_1\operatorname{ReLU}'(z_1),\qquad
\frac{\partial L}{\partial w_{11}}=x_1\delta_1,\quad
\frac{\partial L}{\partial w_{21}}=x_2\delta_1,\quad
\frac{\partial L}{\partial b_1}=\delta_1
$$

모든 은닉 노드 $j$에 같은 식이 적용됩니다.

$$
\delta_j=(\hat y-y)\,v_j\operatorname{ReLU}'(z_j),\qquad
\frac{\partial L}{\partial w_{ij}}=x_i\delta_j
$$

출력층 가중치는 손실과 바로 이어져 더 짧습니다. $\partial L/\partial v_j=h_j(\hat y-y)$, $\partial L/\partial b_{\mathrm{out}}=\hat y-y$입니다.

이 식들에 들어가는 $\hat y$, $z_j$, $h_j$는 순전파에서 이미 구한 값이라 다시 계산하지 않고 그대로 씁니다.

그래서 학습은 **순전파 → 손실 계산 → 역전파 → 파라미터 갱신** 순서로 진행됩니다.

## 숫자로 한 번 따라가기

$x_1=1$, $x_2=2$, 정답 $y=4$로 두겠습니다(설명용 값입니다). 처음 값은 다음과 같고, $b_j$와 $b_{\mathrm{out}}$은 0입니다.

| 은닉 노드 $j$ | $w_{1j}$ | $w_{2j}$ | $v_j$ |
| --- | ---: | ---: | ---: |
| 1 | 1 | 0 | 1 |
| 2 | 0 | 1 | 1 |
| 3 | −1 | 0 | 1 |

**순전파.** $z=(1,\,2,\,-1)$이므로 $h=(1,\,2,\,0)$, 예측은 $\hat y=3$, 손실은 $L=\frac12(3-4)^2=0.5$입니다.

**역전파.** $\hat y-y=-1$이고 ReLU 기울기는 $(1,\,1,\,0)$이므로 $\delta=(-1,\,-1,\,0)$입니다. 노드 3은 ReLU의 음수 구간이라 이 노드를 지나는 미분은 모두 0입니다.

| 파라미터 | 노드 1 | 노드 2 | 노드 3 |
| --- | ---: | ---: | ---: |
| $\partial L/\partial w_{1j}=x_1\delta_j$ | −1 | −1 | 0 |
| $\partial L/\partial w_{2j}=x_2\delta_j$ | −2 | −2 | 0 |
| $\partial L/\partial v_j=h_j(\hat y-y)$ | −1 | −2 | 0 |

$\partial L/\partial b_j$는 $\delta_j$와 같고, $\partial L/\partial b_{\mathrm{out}}=-1$입니다.

**갱신.** 학습률 $\eta=0.01$로 모든 파라미터를 $\text{값}-\eta\times\text{미분}$으로 바꿉니다. 예를 들어 $w_{11}$은 $1-0.01(-1)=1.01$입니다. 갱신한 값으로 다시 순전파하면 $h=(1.06,\,2.06,\,0)$이고, $v=(1.01,\,1.02,\,1)$, $b_{\mathrm{out}}=0.01$이므로

$$
\hat y=1.06(1.01)+2.06(1.02)+0.01=3.1818
$$

손실은 0.5에서 약 0.3347로 줄었습니다.

## 참고 자료

- 혁펜하임, 『이지 딥러닝』, 챕터 3.
- [Stanford CS231n · 연쇄 법칙과 역전파](https://cs231n.github.io/optimization-2/).
