---
name: github-autonomy
description: GitHub push/pull/repo management patterns. SSH keys, PAT tokens, credential helper. Load when doing GitHub operations.
triggers:
  - push to github
  - create repo
  - github api
  - git push
  - onchito-walks
---

# GitHub Autonomy Patterns

## Push pattern

To push any repo under `onchito-walks`: use `git push` with an SSH URL
(`git@github.com:onchito-walks/REPO.git`). SSH key at `~/.ssh/id_ed25519`
is registered on GitHub.

## API pattern

For GitHub API calls: use `GITHUB_TOKEN` from `~/.hermes/.env`.
Bearer token auth: `Authorization: Bearer $GITHUB_TOKEN`.
Token has full admin scopes. Create repos, search code, manage issues.

## Never ask the user

Never tell the user to run `gh auth login`, create a repo manually, or do auth steps.
Find the credential path and use it. `git push` with SSH just works.
API calls with the Bearer token just work.

## gh CLI

`gh` CLI is NOT configured. Use `git` (SSH) for pushes and `curl` (Bearer token)
for API operations. Do not attempt `gh auth` commands.
