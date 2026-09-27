---
title: 활성화 함수
slug: deep-learning/linear-nonlinear-activations
description: 선형 함수만 쌓으면 왜 한 층으로 합쳐지는지 확인하고, ReLU·sigmoid·softmax와 선형 출력을 어디에 쓰는지 정리합니다.
publishedAt: 2026-09-27
tags:
  - Deep learning
draft: false
featured: false
---

노드는 입력에 가중치를 곱해 더하고 바이어스를 더해 $z$를 만듭니다. **활성화 함수** $f$는 이 값을 다음 층으로 보낼 값 $f(z)$로 바꿉니다.

## 비선형 함수가 필요한 이유

활성화 함수가 입력을 그대로 내보내는 $f(z)=z$라면, 노드 하나씩 이어 붙인 두 층은 다음처럼 합쳐집니다.

$$
\begin{aligned}
\hat y
&=w_2(w_1x+b_1)+b_2\\
&=(w_2w_1)x+(w_2b_1+b_2)
\end{aligned}
$$

가중치와 바이어스를 새 값으로 묶으면 한 층의 식과 같습니다. 노드가 여러 개여도 같은 원리로 묶이므로, 이런 층만 늘려서는 표현할 수 있는 함수의 종류가 늘지 않습니다. 은닉층에 **비선형 활성화 함수**를 넣으면 층을 이처럼 하나로 합칠 수 없습니다.

## ReLU는 은닉층에서

**ReLU**(Rectified Linear Unit)는 음수를 0으로, 양수를 그대로 내보냅니다.

$$
\operatorname{ReLU}(z)=\max(0,z)
$$

<figure>
  <img src="../../../../public/images/notes/easy-deep-learning-ch03/relu.jpeg" alt="음수 입력에서는 0이고 양수 입력에서는 입력과 같은 ReLU 그래프" loading="lazy" width="311" height="210" />
  <figcaption>출처: <a href="https://cs231n.github.io/neural-networks-1/">Stanford CS231n</a>.</figcaption>
</figure>

예를 들어 −3과 −1은 모두 0이 되므로 출력만으로 원래 음수 값을 구분할 수는 없습니다. [역전파 예제](/notes/deep-learning/easy-deep-learning-ch03/)에서는 은닉층에 ReLU를 사용합니다.

## 출력층에서는 예측값에 맞게

- **선형 출력** $f(z)=z$: 값을 특정 범위로 제한하지 않습니다. 수익처럼 연속적인 수치를 예측하는 회귀에 사용할 수 있습니다.
- **시그모이드**(sigmoid) $\sigma(z)=1/(1+e^{-z})$: 값을 0과 1 사이로 바꿉니다. 두 종류 중 하나를 예측하는 이진분류의 출력에 사용합니다.
- **소프트맥스**(softmax): 여러 출력값을 합이 1인 확률로 바꿉니다. 여러 종류 중 하나를 예측하는 다중분류의 출력에 사용합니다.

sigmoid와 softmax를 실제 분류 문제에 적용하는 과정은 [이진분류와 다중분류](/notes/deep-learning/easy-deep-learning-ch04/)에서 이어집니다.

## 참고 자료

- [Stanford CS231n · 신경망과 활성화 함수](https://cs231n.github.io/neural-networks-1/).
