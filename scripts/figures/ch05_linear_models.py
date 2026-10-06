"""같은 6점을 분류하는 두 학습 모델. 설명을 위한 합성 데이터다.

두 입력을 [-1, 1]로 맞춰 단위 차이를 제거한다.
퍼셉트론: 가중치 0부터 시작, 불합격→합격 순서로 오분류만 갱신.
시그모이드: 평균 BCE + 0.02 / 2 * ||w||², 절편은 규제하지 않는다.
분리 가능한 데이터에서 BCE만으로는 유한한 최솟값이 없으므로 L2 규제를 쓴다.
필요 패키지: numpy, scipy.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit


PASS = [(9.5, 70), (8, 60), (4.5, 88)]
FAIL = [(1.5, 80), (5.5, 15), (7, 25)]
DATA = np.asarray(FAIL + PASS, dtype=float)
LABELS = np.array([0, 0, 0, 1, 1, 1])
FEATURES = np.column_stack((DATA / [5, 50] - 1, np.ones(len(DATA))))
L2 = 0.02


def fit_perceptron():
    weights = np.zeros(3)
    for _ in range(1000):
        for features, target in zip(FEATURES, LABELS):
            prediction = int(features @ weights >= 0)
            if prediction != target:
                weights += (target - prediction) * features
        if np.all((FEATURES @ weights >= 0) == LABELS):
            return weights
    raise RuntimeError("퍼셉트론이 모든 예시를 분류하지 못했습니다.")


def fit_sigmoid():
    def objective(weights):
        scores = FEATURES @ weights
        loss = np.mean(np.logaddexp(0, scores) - LABELS * scores)
        loss += L2 / 2 * (weights[:2] @ weights[:2])
        gradient = FEATURES.T @ (expit(scores) - LABELS) / len(DATA)
        gradient[:2] += L2 * weights[:2]
        return loss, gradient

    result = minimize(objective, np.zeros(3), jac=True, method="BFGS",
                      options={"gtol": 1e-8})
    if not result.success:
        raise RuntimeError(result.message)
    return result.x


def boundary_y(weights, study):
    """점수 0인 경계를 원래 단위(공부 시간, 출석률)로 환산한다."""
    return 50 * (1 - (weights[0] * (np.asarray(study) / 5 - 1)
                      + weights[2]) / weights[1])


def boundary_segment(weights):
    """0~10시간, 출석률 0~100% 영역에 보이는 선분의 끝점."""
    points = [(x, float(boundary_y(weights, x))) for x in (0, 10)
              if 0 <= boundary_y(weights, x) <= 100]
    for attendance in (0, 100):
        study = 5 * (1 - (weights[1] * (attendance / 50 - 1)
                          + weights[2]) / weights[0])
        if 0 <= study <= 10:
            points.append((float(study), attendance))
    return sorted(points)[0], sorted(points)[-1]


def minimum_margin(weights):
    signed_distance = (2 * LABELS - 1) * (FEATURES @ weights)
    return float(np.min(signed_distance) / np.linalg.norm(weights[:2]))


STEP_WEIGHTS = fit_perceptron()
SIGMOID_WEIGHTS = fit_sigmoid()
for weights in (STEP_WEIGHTS, SIGMOID_WEIGHTS):
    assert np.all((FEATURES @ weights >= 0) == LABELS), "두 모델 모두 6/6 분류해야 함"
assert minimum_margin(SIGMOID_WEIGHTS) > minimum_margin(STEP_WEIGHTS)
differences = boundary_y(STEP_WEIGHTS, [0, 10]) - boundary_y(SIGMOID_WEIGHTS, [0, 10])
assert np.all(differences > 0), "그림의 두 경계는 겹치지 않아야 함"


if __name__ == "__main__":
    for name, weights in (("유닛 스텝", STEP_WEIGHTS), ("시그모이드", SIGMOID_WEIGHTS)):
        print(f"{name}: 6/6 분류, 가중치 {weights}, "
              f"정규화한 입력 공간의 최소 거리 {minimum_margin(weights):.4f}")
