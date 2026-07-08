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

A hunter does not carry every arrow nocked at once. The bow stays light —
just the grip and the string. Broadheads wait in the quiver for specific game.
Field points wait for everyday work. At night, the fletcher inspects every shaft,
sharpens dull broadheads, replaces bent field points, and catalogs what's ready
for the morning hunt.

Quiver is that quiver. It ensures each session carries exactly the arrows it
needs and nothing more. It lives to make agents faster, cheaper, and harder
to frustrate — not by taking arrows away, but by keeping them sheathed until
the target demands them.

---

## Architecture

```
                          THE BOW (always in hand)
                    ┌─────────────────────────────┐
                    │  AGENTS.md (3.1 KB)         │
                    │  SOUL.md   (3.5 KB)         │
                    │  Budget: <16 KB combined    │
                    └─────────────┬───────────────┘
                                  │
                    THE ARCHER (your session)
                                  │
                                  ▼
               ┌──────────────────────────────────────┐
               │            THE QUIVER                 │
               │                                      │
               │  BROADHEADS        FIELD POINTS      │
               │  (tools)           (skills)          │
               │  ┌──────────┐     ┌──────────────┐  │
               │  │ browser  │     │ research-    │  │
               │  │ img_gen  │     │ methodology  │  │
               │  │ vid_gen  │     │ search-      │  │
               │  │ tts      │     │ routing      │  │
               │  │ x_search │     │ github-      │  │
               │  │ vision   │     │ autonomy     │  │
               │  │ video    │     │ harness-     │  │
               │  │ ses_srch │     │ compensation │  │
               │  │ code_exec│     │ lazy-tools   │  │
               │  │          │     │ credential-  │  │
               │  │          │     │ isolation    │  │
               │  └──────────┘     └──────────────┘  │
               │                                      │
               │  Cataloged in GBrain.                │
               │  Drawn via subagent dispatch.        │
               │  Frustration = auto-draw.            │
               └──────────────────────────────────────┘
                                  │
                                  ▼
               ┌──────────────────────────────────────┐
               │        THE FLETCHER                  │
               │        (nightly, 02:00 UTC)          │
               │                                      │
               │  Sharpens broadheads (promotes       │
               │  frequently-used tools to active).   │
               │  Replaces field points (flags        │
               │  stale skills, overlap, dead crons). │
               │  Trims the bow (enforces SOUL.md     │
               │  and AGENTS.md size budgets).        │
               │  Catalogs new heads. Patches the     │
               │  catalog. Updates the README.        │
               └──────────────────────────────────────┘
```

### The Bow — AGENTS.md + SOUL.md

Always in hand. Must be light enough to draw without thinking. Strict size budgets
enforced by the fletcher every night.

| File | Before | After | What moved |
|---|---|---|---|
| AGENTS.md | 19.0 KB | 3.1 KB | Research, search routing, delegation, GitHub → field points |
| SOUL.md | 10.1 KB | 3.5 KB | Removed overlaps, tightened prose |
| Combined | 29.1 KB | 6.6 KB | -77% |

### Broadheads — Tools for Specific Game

Heavy tools. Disabled globally, cataloged in GBrain (`systems/tool-catalog`), dispatched
as isolated subagents when the target demands them. A broadhead is never nocked unless
there's game in sight.

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

### Field Points — Skills for Everyday Work

General-purpose arrows. Always in the quiver, drawn on demand when the task calls for
them. Each field point loads its full content only when triggered — never burns tokens
in sessions that don't need it.

| Field point | Drawn when |
|---|---|
| research-methodology | Any research task ("look up", "study", "investigate") |
| search-routing | Any search ("find", "search for") |
| github-autonomy | GitHub operations ("push", "repo", "create issue") |
| harness-compensation | Subagent delegation, verification, context reset |
| lazy-tools (Quiver) | Frustration detection, tool dispatch |
| credential-isolation | Credential operations ("update the key") |
| leviathan-routing-architecture | Model/provider/routing changes |

### The Fletcher — Nightly Maintenance

Every night at 02:00 UTC, the fletcher works through the quiver:

- **Sharpens broadheads**: Promotes tools requested >3x/day back to active duty.
- **Replaces field points**: Flags stale skills, overlapping triggers, dead crons.
- **Trims the bow**: Flags AGENTS.md/SOUL.md if they exceed the 8 KB budget.
- **Catalogs new heads**: Finds undiscovered tools and adds them to GBrain.
- **Updates the ledger**: Patches the lazy-tools skill, updates this README.

---

## Production Configuration (Hermes Agent, July 2026)

### The Bow — 8 toolsets, 15 tools, 36.9 KB

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

### Broadheads — Dispatched via subagent

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

### Field Points — Skills loaded on demand

| Field point | Trigger |
|---|---|
| `research-methodology` | research, look up, study, investigate |
| `search-routing` | search, find, look up |
| `github-autonomy` | push, github, repo, create issue |
| `harness-compensation` | delegation, verification, subagent work |
| `lazy-tools` | frustration detection, tool dispatch |
| `credential-isolation` | credential, API key, token |
| `leviathan-routing-architecture` | model, provider, routing |

### MCP Servers

| Server | Total tools | In Quiver | Filter method |
|---|---|---|---|
| GBrain | 85 | **25** (only actually-used) | `tools: {include: [...]}` |
| GitHub | 30+ | **13** | `tools: {include: [...]}` |
| Linear | all | all | unused, candidate for removal |
| Spacedoom | all | all | low volume, acceptable |

### Performance

| Layer | Before | After | Change |
|---|---|---|---|
| **The Bow** | | | |
| AGENTS.md | 19.0 KB | 3.1 KB | **-84%** |
| SOUL.md | 10.1 KB | 3.5 KB | **-65%** |
| Combined | 29.1 KB | 6.6 KB | **-77%** |
| **Broadheads** | | | |
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

### 1. The bow stays light

SOUL.md and AGENTS.md are always in hand. They must be small enough to draw without
thinking. Content that's only needed sometimes lives in the quiver as field points.

### 2. Broadheads match the game

Don't nock a broadhead for a rabbit. Don't nock a field point for a bear. Match the
arrow to the target. Heavy tools (browser, image gen) dispatch as subagents. Light
tools (web search, file read) stay nocked.

### 3. Frustration is a first-class signal

When the archer curses, the quiver opens. "Why can't you," "this is broken," "just
do it" — these are not complaints. They are the sound of a broadhead not being drawn
when it should have been. Quiver detects them and dispatches immediately.

### 4. The fletcher works while the archer sleeps

Tool catalogs rot. Skills go stale. The bow accumulates weight. A nightly cron that
analyzes real usage data and patches the system is the only sustainable approach.
Quiver improves every 24 hours without the archer touching a thing.

### 5. Semantic matching over keyword lists

Hardcoded trigger phrases break when the archer uses different words. Broadheads and
field points are stored with rich descriptions in a vector database. The archer says
what they need; Quiver finds the right arrow by meaning, not by keyword.

### 6. Audit over assumption

Never assume the quiver is correctly stocked. The fletcher audits the full inventory
every night: what exists, what's used, what's redundant, what's broken. The catalog
is only as good as the ground truth it reflects.

---

## Tech Stack

Quiver is deployment-agnostic. This implementation targets the Hermes Agent ecosystem.

| Component | Implementation | Why |
|---|---|---|
| **Tool Catalog** | GBrain vector DB (pgvector) | Already deployed, zero additional infra |
| **Intent Matcher** | GBrain semantic search | Hybrid vector + keyword + graph |
| **Frustration Detector** | Skill-level pattern matching | Fast, no API call for detection |
| **Subagent Dispatcher** | Hermes `delegate_task` with `toolsets` | Native, supports tool-restricted workers |
| **The Fletcher** | Hermes cron (LLM-driven) | Reads sessions, patches skills, updates catalog |
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
│   └── nightly-learn-prompt.md  # The Fletcher's instructions
└── scripts/
    ├── seed-catalog.py          # One-shot catalog seeder
    ├── sk                       # Dead-simple credential setter
    └── set-credential.py        # Credential validation + storage
```

## Installation

```bash
# 1. Disable broadheads (heavy tools)
hermes tools disable browser session_search code_execution vision \
  image_gen video_gen tts x_search video clarify homeassistant yuanbao

# 2. Filter MCP servers to used-only tools
# Add tools: {include: [...]} to mcp_servers.gbrain and mcp_servers.github in config.yaml

# 3. Install the lazy-tools skill (the Quiver router)
cp skills/lazy-tools/SKILL.md ~/.hermes/skills/devops/lazy-tools/SKILL.md

# 4. Seed the tool catalog in GBrain
python3 scripts/seed-catalog.py

# 5. Create the Fletcher cron
hermes cron create --name lazy-tools-nightly-learn --schedule "0 2 * * *" \
  --skills lazy-tools --toolsets web,terminal,file,skills,delegation \
  --prompt "$(cat crons/nightly-learn-prompt.md)"

# 6. Verify
hermes prompt-size     # bow should be ~37 KB tool schemas, ~22 KB system prompt
hermes tools list      # 8 toolsets enabled, broadheads disabled
```

---

## Limitations

**MCP tool filtering requires gateway restart.** `tools: {include: [...]}` is read
at gateway initialization. After updating the config, reload the gateway.

**Broadheads add latency.** Subagent dispatch takes 5-15 seconds. Worth it for heavy
tools that would otherwise bloat every turn, but noticeably slower than a nocked arrow.

**Frustration detection is keyword-based.** It catches common patterns but may miss
subtle frustration. The fletcher improves this nightly from real session data.

**Not all toolsets can be split.** `file` includes read_file, search_files, write_file,
AND patch. You can't disable patch while keeping read. Toolset granularity is a Hermes
limitation, not a Quiver limitation.

---

## License

MIT — same as Hermes Agent. Quiver is a routing and maintenance pattern, not a platform.
