# agency-ops-openclaw-skills

Central repo for OpenClaw skill definitions used across projects.

## Structure

- `.claude/skills/<skill-name>/SKILL.md` - Canonical skill specs.

## Current skills

- `playwright-lean`

## Usage

- Treat this as source-of-truth for cross-project skill reuse.
- Runtime copies can be synced from here into:
  - `~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/`
  - project-local skill directories when needed.
