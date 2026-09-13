---
title: "이지 딥러닝 3장 · MLP의 행렬 표현과 역전파"
description: ""
publishedAt: 2026-09-13
category: deep-learning
type: concept
tags: [딥러닝, 이지딥러닝, MLP, 행렬, 역전파]
draft: false
featured: false
---

## 이번 장에서 이해하려는 것

MLP를 행렬과 수식으로 표현하는 방법. 역전파로 각 가중치와 바이어스의 미분값을 계산하는 과정.

## 1. MLP를 행렬로 표현하기

### 노드마다 계산하면 식이 길어진다

2장에 이어 조회수와 영상 길이로 수익을 예측한다고 해보자. 이번에는 다음 구조의 **다층 퍼셉트론**(Multi-Layer Perceptron, MLP)을 사용한다.

| 층 | 노드 수 | 값 |
| --- | --- | --- |
| 입력층 | 2개 | 조회수 $x_1$, 영상 길이 $x_2$ |
| 은닉층 | 3개 | 변환한 특징 $h_1,h_2,h_3$ |
| 출력층 | 1개 | 예측 수익 $\hat y$ |

은닉층의 활성화 함수를 $f_1$이라고 하면, 세 노드의 출력은 다음과 같다.

$$
\begin{aligned}
h_1&=f_1(x_1w_{11}+x_2w_{21}+b_1)\\
h_2&=f_1(x_1w_{12}+x_2w_{22}+b_2)\\
h_3&=f_1(x_1w_{13}+x_2w_{23}+b_3)
\end{aligned}
$$

$w_{ij}$는 입력 $i$에서 은닉 노드 $j$로 이어지는 가중치다. 노드 수가 늘어나면 같은 형태의 식을 계속 적어야 한다.

### 입력을 벡터로 묶기

입력 두 개를 **행벡터** $\mathbf{x}=[x_1\;x_2]$로 묶는다. 첫 번째 은닉 노드의 가중합은 행벡터와 열벡터의 곱, 즉 내적으로 쓸 수 있다.

$$
z_1=
\begin{bmatrix}x_1&x_2\end{bmatrix}
\begin{bmatrix}w_{11}\\w_{21}\end{bmatrix}+b_1
$$

$$
h_1=f_1(z_1)
$$

세 노드의 가중치를 열마다 모으면 **가중치 행렬**이 된다.

$$
\mathbf{W}^{(1)}=
\begin{bmatrix}
w_{11}&w_{12}&w_{13}\\
w_{21}&w_{22}&w_{23}
\end{bmatrix},\qquad
\mathbf{b}^{(1)}=\begin{bmatrix}b_1&b_2&b_3\end{bmatrix}
$$

이제 은닉층 전체를 한 번에 계산할 수 있다.

$$
\mathbf{z}=\mathbf{x}\mathbf{W}^{(1)}+\mathbf{b}^{(1)},\qquad
\mathbf{h}=f_1(\mathbf{z})
$$

$f_1$은 벡터의 각 원소에 따로 적용한다. 위첨자 $(1)$은 첫 번째 가중치 층을 뜻한다.

### 출력층까지 한 식으로

출력층의 가중치를 $\mathbf{W}^{(2)}=[v_1\;v_2\;v_3]^\mathsf{T}$, 바이어스를 $b^{(2)}$라고 하자. 출력층 활성화 함수 $f_2$까지 적용하면 다음과 같다.

$$
\hat y=f_2\left(\mathbf{h}\mathbf{W}^{(2)}+b^{(2)}\right)
$$

$$
\hat y=f_2\left(f_1\left(\mathbf{x}\mathbf{W}^{(1)}+\mathbf{b}^{(1)}\right)\mathbf{W}^{(2)}+b^{(2)}\right)
$$

| 계산 | 크기 변화 |
| --- | --- |
| 입력 × 은닉층 가중치 | $(1\times2)(2\times3)=1\times3$ |
| 은닉층 바이어스 더하기 | $1\times3$ 유지 |
| 활성화 함수 적용 | $1\times3$ 유지 |
| 은닉층 출력 × 출력층 가중치 | $(1\times3)(3\times1)=1\times1$ |

MLP는 **행렬 곱 → 바이어스 덧셈 → 활성화 함수**를 반복하는 함수로 정리된다.

## 2. 비선형 활성화 함수가 필요한 이유

### 선형 계산만 반복하면

층을 깊게 쌓으면 더 복잡한 관계를 표현할 수 있을까? 활성화 함수가 모두 입력을 그대로 내보내는 $f(z)=z$라면, 두 층의 계산은 다음처럼 합쳐진다.

$$
\begin{aligned}
\hat y
&=(\mathbf{x}\mathbf{W}^{(1)}+\mathbf{b}^{(1)})\mathbf{W}^{(2)}+b^{(2)}\\
&=\mathbf{x}(\mathbf{W}^{(1)}\mathbf{W}^{(2)})
 +\mathbf{b}^{(1)}\mathbf{W}^{(2)}+b^{(2)}\\
&=\mathbf{x}\mathbf{W}_{\mathrm{eff}}+b_{\mathrm{eff}}
\end{aligned}
$$

여러 가중치 행렬은 하나의 행렬로, 바이어스도 하나로 묶인다. 아무리 층을 늘려도 **완전연결층 하나로 표현할 수 있는 형태**가 된다. 바이어스를 포함한 이런 변환은 엄밀히는 아핀 변환이다.

비선형 활성화 함수를 사이에 넣으면 이처럼 하나로 합칠 수 없게 된다. 조회수나 영상 길이에 따라 수익의 증가 양상이 달라지는 관계도 표현할 수 있다.

### 선형 활성화 함수를 쓰는 곳

은닉층에서는 비선형 관계를 만들고, 출력층에서는 예측할 값에 맞춰 활성화 함수를 선택한다.

대표 예시: **연속적인 수치를 예측하는 회귀의 출력층**. $f_2(z)=z$를 쓰면 출력값이 0~1 같은 특정 구간에 묶이지 않는다. 이번 수익 예측 예제도 이 방식을 사용한다.

모델 중간에서도 선형 출력을 활용한다. 뒤에서 살펴볼 MobileNetV2의 좁은 병목층이 그 예다.

## 3. ReLU와 정보 손실

### 음수는 0, 양수는 그대로

**ReLU**(Rectified Linear Unit)는 음수 입력을 0으로 만들고 양수 입력은 그대로 출력한다.

$$
\operatorname{ReLU}(z)=\max(0,z)
$$

<figure>
  <img src="/images/notes/easy-deep-learning-ch03/relu.jpeg" alt="입력이 음수일 때 출력이 0이고, 양수일 때 출력이 입력과 같은 ReLU 그래프" loading="lazy" width="311" height="210" />
  <figcaption>출처: <a href="https://cs231n.github.io/neural-networks-1/">Stanford CS231n</a>.</figcaption>
</figure>

| 입력 | −3 | −1 | 0 | 2 |
| --- | --- | --- | --- | --- |
| ReLU 출력 | 0 | 0 | 0 | 2 |

−3과 −1은 다른 값이지만 출력은 모두 0이다. 이 출력만 보고 원래 음수 값을 구분할 수는 없다.

### 좁은 층에서 정보를 남기는 방법

특징을 적은 수의 채널로 압축한 상태에서 음수 성분까지 없애면 필요한 정보가 사라질 수 있다. **MobileNetV2**는 이를 줄이기 위해 좁은 병목층의 출력에 비선형 활성화 함수를 붙이지 않는 **선형 병목**(Linear Bottleneck)을 사용한다.

<figure>
  <img src="/images/notes/easy-deep-learning-ch03/linear-bottleneck.png" alt="좁은 입력을 넓은 중간 표현으로 확장해 처리하고 다시 좁은 출력으로 압축하는 MobileNetV2 블록" loading="lazy" width="1027" height="445" />
  <figcaption>출처: <a href="https://arxiv.org/html/1801.04381v4">Sandler et al., MobileNetV2, 2018</a>.</figcaption>
</figure>

그림의 흐름은 **좁은 입력 → 넓은 중간 표현 → 좁은 출력**이다. 넓은 내부에서는 ReLU6를 쓰고, 마지막 압축 결과는 선형으로 내보낸다. ReLU6는 ReLU의 양수 출력을 6에서 한 번 더 제한한 함수다.

이것은 MobileNetV2의 병목 구조에 맞춘 설계다. 층의 노드 수가 줄어든다는 이유만으로 항상 활성화 함수를 제거하는 것은 아니다. [MobileNetV2 논문](https://arxiv.org/abs/1801.04381)

## 4. 역전파

### 어떤 가중치를 얼마나 바꿔야 할까

예측 수익이 실제 수익보다 작게 나왔다고 해보자. 출력층뿐 아니라 은닉층의 가중치도 예측에 영향을 준다. 각 파라미터를 조금 바꿀 때 손실이 얼마나 변하는지 알아야 갱신 방향을 정할 수 있다.

**역전파**(Backpropagation)는 출력 쪽에서 입력 쪽으로 계산을 거슬러 올라가며, 손실의 편미분을 구하는 알고리즘이다.

이번 예제에서는 은닉층에 ReLU, 출력층에 선형 활성화 함수를 쓴다. 한 영상의 손실은 미분을 간단히 하려고 제곱 오차에 $1/2$을 곱한다.

$$
L=\frac12(\hat y-y)^2
$$

### 연결된 계산은 연쇄 법칙으로 미분한다

첫 번째 가중치 $w_{11}$이 손실에 영향을 주는 경로를 따라가면 다음과 같다.

$$
w_{11}\;\longrightarrow\;z_1\;\longrightarrow\;h_1
\;\longrightarrow\;\hat y\;\longrightarrow\;L
$$

$w_{11}$이 바뀌면 가중합 $z_1$, 은닉 출력 $h_1$, 예측 $\hat y$가 차례로 바뀐다. 각 단계의 변화율을 곱하는 것이 **연쇄 법칙**(Chain Rule)이다.

$$
\frac{\partial L}{\partial w_{11}}
=\frac{\partial L}{\partial\hat y}
\frac{\partial\hat y}{\partial h_1}
\frac{\partial h_1}{\partial z_1}
\frac{\partial z_1}{\partial w_{11}}
$$

| 단계 | 변화율 |
| --- | --- |
| 예측 → 손실 | $\partial L/\partial\hat y=\hat y-y$ |
| 은닉 출력 → 예측 | $\partial\hat y/\partial h_1=v_1$ |
| 가중합 → 은닉 출력 | $\partial h_1/\partial z_1=f_1'(z_1)$ |
| 가중치 → 가중합 | $\partial z_1/\partial w_{11}=x_1$ |

따라서 네 값을 곱하면 된다.

$$
\frac{\partial L}{\partial w_{11}}
=(\hat y-y)v_1f_1'(z_1)x_1
$$

### 뒤에서 구한 값을 앞에서도 재사용하기

은닉 노드 $j$까지 전달된 미분값을 $\delta_j$로 묶어보자.

$$
\delta_j=\frac{\partial L}{\partial z_j}
=(\hat y-y)v_jf_1'(z_j)
$$

이 값만 구하면 해당 노드로 들어오는 가중치와 바이어스의 미분을 바로 계산할 수 있다.

$$
\frac{\partial L}{\partial w_{ij}}=x_i\delta_j,\qquad
\frac{\partial L}{\partial b_j}=\delta_j
$$

출력층의 미분은 다음과 같다.

$$
\frac{\partial L}{\partial v_j}=h_j(\hat y-y),\qquad
\frac{\partial L}{\partial b^{(2)}}=\hat y-y
$$

역전파는 이렇게 **뒤에서 계산한 미분값을 재사용**한다. 여러 경로가 한 값으로 모이면 각 경로에서 전달된 미분값을 더한다. [역전파 참고](https://cs231n.github.io/optimization-2/)

### 행렬로 묶은 역전파

앞에서 행벡터로 표현했으므로 미분도 같은 크기로 묶을 수 있다. $\delta^{(2)}=\hat y-y$라고 두면 다음과 같다.

$$
\boldsymbol{\delta}^{(1)}
=\left(\delta^{(2)}(\mathbf{W}^{(2)})^\mathsf{T}\right)
\odot f_1'(\mathbf{z})
$$

$$
\frac{\partial L}{\partial\mathbf{W}^{(1)}}
=\mathbf{x}^\mathsf{T}\boldsymbol{\delta}^{(1)},\qquad
\frac{\partial L}{\partial\mathbf{b}^{(1)}}
=\boldsymbol{\delta}^{(1)}
$$

$$
\frac{\partial L}{\partial\mathbf{W}^{(2)}}
=\mathbf{h}^\mathsf{T}\delta^{(2)},\qquad
\frac{\partial L}{\partial b^{(2)}}=\delta^{(2)}
$$

$\odot$는 같은 위치의 원소끼리 곱한다는 뜻이다. 첫 가중치의 미분 행렬은 $2\times3$, 출력층 가중치의 미분은 $3\times1$로 원래 파라미터와 크기가 같다.

역전파로 미분값을 구한 다음, 2장에서 배운 GD나 Adam 같은 최적화 방법으로 파라미터를 갱신한다.

## 5. 학습할 때 순전파가 필요한 이유

미분식에는 $\hat y-y$, $h_j$, $f_1'(z_j)$가 들어간다. 이 값들은 현재 입력과 파라미터로 직접 계산해야 알 수 있다.

입력부터 출력까지 계산하는 **순전파**(Forward Propagation)는 예측값뿐 아니라 역전파에 필요한 중간값도 구한다.

| 순전파에서 구하는 값 | 역전파에서 사용하는 곳 |
| --- | --- |
| 예측 $\hat y$ | 정답과의 차이 $\hat y-y$ 계산 |
| 은닉 출력 $h_j$ | 출력층 가중치 $v_j$의 미분 |
| 활성화 전 값 $z_j$ | ReLU의 미분값 결정 |

ReLU는 입력이 양수인 구간에서 기울기가 1, 음수인 구간에서 0이다. 그래서 **이번 입력에서 어떤 노드가 양수였는지** 알아야 역전파를 진행할 수 있다. 0에서는 미분이 정의되지 않으며, 구현에서는 보통 0으로 처리한다.

학습 흐름: **순전파 → 손실 계산 → 역전파 → 파라미터 갱신**. 갱신 후에는 바뀐 파라미터로 다시 순전파한다.

## 예제로 확인해 보기

앞에서 사용한 입력 2개·은닉 노드 3개·출력 1개 구조에 숫자를 넣어보자. 입력은 단위를 조정한 설명용 값이며, 실제 영상 데이터는 아니다.

$$
\mathbf{x}=\begin{bmatrix}1&2\end{bmatrix},\qquad y=4
$$

$$
\mathbf{W}^{(1)}=
\begin{bmatrix}1&0&-1\\0&1&0\end{bmatrix},\qquad
\mathbf{b}^{(1)}=\begin{bmatrix}0&0&0\end{bmatrix}
$$

$$
\mathbf{W}^{(2)}=\begin{bmatrix}1\\1\\1\end{bmatrix},\qquad b^{(2)}=0
$$

### 순전파로 예측과 손실 계산

| 단계 | 결과 |
| --- | --- |
| 은닉층 가중합 | $\mathbf{z}=[1\;2\;{-1}]$ |
| ReLU 적용 | $\mathbf{h}=[1\;2\;0]$ |
| 예측 수익 | $\hat y=1+2+0=3$ |
| 손실 | $L=\frac12(3-4)^2=0.5$ |

### 역전파로 미분값 계산

예측과 정답의 차이는 $3-4=-1$이다. 은닉층의 ReLU 기울기는 $[1\;1\;0]$이므로 다음과 같이 전달된다.

$$
\boldsymbol{\delta}^{(1)}=\begin{bmatrix}-1&-1&0\end{bmatrix}
$$

$$
\frac{\partial L}{\partial\mathbf{W}^{(1)}}
=\begin{bmatrix}1\\2\end{bmatrix}
\begin{bmatrix}-1&-1&0\end{bmatrix}
=\begin{bmatrix}-1&-1&0\\-2&-2&0\end{bmatrix}
$$

$$
\frac{\partial L}{\partial\mathbf{b}^{(1)}}=\begin{bmatrix}-1&-1&0\end{bmatrix}
$$

$$
\frac{\partial L}{\partial\mathbf{W}^{(2)}}=\begin{bmatrix}-1\\-2\\0\end{bmatrix},\qquad
\frac{\partial L}{\partial b^{(2)}}=-1
$$

세 번째 은닉 노드는 이번 입력에서 ReLU의 음수 구간에 있었다. 이 경로로 전달되는 미분값은 0이다.

### 파라미터를 갱신한 뒤 다시 예측

학습률 $\eta=0.01$로 위 파라미터들을 한꺼번에 갱신한다.

$$
\theta_{\mathrm{new}}=\theta-0.01\frac{\partial L}{\partial\theta}
$$

| 항목 | 갱신 전 | 갱신 후 |
| --- | --- | --- |
| 예측 수익 | 3 | 3.1818 |
| 손실 | 0.5 | 약 0.3347 |

순전파에서 구한 값으로 미분을 계산하고, 그 미분으로 갱신한 결과 예측이 정답 4에 가까워졌다.

## 발표에서 전달할 핵심

1. 노드별 계산은 행렬 곱과 바이어스 벡터로 묶을 수 있다.
2. 선형 계산만 쌓으면 하나의 층으로 합쳐지므로, 비선형 활성화 함수가 필요하다.
3. 역전파는 연쇄 법칙으로 미분값을 뒤에서부터 계산하고 재사용한다.
4. 순전파의 예측값과 중간값이 있어야 역전파를 계산할 수 있다.

## 참고 자료

- 혁펜하임, 『이지 딥러닝』, 챕터 3.
- [Stanford CS231n · 신경망과 활성화 함수](https://cs231n.github.io/neural-networks-1/).
- [Stanford CS231n · 연쇄 법칙과 역전파](https://cs231n.github.io/optimization-2/).
- [Sandler et al., MobileNetV2: Inverted Residuals and Linear Bottlenecks, 2018](https://arxiv.org/abs/1801.04381).
