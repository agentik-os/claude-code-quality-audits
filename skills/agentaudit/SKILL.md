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
- Cron reliability without an agent harness → `automationaudit`

## Runtime
Claude: `/agentaudit`. Cursor / Grok: this skill on the **AGK Audit** face.
Grok Bot hard-caps 50 agents. Do not spawn a dedicated auditor chat.

## Default posture
**Always READ-ONLY.** This skill **refuses `--fix`.** Hand `fix-plan.json` to a Builder.
Re-audit in a **fresh session**. RED: findings + evidence + impact + rec only.

## Tenancy
One tenant per run. Never load sibling-client secrets. CLIENT never on Omega.
Abort if tenant is unset.

## Recipe
1. Tenant lock. Abort if CLIENT is on Omega.
2. Read and follow `audits/agentaudit.md`.
3. Inventory only — no live injection, no exfil demonstration.
4. Map findings to ASI01–ASI10 / LLM01–LLM10 when an official ID exists.
5. Label `tool-backed` | `llm-judgment` | `inventory-only`.
6. Emit `audits/.agentaudit/` 8-file contract with `mode=readonly`.

## Full protocol
See [`audits/agentaudit.md`](../../audits/agentaudit.md).
