#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
app_dir="$repo_root/app"

if [[ -f "$app_dir/venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$app_dir/venv/bin/activate"
else
  echo "Virtualenv not found at $app_dir/venv." >&2
  echo "Create it with: python -m venv \"$app_dir/venv\" && source \"$app_dir/venv/bin/activate\" && pip install -r \"$app_dir/requirements.txt\"" >&2
  exit 1
fi

cd "$app_dir"
exec streamlit run app.py
