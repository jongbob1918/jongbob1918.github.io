---
title: 선형·비선형 활성화 함수와 ReLU
slug: deep-learning/linear-nonlinear-activations
description: 비선형 활성화 함수가 필요한 이유와 선형 출력을 쓰는 경우를 살펴보고, ReLU의 정보 손실을 MobileNetV2 사례에 연결합니다.
publishedAt: 2026-09-27
tags:
  - Deep learning
draft: false
featured: false
---

## 비선형 활성화 함수가 필요한 이유

### 선형 계산만 반복하면

층을 깊게 쌓으면 더 복잡한 관계를 표현할 수 있을까요? 노드 하나씩 이어 붙여 생각해 보겠습니다. 활성화 함수가 입력을 그대로 내보내는 $f(z)=z$라면, 두 층의 계산은 다음처럼 합쳐집니다.

$$
\begin{aligned}
\hat y
&=w_2(w_1x+b_1)+b_2\\
&=(w_2w_1)x+(w_2b_1+b_2)
\end{aligned}
$$

가중치와 바이어스를 새 값으로 묶으면 한 층의 식과 같습니다. 노드가 여러 개여도 같은 원리로 묶이므로, 이런 층만 늘려서는 표현할 수 있는 함수의 종류가 늘지 않습니다. 바이어스를 포함한 이런 변환은 엄밀히는 아핀 변환입니다.

비선형 활성화 함수를 사이에 넣으면 이처럼 하나로 합칠 수 없게 됩니다. 조회수나 영상 길이에 따라 수익의 증가 양상이 달라지는 관계도 표현할 수 있습니다. 여러 노드의 계산을 행렬로 묶는 방법은 [MLP를 행렬로 표현하기](/notes/deep-learning/mlp-matrix-representation/)에서 다룹니다.

### 선형 활성화 함수를 쓰는 곳

은닉층에서는 비선형 관계를 만들고, 출력층에서는 예측할 값에 맞춰 활성화 함수를 선택합니다.

연속적인 수치를 예측하는 회귀의 출력층이 한 예입니다. $f(z)=z$를 쓰면 출력값이 0~1 같은 특정 구간에 묶이지 않습니다. [역전파 예제](/notes/deep-learning/easy-deep-learning-ch03/)의 수익 예측도 이 방식을 사용합니다.

모델 중간에서도 선형 출력을 활용합니다. 아래의 MobileNetV2 병목층이 그 예입니다.

## ReLU와 정보 손실

### 음수는 0, 양수는 그대로

**ReLU**(Rectified Linear Unit)는 음수 입력을 0으로 만들고 양수 입력은 그대로 출력합니다.

$$
\operatorname{ReLU}(z)=\max(0,z)
$$

<figure>
  <img src="../../../../public/images/notes/easy-deep-learning-ch03/relu.jpeg" alt="입력이 음수일 때 출력이 0이고, 양수일 때 출력이 입력과 같은 ReLU 그래프" loading="lazy" width="311" height="210" />
  <figcaption>출처: <a href="https://cs231n.github.io/neural-networks-1/">Stanford CS231n</a>.</figcaption>
</figure>

| 입력 | −3 | −1 | 0 | 2 |
| --- | --- | --- | --- | --- |
| ReLU 출력 | 0 | 0 | 0 | 2 |

−3과 −1은 다른 값이지만 출력은 모두 0입니다. 이 출력만 보고 원래 음수 값을 구분할 수는 없습니다.

### 좁은 층에서 정보를 남기는 방법

특징을 적은 수의 채널로 압축한 상태에서 음수 성분까지 없애면 필요한 정보가 사라질 수 있습니다. **MobileNetV2**는 이를 줄이기 위해 좁은 병목층의 출력에 비선형 활성화 함수를 붙이지 않는 **선형 병목**(Linear Bottleneck)을 사용합니다.

<figure>
  <img src="../../../../public/images/notes/easy-deep-learning-ch03/linear-bottleneck.png" alt="좁은 입력을 넓은 중간 표현으로 확장해 처리하고 다시 좁은 출력으로 압축하는 MobileNetV2 블록" loading="lazy" width="1027" height="445" />
  <figcaption>출처: <a href="https://arxiv.org/html/1801.04381v4">Sandler et al., MobileNetV2, 2018</a>.</figcaption>
</figure>

그림의 흐름은 **좁은 입력 → 넓은 중간 표현 → 좁은 출력**입니다. 넓은 내부에서는 ReLU6를 쓰고, 마지막 압축 결과는 선형으로 내보냅니다. ReLU6는 ReLU의 양수 출력을 6에서 한 번 더 제한한 함수입니다.

이것은 MobileNetV2의 병목 구조에 맞춘 설계입니다. 층의 노드 수가 줄어든다는 이유만으로 항상 활성화 함수를 제거하는 것은 아닙니다. [MobileNetV2 논문](https://arxiv.org/abs/1801.04381)

## 참고 자료

- [Stanford CS231n · 신경망과 활성화 함수](https://cs231n.github.io/neural-networks-1/).
- [Sandler et al., MobileNetV2: Inverted Residuals and Linear Bottlenecks, 2018](https://arxiv.org/abs/1801.04381).
