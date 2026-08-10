#!/usr/bin/env bash
# Prepare channel content and serve the Jekyll site locally.
# Open: http://127.0.0.1:4000/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WEBSITE="$ROOT/website"

export RBENV_VERSION="${RBENV_VERSION:-3.3.10}"

python3 "$WEBSITE/scripts/prepare_site.py" "$@"

cd "$WEBSITE"
if [[ ! -d vendor/bundle ]]; then
  bundle config set --local path 'vendor/bundle'
  bundle install
fi

exec bundle exec jekyll serve --livereload --host 127.0.0.1
