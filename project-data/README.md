# Project detail content

프로젝트 상세페이지는 `project-data/*.md`에서 자동 생성합니다. 새 프로젝트는 `project-data/templates/project-template.md`를 복사해서 작성합니다.

- 제목, 팀, 기간, 기술, 저장소와 대표 미디어: Markdown 상단의 YAML 영역
- 홈페이지 프로젝트 카드: YAML의 `card`
- Overview: YAML의 `overview`
- 본문 섹션: Markdown의 `## 원하는 제목`
- 섹션 안의 소제목: Markdown의 `### 원하는 소제목`
- 공통 레이아웃과 미디어 출력: `templates/project-detail.mjs`
- 공통 폰트, 너비, 색상, 간격과 반응형 스타일: `styles.css`의 `Case study` 영역

`Technical Details`, `System`, `Hardware`, `Troubleshooting` 같은 고정 섹션 이름은 없습니다. `##` 제목을 추가·삭제하거나 순서를 바꾸면 생성된 상세페이지에도 그대로 반영됩니다.

빌드할 때 각 Markdown의 `card` 정보를 모아 `projects.json`도 자동 생성합니다. 따라서 새 프로젝트를 추가할 때 `script.js`나 `projects.json`을 직접 수정하지 않습니다. `group`은 `key` 또는 `side`, `order`는 홈페이지에서 표시할 순서입니다.

수정 후 아래 명령으로 `projects/*.html`을 다시 생성합니다.

```bash
npm run build:projects
```

`projects/*.html`은 생성 결과물이므로 직접 수정하지 않습니다.

## 대표 미디어 설정

이미지는 다음과 같이 설정합니다.

```yaml
demo:
  type: image
  src: ../assets/images/project-name.png
  alt: 프로젝트 대표 이미지 설명
  caption: 선택 입력 문구
```

로컬 영상은 `assets/videos`에 넣고 다음과 같이 설정합니다.

```yaml
demo:
  type: video
  src: ../assets/videos/project-demo.mp4
  poster: ../assets/images/project-poster.png
  caption: 프로젝트 대표 시연
```

YouTube 영상은 Embed 주소를 사용합니다.

```yaml
demo:
  type: youtube
  src: https://www.youtube.com/embed/VIDEO_ID
  alt: 프로젝트 시연 영상
  caption: 프로젝트 대표 시연
```

대표 미디어가 필요 없으면 `demo` 항목 전체를 삭제합니다. 본문 중간에 이미지를 추가할 때는 일반 Markdown 이미지 문법을 사용합니다.

```md
![이미지 설명](../assets/images/example.png)
```

본문 중간에 영상을 넣어야 할 때는 Markdown 안에 표준 HTML `video` 요소를 사용할 수 있습니다.

```html
<video controls poster="../assets/images/poster.png">
  <source src="../assets/videos/demo.mp4" type="video/mp4">
</video>
```

## Overview 작성 규칙

Overview는 비전공자와 면접관이 프로젝트를 10초 안에 이해할 수 있도록 작성합니다.

### 문장 구조

1. 프로젝트가 필요한 배경 또는 해결하려는 문제
2. 개발한 시스템과 핵심 기능
3. 사용자 요청부터 결과까지의 대표 동작

### 기본 템플릿

> `[환경 또는 사용자]`에게는 `[해결하려는 문제]`가 있습니다. 이를 해결하기 위해 `[핵심 기능 2~3개]`를 통합한 `[시스템]`을 개발했습니다. `[요청 또는 조건]`이 발생하면 `[처리 과정]`을 거쳐 `[결과]`를 수행합니다.

### 작성 기준

- 3문장, 한 문단으로 작성합니다.
- 한 문장에는 한 가지 핵심 내용만 담습니다.
- 비전공자가 이해할 수 있는 표현을 먼저 사용합니다.
- 기술 이름을 나열하는 대신 대표 동작 시나리오를 보여줍니다.
- 세부 기술과 트러블슈팅은 본문 섹션에서 설명합니다.
- 검증되지 않은 수치나 `완전한`, `획기적인`, `혁신적인` 등의 과장 표현을 사용하지 않습니다.
