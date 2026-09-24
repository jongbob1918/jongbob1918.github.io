# 프로젝트와 카테고리 작성

홈페이지 카테고리·카드와 상세 페이지는 설정 파일과 Markdown에서 자동 생성합니다. `index.html`, `script.js`, `projects.json`, `projects/*.html`에 프로젝트 내용을 직접 추가하지 않습니다. About의 경력·교육은 별도 소개 내용이며 자동 연동 대상이 아닙니다.

## 카테고리와 우선순위

`project-data/categories.json`에 카테고리를 등록합니다.

```json
{
  "id": "maxerve",
  "titleKo": "맥서브",
  "titleEn": "MAXERVE",
  "priority": 4,
  "layout": "main"
}
```

- `priority`: 양의 정수. 작은 숫자가 먼저 표시됩니다. 현재 LK 1, ADDINEDU 2, Side 3입니다.
- 같은 우선순위면 `id` 오름차순으로 정렬합니다. 표시 순서를 확실히 지정하려면 서로 다른 값을 사용합니다.
- `layout`: `main`은 이미지·본문이 나란한 큰 카드, `compact`는 작은 카드입니다. 카테고리 이름과 카드 디자인은 독립적입니다.
- `titleKo`, `titleEn`: 언어별 카테고리 이름입니다.
- `color`, `darkColor`: 선택 사항. 제목 색을 `#174b88` 같은 여섯 자리 HEX로 지정합니다.
- 프로젝트가 없는 카테고리는 숨깁니다. 프로젝트를 추가하면 해당 영역이 자동으로 나타납니다.
- 카테고리 앵커는 `#maxerve-projects`처럼 `{id}-projects`로 생성됩니다.

## 프로젝트 추가

`project-data/templates/project-template.md`와 `project-template-en.md`를 복사해 각각 `project-data/{slug}.md`, `project-data/en/{slug}.md`로 저장합니다. 두 언어 파일이 모두 필요하며 `slug`가 같아야 합니다. 문장은 직접 작성하고 번역하며, 빌드가 자동으로 문장을 만들지는 않습니다.

```yaml
---
slug: example-robot
category: maxerve
order: 1
detail: false
title: 로봇 프로젝트
---
```

위처럼 카드만 등록할 수도 있습니다. 영어 파일에는 같은 `slug`와 영어 `title`을 작성합니다.

- 필수: 한국어 파일의 `slug`, `category`, `title`; 영어 파일의 `slug`, `title`.
- `order`: 카테고리 내부 순서. 작은 숫자부터 표시하며 생략하면 999입니다. 같으면 `slug`순입니다.
- `detail: false`: 카드만 표시하고 클릭 링크와 상세 페이지를 만들지 않습니다. 상세 내용 작성 후 `true`로 바꾸면 됩니다. 기본값은 `true`입니다.
- 기간·인원·담당·스킬·설명·이미지·저장소는 선택 입력입니다. 없는 항목은 표시하지 않습니다.
- `period`는 `"2026.02"`처럼 따옴표로 감싸 숫자나 날짜로 해석되지 않게 합니다. `team`도 `"4명"` 같은 문자열입니다.
- `slug`와 카테고리 `id`는 소문자 영문·숫자·하이픈만 사용합니다. `key`는 전체 프로젝트 영역에 예약된 카테고리 ID입니다. 중복 slug, 등록하지 않은 카테고리, 잘못된 우선순위는 빌드 오류로 알려줍니다.

## 카드와 상세 페이지의 원본

| 항목 | 입력 위치 |
|---|---|
| 제목 | 각 언어 MD의 `title` |
| 기간 / 인원 | 각 언어 MD의 `period` / `team` |
| 담당한 일 | 각 언어 MD의 `role` |
| 카드 아래 설명 | 각 언어 MD의 `description` |
| 상세 Overview | 각 언어 MD의 `overview` |
| 공통 스킬 | 한국어 MD의 `skills` |
| 카드에 별도 표시할 스킬 | 선택 항목 `card.skills`; 없으면 `skills` 사용 |
| 카드 이미지 / 대체 텍스트 | `card.image` / `card.imageAlt` |
| 이미지 표시 방식 | `card.imageFit`: `cover` 또는 `contain` |
| GitHub 링크 | `repository`; 없으면 링크 숨김 |
| 상세 본문 | `##` 제목과 그 아래 Markdown |

예전 `group`, `card.titleEn`, `card.descriptionKo/En`, `card.contributionKo/En`, `card.keywords`는 사용하지 않습니다. LK도 다른 프로젝트와 동일하게 MD에서 관리합니다.

## 빌드와 배포

```bash
npm run build:projects
node --test scripts/test-project-build.mjs
npm run build
```

빌드가 우선순위로 정렬한 카테고리·프로젝트를 `projects.json`에 기록하고 상세 HTML을 생성합니다. `main`으로 푸시하면 GitHub Actions가 다시 빌드해 배포합니다. 로컬 MD 수정만으로 공개 사이트가 바뀌지는 않습니다.

프로젝트 MD를 삭제하거나 `detail: false`로 바꾸면 해당 자동 생성 상세 HTML도 다음 빌드에서 정리합니다. 수동 작성 HTML은 삭제하지 않습니다. 카테고리를 삭제할 때는 연결된 프로젝트의 `category`도 함께 수정해야 합니다.

## 대표 미디어 설정

이미지는 다음과 같이 설정합니다.

```yaml
demo:
  type: image
  src: ../assets/images/project-name.png
  alt: 프로젝트 대표 이미지 설명
```

로컬 영상은 `assets/videos`에 넣고 다음과 같이 설정합니다.

```yaml
demo:
  type: video
  src: ../assets/videos/project-demo.mp4
  poster: ../assets/images/project-poster.png
```

YouTube 영상은 Embed 주소를 사용합니다.

```yaml
demo:
  type: youtube
  src: https://www.youtube.com/embed/VIDEO_ID
  alt: 프로젝트 시연 영상
```

대표 미디어가 필요 없으면 `demo` 항목 전체를 삭제합니다. 이미지와 영상 아래에는 별도 캡션을 표시하지 않습니다. 본문 중간에 이미지를 추가할 때는 일반 Markdown 이미지 문법을 사용합니다.

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
