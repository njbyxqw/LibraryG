#!/usr/bin/env bash
# Report staged additions/modifications over 5 MiB before creating a commit.
# Override LG_LARGE_FILE_BYTES only for a deliberate, reviewed exception.
set -euo pipefail

limit_bytes="${LG_LARGE_FILE_BYTES:-5242880}"
found=0

while IFS= read -r -d '' file_path; do
  byte_count="$(git cat-file -s ":${file_path}")"
  if (( byte_count > limit_bytes )); then
    printf '%s bytes\t%s\n' "$byte_count" "$file_path"
    found=1
  fi
done < <(git diff --cached --name-only -z --diff-filter=ACMR)

if (( found == 1 )); then
  printf '%s\n' 'Above files exceed the default 5 MiB review threshold; keep, externalize, or use Git LFS deliberately.' >&2
  exit 1
fi

printf '%s\n' 'No staged additions or modifications exceed 5 MiB.'
