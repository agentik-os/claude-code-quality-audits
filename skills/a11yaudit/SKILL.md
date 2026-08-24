---
name: a11yaudit
description: >
  WCAG 2.2 AA accessibility forensic audit covering keyboard navigation,
  screen readers, contrast, and the WCAG 2.2 criteria 2.4.11 Focus Not
  Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size (Minimum),
  3.2.6 Consistent Help, 3.3.7 Redundant Entry, and 3.3.8 Accessible
  Authentication. READ-ONLY. Loads audits/a11yaudit.md. One AGK Audit
  face — do not spawn a dedicated chat.
---

# a11yaudit — skill wrapper

## When to use
WCAG 2.2 AA: keyboard, screen readers, contrast, plus 2.4.11 Focus Not
Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size (Minimum),
3.2.6 Consistent Help, 3.3.7 Redundant Entry, and 3.3.8 Accessible Authentication.

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
