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
  - "search github"
  - "can't you just"
  - "why won't"
  - "this is broken"
  - "fix this"
---

# Lazy Tools — Self-Learning Tool Router

## Why tools are disabled

Browser (10 tools, ~18KB), image generation, video generation, text-to-speech, X/Twitter search,
video analysis, and GitHub MCP are disabled globally to save ~13.7 KB (~3,400 tokens) per turn.
The tools still exist — they're just not loaded into the default session context.

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
| image_gen | ["image_gen"] |
| video_gen | ["video_gen"] |
| tts | ["tts"] |
| x_search | ["x_search", "web"] |
| video | ["video"] |
| github_mcp | ["web", "terminal"] — use gh CLI or curl, MCP tools are for the main session only |

### GitHub MCP note

GitHub MCP tools (mcp__github__*) are MCP-mounted and can't be passed to subagents via toolsets.
Instead, for GitHub tasks, spawn a subagent with terminal access and use `gh` CLI or `curl`
with the GitHub token from the environment. The subagent should use `terminal` commands:
- `gh issue list` / `gh pr list`
- `curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/...`

## Nightly Learning

A cron job (`lazy-tools-nightly-learn`) runs daily at 02:00 UTC. It:
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
