---
name: audit-pilot
description: >
  Chooser for the Quality Arsenal. Use when the user says audit-pilot, audit
  my PR, audit the diff, what should I audit before merge, smart audit.
  Maps git diff / PR / ticket to a scored audit set (including agentaudit
  for MCP/skills/harness). Does not apply fixes. One face.
---

# audit-pilot — chooser

## When to use
- Pre-merge / PR / commit / feature description
- "Which audits matter right now?"
- After AGK Review, before running domain audits

## When not to use
- User already named `/secaudit` (run that skill)
- User wants a dashboard → audit-tracker (via quality-arsenal)

## Recipe
1. Tenant lock. CLIENT never on Omega.
2. Build a change profile from git diff / PR / ticket (do not invent files).
3. Score all 19 audits. Include `agentaudit` when MCP, skills, providers.toml,
   session spawn, YOLO, or oracle/worker files change.
4. Freshness debounce via `audits/SYNTHESIS.md` and per-audit `verdict.json`.
5. Emit REQUIRED / RECOMMENDED / SKIP with reasons. Always skip something.
6. Dispatch stays READ-ONLY on the AGK Audit face — do not spawn one chat per audit.
7. Writer-done is not done: Review → this chooser → Audit → Builder → fresh re-audit → Afterwork.

## Full protocol
See [`audits/audit-pilot.md`](../../audits/audit-pilot.md).
