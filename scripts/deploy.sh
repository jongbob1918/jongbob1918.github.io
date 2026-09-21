#!/usr/bin/env bash
set -euo pipefail

script_path=$(readlink -f -- "${BASH_SOURCE[0]}")
repo_root=$(cd -- "$(dirname -- "$script_path")/.." && pwd -P)
current_root=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [[ "$current_root" != "$repo_root" ]]; then
  printf '블로그 레포 안에서 deploy를 실행하세요: %s\n' "$repo_root" >&2
  exit 1
fi
cd -- "$repo_root"

if [[ "$(git branch --show-current)" != main ]]; then
  printf '자동 배포는 main 브랜치에서 실행하세요.\n' >&2
  exit 1
fi

message=${*:-"Update blog $(date '+%Y-%m-%d %H:%M:%S')"}
printf '블로그 빌드를 확인합니다.\n'
npm run build

printf '레포 전체 변경을 등록합니다 (git add .).\n'
git add .
if git diff --cached --quiet; then
  printf '새로 커밋할 변경이 없습니다. 기존 커밋을 push합니다.\n'
else
  git commit -m "$message"
fi

git push origin main
printf '\n업로드 완료. GitHub Actions에서 자동 배포가 진행됩니다.\n'
printf 'https://github.com/jongbob1918/jongbob1918.github.io/actions\n'
