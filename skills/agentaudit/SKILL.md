---
name: agentaudit
description: >
  Harness / orchestration / MCP / injection / tenancy forensic audit.
  Use when reviewing agent runtimes, MCP supply chain, YOLO or approval
  gates, empty-pane / session_id-null spawn, confused-deputy A2A, memory
  poisoning, evals/judges as gates, or AGK/CLIENT/LEVERAGE/PERSONAL isolation.
  Always READ-ONLY. Never emit exploit PoCs. One AGK Audit face.
---

# agentaudit — skill wrapper

## When to use
- MCP servers, `providers.toml`, skills, oracle/worker spawn paths
- Prompt injection via repos or tool output (untrusted fences)
- Tenant isolation, YOLO, judges that do not actually gate merge

## When not to use
- Product HTTP / classic OWASP → `secaudit`

## Runtime
Claude: `/agentaudit`. Cursor / Grok: this skill on the **AGK Audit** face.

## Default posture
**Always READ-ONLY.** No `--fix` path. Hand `fix-plan.json` to a Builder.
Re-audit in a **fresh session**. RED: findings + evidence + impact + rec only.

## Tenancy
One tenant per run. Never load sibling-client secrets. CLIENT never on Omega.

## Recipe
1. Tenant lock. Abort if CLIENT is on Omega.
2. Obey AGK-AUDIT-OVERRIDE-V2 then follow `audits/agentaudit.md`.
3. Inventory only — no live injection, no exfil demonstration.
4. Emit `audits/.agentaudit/` with `mode=readonly`.

## Full protocol
See [`audits/agentaudit.md`](../../audits/agentaudit.md).
