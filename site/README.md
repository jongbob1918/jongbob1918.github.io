# 노트 이미지 경로

블로그 노트에서 쓰는 이미지는 `site/public/images/notes/<글 slug>/`에 저장한다. 예를 들어 `deeplearning_1.md`의 이미지는 `site/public/images/notes/easy-deep-learning-ch01/`에 둔다. 파일명은 내용을 알 수 있는 영문 소문자와 하이픈으로 짓는다.

옵시디언과 블로그에서 같은 파일을 볼 수 있도록 노트에는 파일 기준 상대경로를 쓴다. `site/src/content/notes/Machine Learning｜Deep Learning/`에 있는 글의 예시는 다음과 같다.

```html
<img src="../../../../public/images/notes/easy-deep-learning-ch01/restaurant-rl-01-random-exploration.png" alt="무작위 탐색 중 공사 구간에 들어가 벌점을 받는 단계" loading="lazy" />
```

빌드 시 이 경로는 블로그 주소 `/images/notes/easy-deep-learning-ch01/restaurant-rl-01-random-exploration.png`로 바뀐다. 다른 폴더에 노트를 추가할 때는 해당 노트에서 `site/public`까지의 상대경로를 사용한다.

`npm run build:notes`는 이미지 참조가 존재하는지와 사용하지 않는 공개 이미지가 남아 있는지 확인한다. 이미지 출처나 라이선스 기록은 해당 글의 이미지 폴더에 둔다.

## 공통 읽기 규격

본문·목차·제목·수식·그림 크기와 간격은 `src/config/reading.yaml`에서 관리한다. `src/config/reading.mjs`가 빌드 시 필수 양수 설정을 검증하고 CSS 변수를 생성하며, 모든 글은 `src/styles/reading.css`를 사용한다. 개별 글에 크기나 간격 스타일을 추가하지 않는다.

본문은 PC 18px / 모바일 17px, 목차 16px, 줄 높이 1.75이다. 문단 간격은 18/17px, 수식 24/20px, 그림 32/24px, 그림 설명 8px이다. 일반 블록의 인접 여백은 큰 값 하나를 적용한다. 제목 직후에는 해당 제목의 아래 여백을 적용해 제목과 설명을 묶는다. 그림 설명은 figure 내부 figcaption으로 작성한다. 긴 독립 수식은 해당 영역에서 가로 스크롤한다.

문단은 빈 줄로 구분하되 여러 빈 줄·공백·반복 `<br>`로 배치하지 않는다. 일반 개행은 브라우저가 문장 흐름으로 처리한다. 표 내부처럼 의미가 있는 명시적 줄바꿈은 유지한다. 모바일 목차는 본문 위에 표시한다.

### 제목 단계와 학습 흐름

| 단계 | 크기 PC / 모바일 | 위 여백 PC / 모바일 | 아래 여백 |
| --- | --- | --- | --- |
| `##` 큰 개념 | 32 / 28px | 64 / 48px | 24px |
| `###` 질문·소절 | 24 / 22px | 48 / 40px | 16px |
| `####` 계산 단계 | 20 / 19px | 28 / 24px | 12px |
| `#####` 보충 항목 | 18 / 17px | 24 / 20px | 8px |
| `######` 하위 보충 | 18 / 17px | 20 / 16px | 8px |

본문 폭은 760px로 유지한다. 각 소절은 하나의 질문이나 계산 단계를 맡고, 그림에서 볼 부분을 먼저 짚는다. 필요하면 작은 수치 예시로 계산 의미를 확인한다. 긴 식은 KaTeX의 `aligned` 또는 `gathered` 환경으로 계산 순서를 보존하며 나눈다. 같은 계산을 그림과 수식으로 반복하지 않는다. 이를 모든 문단에 고정 템플릿으로 강제하지는 않는다.

설명 방식 참고: [Jay Alammar](https://jalammar.github.io/illustrated-transformer/), [Victor Zhou](https://victorzhou.com/blog/intro-to-neural-networks/). 위 수치는 해당 사이트의 복사본이 아니라 한글 본문에 맞춘 자체 규격이다. 역전파 글에서 설명·그림·계산 배치를 먼저 검토했다.
