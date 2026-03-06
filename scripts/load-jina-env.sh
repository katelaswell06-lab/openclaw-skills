#!/usr/bin/env bash
set -euo pipefail

# Load JINA_API_KEY from env first, then fallback to ~/.jina-credentials.
# This keeps credentials out of repo history while preserving your home-credential pattern.
if [[ -n "${JINA_API_KEY:-}" ]]; then
  export JINA_API_KEY
  echo "JINA_API_KEY loaded from environment"
  exit 0
fi

if [[ -f "$HOME/.jina-credentials" ]]; then
  # shellcheck disable=SC1090
  # Expected file format: export JINA_API_KEY="..."
  . "$HOME/.jina-credentials"
fi

if [[ -z "${JINA_API_KEY:-}" ]]; then
  echo "Warning: JINA_API_KEY not set. Run: export JINA_API_KEY=..." >&2
  exit 1
fi

echo "JINA_API_KEY loaded from ~/.jina-credentials"
