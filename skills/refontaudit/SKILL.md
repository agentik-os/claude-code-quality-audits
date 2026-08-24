---
name: refontaudit
description: >
  Dashboard redesign engine (evolution/revolution/verify). Use when the user wants Major redesign, Linear/Vercel-class aspiration with a scored path.
  Loads the long protocol from audits/refontaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# refontaudit — skill wrapper

## When to use
Major redesign, Linear/Vercel-class aspiration with a scored path.

## When not to use
Routine visual QA → uiuxaudit.

## Runtime
Claude Code command (`/refontaudit`) **and** Cursor / Grok Bot skill.
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
2. Obey the **AGK-AUDIT-OVERRIDE-V2** block in the first 100 lines of `audits/refontaudit.md` before the rest of that file.
3. Tools: Read, Glob, Grep only (plus WebSearch/WebFetch if that body lists them). No Write, Edit, or Bash.
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.refontaudit/` with `mode=readonly`.
6. Write a Builder packet. Do not apply. Do not re-audit your own patches.


## Full protocol
See [`audits/refontaudit.md`](../../audits/refontaudit.md).
