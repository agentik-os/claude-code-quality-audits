---
name: retentionaudit
description: >
  Product/CPO frameworks audit. ALWAYS READ-ONLY — ignores --fix. Use when the user wants What to build next, Hooked/JTBD/Moments/Fogg, RICE.
  Loads the long protocol from audits/retentionaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# retentionaudit — skill wrapper

## When to use
What to build next, Hooked/JTBD/Moments/Fogg, RICE.

## When not to use
PRD completeness of what exists → featureaudit.

## Runtime
Claude Code command (`/retentionaudit`) **and** Cursor / Grok Bot skill.
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
1. Confirm tenant and READ-ONLY (refuse product edits unless `retentionaudit` allows `--fix` and the user spelled it).
2. `retentionaudit` special cases: `retentionaudit` never edits; `agentaudit` refuses `--fix`; `secaudit`/`agentaudit` never emit exploit PoCs.
3. Read and follow the forensic protocol in `audits/retentionaudit.md` (same repo as this skill).
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.retentionaudit/`.
6. If findings exist, write a Builder packet. Do not re-audit your own patches in this session.

## Full protocol
See [`audits/retentionaudit.md`](../../audits/retentionaudit.md).
