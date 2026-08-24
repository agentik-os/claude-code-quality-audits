---
name: uiuxaudit
description: >
  Design-coherence forensic audit. Use when the user wants Visual consistency, design system, pixel/spacing drift.
  Loads the long protocol from audits/uiuxaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# uiuxaudit — skill wrapper

## When to use
Visual consistency, design system, pixel/spacing drift.

## When not to use
Accessibility law → a11yaudit. Journeys → flowaudit.

## Runtime
Claude Code command (`/uiuxaudit`) **and** Cursor / Grok Bot skill.
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
1. Confirm tenant and READ-ONLY (refuse product edits unless `uiuxaudit` allows `--fix` and the user spelled it).
2. `uiuxaudit` special cases: `retentionaudit` never edits; `agentaudit` refuses `--fix`; `secaudit`/`agentaudit` never emit exploit PoCs.
3. Read and follow the forensic protocol in `audits/uiuxaudit.md` (same repo as this skill).
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.uiuxaudit/`.
6. If findings exist, write a Builder packet. Do not re-audit your own patches in this session.

## Full protocol
See [`audits/uiuxaudit.md`](../../audits/uiuxaudit.md).
