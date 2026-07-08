# Quiver — Adaptive Tool Router & Maintainer for AI Agents

AI agents are born into the world carrying every tool they might ever need.
Thirty-three schemas, sixty kilobytes, loaded into every conversation turn
whether they're used or not. Most of those tools never fire. They just sit
there, burning tokens, slowing responses, bloating context windows that
are already fighting for space. The agent spends 40% of its attention
budget on tools it will never call.

Quiver fixes this. It is a tool router and maintainer that ensures each
session carries exactly the tools it needs and nothing more. When a tool
isn't loaded, it isn't gone — it's cataloged in a vector database, matched
to user intent through semantic search, and dispatched through isolated
subagents the moment it's needed. The user never hears "I can't do that."
They just get results.

But Quiver doesn't stop at routing. It audits the entire tool inventory
every night: which scripts are stale, which skills overlap, which crons
have gone silent, which tools have earned their place in the default
loadout and which should be demoted. It patches its own catalog, updates
its own documentation, and gets smarter every 24 hours without human
intervention.

Quiver exists because tools should serve the session, not the other way
around. It lives to make agents faster, cheaper, and harder to frustrate.

---

## Architecture

Quiver sits between the agent's tool registry and the LLM's context window. It replaces
the "load everything" model with "retrieve what's needed" — the same architectural shift
that made RAG dominant over full-document context windows. Beyond routing, it audits the
entire tool inventory: scripts, skills, crons, MCP servers, and Hermes-native toolsets.

```
                          USER INTENT
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                      QUIVER                                   │
│                                                               │
│   ┌─────────────────┐    ┌──────────────────┐                │
│   │   TOOL CATALOG   │    │  FRUSTRATION     │                │
│   │   (vector DB)    │◄───│  DETECTOR        │                │
│   │                  │    │                  │                │
│   │  All tools:      │    │ "why can't you"  │                │
│   │  - Hermes native │    │ "this is broken" │                │
│   │  - MCP servers   │    │ "just do it"     │                │
│   │  - Scripts       │    └────────┬─────────┘                │
│   │  - Skills        │             │                          │
│   │  - Crons         │             ▼                          │
│   └────────┬─────────┘    ┌──────────────────┐                │
│            │              │  INTENT → TOOL   │                │
│            │              │  MATCHER         │                │
│            │              │                  │                │
│            │              │ semantic search  │                │
│            │              │ over catalog     │                │
│            └──────┬───────┴────────┬─────────┘                │
│                   │                │                          │
│                   ▼                ▼                          │
│          ┌────────────────────────────────────┐              │
│          │       SUBAGENT DISPATCHER           │              │
│          │                                     │              │
│          │  delegate_task(                     │              │
│          │    goal="handle user intent",       │              │
│          │    toolsets=["browser", "web"]      │              │
│          │  )                                  │              │
│          └────────────────────────────────────┘              │
│                                                               │
│   ┌─────────────────────────────────────────────────────┐    │
│   │              TOOL MAINTAINER (cron)                  │    │
│   │                                                     │    │
│   │  Audits: which tools exist, which are used, which   │    │
│   │  are redundant, which are broken, which can be      │    │
│   │  consolidated. Patches catalog. Updates README.     │    │
│   │  Flags: stale scripts, unused skills, dead crons.   │    │
│   └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

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
| Tool schemas in context | 61.6 KB | 36.9 KB | **-40%** |
| Hermes tools loaded | 33 | 15 | **-55%** |
| GBrain MCP tools | 85 | 25 | **-71%** |
| Per-turn tokens saved | — | ~6,000 | — |
| Monthly token savings (est.) | — | 15-20M | **~30%** |
| Monthly cost savings (est.) | — | $8-12 | **~30%** |
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
