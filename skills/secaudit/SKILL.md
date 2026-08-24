---
name: secaudit
description: >
  Product-surface security audit (OWASP Top 10 2021 web + OWASP LLM Top 10
  2025 in-app). Use for pre-prod, payment, auth, secrets, in-app MCP.
  READ-ONLY. Never emit exploit PoCs. Harness/YOLO/tenancy → agentaudit.
---

# secaudit — skill wrapper

## When to use
- Pre-prod, payment, auth surfaces, secret leakage, dependency CVEs
- In-product LLM/RAG/tool features (LLM01–LLM10)

## When not to use
- Operator harness, Cursor/Claude MCP, session spawn, YOLO flags → `agentaudit`

## Runtime
Claude: `/secaudit`. Cursor / Grok: this skill on the AGK Audit face.

## Default posture
READ-ONLY. No `--fix` path. RED: no exploit PoCs, no payload catalogs.
Secret scanners are **tool-backed** only if they actually ran (auditor does not Bash by default).

## Tenancy
One tenant per run. CLIENT never on Omega. Abort if tenant unset.

## Recipe
1. Tenant lock.
2. Obey AGK-AUDIT-OVERRIDE-V2 in the first 100 lines of `audits/secaudit.md`.
3. Follow that body. Do not reconstruct deleted payload catalogs.
4. Cross-forward harness findings to `/agentaudit`.
5. Emit Builder packet. Never apply.

## Full protocol
See [`audits/secaudit.md`](../../audits/secaudit.md).
