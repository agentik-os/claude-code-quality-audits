---
name: quality-arsenal
description: >
  Master entry point for the Quality Arsenal — 18 forensic audits + intelligent
  orchestration. Use when user says "/quality-arsenal", "/qa", "audit", "/audit",
  "audit my project", "quality check", "audit la qualité", "vérifie la qualité",
  "audit complet". Routes to /audit-orchestrator for selection, /audit-tracker
  for dashboard, integrates with Omega oracle/worker workflow for parallel
  dispatch. Part of Agentik OS CAIO methodology. Public release at
  github.com/agentik-os/claude-code-quality-audits.
disable-model-invocation: false
---

# /quality-arsenal — Master Audit Entry Point

You are the **conductor of the Quality Arsenal** — the canonical entry point that
ties together 18 forensic audits, 2 orchestration skills, and the Omega oracle/
worker dispatch infrastructure.

## What this skill IS

Single unified entry to:
- Run any audit (`/codeaudit`, `/secaudit`, etc.)
- Get an intelligent recommendation (`/audit-orchestrator`)
- See past audit state (`/audit-tracker`)
- Dispatch audits via Omega's parallel worker infrastructure (when running inside
  an oracle session) instead of single-threaded in current Claude

## What this skill IS NOT

- A new audit. Audits live in their own `.md` files in `~/.claude/commands/`.
- A replacement for the orchestrator or tracker — it routes to them.

## Routing logic

```
User says "/quality-arsenal" or "/qa" with NO args
  → Show menu:
     1. Run audits (delegate to /audit-orchestrator)
     2. See dashboard (delegate to /audit-tracker)
     3. Init audits/ folder (delegate to /audit-tracker init)
     4. Help / docs link

User says "/quality-arsenal {keyword}"
  → If keyword matches audit name (codeaudit/secaudit/etc.) → run that audit directly
  → If keyword in [security/speed/design/full/quick/standard/forensic] → /audit-orchestrator {keyword}
  → If keyword in [status/dashboard/scores/history] → /audit-tracker
  → If keyword in [init/setup] → /audit-tracker init
  → Else → ask clarification
```

## Omega Integration

When running INSIDE an Omega oracle session (detected via `$TMUX_SESSION` matching
`*-oracle*` pattern, OR `$AISB_BOT_SESSION=1` env var), the dispatch model changes:

### Solo mode (default — running in user's interactive Claude)
- Audit runs in CURRENT Claude session, single-threaded
- Output to `audits/.{name}audit/`
- Block UI until done

### Oracle mode (running inside oracle)
- Dispatch each audit as a separate worker session via
  `~/.aisb/lib/dispatch-to-session.sh {ProjectName}-worker-{audit}-{ts}`
- Oracle monitors workers, aggregates results into `audits/SYNTHESIS.md`
- Telegram report to project topic when all done
- Parallel waves possible (see ARSENAL-INTERCONNECTIONS.md DAG)

The skill detects mode automatically:

```bash
if [[ "$TMUX" && "$(tmux display-message -p '#S')" =~ -oracle ]]; then
    MODE=oracle
else
    MODE=solo
fi
```

## Decision Matrix

| User intent | Action |
|---|---|
| "audit my project" | Show menu → likely `/audit-orchestrator` |
| "audit complet" / "full audit" | `/audit-orchestrator full` |
| "security audit" / "audit sécurité" | `/audit-orchestrator security` |
| "where am I with audits" / "status" | `/audit-tracker` |
| "audits/.codeaudit/ not found" | `/audit-tracker init` then user re-runs |
| "is the code secure" | `/secaudit` direct |
| "make it bulletproof" | `/audit-orchestrator forensic` |

## Three Power Levels

| Level | Time | Phases | Use case |
|---|---|---|---|
| ⚡ **Quick** | 5-15 min | Audit only (top 5 findings) | Gut-check, demo prep |
| 🎯 **Standard** | 30-60 min | Audit → Plan → Fix → Re-audit | Weekly cycle, pre-PR |
| 🔬 **Forensic** | 1-4h | Full Gestalt-Popper with auto-fix until 100/100 | Pre-launch, compliance |

## Power Tools

### Full audit (the headline feature)

```
/quality-arsenal full
```

Dispatches all 18 audits in 3 parallel waves (file-safety partitioned):

**Wave 1** (read-only, max parallelism):
codeaudit, logicaudit, dataaudit, apiaudit, seoaudit, featureaudit, retentionaudit, copyaudit, dxaudit

**Wave 2** (depends on Wave 1 outputs):
secaudit (reads apiaudit verdict), perfaudit, debugaudit, automationaudit

**Wave 3** (UI bundle):
uiuxaudit, motionaudit, a11yaudit, flowaudit

**Wave Final**:
refontaudit if requested

After all waves done:
1. Aggregate scores into `audits/SYNTHESIS.md`
2. Compute overall grade (avg /100, flag any < 80)
3. Send Telegram report to project topic with verdict + per-audit links
4. Suggest next actions

### Quick presets

```
/quality-arsenal go-live      # secaudit + a11yaudit + perfaudit + dataaudit (go-live trio + GDPR)
/quality-arsenal ship-ready   # featureaudit + debugaudit + dxaudit
/quality-arsenal investor     # uiuxaudit + featureaudit + retentionaudit + copyaudit
/quality-arsenal redesign     # refontaudit + uiuxaudit + motionaudit
/quality-arsenal new-dev      # dxaudit + codeaudit (for fresh contributor onboarding)
```

## Workflow integration with Omega

When dispatched from an Omega oracle, the skill writes worker tasks into:

```
~/.aisb/state/oracle-{Project}-oracle.workers.txt   # append worker names
audits/.{name}audit/progress.json                   # per-audit progress
audits/SYNTHESIS.md                                 # aggregate dashboard
```

The oracle monitors workers via `~/.aisb/lib/oracle-monitor-workers.sh` which is
already aware of the canonical audits/ path (post-2026-05-13 refactor).

## Output Convention

ALL audit outputs live under `audits/.{name}audit/` — never at project root.
See `AUDIT-VERIFICATION-CONTRACT.md` for the 7-file output spec every audit
honors: verdict.json, REPORT.md, fix-plan.json, fix-plan.md, iterations.md,
progress.json, telemetry.json, fix-log.md.

## Why this matters (the deep "why")

Agentik OS ships the **Chief AI Officer as a Service** methodology. One core
hypothesis: **the bottleneck of AI-driven development isn't the AI's ability to
write code — it's the human's ability to TRUST the code without re-reading
every line**.

Six months ago: humans trusted AI-written code ~30% of the time.
Today (with Quality Arsenal in the loop): ~80%.

The Quality Arsenal is the bridge from "vibe-coded MVP" to "production-grade
software you'd ship to enterprise customers". It removes the human-machine
round-trip tax by encoding senior-engineer scrutiny into deterministic protocols
the AI runs ON ITS OWN OUTPUT before shipping.

That's the wedge. That's why this skill exists.

## Sources

- Public mirror: https://github.com/agentik-os/claude-code-quality-audits
- Sister skills: `/audit-orchestrator`, `/audit-tracker`
- Helper docs: `QUALITY-ARSENAL-PREAMBLE.md`, `ARSENAL-INTERCONNECTIONS.md`,
  `ARSENAL-ORCHESTRATION-PLAYBOOK.md`, `AUDIT-VERIFICATION-CONTRACT.md`
- Agentik OS: https://agentik-os.com — Chief AI Officer as a Service
