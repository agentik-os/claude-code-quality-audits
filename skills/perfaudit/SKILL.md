---
name: perfaudit
description: >
  Core Web Vitals + bundle + N+1 audit. Use when the user wants Slow site, Lighthouse, import weight, query amplification.
  Loads the long protocol from audits/perfaudit.md. Default READ-ONLY.
  One AGK Audit face — do not spawn a dedicated chat for this audit.
---

# perfaudit — skill wrapper

## When to use
Slow site, Lighthouse, import weight, query amplification.

## When not to use
SEO ranking narrative → seoaudit (reads this verdict).

## Runtime
Claude Code command (`/perfaudit`) **and** Cursor / Grok Bot skill.
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
2. Obey the **AGK-AUDIT-OVERRIDE-V2** block in the first 100 lines of `audits/perfaudit.md` before the rest of that file.
3. Tools: Read, Glob, Grep only (plus WebSearch/WebFetch if that body lists them). No Write, Edit, or Bash.
4. Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.
5. Emit the 8-file output contract under `audits/.perfaudit/` with `mode=readonly`.
6. Write a Builder packet. Do not apply. Do not re-audit your own patches.


## Full protocol
See [`audits/perfaudit.md`](../../audits/perfaudit.md).
