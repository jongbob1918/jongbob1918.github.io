---
title: MLP를 행렬로 표현하기
slug: deep-learning/mlp-matrix-representation
description: 노드별 계산을 행벡터와 가중치 행렬로 묶고, 입력부터 출력까지 각 값의 크기를 확인합니다.
publishedAt: 2026-09-27
tags:
  - Deep learning
draft: false
featured: false
---

## 노드별 계산에서 행렬 곱까지

### 노드마다 계산하면 식이 길어집니다

조회수와 영상 길이로 수익을 예측한다고 해 보겠습니다. 이번에는 다음 구조의 **다층 퍼셉트론**(Multi-Layer Perceptron, MLP)을 사용합니다.

| 층 | 노드 수 | 값 |
| --- | --- | --- |
| 입력층 | 2개 | 조회수 $x_1$, 영상 길이 $x_2$ |
| 은닉층 | 3개 | 변환한 특징 $h_1,h_2,h_3$ |
| 출력층 | 1개 | 예측 수익 $\hat y$ |

은닉층의 활성화 함수를 $f_1$이라고 하면, 세 노드의 출력은 다음과 같습니다.

$$
\begin{aligned}
h_1&=f_1(x_1w_{11}+x_2w_{21}+b_1)\\
h_2&=f_1(x_1w_{12}+x_2w_{22}+b_2)\\
h_3&=f_1(x_1w_{13}+x_2w_{23}+b_3)
\end{aligned}
$$

$w_{ij}$는 입력 $i$에서 은닉 노드 $j$로 이어지는 가중치입니다. 노드 수가 늘어나면 같은 형태의 식을 계속 적어야 합니다.

### 입력을 벡터로 묶기

입력 두 개를 **행벡터** $\mathbf{x}=[x_1\;x_2]$로 묶습니다. 첫 번째 은닉 노드의 가중합은 행벡터와 열벡터의 곱, 즉 내적으로 쓸 수 있습니다.

$$
z_1=
\begin{bmatrix}x_1&x_2\end{bmatrix}
\begin{bmatrix}w_{11}\\w_{21}\end{bmatrix}+b_1
$$

$$
h_1=f_1(z_1)
$$

세 노드의 가중치를 열마다 모으면 **가중치 행렬**이 됩니다.

$$
\mathbf{W}^{(1)}=
\begin{bmatrix}
w_{11}&w_{12}&w_{13}\\
w_{21}&w_{22}&w_{23}
\end{bmatrix},\qquad
\mathbf{b}^{(1)}=\begin{bmatrix}b_1&b_2&b_3\end{bmatrix}
$$

이제 은닉층 전체를 한 번에 계산할 수 있습니다.

$$
\mathbf{z}=\mathbf{x}\mathbf{W}^{(1)}+\mathbf{b}^{(1)},\qquad
\mathbf{h}=f_1(\mathbf{z})
$$

$f_1$은 벡터의 각 원소에 따로 적용합니다. 위첨자 $(1)$은 첫 번째 가중치 층을 뜻합니다.

### 출력층까지 한 식으로

출력층의 가중치를 $\mathbf{W}^{(2)}=[v_1\;v_2\;v_3]^\mathsf{T}$, 바이어스를 $b^{(2)}$라고 하겠습니다. 출력층 활성화 함수 $f_2$까지 적용하면 다음과 같습니다.

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

MLP는 **행렬 곱 → 바이어스 덧셈 → 활성화 함수**를 반복하는 함수로 정리됩니다.

이 계산에서 활성화 함수가 하는 일은 [선형·비선형 활성화 함수](/notes/deep-learning/linear-nonlinear-activations/)에서, 미분값을 뒤로 전달하는 과정은 [역전파](/notes/deep-learning/easy-deep-learning-ch03/)에서 이어집니다.

## 참고 자료

- 혁펜하임, 『이지 딥러닝』, 챕터 3.
