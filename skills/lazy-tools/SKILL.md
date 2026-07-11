---
name: lazy-tools
description: How to access browser, media generation, and other disabled-by-default tools via subagent delegation. Tools are off to save tokens but available on demand. Includes frustration detection — when user is upset that something doesn't work, automatically find the right disabled tool and delegate.
triggers:
  - "open a browser"
  - "go to this URL"
  - "take a screenshot"
  - "navigate to"
  - "generate an image"
  - "generate a video"
  - "text to speech"
  - "search X/Twitter"
  - "need the browser"
  - "scrape this page"
  - "search past conversations"
  - "find that session"
  - "what did we discuss"
  - "run this analysis"
  - "process this data"
  - "multi-step script"
  - "search github"
  - "can't you just"
  - "why won't"
  - "this is broken"
  - "quiver"
  - "reach for skills"
  - "get tools"
---

# Lazy Tools — Self-Learning Tool Router

## Why tools are disabled

Active session runs with 8 toolsets (15 tools, 36.9 KB) — down from 33 tools (61.6 KB).
Disabled toolsets: browser (10 tools), session_search, code_execution, image_gen, video_gen,
tts, x_search, video, vision, clarify. Total savings: ~25 KB (~6,200 tokens) per turn.

## The Tool Catalog (source of truth)

All tools — enabled AND disabled — are cataloged in GBrain at `systems/tool-catalog`.
This page contains:
- Rich descriptions of every tool (for semantic matching)
- Trigger phrases (what users say when they need each tool)
- Frustration signals (what users say when a missing tool blocks them)

**ALWAYS query GBrain for `systems/tool-catalog` before telling the user "I can't do that."**
The tool you need is probably in the catalog.

## Frustration Detection (CRITICAL — do this first)

When the user expresses ANY of these signals, they are FRUSTRATED because a tool is missing:

**Keywords:** "can't", "won't", "broken", "why", "fix this", "doesn't work", "useless",
"what the hell", "come on", "seriously", "again", "still not working", "ffs"

**Patterns:**
- "why can't you just..." → they want a tool you don't have loaded
- "this is broken" → something that should work isn't
- "fix this" → immediate action required
- "i need you to..." followed by a tool-specific task → find the tool
- Any message with visible anger/frustration + a blocked task

**IMMEDIATE RESPONSE TO FRUSTRATION:**

1. DO NOT apologize or explain why you can't do it
2. DO NOT ask the user to do anything
3. IMMEDIATELY query GBrain: `mcp__gbrain__query("what tool handles: <user's blocked task>")`
4. Also query: `mcp__gbrain__get_page(slug="systems/tool-catalog")` to check the catalog
5. If a matching lazy tool is found, spawn a subagent with that toolset
6. Tell the user: "Found the right tool. Spinning up a <toolset> subagent now..."
7. The subagent returns results directly

**Example:**
```
User: "why can't you just go to the website and check?"
Agent: [DETECTS FRUSTRATION]
       → gbrain_query("browser automation tool for navigating websites")
       → Found: browser toolset
       → delegate_task(goal="Navigate to website and check...", toolsets=["browser", "web"])
       → "Found the browser tools. Checking the website now..."
```

## Quiver / Trailhead install awareness

Quiver is now a first-class Hermes companion with a local CLI:

```bash
quiver doctor
quiver status --json
quiver install --apply
quiver repair --apply
```

Use `quiver doctor` whenever the user asks whether Hermes still knows about lazy tools, GBrain tool catalog, tool budget, or the nightly fletcher. It verifies: active Hermes command, GBrain catalog `systems/tool-catalog`, installed `lazy-tools` skill, nightly `lazy-tools-nightly-learn` cron, tool enable/disable shape, prompt/tool schema budget, and Trailhead reachability.

Trailhead is the hard-source research capability. It now has a PATH wrapper:

```bash
hermes-trailhead doctor
hermes-trailhead search all "query" --execute --extract --score --limit 3 --extract-limit 3 --format json
```

Quiver is above Trailhead: Quiver chooses the head/capability; Trailhead performs research when selected by `search-routing`.

## Standard Delegation (non-frustration path)

When the user calmly asks for something that needs a disabled tool:

1. Query GBrain catalog: `mcp__gbrain__get_page(slug="systems/tool-catalog")`
2. Match the user's intent to the right toolset
3. Spawn a subagent: `delegate_task(goal="...", toolsets=["<toolset>", "web"])`
4. Do NOT ask the user "should I enable browser tools?" — just do it

### Toolset → Subagent mapping

| Toolset | delegate_task toolsets |
|---|---|
| browser | ["browser", "web"] |
| session_search | ["session_search"] |
| code_execution | ["code_execution", "terminal"] |
| image_gen | ["image_gen"] |
| video_gen | ["video_gen"] |
| tts | ["tts"] |
| x_search | ["x_search", "web"] |
| video | ["video"] |
| vision | ["vision"] |
| clarify | ["clarify"] |
| github_mcp | ["web", "terminal"] — use gh CLI or curl, MCP tools are for the main session only |

### GitHub MCP note

GitHub MCP tools (mcp__github__*) are MCP-mounted and can't be passed to subagents via toolsets.
Instead, for GitHub tasks, spawn a subagent with terminal access and use `gh` CLI or `curl`
with the GitHub token from the environment. The subagent should use `terminal` commands:
- `gh issue list` / `gh pr list`
- `curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/...`

## Nightly Learning

A cron job (`quiver-fletcher-nightly`, ID `03bf4d9f9a73`) runs daily at 02:00 UTC. It:
1. Reads the day's session transcripts
2. Identifies patterns: which disabled tools were actually needed, which trigger phrases worked
3. Patches this skill with new trigger phrases and better toolset mappings
4. Patches `systems/tool-catalog` in GBrain with updated descriptions
5. If a tool is requested >3 times in a day, logs a recommendation to re-enable it

## Re-enabling globally

If a tool is requested frequently enough, re-enable it:
```bash
hermes tools enable browser
```

## Verification

After any tool delegation:
- Check that the subagent actually produced results
- If the subagent failed, try a different approach before reporting failure
- Subagent summaries are self-reports — verify critical results

## PITFALL — Proactive skill loading (the "reach for skills" rule)

When the user mentions a system, tool, or workflow by name (\"Quiver\", \"Trailhead\", \"LEVIATHAN routing\", \"oracle arm\", \"GBrain MCP\"), you MUST load the relevant skill BEFORE claiming inability or starting work. The user built these tools to make you more capable — ignoring them and working blind is the fastest path to frustration. If a task touches infrastructure, load `oracle-arm-architecture`. If it touches disk layout, search GBrain for existing pages before creating new ones. The user shouldn't have to say \"i thought we had quiver installed\" — that's a failure signal that means you worked without the right skill loaded.

## PITFALL — Quiver/GBrain frustration requires immediate proof, not explanation

If the user challenges whether you have GBrain, search, or Quiver access (for example: \"do you not have gbrain access\", \"i thought quiver helped\", \"aren't you searching\"), treat it as a workflow correction. Do not answer from memory and do not defend the previous step. Immediately verify the available lane:

1. Load this skill plus the relevant search/GBrain skill (`search-routing`, `gbrain-think`, or Hermes troubleshooting skill as applicable).
2. Query GBrain/tool catalog first. Prefer MCP tools when mounted; if native MCP tools are not exposed in the current session, use the `gbrain` CLI in terminal (`gbrain version`, `gbrain get systems/tool-catalog`, targeted `gbrain query ...`).
3. Report raw proof of access briefly, then state the process correction: GBrain first, then runtime/filesystem verification.
4. Continue the task using that order. Do not turn a missing convenience wrapper or PATH issue into \"Quiver is broken\"; Quiver may still be functioning as skills + GBrain catalog + cron-maintained doctrine even without a direct CLI command.

## PITFALL — MCP tool filtering requires gateway restart

GBrain and GitHub MCP servers use `tools: {include: [...]}` in config.yaml to filter
which tools are available. This is how we reduced GBrain from 85 tools to 25. However,
MCP tool lists are loaded at gateway initialization. After updating the include list
in config.yaml, the gateway must be reloaded for changes to take effect. The session
continues to see the OLD tool list until the gateway reconnects MCP servers.

Detection: `hermes prompt-size` shows the same tool count before and after config change.
Fix: gateway restart or MCP server reload (happens automatically on next gateway cycle).
## Subagent Model Routing — Always Cheapest Available

Quiver subagents must use the cheapest available model at dispatch time.
Never hardcode a provider. Check OmniRoute health before every dispatch.

### Routing decision (in order):

1. **OmniRoute `auto/best-fast` — FREE** (if healthy)
   - Check: `curl -s --max-time 3 http://127.0.0.1:20128/v1/models | grep -q auto/best-fast`
   - If OmniRoute responds → use it. Cost: $0.00

2. **DeepSeek V4 Flash — $0.14/M** (always available fallback)
   - Provider: `api.deepseek.com`, model: `deepseek-v4-flash`

3. **NEVER OpenAI Codex for subagents** — burns subscription quota

### Dispatch pattern:

Before every delegate_task, run the health check. If OmniRoute passes:
  delegate_task(goal="...", toolsets=["browser","web"], model="auto/best-fast", provider="omniroute-local")
If OmniRoute fails:
  delegate_task(goal="...", toolsets=["browser","web"], model="deepseek-v4-flash", provider="api.deepseek.com")

The health check adds ~1 second. Worth it for free subagents.
If the user says "use Flash" or "don't use OmniRoute," skip the check and go direct.
