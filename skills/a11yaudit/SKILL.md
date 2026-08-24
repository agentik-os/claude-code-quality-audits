---
name: a11yaudit
description: >
  WCAG 2.2 AA accessibility forensic audit. Use when the user wants Keyboard, screen readers, contrast, 2.
  Loads the long protocol from audits/a11yaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# a11yaudit — skill wrapper

## When to use
Keyboard, screen readers, contrast, 2.2 criteria (focus not obscured, target size, accessible auth).

## When not to use
Visual design only → uiuxaudit.

## Runtime
Claude Code command (`/a11yaudit`) **and** Cursor / Grok Bot skill.
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
2. Obey the **AGK-AUDIT-OVERRIDE-V2** block in the first 100 lines of `audits/a11yaudit.md` before the rest of that file.
3. Tools: Read, Glob, Grep only (plus WebSearch/WebFetch if that body lists them). No Write, Edit, or Bash.
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.a11yaudit/` with `mode=readonly`.
6. Write a Builder packet. Do not apply. Do not re-audit your own patches.


## Full protocol
See [`audits/a11yaudit.md`](../../audits/a11yaudit.md).
