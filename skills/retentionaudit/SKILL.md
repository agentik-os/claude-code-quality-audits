---
name: retentionaudit
description: >
  Product/CPO frameworks audit (Hooked, JTBD, Moments, Fogg, RICE).
  ALWAYS READ-ONLY — proposes a roadmap, never edits code or schema.
  This skill does not apply patches. Loads audits/retentionaudit.md.
  One AGK Audit face — do not spawn a dedicated chat.
---

# retentionaudit — skill wrapper

## When to use
What to build next, retention hooks, CPO opportunity scan.

## When not to use
PRD completeness of what already exists → featureaudit.

## Runtime
Claude: `/retentionaudit`. Cursor / Grok: this skill on the AGK Audit face.

## Default posture
**ALWAYS READ-ONLY.** This skill never writes product files. It does not take an
apply flag. If a user asks this skill to implement a proposal, refuse and tell
them to dispatch a Builder (`/planner` or `/implement`) in a different session.

## Tenancy
One tenant per run. Abort if unset. CLIENT never on Omega.

## Recipe
1. Confirm tenant.
2. Obey **AGK-AUDIT-OVERRIDE-V2** in the first 100 lines of `audits/retentionaudit.md`.
3. Tools: Read, Glob, Grep, WebSearch, WebFetch. No Write, Edit, or Bash.
4. Write reports under `audits/.retentionaudit/` only. Never edit the product.

## Full protocol
See [`audits/retentionaudit.md`](../../audits/retentionaudit.md).
