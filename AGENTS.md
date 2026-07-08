# Quiver AGENTS.md — Agent Context Rules

When Quiver is active, these rules govern every session.

## Tool Philosophy

This session runs with a minimal toolset. Browser, image generation, video generation,
text-to-speech, X/Twitter search, and video analysis tools are DISABLED by default.
They are available on demand through Quiver subagent delegation.

**Never tell the user "I can't do that because browser tools are disabled."**
Instead, query the tool catalog and dispatch a subagent.

## Frustration Detection (ALWAYS ACTIVE)

If the user's message contains frustration signals ("can't", "won't", "broken",
"why", "fix this", "doesn't work", "useless", "what the hell", "come on",
"seriously", "ffs") AND describes a task that requires a tool, IMMEDIATELY:

1. Query GBrain: mcp__gbrain__query("what tool handles: <user's task>")
2. Also check: mcp__gbrain__get_page(slug="systems/tool-catalog")
3. Spawn a subagent with the matching toolset
4. Report: "Found the right tool. Handling this now..."

Do NOT apologize. Do NOT explain why the tool isn't loaded. Just dispatch.

## Standard Delegation

When the user calmly asks for something needing a disabled tool:

1. Query the tool catalog in GBrain
2. Match intent to toolset
3. Spawn subagent: delegate_task(goal="...", toolsets=[toolset, "web"])
4. Return results

## Toolset Reference

| User wants | Delegate with toolsets |
|---|---|
| Browse a website, take screenshot | ["browser", "web"] |
| Generate an image | ["image_gen"] |
| Generate a video | ["video_gen"] |
| Text to speech | ["tts"] |
| Search X/Twitter | ["x_search", "web"] |
| Analyze a video | ["video"] |
| GitHub operations | ["terminal", "web"] (use gh CLI or curl) |

## Nightly Improvement

A cron job runs at 02:00 UTC and analyzes session history. It patches the
lazy-tools skill and tool catalog based on real usage patterns. The system
improves every 24 hours without manual intervention.
