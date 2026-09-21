# 블로그 배포

이 PC에서는 레포 안에서 다음 명령을 실행한다.

```bash
deploy
```

커밋 메시지를 직접 지정할 수도 있다.

```bash
deploy "딥러닝 01 수정"
```

`npm run build` → `git add .` → `git commit` → `git push origin main` 순서로 실행한다. 빌드나 Git 명령이 실패하면 다음 단계로 넘어가지 않는다. 변경이 없으면 커밋을 생략하고 push한다. main 브랜치에서만 실행한다.

`git add .`는 레포 루트에서 실행하므로 하위 폴더에서 명령을 실행해도 레포 전체 변경을 포함한다. `.gitignore`에 없는 이미지, 옵시디언 설정, 임시 파일도 모두 포함한다.

push가 끝나면 GitHub Actions가 배포한다. 스크립트의 업로드 완료 메시지는 배포 완료를 뜻하지 않는다. [Actions](https://github.com/jongbob1918/jongbob1918.github.io/actions)에서 결과를 확인한다.

다른 PC에서는 레포 루트에서 `bash scripts/deploy.sh` 또는 `npm run deploy`를 실행한다. `deploy`라는 명령으로 쓰려면 다음과 같이 등록한다 (`~/.local/bin`이 PATH에 있어야 한다).

```bash
mkdir -p ~/.local/bin
ln -s "$PWD/scripts/deploy.sh" ~/.local/bin/deploy
```
