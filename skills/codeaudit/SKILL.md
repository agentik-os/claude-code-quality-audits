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
There is **no `--fix` path** on AGK Audit. Apply requires a **different agent**
(Builder: Omega `claude|codex|glm`, or Cursor Cloud on CLIENT).
Re-audit is a **fresh session**.


## Tenancy
One tenant per run (`AGK` | `CLIENT` | `LEVERAGE` | `PERSONAL`).
Never load sibling-client secrets. CLIENT never on Omega.
Abort if tenant is unset.

## Recipe
1. Confirm tenant. Abort if unset. CLIENT never on Omega.
2. Obey the **AGK-AUDIT-OVERRIDE-V2** block in the first 100 lines of `audits/codeaudit.md` before the rest of that file.
3. Tools: Read, Glob, Grep only (plus WebSearch/WebFetch if that body lists them). No Write, Edit, or Bash.
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.codeaudit/` with `mode=readonly`.
6. Write a Builder packet. Do not apply. Do not re-audit your own patches.


## Full protocol
See [`audits/codeaudit.md`](../../audits/codeaudit.md).
