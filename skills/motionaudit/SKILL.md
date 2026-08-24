---
name: motionaudit
description: >
  Animation / motion-DNA audit. ABORTS on non-UI. Use when the user wants Transitions, easing, reduced-motion.
  Loads the long protocol from audits/motionaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# motionaudit — skill wrapper

## When to use
Transitions, easing, reduced-motion.

## When not to use
CLI/library → skip.

## Runtime
Claude Code command (`/motionaudit`) **and** Cursor / Grok Bot skill.
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
1. Confirm tenant and READ-ONLY (refuse product edits unless `motionaudit` allows `--fix` and the user spelled it).
2. `motionaudit` special cases: `retentionaudit` never edits; `agentaudit` refuses `--fix`; `secaudit`/`agentaudit` never emit exploit PoCs.
3. Read and follow the forensic protocol in `audits/motionaudit.md` (same repo as this skill).
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.motionaudit/`.
6. If findings exist, write a Builder packet. Do not re-audit your own patches in this session.

## Full protocol
See [`audits/motionaudit.md`](../../audits/motionaudit.md).
