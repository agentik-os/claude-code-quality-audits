<div align="center">

# Quality Arsenal

### Forensic audit **protocols** — not a measured catch-rate, not a 200-agent OS

*Part of [**Agentik OS**](https://agentik-os.com) — Chief AI Officer as a Service*

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Audits: 19](https://img.shields.io/badge/Forensic_Audits-19-blue)](audits/)
[![Default: READ-ONLY](https://img.shields.io/badge/Default-READ--ONLY-lightgrey)](#-auditor-≠-fixer)
[![Runtimes: dual](https://img.shields.io/badge/Runtime-Claude_+_Cursor_/_Grok-purple)](#-install)
[![Agentik OS](https://img.shields.io/badge/Agentik_OS-Chief_AI_Officer-purple)](https://agentik-os.com)

</div>

---

## What this repo actually is

This repository is a **protocol pack**: 19 Gestalt-Popper forensic audits (the original 18 plus `/agentaudit`), plus orchestrators (`quality-arsenal`, `audit-pilot`, `audit-orchestrator`, `audit-tracker`, `newcmd`).

It is **two surfaces for one face**:

| Surface | What you install | Who loads it |
|---|---|---|
| **Claude Code commands** | `audits/*.md` → `~/.claude/commands/` | `/codeaudit`, `/secaudit`, … |
| **Cursor / Grok Bot skills** | `skills/*/SKILL.md` | One face agent — **AGK Audit** — loads skills. Do **not** design 18 auditor chats. |

The long forensic bodies stay in `audits/*.md`. Skills are short wrappers (name, when-to-use, recipe) that point at those bodies.

**Grok Bot hard-caps 50 agents.** This pack's integration target is **one** `AGK Audit` face plus skills, not a swarm of auditor personas.

---

## What this repo is not

| Claim previously sold as fact | Status in this repo |
|---|---|
| Trust in AI code rose **30% → 80%** (+50 pts) | **Unverified.** Internal dogfood anecdote. No public dataset, no methodology, no third-party replication. Removed as a headline metric. |
| **89%** pre-merge catch-rate, **+134%** bugs vs vanilla | **Unverified.** Same. Do not treat `verdict.json` scores as a published benchmark. |
| **200-agent** / **200+ agent** operating system | **Marketing copy, not a capability of this repo.** This pack is 19 audits + orchestrators. Grok Bot caps at 50 agents. |
| Same input → same `verdict.json` | **Protocol intent**, not a measured property. LLM temperature, tool availability, and runtime (Claude vs Cursor vs Grok) will move findings. |
| Auto-fix until 100/100 in the same session | **Conflict of interest.** Default is READ-ONLY. See [Auditor ≠ fixer](#-auditor--fixer). |

This README will not invent replacement percentages.

**What is specified (protocol, not performance):** Gestalt-Popper doctrine, scored `verdict.json`, 8-file output contract, cross-audit DAG, scoped flags, one-tenant-per-run, optional `--fix` that is never the default.

---

## The problem (without the trust-curve chart)

AI can write a lot of code. Humans still cannot tell, from a chat transcript, whether that code is safe to merge. Vanilla "review this" prompts are unreproducible and unspecialized.

This pack encodes **senior-engineer scrutiny as named protocols** so a face agent can run a scoped audit and emit falsifiable findings. That is a process claim. It is not a proof that the code is production-ready.

**A writer saying "done" is not done.** In the Agentik (AGK) loop:

1. **Review** — fresh session, reasons *not* to merge (no author marking their own homework).
2. **Audit** — this arsenal, scoped by `/audit-pilot` from the diff/PR.
3. **Afterwork** — human-readable packet (PDF or equivalent) from the verdicts.

Re-audit after a fix is a **fresh session**, not the same auditor continuing to grade its own patches.

---

## Auditor ≠ fixer

**Default posture: READ-ONLY findings.**

The auditor must not be the fixer in the same session. Auto-fix-in-the-same-session is a 2026 agentic conflict of interest: the model that missed a bug is asked to certify the patch.

| Role | Who | What they may do |
|---|---|---|
| **Auditor** (this pack) | AGK Audit face + skills | Read, score, emit findings + `fix-plan.json`. No product edits. |
| **Builder** | Omega workers (`claude` \| `codex` \| `glm`) or **Cursor Cloud on CLIENT** | Apply the handoff. CLIENT workloads never run on Omega. |
| **Re-auditor** | Fresh session, same protocol | Re-run scoped audits on the Builder diff. |

`--fix` remains **documented and optional**. It is never the default. Use it only when a human explicitly accepts the conflict (solo dogfood, no second agent available). `/retentionaudit` stays proposal-only even with `--fix`. `/agentaudit` never applies harness patches in-session.

---

## Tenancy

**One tenant per run.** Never load sibling-client secrets.

| Tenant | Where it may run | Rule |
|---|---|---|
| **AGK** | Omega / Agentik infra | Internal Agentik OS work |
| **CLIENT** | Cursor Cloud (or the client's own runtime) | **Never on Omega.** No AGK secrets in the session. |
| **LEVERAGE** | Isolated leverage workspace | No CLIENT or PERSONAL secrets |
| **PERSONAL** | Operator's personal runtime | No CLIENT or AGK sibling secrets |

If tenant is unset, **abort**. Do not guess. Do not glob `providers.toml` / `.env` trees from other tenants.

---

## Install

### Claude Code (commands)

```bash
mkdir -p ~/.claude/commands
cd ~/.claude/commands
git clone https://github.com/agentik-os/claude-code-quality-audits.git tmp
cp tmp/audits/*.md .
rm -rf tmp
```

Then in Claude Code:

```
/quality-arsenal init
/audit-pilot pr                  # choose audits from the diff — READ-ONLY
/secaudit --focus=auth           # one audit
```

### Cursor / Grok Bot (skills)

Copy the skill wrappers into the host's skills directory. The wrappers load `audits/*.md`; keep the repo (or a clone) on disk so the face agent can Read the forensic bodies.

```bash
# Cursor — project skills
mkdir -p .cursor/skills
cp -R /path/to/claude-code-quality-audits/skills/* .cursor/skills/

# Cursor — user skills (available in every project)
mkdir -p ~/.cursor/skills
cp -R /path/to/claude-code-quality-audits/skills/* ~/.cursor/skills/
```

Grok Bot: load `skills/*/SKILL.md` as a skill pack on the **single** `AGK Audit` face. Do not instantiate one bot per audit.

Point the face at the cloned `audits/` tree (same repo). Skills are recipes; the protocols are the `.md` bodies.

### First use (any runtime)

```
quality-arsenal init             # creates audits/ + .gitignore
audit-pilot pr                   # maps diff → which audits (chooser)
quality-arsenal go-live          # secaudit + agentaudit + a11yaudit + perfaudit + dataaudit
```

`--fix` is opt-in and must be spelled. Bare invocations are READ-ONLY.

---

## Three power levels (findings depth — not fix depth)

The orchestrator picks **how deep to look**. Fixing is a separate handoff unless `--fix` was explicit.

### Quick (5–15 min)
- Top findings only; skip Plan execution
- Output: markdown report of worst offenders
- **When**: pre-meeting gut-check, triage

### Standard (30–60 min) — **DEFAULT**
- Full scored pipeline: Audit → Plan (**handoff**, not apply)
- Score normalized to /100, persisted to `verdict.json`
- Output: `audits/.{name}audit/` (8-file contract)
- **When**: weekly quality cycle, pre-PR validation

### Forensic (1–4h per audit)
- Full Gestalt-Popper with extended phases
- Plan covers P0/P1/P2; Builder applies; **fresh session** re-audits (cap 3 cycles)
- **When**: pre-launch gate, compliance, harness review

Quick/Standard/Forensic are **depth** knobs. They are not a license to skip the READ-ONLY default.

---

## The 19 audits

| Audit | Domain | When to pick |
|---|---|---|
| `/codeaudit` | Code architecture | Refactor, debt, new codebase |
| `/secaudit` | App security (OWASP web + LLM 2025 surfaces) | Pre-prod, payment, auth, MCP-in-app |
| `/agentaudit` | **Harness / orchestration / MCP / injection** | Agent runtimes, YOLO gates, tenancy, memory, evals |
| `/uiuxaudit` | Design coherence | Visual consistency, design system |
| `/flowaudit` | User journeys | Onboarding, conversion, dead-ends |
| `/debugaudit` | Runtime bugs | Console errors, broken features |
| `/featureaudit` | PRD completeness | Ship-readiness, gaps |
| `/perfaudit` | Core Web Vitals | Slow site, bundle, N+1 |
| `/a11yaudit` | **WCAG 2.2 AA** | Accessibility, keyboard, contrast |
| `/seoaudit` | Discoverability | Search + **GEO/AEO** (still relevant in 2026) |
| `/dataaudit` | Schema integrity | Orphans, migrations, GDPR/RGPD |
| `/apiaudit` | API contracts | Endpoints, auth matrix |
| `/copyaudit` | Messaging | Claims vs reality, CTA |
| `/dxaudit` | Dev experience | README, onboarding |
| `/motionaudit` | Animation | Transitions, reduced motion |
| `/automationaudit` | Cron/scripts | Daemons, silent failures |
| `/logicaudit` | Architecture | Algorithms, redundancy |
| `/retentionaudit` | Product/CPO | Feature opportunities (**always READ-ONLY**) |
| `/refontaudit` | Dashboard redesign | Major redesign |

**Orchestrators (not domain audits):**

- `/audit-pilot` — **chooser**: git diff / PR → which audits, when, scoped
- `/audit-orchestrator` — power-level + intent parser
- `/audit-tracker` — dashboard + freshness + `init`
- `/quality-arsenal` — **AGK Audit face** / master router
- `/newcmd` — forge for new skills (default Type-1 posture is READ-ONLY)

---

## 2026 agentic threat model

Vanilla web OWASP is not enough for agentic systems. This pack covers the gap **without exploding to 30 audits**:

- **`/secaudit` extended** — LLM application surfaces (OWASP Top 10 for LLM Applications 2025), MCP connectors used *by the product*, secrets in env / `providers.toml` / chat logs. **RED:** findings + evidence + impact + recommendation only. **Never emit exploit PoCs or working payloads.**
- **`/agentaudit` (new)** — harness and orchestration: prompt injection in repos and tool output (untrusted fences), tool-call exfil, MCP supply chain, confused-deputy agent-to-agent, tenant isolation (AGK / CLIENT / LEVERAGE / PERSONAL), YOLO / approval gates, empty-pane / `session_id=null` spawn, evals/judges as gates, memory poisoning. Maps to OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10) where a check has a published ID.

Standards this pack claims (and only these):

| Domain | Standard in-repo | Backing |
|---|---|---|
| Web a11y | **WCAG 2.2 AA** (was 2.1) | axe-core / Playwright = **tool-backed**; journey judgment = **LLM** |
| Web AppSec | OWASP Top 10 **2021** (latest completed web Top 10 as of this edit) | scanners + LLM synthesis |
| LLM apps | OWASP Top 10 for LLM Applications **2025** | mostly **LLM-judgment** + config inventory |
| Agents | OWASP Top 10 for Agentic Applications **2026** | `/agentaudit` — inventory + policy, **not** exploit reproduction |
| Secrets | gitleaks / trufflehog / GitHub secret scanning (current 2026 tools) | **tool-backed** when the binary is present; otherwise LLM-judgment and labeled as such |
| GEO/AEO | Still in `/seoaudit` | crawl tools + LLM citation-pattern judgment |

Every finding should say **tool-backed** vs **LLM-judgment**. Do not present a vibe as a scanner result.

---

## AGK loop (how the arsenal is supposed to run)

```
Review (fresh; reasons not to merge)
    →  audit-pilot (chooser: diff/PR → audit set)
    →  Audit (this pack, scoped, READ-ONLY)
    →  Builder handoff (Omega workers claude|codex|glm, or Cursor Cloud on CLIENT)
    →  Re-audit (FRESH session)
    →  Afterwork packet (PDF / SYNTHESIS.md)
```

`/audit-pilot` stays the chooser. `/quality-arsenal` is the face. Writer-done ≠ done.

---

## Dual category: tool-backed vs LLM-judgment

Not all checks are the same kind of evidence:

### Agentic — pure LLM scrutiny
`/codeaudit`, `/logicaudit`, `/featureaudit`, `/retentionaudit`, `/dxaudit`, `/copyaudit` (mostly), `/agentaudit` (policy/harness — label each check).

**Strength:** nuance. **Weakness:** not deterministic. Say so in `verdict.json`.

### Programmatic — deterministic tooling
No audit here is 100% programmatic. Closest: `/a11yaudit` + `/perfaudit` (axe-core, Lighthouse), `/secaudit` secrets/CVE phases (gitleaks, osv-scanner / npm audit) when those tools actually ran.

### Hybrid
Most of the rest. Tools produce raw data; the LLM prioritizes and falsifies.

---

## Output contract

```
your-project/
├── audits/
│   ├── SYNTHESIS.md
│   ├── .codeaudit/verdict.json
│   ├── .secaudit/...
│   ├── .agentaudit/...
│   └── ...
```

8-file contract: `verdict.json`, `REPORT.md` (or `verdict.md`), `fix-plan.json`, `fix-plan.md`, `iterations.md`, `progress.json`, `telemetry.json`, `fix-log.md` (empty in READ-ONLY). See `audits/AUDIT-VERIFICATION-CONTRACT.md`.

In READ-ONLY, `fix-plan.*` is a **Builder packet**, not a log of edits applied. `fix-log.md` records "no product files modified" or the `--fix` exception.

---

## Safety

- **READ-ONLY default** — no product edits unless `--fix`
- **No exploit PoCs** — especially `/secaudit` and `/agentaudit`
- **One tenant per run** — no sibling-client secrets
- **CLIENT never on Omega**
- **No destructive DB ops without backup** — `/dataaudit`
- **`/retentionaudit` never edits code**
- **Rate-limit gates** on API-touching audits
- **Concurrency locks** — `.{audit}/.lock`, 4h stale
- **Cycle caps** — Builder/re-audit loops max 3; never infinite same-session auto-fix
- **Grok Bot ≤ 50 agents** — one face, not 19 auditor chats

---

## How `/newcmd` forges skills

`/newcmd` is the meta-skill. Type 1 (forensic audit) DNA is now:

1. Popper falsification
2. Scoring matrix
3. **Plan + Builder handoff** (not same-session auto-fix). `--fix` is optional and declared.
4. Parallel waves **within one face** (respect the 50-agent cap)

---

## Read in this order

1. **README.md** (this) — protocol vs claim
2. `audits/QUALITY-ARSENAL-PREAMBLE.md` — shared doctrine (v2: READ-ONLY, tenancy, dual runtime)
3. `audits/ARSENAL-ORCHESTRATION-PLAYBOOK.md` — AGK loop + dispatch
4. `audits/ARSENAL-INTERCONNECTIONS.md` — DAG
5. `audits/AUDIT-VERIFICATION-CONTRACT.md` — output + do-no-harm
6. `skills/` — Cursor / Grok wrappers
7. Individual `audits/*.md` bodies

---

## For contributors

PRs welcome. To add an audit: `/newcmd`, then a `skills/<id>/SKILL.md` wrapper that points at `audits/<id>.md`. Do not duplicate 80k-line bodies into skills.

Do not add unverified percentages to the README. If you have a real eval, publish the method and the dataset.

---

## Links

- **Agentik OS**: https://agentik-os.com
- **This repo**: https://github.com/agentik-os/claude-code-quality-audits
- **Contact**: `x@agentik-os.com`
- **Standards (external):** [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [OWASP Top 10 2021](https://owasp.org/Top10/), [OWASP LLM Top 10 2025](https://genai.owasp.org/), [OWASP Agentic Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

---

## License

MIT — use freely, attribute kindly.

```
Copyright (c) 2026 Agentik OS
```

---

<div align="center">

**Protocols by [Agentik OS](https://agentik-os.com). Metrics in older READMEs were unverified dogfood — they are not facts.**

[Star ⭐](https://github.com/agentik-os/claude-code-quality-audits) · [Issues 🐛](https://github.com/agentik-os/claude-code-quality-audits/issues)

</div>
