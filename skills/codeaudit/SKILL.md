---
name: codeaudit
description: >
  Forensic code-architecture audit (Gestalt-Popper). Use when the user wants Refactor, technical debt, phantom deps, AI-generated maintainability.
  Loads the long protocol from audits/codeaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# codeaudit — skill wrapper

## When to use
Refactor, technical debt, phantom deps, AI-generated maintainability.

## When not to use
Security exploit review → secaudit / agentaudit. Runtime bugs → debugaudit.

## Runtime
Claude Code command (`/codeaudit`) **and** Cursor / Grok Bot skill.
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
1. Confirm tenant and READ-ONLY (refuse product edits unless `codeaudit` allows `--fix` and the user spelled it).
2. `codeaudit` special cases: `retentionaudit` never edits; `agentaudit` refuses `--fix`; `secaudit`/`agentaudit` never emit exploit PoCs.
3. Read and follow the forensic protocol in `audits/codeaudit.md` (same repo as this skill).
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.codeaudit/`.
6. If findings exist, write a Builder packet. Do not re-audit your own patches in this session.

## Full protocol
See [`audits/codeaudit.md`](../../audits/codeaudit.md).
