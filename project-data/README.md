# Project detail content

상세 페이지의 공통 HTML 구조는 `templates/project-detail.mjs`에서 관리합니다.

- 공통 레이아웃, 헤더, 뒤로 가기 아이콘, GitHub 아이콘, 섹션 출력 방식 변경: `templates/project-detail.mjs`
- 공통 색상, 간격, 반응형 스타일 변경: `styles.css`의 `Case study` 영역
- 프로젝트별 제목, 팀, 기간, 기술, Overview, Demo 변경: 해당 프로젝트의 `.mjs` 파일
- 프로젝트별 세부 섹션 변경: `sections` 배열에서 해당 `id` 객체의 `title` 또는 `body` 수정
- 섹션 순서 변경: `sections` 배열의 객체 순서 변경
- 섹션 추가·삭제: `sections` 배열에 객체를 추가하거나 제거

수정 후 아래 명령으로 `projects/*.html`을 다시 생성합니다.

```bash
npm run build:projects
```

`projects/*.html`은 생성 결과물이므로 직접 수정하지 않습니다.
