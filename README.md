# Quiver — Adaptive Context Optimizer for AI Agents

AI agents are born carrying every arrow they might ever need — thirty-three
of them, broadheads and field points alike, every shaft carved with every
lesson ever learned. They draw the whole quiver on every turn whether they're
aiming at anything or not. Most of those arrows never fly. They just sit
there, heavy on the string, burning attention on tools no target demands.

A hunter's quiver does not work this way. The quiver itself — the leather,
the stitching, the strap — is always on the hip. Light enough to forget it's
there. Inside: broadheads for the hunt, field points for everyday work. The
hunter reaches in and draws only the head the target demands. At night, the
fletcher empties the quiver, sharpens dull broadheads, replaces bent field
points, and checks that the leather hasn't stretched.

Quiver is that quiver. AGENTS.md and SOUL.md form the bag — always carried,
kept lean. Broadheads and field points fill it — drawn on demand. The fletcher
works nightly while the archer sleeps.

---

## Architecture

```
                      THE QUIVER (always on the hip)
               ┌─────────────────────────────────────────┐
               │  AGENTS.md (3.1 KB) + SOUL.md (3.5 KB) │
               │  Budget: <16 KB combined                │
               │                                         │
               │  ┌──────────────────────────────────┐   │
               │  │        BROADHEADS                │   │
               │  │  (heavy tools, subagent dispatch)│   │
               │  │                                  │   │
               │  │  browser (10)    image_gen       │   │
               │  │  session_search  video_gen       │   │
               │  │  code_execution  tts             │   │
               │  │  vision          x_search        │   │
               │  │  video                           │   │
               │  └──────────────────────────────────┘   │
               │                                         │
               │  ┌──────────────────────────────────┐   │
               │  │        FIELD POINTS              │   │
               │  │  (skills, loaded on demand)      │   │
               │  │                                  │   │
               │  │  research-methodology            │   │
               │  │  search-routing                  │   │
               │  │  github-autonomy                 │   │
               │  │  harness-compensation            │   │
               │  │  lazy-tools                      │   │
               │  │  credential-isolation            │   │
               │  │  leviathan-routing-architecture  │   │
               │  └──────────────────────────────────┘   │
               └─────────────────────────────────────────┘
                                  │
                                  ▼
               ┌─────────────────────────────────────────┐
               │           THE FLETCHER                  │
               │           (nightly, 02:00 UTC)          │
               │                                         │
               │  Sharpens broadheads. Replaces field    │
               │  points. Trims the leather. Catalogs    │
               │  new heads. Patches the catalog.        │
               └─────────────────────────────────────────┘
```

### The Quiver — AGENTS.md + SOUL.md

The leather and stitching. Always on the hip. Must be light enough to forget it's
there. Strict size budgets enforced by the fletcher every night.

| File | Before | After | What moved |
|---|---|---|---|
| AGENTS.md | 19.0 KB | 3.1 KB | Research, routing, delegation, GitHub → field points |
| SOUL.md | 10.1 KB | 3.5 KB | Removed overlaps, tightened prose |
| Combined | 29.1 KB | 6.6 KB | -77% |

### Broadheads — Heavy Tools

Inside the quiver. Disabled globally, cataloged in GBrain (`systems/tool-catalog`),
dispatched as isolated subagents. A broadhead is never drawn unless there's big game.

| Broadhead | Tools | Drawn when |
|---|---|---|
| browser | 10 | "go to this website", "take a screenshot" |
| session_search | 1 | "find that conversation" |
| code_execution | 1 | "run this analysis" |
| image_gen | 1 | "generate an image" |
| video_gen | 1 | "make a video" |
| tts | 1 | "read this aloud" |
| x_search | 1 | "search twitter" |
| vision | 1 | "analyze this image" |
| video | 1 | "what's in this clip" |

### Field Points — Skills

Inside the quiver. Loaded on demand when the task calls for them. Never burn tokens
in sessions that don't need them.

| Field point | Drawn when |
|---|---|
| research-methodology | research, look up, study, investigate |
| search-routing | search, find |
| github-autonomy | push, repo, github |
| harness-compensation | delegation, verification, subagents |
| lazy-tools | frustration detection, tool dispatch |
| credential-isolation | credential, API key, token |
| leviathan-routing-architecture | model, provider, routing |

### The Fletcher — Nightly, 02:00 UTC

- **Sharpens broadheads**: Promotes frequently-used tools back to active.
- **Replaces field points**: Flags stale skills, overlapping triggers, dead crons.
- **Trims the leather**: Flags AGENTS.md/SOUL.md if they exceed the 8 KB budget.
- **Catalogs new heads**: Finds undiscovered tools and adds them to GBrain.
- **Updates the ledger**: Patches the lazy-tools skill, updates this README.

---

## Production Configuration (Hermes Agent, July 2026)

### Always loaded (the shaft + light heads)

| Toolset | Tools | Why |
|---|---|---|
| `terminal` | 1 | 92% of sessions |
| `file` | 4 | 80%+ of sessions |
| `web` | 2 | Core research |
| `skills` | 3 | Skill management |
| `memory` | 1 | Persistence |
| `delegation` | 1 | Quiver's engine |
| `cronjob` | 1 | Scheduled work |
| `todo` | 1 | Task tracking |

### Broadheads (subagent dispatch)

| Broadhead | Tools | Subagent toolsets |
|---|---|---|
| `browser` | 10 | `["browser", "web"]` |
| `session_search` | 1 | `["session_search"]` |
| `code_execution` | 1 | `["code_execution", "terminal"]` |
| `vision` | 1 | `["vision"]` |
| `image_gen` | 1 | `["image_gen"]` |
| `video_gen` | 1 | `["video_gen"]` |
| `tts` | 1 | `["tts"]` |
| `x_search` | 1 | `["x_search", "web"]` |
| `video` | 1 | `["video"]` |

### Field points (skills on demand)

| Field point | Trigger |
|---|---|
| `research-methodology` | research, look up, study |
| `search-routing` | search, find |
| `github-autonomy` | push, repo, github |
| `harness-compensation` | delegation, verification |
| `lazy-tools` | frustration, tool dispatch |
| `credential-isolation` | credential, API key |
| `leviathan-routing-architecture` | model, provider, routing |

### MCP Servers

| Server | Total | In Quiver | Method |
|---|---|---|---|
| GBrain | 85 | **25** | `tools: {include: [...]}` |
| GitHub | 30+ | **13** | `tools: {include: [...]}` |

### Performance

| Part | Before (Jun 2026) | After (Jun 2026) | Current (Jul 09 2026) | Change |
|---|---|---|---|---|
| **Shaft** | | | | |
| AGENTS.md | 19.0 KB | 3.1 KB | 3.5 KB | **-82%** |
| SOUL.md | 10.1 KB | 3.5 KB | 3.5 KB | **-65%** |
| Combined | 29.1 KB | 6.6 KB | 7.0 KB | **-76%** |
| **Heads** | | | | |
| Hermes tools loaded | 33 | 15 | 15 | **-55%** |
| Tool schemas | 61.6 KB | 36.9 KB | 36.9 KB | **-40%** |
| GBrain MCP tools | 85 | 25 | 25 | **-71%** |
| GitHub MCP tools | 30+ | 13 | 13 | **-57%** |
| **Impact** | | | | |
| System prompt | 33.3 KB | 21.6 KB | 21.4 KB | **-36%** |
| Per-turn tokens saved | — | ~12,000 | ~12,000 | — |
| Monthly savings | — | ~120M tokens / ~$65 | ~130M tokens / ~$70 | — |
| "I can't do that" rate | frequent | near-zero | near-zero | — |

---

## Design Principles

**The shaft is always there.** AGENTS.md + SOUL.md form every arrow. Keep them light.

**The head matches the target.** Broadhead for the hunt. Field point for everyday
work. Never draw a head the target doesn't demand.

**Frustration is a draw signal.** "Why can't you" means a broadhead should have been
nocked. Quiver detects this and dispatches immediately.

**The fletcher works while the archer sleeps.** Nightly analysis of real usage data.
Catalog patches. Budget enforcement. No human intervention needed.

**Semantic matching over keywords.** Arrowheads are stored with rich descriptions in
a vector database. The hunter says what they need; Quiver finds the right head by
meaning, not by memorized trigger phrases.

---

## Tech Stack

| Component | Implementation | Why |
|---|---|---|
| **Catalog** | GBrain vector DB (pgvector) | Already deployed, zero new infra |
| **Intent matching** | GBrain semantic search | Hybrid vector + keyword + graph |
| **Frustration detection** | Skill-level pattern matching | Fast, no API call |
| **Dispatch** | Hermes `delegate_task` with `toolsets` | Native tool-restricted workers |
| **The Fletcher** | Hermes cron (LLM-driven) | Reads sessions, patches skills, updates catalog |
| **Config** | Hermes `hermes tools enable/disable` | Native, persistent |

---

## Installation

Quiver now has a tiny stdlib CLI so Hermes can prove the integration instead of relying on a remembered checklist.

```bash
# Put the quiver command on PATH for this machine
sudo bash scripts/install-quiver-wrapper.sh

# Verify the integration
quiver doctor
quiver status --json

# Dry-run the install plan
quiver install

# Apply/repair drift in the active Hermes profile
quiver install --apply
quiver repair --apply
```

The CLI manages the same native Hermes/GBrain pieces Quiver has always used:

```bash
# 1. Sheathe the broadheads
hermes tools disable browser session_search code_execution vision \
  image_gen video_gen tts x_search video clarify homeassistant yuanbao

# 2. Keep light heads nocked
hermes tools enable web terminal file skills todo memory delegation cronjob

# 3. Filter MCP servers
# Add tools: {include: [...]} to mcp_servers.gbrain and mcp_servers.github
# Then restart/reload the gateway because MCP tool lists load at startup.

# 4. Install the router skill
cp skills/lazy-tools/SKILL.md "$HERMES_HOME/skills/devops/lazy-tools/SKILL.md"

# 5. Seed the catalog
python3 scripts/seed-catalog.py  # prints catalog metadata; quiver install --apply writes it via gbrain

# 6. Wake the fletcher
hermes cron create --name lazy-tools-nightly-learn --schedule "0 2 * * *" \
  --skills lazy-tools --toolsets web,terminal,file,skills,delegation \
  --prompt "$(cat crons/nightly-learn-prompt.md)"

# 7. Verify
hermes prompt-size     # shaft + light heads = ~37 KB schemas, ~22 KB prompt
hermes tools list      # light heads enabled, broadheads sheathed
```

See `docs/HERMES-INTEGRATION.md` for the integration contract and sync rules.

## Limitations

MCP tool filtering requires gateway restart. Broadheads add 5-15s subagent dispatch
latency. Frustration detection is keyword-based, improved nightly. Toolset granularity
is a Hermes limitation (can't split `file` to keep read_file but drop patch).

**Known (Jul 2026):** OmniRoute provider probe engine can exceed 600s timeout under
load (job `90ae4bb2ff1f`). Cron delivery to non-local platforms silently fails if
the platform is not configured (3 affected jobs: schema-pack, weekly-spend,
weekly-synthesis — all targeting Telegram, which is not configured). Skills directory
contains legacy gstack nested copies (`.hermes/skills/gstack/.hermes/skills/...`) that
could be consolidated. Hermes v0.15+ changed cron subcommand from `cronjob` to `cron`.

## License

MIT
