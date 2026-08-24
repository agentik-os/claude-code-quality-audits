---
name: debugaudit
description: >
  Runtime bug hunter. Use when the user wants Console errors, broken features, smoke after dependency bumps.
  Loads the long protocol from audits/debugaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# debugaudit — skill wrapper

## When to use
Console errors, broken features, smoke after dependency bumps.

## When not to use
Architecture debt → codeaudit.

## Runtime
Claude Code command (`/debugaudit`) **and** Cursor / Grok Bot skill.
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
1. Confirm tenant and READ-ONLY (refuse product edits unless `debugaudit` allows `--fix` and the user spelled it).
2. `debugaudit` special cases: `retentionaudit` never edits; `agentaudit` refuses `--fix`; `secaudit`/`agentaudit` never emit exploit PoCs.
3. Read and follow the forensic protocol in `audits/debugaudit.md` (same repo as this skill).
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.debugaudit/`.
6. If findings exist, write a Builder packet. Do not re-audit your own patches in this session.

## Full protocol
See [`audits/debugaudit.md`](../../audits/debugaudit.md).
