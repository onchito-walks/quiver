# Quiver / Hermes Integration

Quiver is not a daemon and should not become one. It is the Hermes capability-selection layer: the always-light shaft (AGENTS.md/SOUL.md), the lazy tool catalog in GBrain, the `lazy-tools` skill, Hermes tool enable/disable state, MCP include filters, and the nightly fletcher cron.

The CLI exists so the system can prove that integration instead of relying on memory.

## Commands

```bash
quiver doctor          # verify Hermes/GBrain/skill/cron/tool budget state
quiver status          # same as doctor, human-readable
quiver status --json   # machine-readable status
quiver install         # dry-run install plan
quiver install --apply # copy skill, seed GBrain catalog, enforce tools, ensure cron
quiver repair --apply  # repair drift
```

## Integration contract

Quiver keeps Hermes light while preserving function:

1. Heavy broadheads stay disabled in the default session: browser, session_search, code_execution, vision, video, image/video generation, X search, TTS, clarify.
2. Light heads stay enabled: web, terminal, file, skills, todo, memory, delegation, cronjob.
3. The GBrain page `systems/tool-catalog` is the semantic registry for all heads.
4. The `lazy-tools` skill is the runtime router: frustration signals and tool requests query GBrain, then dispatch a bounded subagent with the needed toolset.
5. The nightly fletcher cron learns from real sessions and keeps the skill/catalog fresh.

## Relationship to Trailhead

Quiver is above Trailhead in the stack.

- Quiver decides which capability Hermes should draw.
- Trailhead is a research capability: hard-source search across social/practitioner/docs/GitHub/web terrain.

They should both expose `doctor/status/install/repair`, but they do not do the same job. Trailhead makes research deeper. Quiver makes every session lighter without losing access to tools.

## Sync rules

- Changes to this repo must be committed and pushed to GitHub.
- Installed Hermes skill copy must match `skills/lazy-tools/SKILL.md` unless there is a deliberate local override.
- GBrain `systems/tool-catalog` must be refreshed after catalog edits.
- Hermes gateway should be restarted/reloaded after MCP include-filter changes because MCP tool lists are loaded at startup.
