# openclaw-skills

Central repo for OpenClaw skill definitions used across projects.

## Structure

- `.claude/skills/<skill-name>/SKILL.md` - Canonical skill specs.

## Current skills

- `playwright-lean`

## Usage

- Use this as source-of-truth for cross-project skill reuse.
- Runtime copies can be synced from here into:
  - `~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/`
  - project-local skill directories as needed.

## Secret loading convention (shared pattern)

For command-line scripts that need API keys, use this pattern:

- Prefer runtime env var if available: `JINA_API_KEY`.
- Fallback to `~/.jina-credentials` with:
  ```bash
  export JINA_API_KEY="..."
  ```

Example helper:
```bash
cd ~/apps/openclaw-skills
source scripts/load-jina-env.sh
```
