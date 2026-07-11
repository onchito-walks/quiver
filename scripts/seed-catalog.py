#!/usr/bin/env python3
"""Seed the Janus tool catalog in GBrain. Run once after installation.

This script writes the complete tool catalog to GBrain at systems/tool-catalog.
The catalog is a vectorized registry of all Hermes tools — enabled AND disabled —
used by the Janus router for semantic intent-to-tool matching.

Prerequisites:
    - GBrain running and accessible via MCP
    - Hermes tools configured (hermes tools list)

Usage:
    python3 seed-catalog.py
"""

CATALOG_SLUG = "systems/tool-catalog"

CATALOG_CONTENT = """---
type: catalog
tags: [tools, lazy-loading, tool-catalog, janus]
---

# Tool Catalog — Complete Registry for Janus Router

All available Hermes Agent tools, including disabled ones. Used by the Janus router
to semantically match user intent to the right toolset. Query this page to find
which tools handle a task.

## Active Tools (always loaded in default session)

- **web**: Web search and content extraction via SearXNG, Tavily, web_extract
- **terminal**: Shell command execution, background processes, PTY support
- **file**: File read, write, search (ripgrep-backed), patch (fuzzy matching)
- **code_execution**: Python scripting with tool access for multi-step logic
- **vision**: Image analysis, OCR, screenshot interpretation
- **skills**: Skill management — create, load, patch, delete skills
- **todo**: Task planning and tracking across complex multi-step work
- **memory**: Persistent memory across sessions, injected into every turn
- **session_search**: FTS5-backed search over past conversation history
- **clarify**: User clarification questions with multiple-choice support
- **delegation**: Subagent spawning with custom toolsets, parallel batch mode
- **cronjob**: Scheduled job management — create, list, update, pause, remove
- **gbrain_mcp**: GBrain knowledge base — query, pages, facts, graph, search, recall

## Lazy Tools (disabled by default, loaded via Janus subagent delegation)

### browser

**Description:** Full browser automation: navigate to URLs, click elements identified
by ref IDs, fill forms, take screenshots with visual annotation, extract page content
as markdown, scroll pages, read the JavaScript console, analyze visual page state with
vision integration. Use when the user wants to visit a website, scrape a page that
requires JavaScript rendering, take a screenshot of a web page, interact with web forms,
or inspect visual elements that text extraction can't capture.

**Tools count:** 10 (navigate, click, snapshot, scroll, type, press, back, console,
get_images, vision)

**User says:** "go to", "open this", "visit", "browse", "screenshot", "navigate to",
"scrape this page", "show me the website", "what does this page say", "click on",
"fill out the form", "login to", "check this URL", "look at this site"

**Frustration signals:** "why can't you open", "just go to the website", "i need you
to browse", "can't you just look at", "open this url", "visit this link", "go to
this page", "check the website"

### image_gen

**Description:** Generate high-quality images from text prompts (text-to-image) or
edit/transform existing images (image-to-image). Supports aspect ratios (landscape,
square, portrait), reference images for style/composition guidance. Backend is
user-configured (FAL.ai, OpenAI, xAI). Use when user asks to create, generate, or
make an image, illustration, artwork, or visual concept.

**Tools count:** 1

**User says:** "generate an image", "create a picture", "make an image of",
"draw me", "illustrate", "visualize this concept", "design a", "render a"

**Frustration signals:** "generate an image of", "can you make art", "create a
picture", "why can't you draw", "make me a visual"

### video_gen

**Description:** Generate videos from text prompts (text-to-video) or animate still
images (image-to-video). Supports duration (1-15s), aspect ratios (16:9, 9:16, 1:1),
resolution (up to 1080p), and optional audio. Use when user asks to create, generate,
or make a video, animation, or motion visual.

**Tools count:** 1

**User says:** "generate a video", "create a video", "make a video of", "animate
this", "video of", "turn this into a video"

**Frustration signals:** "make a video", "create an animation", "generate video of",
"can you animate"

### tts

**Description:** Convert text to speech audio. Multiple voice providers supported
(OpenAI, xAI, ElevenLabs, Edge). Use when user asks to read text aloud, speak
something, or convert text to audio format.

**Tools count:** 1

**User says:** "read this aloud", "speak this", "text to speech", "say this",
"read it to me", "convert to audio", "narrate this"

**Frustration signals:** "read it out loud", "can you speak", "say something",
"why can't you read this"

### x_search

**Description:** Search X/Twitter for tweets, trends, and user posts. Use when user
asks about what's happening on X/Twitter, wants to search for tweets, find someone's
posts, or check trending topics.

**Tools count:** 1

**User says:** "search twitter", "what's on x", "find tweets about", "check X for",
"what are people saying on twitter", "search for @", "trending on twitter"

**Frustration signals:** "search twitter for", "check X", "what's trending on",
"find this tweet", "look up on twitter"

### video

**Description:** Analyze video files from URLs or local paths using multimodal AI.
Extract descriptions, answer questions about video content. Supports mp4, webm,
mov, avi, mkv, mpeg. Use when user shares a video and asks about its contents
or wants analysis of visual media.

**Tools count:** 1

**User says:** "analyze this video", "what's in this video", "watch this",
"describe this video", "summarize this clip"

**Frustration signals:** "analyze this video", "look at this video", "what's
in this clip", "can you watch"

### github_mcp

**Description:** GitHub API access: search code across repositories, list and create
issues, search issues and pull requests, list commits, fork repositories, get pull
request details. Note: MCP tools can't be delegated to subagents directly. For
subagent-based GitHub access, use terminal with gh CLI or curl + GITHUB_TOKEN.

**Tools count:** 8 (search_code, list_issues, create_issue, get_issue, list_pull_requests,
get_pull_request, search_issues, list_commits, fork_repository)

**User says:** "search github for", "find the issue", "check the PR", "github repo",
"create an issue for", "fork this repo", "list commits on", "search code on github"

**Frustration signals:** "search github for", "find this on github", "check that
repo", "why can't you search github", "look up the issue"

### hermes_trailhead

**Description:** Hermes-native hard-source research tool. Searches all source terrain
(web, X/Twitter, Reddit, TikTok, Instagram, YouTube, GitHub, forums/docs), extracts
summaries/transcripts/metadata, scores source quality, and reports caveats. Use when
research needs practitioner/social/current/hard-source evidence instead of generic web only.

**Command:** `hermes-trailhead search all "query" --execute --extract --score --format json`

**User says:** "search trailhead", "use Trailhead", "hard-source research", "what are
people saying", "social/practitioner evidence", "search all lanes", "prove it online"

**Frustration signals:** "why didn't you use trailhead", "this research is weak",
"you missed Reddit/X/GitHub", "search the whole internet", "none of your solutions work"

### quiver_cli

**Description:** Local Quiver integration manager. Verifies and repairs Hermes lazy-tool
state: GBrain tool catalog, lazy-tools skill, broadhead disablement, light-head enablement,
prompt budget, nightly fletcher cron, and Trailhead reachability.

**Command:** `quiver doctor` / `quiver repair --apply`

**User says:** "does Hermes know about Quiver", "is Quiver installed", "why are tools missing",
"token bloat", "keep the functions but lighten tokens", "tool catalog", "fletcher"

**Frustration signals:** "I thought Quiver helped", "can't you search/use tools", "why don't
you know about my tools", "did you forget GBrain/Quiver"

## Routing Logic

### Standard delegation flow

1. User asks for something that needs a disabled tool
2. Agent queries this catalog via GBrain semantic search
3. Matching toolset identified by description similarity to user intent
4. Subagent spawned with exact toolsets needed: delegate_task(toolsets=[toolset, "web"])
5. Subagent returns results to user

### Frustration detection flow

1. User expresses frustration ("can't", "won't", "broken", "why", "fix this")
2. Agent IMMEDIATELY queries this catalog — do not apologize, do not explain
3. Match user's blocked task to the closest toolset
4. Spawn subagent without asking permission
5. Report: "Found the right tool. Spinning up a [toolset] subagent now..."

### Promotion threshold

If a disabled tool is requested via subagent delegation more than 3 times in a
single day for 3 consecutive days, the nightly learner recommends re-enabling it
globally. The tool has proven it belongs in the default session.
"""

if __name__ == "__main__":
    print(f"This script seeds GBrain with the Janus tool catalog at '{CATALOG_SLUG}'.")
    print("Run this through a Hermes session with GBrain MCP access, or use:")
    print(f"  mcp__gbrain__put_page(slug='{CATALOG_SLUG}', content=...)")
    print()
    print("Catalog content length:", len(CATALOG_CONTENT), "chars")
