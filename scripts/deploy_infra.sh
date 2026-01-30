#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cdk_dir="$repo_root/infra/cdk"

if [[ ! -f "$cdk_dir/package.json" ]]; then
  echo "CDK project not found at $cdk_dir" >&2
  exit 1
fi

cd "$cdk_dir"

if [[ ! -d node_modules ]]; then
  npm install
fi

# CDK uses standard AWS credential resolution:
# - AWS_PROFILE if set (named profile in ~/.aws/config)
# - or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY (+ optional AWS_SESSION_TOKEN)
exec npx cdk deploy
