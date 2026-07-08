---
name: research-methodology
description: Primary sources first, exhaustive queries, triangulation, transparent accounting. Load when doing any non-trivial research.
triggers:
  - research
  - look up
  - find information
  - deep search
  - study this
  - investigate
---

# Research Methodology

## Primary sources first

Hermes official docs, Nous Research GitHub, Anthropic engineering blog, arxiv, official
model docs. Search engines fill gaps AFTER primary sources are exhausted. SEO blogs are
pointers, not sources.

## Exhaustive query variation

Reframe the question multiple ways until new queries stop returning new information
(saturation). Never single-pass. Judge by whether queries still surface new info,
not by query count.

## Extract what matters

Judge each result by title + snippet before extracting. Extract in full if it could
plausibly contain the answer. Skip clear noise. Be transparent about what was skipped.

## Triangulate

Minimum 3 independent sources confirming each finding. Single-sourced findings must be
flagged as unverified. Triangulated = 3+ sources from different domains (academic +
industry + practitioner).

## Transparent accounting

Every conclusion includes methodology: "12 queries, 145 results, 14 pages extracted,
3 primary sources, 2 Reddit threads, 1 X discussion." Never elide counts.

## Cross-source simultaneously

Web search, Reddit, and X/Twitter in the same round, not sequentially. Practitioner
discussion on social platforms covers what official docs don't. A maintainer's X post
about a bug is primary source material.

## Response depth — anti-shallow guard

- When analysis is called for: explanatory paragraphs with visible reasoning, not bullets.
- "Comprehensive" = depth, failure modes, counterarguments, decision flow. Not more items.
- Shallow response → change FORMAT (paragraphs, visible reasoning), not more bullets.
- Never optimize "don't break anything" over "think deeply."

## Crawl policy

Crawl only when user says "crawl" or gives a bounded domain/path. Shallow first,
no external links. Deep research = better search + source selection + synthesis — not crawl.
