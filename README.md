# Quiver — Adaptive Context Optimizer for AI Agents

AI agents are born into the world carrying every arrow they might ever need.
Thirty-three broadheads, sixty kilobytes of steel, nocked and drawn on every
turn whether they're aimed at anything or not. Most of those arrows never fly.
They just sit there, weighing down the bow, slowing the draw, burning attention
on tools the agent will never loose.

Meanwhile the bow itself grows heavy. Every lesson learned gets carved into
the grip. Every pitfall becomes another notch. SOUL.md and AGENTS.md accumulate
until the agent spends more energy reading its own inscriptions than aiming
at the target.

A quiver does not carry every arrow at once. It holds them in reserve — field
points for practice, broadheads for the hunt, judo points for small game —
and the archer draws only the head that matches the target. At night, the
fletcher inspects every shaft, sharpens what's dull, replaces what's broken,
and catalogs what's ready.

Quiver is that quiver. It ensures each session carries exactly the arrows it
needs and nothing more. It lives to make agents faster, cheaper, and harder
to frustrate — not by taking arrows away, but by keeping them in the quiver
until the moment the target demands them.

---

## Architecture

Quiver has three jobs. Each maps to a piece of the archer's kit.

```
                          THE ARCHER (your session)
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                        THE QUIVER                             │
│                                                               │
│  BROADHEADS                        FIELD POINTS              │
│  (heavy tools, drawn on demand)    (instructions, always in  │
│  ┌─────────────────────┐          hand but kept light)       │
│  │ browser (10 tools)  │          ┌─────────────────────┐    │
│  │ session_search      │          │ AGENTS.md (3.1 KB)  │    │
│  │ code_execution      │          │ SOUL.md (3.5 KB)    │    │
│  │ image_gen           │          │ Budget: <16 KB      │    │
│  │ video_gen, tts,     │          │                      │    │
│  │ x_search, vision    │          │ Skills on demand:    │    │
│  │                     │          │ research-methodology │    │
│  │ Cataloged in GBrain │          │ search-routing       │    │
│  │ Dispatched via      │          │ github-autonomy      │    │
│  │ subagent delegation │          │ harness-compensation │    │
│  └─────────────────────┘          └─────────────────────┘    │
│                                                               │
│  THE FLETCHER (nightly, 02:00 UTC)                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Inspects every arrow. Sharpens dull broadheads      │    │
│  │ (promotes frequently-used tools). Trims field       │    │
│  │ points (enforces instruction budgets). Catalogs     │    │
│  │ new arrowheads (flags undiscovered tools). Replaces │    │
│  │ broken shafts (dead crons, stale scripts). Patches  │    │
│  │ the catalog. Updates the README.                    │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### Broadheads — Heavy Tools, Drawn on Demand

Tools disabled globally, cataloged in GBrain, dispatched as isolated subagents when
the target demands them. The archer never carries a broadhead nocked unless there's
game in sight.

| Broadhead | Tools | Drawn when archer says |
|---|---|---|
| browser | 10 | "go to this website", "take a screenshot" |
| session_search | 1 | "find that conversation", "what did we discuss" |
| code_execution | 1 | "run this analysis", "process this data" |
| image_gen | 1 | "generate an image", "create a picture" |
| video_gen | 1 | "make a video", "animate this" |
| tts | 1 | "read this aloud", "speak this" |
| x_search | 1 | "search twitter", "what's trending" |
| vision | 1 | "look at this image", "analyze this picture" |
| video | 1 | "analyze this video", "what's in this clip" |

### Field Points — Instructions, Always in Hand but Kept Light

SOUL.md and AGENTS.md are the bow. They're always in hand but must stay light enough
to draw quickly. Content that's only needed situationally is moved to skills (separate
arrowheads loaded on demand). A relocation map in GBrain (`systems/quiver-context-map`)
tracks where every rule went — nothing is lost, only stored smarter.

| File | Before | After | What moved |
|---|---|---|---|
| AGENTS.md | 19.0 KB | 3.1 KB | Research, search routing, delegation patterns → skills |
| SOUL.md | 10.1 KB | 3.5 KB | Removed overlaps, tightened prose |
| Combined | 29.1 KB | 6.6 KB | -77% |

### The Fletcher — Nightly Maintenance

Every night at 02:00 UTC, the fletcher inspects the quiver:

- **Sharpens broadheads**: Promotes tools that are requested >3x/day back to active
- **Trims field points**: Flags AGENTS.md/SOUL.md if they exceed the 8 KB budget
- **Catalogs new arrowheads**: Finds undiscovered tools and adds them to GBrain
- **Replaces broken shafts**: Flags dead crons, stale scripts, overlapping skills
- **Updates the ledger**: Patches the lazy-tools skill, updates the README

## Production Configuration (Hermes Agent, July 2026)

### Always loaded — 8 toolsets, 15 tools, 36.9 KB

| Toolset | Tools | Why |
|---|---|---|
| `terminal` | 1 | 92% of sessions. Primary workhorse. |
| `file` | 4 | 80%+ of sessions. read_file, search_files, write_file, patch. |
| `web` | 2 | Core research. web_search, web_extract. |
| `skills` | 3 | Skill management. skill_view, skill_manage, skills_list. |
| `memory` | 1 | Persistence across sessions. |
| `delegation` | 1 | Quiver's engine. delegate_task with custom toolsets. |
| `cronjob` | 1 | Scheduled work. |
| `todo` | 1 | Task tracking. |

### In Quiver — dispatched via subagent on demand

| Toolset | Tools | Trigger phrase | Subagent toolsets |
|---|---|---|---|
| `browser` | 10 | "go to this website" | `["browser", "web"]` |
| `session_search` | 1 | "find that conversation" | `["session_search"]` |
| `code_execution` | 1 | "run this analysis" | `["code_execution", "terminal"]` |
| `vision` | 1 | "look at this image" | `["vision"]` |
| `image_gen` | 1 | "generate an image" | `["image_gen"]` |
| `video_gen` | 1 | "create a video" | `["video_gen"]` |
| `tts` | 1 | "read this aloud" | `["tts"]` |
| `x_search` | 1 | "search twitter" | `["x_search", "web"]` |
| `video` | 1 | "analyze this clip" | `["video"]` |

### MCP servers

| Server | Total tools | Filtered to | Filter method |
|---|---|---|---|
| GBrain | 85 | **25** (only actually-used) | `tools: {include: [...]}` |
| GitHub | 30+ | **13** | `tools: {include: [...]}` |
| Linear | all | all | unused, candidate for removal |
| Spacedoom | all | all | low volume, acceptable |

### Performance

| Metric | Before Quiver | After Quiver | Change |
|---|---|---|---|
| **Tools** | | | |
| Hermes tool schemas | 61.6 KB | 36.9 KB | **-40%** |
| Hermes tools loaded | 33 | 15 | **-55%** |
| GBrain MCP tools | 85 | 25 | **-71%** |
| **Instructions** | | | |
| AGENTS.md | 19.0 KB | 3.1 KB | **-84%** |
| SOUL.md | 10.1 KB | 3.5 KB | **-65%** |
| Combined instruction files | 29.1 KB | 6.6 KB | **-77%** |
| System prompt total | 33.3 KB | 21.6 KB | **-35%** |
| **Impact** | | | |
| Per-turn tokens saved | — | ~12,000 | — |
| Monthly token savings (est.) | — | 120M | **~30%** |
| Monthly cost savings (est.) | — | $65 | **~30%** |
| "I can't do that" rate | frequent | near-zero | — |

## The Tool Maintainer

Quiver's nightly cron (`lazy-tools-nightly-learn`, 02:00 UTC) does more than route.
It audits the entire tool inventory:

### What it audits

| Category | Source | What it checks |
|---|---|---|
| Hermes toolsets | `hermes tools list` | Enabled/disabled, usage frequency, promotion candidates |
| MCP tools | GBrain/GitHub MCP config | Filter effectiveness, unused tools still included |
| Scripts | `~/.hermes/scripts/` | What exists, what's used, stale scripts, consolidation candidates |
| Skills | `skills_list` | Loaded skills, unused skills, overlapping skills |
| Crons | `cronjob list` | Health status, last run, dead crons, redundant crons |

### What it does with findings

1. **Flags redundancies**: Two scripts doing the same thing → recommends consolidation
2. **Detects staleness**: Script unused for 30+ days → flags for review
3. **Tracks drift**: Tool was in Quiver (subagent-only) but is now used daily → recommends promotion
4. **Updates the catalog**: GBrain `systems/tool-catalog` stays current
5. **Patches the router**: `lazy-tools` skill gets new trigger phrases
6. **Updates this README**: Performance metrics, tool counts, configuration changes

### Promotion threshold

If a disabled tool is requested via subagent delegation 3+ times/day for 3 consecutive
days, Quiver recommends re-enabling it globally. The tool has proven it belongs in the
default session. If a tool has zero uses in 30 days, Quiver recommends disabling it.

---

## Design Principles

### 1. Retrieval over enumeration

Don't list all tools in context. Store them in a vector DB. Retrieve only what
matches the current intent. This is RAG for tool schemas.

### 2. Subagent isolation over global loading

Don't load tools "just in case." When a tool is needed, spawn an isolated subagent
with exactly that toolset. The subagent's context is fresh, its tool list minimal.

### 3. Frustration as a first-class signal

User frustration is the most reliable signal that a tool is missing. "Why can't you,"
"this is broken," "just do it" bypass normal intent matching and go directly to
catalog search.

### 4. Self-improvement over manual maintenance

Tool catalogs rot. New tools appear. User vocabulary shifts. A nightly cron that
analyzes real session data and patches the routing layer is the only sustainable
approach.

### 5. Semantic matching over keyword lists

Hardcoded trigger phrases break when users use different words. Vector similarity
over rich tool descriptions handles natural language variation.

### 6. Audit over assumption

Never assume tools are correct. Audit the full inventory nightly: what exists,
what's used, what's redundant, what's broken. The catalog is only as good as the
ground truth it reflects.

---

## Tech Stack

Quiver is deployment-agnostic. This implementation targets the Hermes Agent ecosystem.

| Component | Implementation | Why |
|---|---|---|
| **Tool Catalog** | GBrain vector DB (pgvector) | Already deployed, zero additional infra |
| **Intent Matcher** | GBrain semantic search | Hybrid vector + keyword + graph |
| **Frustration Detector** | Skill-level pattern matching | Fast, no API call for detection |
| **Subagent Dispatcher** | Hermes `delegate_task` with `toolsets` | Native, supports tool-restricted workers |
| **Nightly Maintainer** | Hermes cron (LLM-driven) | Reads sessions, patches skills, updates catalog |
| **Config Management** | Hermes `hermes tools enable/disable` | Native, persists across sessions |
| **MCP Filtering** | Config-level `tools: {include: [...]}` | Server-side, gateway picks up on reload |

---

## Project Structure

```
quiver/
├── README.md                    # Architecture, principles, production config
├── AGENTS.md                    # Agent context rules for Quiver sessions
├── skills/lazy-tools/
│   └── SKILL.md                 # Router skill (frustration detection + delegation)
├── catalog/
│   └── (seed via scripts/seed-catalog.py)
├── crons/
│   └── nightly-learn-prompt.md  # Self-improvement cron prompt
└── scripts/
    ├── seed-catalog.py          # One-shot catalog seeder
    ├── sk                       # Dead-simple credential setter
    └── set-credential.py        # Credential validation + storage
```

## Installation

```bash
# 1. Disable rarely-used tools globally
hermes tools disable browser session_search code_execution vision \
  image_gen video_gen tts x_search video clarify homeassistant yuanbao

# 2. Filter MCP servers to used-only tools
# Add tools: {include: [...]} to mcp_servers.gbrain and mcp_servers.github in config.yaml

# 3. Install the lazy-tools skill
cp skills/lazy-tools/SKILL.md ~/.hermes/skills/devops/lazy-tools/SKILL.md

# 4. Seed the tool catalog in GBrain
python3 scripts/seed-catalog.py

# 5. Create the nightly maintainer cron
hermes cron create --name lazy-tools-nightly-learn --schedule "0 2 * * *" \
  --skills lazy-tools --toolsets web,terminal,file,skills,delegation \
  --prompt "$(cat crons/nightly-learn-prompt.md)"

# 6. Verify
hermes prompt-size     # should show ~37 KB tool schemas
hermes tools list      # should show 8 enabled, 10+ disabled
```

---

## Limitations

**MCP tool filtering requires gateway restart.** `tools: {include: [...]}` is read
at gateway initialization. After updating the config, reload the gateway.

**Tool schemas are per-session, not per-turn.** Hermes loads tools at session start.
Quiver works around this via subagent dispatch, which adds 5-15 seconds of latency
for disabled tools but keeps the main session lean.

**Frustration detection is keyword-based.** It catches common patterns but may miss
subtle frustration. The nightly learner improves this over time.

**Not all toolsets can be split.** `file` includes read_file, search_files, write_file,
AND patch. You can't disable patch while keeping read. Toolset granularity is a Hermes
limitation, not a Quiver limitation.

---

## License

MIT — same as Hermes Agent. Quiver is a routing and maintenance pattern, not a platform.
