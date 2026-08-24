---
name: quality-arsenal
description: >
  AGK Audit face / router for the Quality Arsenal. Use when the user says
  audit, quality-arsenal, AGK Audit, qa, full audit, go-live, or is unsure
  which protocol to run. Routes to audit-pilot (chooser) and individual
  audit skills. Default READ-ONLY. Do not spawn 18 auditor chats.
---

# quality-arsenal — AGK Audit face

## When to use
- User wants "an audit" without naming a domain
- Init / dashboard / full / go-live presets
- You are the single face agent loading this pack

## When not to use
- A specific domain is already named → load that audit skill directly
- User asked which audits this PR needs → `audit-pilot`

## Runtime
Claude: `/quality-arsenal`. Cursor / Grok: this skill is the face.
Grok Bot hard-caps 50 agents. One face + skills, not 19 auditor bots.

## Recipe
1. Lock tenant (`--tenant` or `AGK_TENANT`). CLIENT → no Omega workers.
2. Default READ-ONLY. `--fix` only if the human spelled it.
3. No args → menu: pilot / orchestrator / tracker init / help.
4. `pr` / `diff` / `pilot` → Read `audits/audit-pilot.md` (or the `audit-pilot` skill).
5. Named audit → Read `audits/<id>.md` via that skill wrapper.
6. `full` / `go-live` → waves from `audits/quality-arsenal.md`. Stay in-process.
7. After verdicts: SYNTHESIS.md + Afterwork packet. Writer-done is not done.
8. AGK loop: Review (fresh) THEN this Audit THEN Afterwork.

## Full protocol
See [`audits/quality-arsenal.md`](../../audits/quality-arsenal.md).
