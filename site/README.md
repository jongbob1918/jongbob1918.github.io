# 노트 이미지 경로

블로그 노트에서 쓰는 이미지는 `site/public/images/notes/<글 slug>/`에 저장한다. 예를 들어 `easy-deep-learning-ch01.md`의 이미지는 `site/public/images/notes/easy-deep-learning-ch01/`에 둔다. 파일명은 내용을 알 수 있는 영문 소문자와 하이픈으로 짓는다.

옵시디언과 블로그에서 같은 파일을 볼 수 있도록 노트에는 파일 기준 상대경로를 쓴다. `site/src/content/notes/Deep learning/`에 있는 글의 예시는 다음과 같다.

```html
<img src="../../../../public/images/notes/easy-deep-learning-ch01/restaurant-rl-01-random-exploration.png" alt="무작위 탐색 중 공사 구간에 들어가 벌점을 받는 단계" loading="lazy" />
```

빌드 시 이 경로는 블로그 주소 `/images/notes/easy-deep-learning-ch01/restaurant-rl-01-random-exploration.png`로 바뀐다. 다른 폴더에 노트를 추가할 때는 해당 노트에서 `site/public`까지의 상대경로를 사용한다.

`npm run build:notes`는 이미지 참조가 존재하는지와 사용하지 않는 공개 이미지가 남아 있는지 확인한다. 이미지 출처나 라이선스 기록은 해당 글의 이미지 폴더에 둔다.
