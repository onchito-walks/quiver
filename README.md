# Quiver — Adaptive Context Optimizer for AI Agents

AI agents are born carrying every arrow they might ever need — thirty-three
of them, broadheads and field points alike, every shaft carved with every
lesson ever learned. They draw the whole quiver on every turn whether they're
aiming at anything or not. Most of those arrows never fly. They just sit
there, heavy on the string, burning attention on tools no target demands.

A hunter's quiver does not work this way. Every arrow has the same shaft —
light, straight, essential. But the head changes. A broadhead for the hunt.
A field point for everyday work. The shaft is always there because without
it there is no arrow. The head is chosen for the target. And at night, the
fletcher inspects every shaft, sharpens dull broadheads, replaces bent field
points, and catalogs what's ready for the morning.

Quiver is that quiver. It ensures each session carries exactly the arrows it
needs and nothing more — shafts kept lean, heads matched to targets, everything
sharpened nightly while the archer sleeps.

---

## Architecture

```
                        THE QUIVER
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    THE SHAFT        THE HEAD       THE FLETCHER
    (every arrow)    (chosen per     (nightly, 02:00)
     always there)    target)
          │               │               │
    ┌──────────┐   ┌──────────────┐  ┌──────────────┐
    │AGENTS.md │   │ BROADHEADS   │  │ Sharpens      │
    │(3.1 KB)  │   │ (heavy tools)│  │ dull heads    │
    │          │   │              │  │              │
    │SOUL.md   │   │ browser      │  │ Replaces      │
    │(3.5 KB)  │   │ image_gen    │  │ bent shafts   │
    │          │   │ video_gen    │  │              │
    │Budget:   │   │ code_exec    │  │ Trims shafts  │
    │<16 KB    │   │ session_srch │  │ to budget     │
    │combined  │   │ tts, vision  │  │              │
    │          │   │ x_search     │  │ Catalogs      │
    │          │   │ video        │  │ new heads     │
    │          │   │              │  │              │
    │          │   │ FIELD POINTS │  │ Patches       │
    │          │   │ (skills)     │  │ catalog       │
    │          │   │              │  │              │
    │          │   │ research-    │  │ Updates       │
    │          │   │ methodology  │  │ README        │
    │          │   │ search-      │  │              │
    │          │   │ routing      │  └──────────────┘
    │          │   │ github-      │
    │          │   │ autonomy     │
    │          │   │ harness-     │
    │          │   │ compensation │
    │          │   │ lazy-tools   │
    │          │   │ credential-  │
    │          │   │ isolation    │
    └──────────┘   └──────────────┘
```

### The Shaft — Every Arrow, Always

AGENTS.md and SOUL.md form the body of every arrow. Without them there is nothing
to loose. They must be light enough that the hunter never notices the weight.

| File | Before | After | What moved |
|---|---|---|---|
| AGENTS.md | 19.0 KB | 3.1 KB | Research, routing, delegation, GitHub → field points |
| SOUL.md | 10.1 KB | 3.5 KB | Removed overlaps, tightened prose |
| Combined | 29.1 KB | 6.6 KB | -77% |

### The Head — Chosen for the Target

**Broadheads** are heavy tools. Disabled globally, cataloged in GBrain, dispatched
as isolated subagents. A broadhead is never attached unless there's big game.

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

**Field points** are skills. Always in the quiver, drawn on demand when the task
calls for them. Never burn tokens in sessions that don't need them.

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

- **Sharpens broadheads**: Promotes frequently-used tools back to active duty.
- **Replaces field points**: Flags stale skills, overlapping triggers, dead crons.
- **Trims shafts**: Flags AGENTS.md/SOUL.md if they exceed the 8 KB budget.
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

| Part | Before | After | Change |
|---|---|---|---|
| **Shaft** | | | |
| AGENTS.md | 19.0 KB | 3.1 KB | **-84%** |
| SOUL.md | 10.1 KB | 3.5 KB | **-65%** |
| **Heads** | | | |
| Hermes tools loaded | 33 | 15 | **-55%** |
| Tool schemas | 61.6 KB | 36.9 KB | **-40%** |
| GBrain MCP tools | 85 | 25 | **-71%** |
| **Impact** | | | |
| System prompt | 33.3 KB | 21.6 KB | **-35%** |
| Per-turn tokens saved | — | ~12,000 | — |
| Monthly savings | — | ~120M tokens / ~$65 | — |
| "I can't do that" rate | frequent | near-zero | — |

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

```bash
# 1. Sheathe the broadheads
hermes tools disable browser session_search code_execution vision \
  image_gen video_gen tts x_search video clarify homeassistant yuanbao

# 2. Filter MCP servers
# Add tools: {include: [...]} to mcp_servers.gbrain and mcp_servers.github

# 3. Install the router
cp skills/lazy-tools/SKILL.md ~/.hermes/skills/devops/lazy-tools/SKILL.md

# 4. Seed the catalog
python3 scripts/seed-catalog.py

# 5. Wake the fletcher
hermes cron create --name lazy-tools-nightly-learn --schedule "0 2 * * *" \
  --skills lazy-tools --toolsets web,terminal,file,skills,delegation \
  --prompt "$(cat crons/nightly-learn-prompt.md)"

# 6. Verify
hermes prompt-size     # shaft + light heads = ~37 KB schemas, ~22 KB prompt
hermes tools list      # 8 nocked, broadheads sheathed
```

## Limitations

MCP tool filtering requires gateway restart. Broadheads add 5-15s subagent dispatch
latency. Frustration detection is keyword-based, improved nightly. Toolset granularity
is a Hermes limitation (can't split `file` to keep read_file but drop patch).

## License

MIT
