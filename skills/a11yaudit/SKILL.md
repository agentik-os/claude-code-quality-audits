---
name: a11yaudit
description: >
  WCAG 2.2 AA accessibility forensic audit. Use when the user wants keyboard
  navigation, screen-reader checks, contrast, and WCAG 2.2 criteria (focus not
  obscured, target size minimum, accessible authentication). READ-ONLY. Loads
  audits/a11yaudit.md. One AGK Audit face — do not spawn a dedicated chat.
---

# a11yaudit — skill wrapper

## When to use
Keyboard, screen readers, contrast, WCAG 2.2 AA (including 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8).

## When not to use
Visual design only → uiuxaudit.

## Runtime
Claude Code command (`/a11yaudit`) **and** Cursor / Grok Bot skill.
Stay on the **AGK Audit** face.

## Default posture
READ-ONLY findings. Do not edit the product. Apply is a Builder (different agent).
Re-audit is a **fresh session**.

## Tenancy
One tenant per run (`AGK` | `CLIENT` | `LEVERAGE` | `PERSONAL`).
Abort if tenant is unset. CLIENT never on Omega.

## Recipe
1. Confirm tenant.
2. Obey **AGK-AUDIT-OVERRIDE-V2** in the first 100 lines of `audits/a11yaudit.md`.
3. Tools: Read, Glob, Grep only. No Write, Edit, or Bash.
4. Emit `audits/.a11yaudit/` with `mode=readonly`. Builder packet only.

## Full protocol
See [`audits/a11yaudit.md`](../../audits/a11yaudit.md).
