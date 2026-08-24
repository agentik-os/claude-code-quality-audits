---
name: secaudit
description: >
  Product-surface security audit (OWASP Top 10 2021 web + OWASP LLM Top 10
  2025 in-app). Use for pre-prod, payment, auth, secrets, in-app MCP.
  Default READ-ONLY. Never emit exploit PoCs. Harness/YOLO/tenancy → agentaudit.
---

# secaudit — skill wrapper

## When to use
- Pre-prod, payment, auth surfaces, secret leakage, dependency CVEs
- In-product LLM/RAG/tool features (LLM01–LLM10)

## When not to use
- Operator harness, Cursor/Claude MCP, session spawn, YOLO flags → `agentaudit`

## Runtime
Claude: `/secaudit`. Cursor / Grok: this skill on the AGK Audit face.
Do not spawn a dedicated security-auditor chat.

## Default posture
READ-ONLY. `--fix` only if the human spelled it (conflict of interest).
RED: no exploit PoCs, no working payloads. Secret scanners (gitleaks /
trufflehog / osv-scanner) are **tool-backed** only if they actually ran.

## Tenancy
One tenant per run. CLIENT never on Omega. Abort if tenant unset.

## Recipe
1. Tenant lock.
2. Follow `audits/secaudit.md` including v1.3 LLM/MCP/secrets addenda.
3. Cross-forward harness findings to `/agentaudit`.
4. Emit Builder packet; do not apply patches unless `--fix`.
5. Fresh session for re-audit.

## Full protocol
See [`audits/secaudit.md`](../../audits/secaudit.md).
