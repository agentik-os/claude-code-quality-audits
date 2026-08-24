---
name: featureaudit
description: >
  PRD completeness audit. Use when the user wants Ship-readiness, missing capabilities, edge-case gaps.
  Loads the long protocol from audits/featureaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# featureaudit — skill wrapper

## When to use
Ship-readiness, missing capabilities, edge-case gaps.

## When not to use
What to build next (CPO) → retentionaudit.

## Runtime
Claude Code command (`/featureaudit`) **and** Cursor / Grok Bot skill.
Grok Bot hard-caps 50 agents. Stay on the **AGK Audit** face.

## Default posture
READ-ONLY findings. Do not edit the product.
`--fix` is optional, never default, and is a conflict of interest.
Prefer handing `fix-plan.json` to a Builder (Omega `claude|codex|glm`, or Cursor Cloud on CLIENT).
Re-audit is a **fresh session**.

## Tenancy
One tenant per run (`AGK` | `CLIENT` | `LEVERAGE` | `PERSONAL`).
Never load sibling-client secrets. CLIENT never on Omega.
Abort if tenant is unset.

## Recipe
1. Confirm tenant and READ-ONLY (refuse product edits unless `featureaudit` allows `--fix` and the user spelled it).
2. `featureaudit` special cases: `retentionaudit` never edits; `agentaudit` refuses `--fix`; `secaudit`/`agentaudit` never emit exploit PoCs.
3. Read and follow the forensic protocol in `audits/featureaudit.md` (same repo as this skill).
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.featureaudit/`.
6. If findings exist, write a Builder packet. Do not re-audit your own patches in this session.

## Full protocol
See [`audits/featureaudit.md`](../../audits/featureaudit.md).
