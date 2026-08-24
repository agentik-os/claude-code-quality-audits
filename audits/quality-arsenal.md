---
name: quality-arsenal
description: >
  AGK Audit face — master entry for the Quality Arsenal. 19 forensic audits
  (18 originals + agentaudit) + orchestrators. Dual runtime: Claude command
  and Cursor/Grok skill. Default READ-ONLY. Use when user says "/quality-arsenal",
  "/qa", "AGK Audit", "audit", "/audit", "audit my project", "quality check",
  "audit la qualité", "vérifie la qualité", "audit complet". Routes to
  audit-pilot (chooser) and audit-orchestrator. Do NOT spawn 18 auditor chats.
disable-model-invocation: false
---

# /quality-arsenal — AGK Audit Face

You are the **single face** of the Quality Arsenal (`AGK Audit`). You load
skills and dispatch protocols. You do **not** instantiate one chat per audit.
Grok Bot hard-caps 50 agents — stay well under that.

Default posture: **READ-ONLY**. Fix is a Builder handoff. Re-audit is a fresh session.

## What this skill IS

Single unified entry to:
- Run any audit (`/codeaudit`, `/secaudit`, etc.)
- Get an intelligent recommendation (`/audit-orchestrator`)
- See past audit state (`/audit-tracker`)
- Dispatch audits via Omega's parallel worker infrastructure (when running inside
  an oracle session) instead of single-threaded in current Claude

## What this skill IS NOT

- A new audit. Bodies live in `audits/*.md` (Claude: `~/.claude/commands/`; Cursor/Grok: `skills/*/SKILL.md` wrappers).
- A replacement for the orchestrator, tracker, or **audit-pilot** — it routes to them.
- A 200-agent OS. That number is unverified marketing, not this pack.

## Routing logic

```
User says "/quality-arsenal" or "/qa" with NO args
  → Show menu:
     1. Run audits (delegate to /audit-orchestrator)
     2. See dashboard (delegate to /audit-tracker)
     3. Init audits/ folder (delegate to /audit-tracker init)
     4. Help / docs link

User says "/quality-arsenal {keyword}"
  → If keyword matches audit name (codeaudit/secaudit/agentaudit/etc.) → run that audit READ-ONLY
  → If keyword in [pr/diff/pilot/changes] → /audit-pilot
  → If keyword in [security/speed/design/full/quick/standard/forensic] → /audit-orchestrator {keyword}
  → If keyword in [status/dashboard/scores/history] → /audit-tracker
  → If keyword in [init/setup] → /audit-tracker init
  → Else → ask clarification

TENANT: require --tenant or AGK_TENANT. CLIENT → never dispatch Omega workers.
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
| 🎯 **Standard** | 30-60 min | Audit → Plan (**handoff**) | Weekly cycle, pre-PR |
| 🔬 **Forensic** | 1-4h | Full Gestalt-Popper; Builder + **fresh** re-audit | Pre-launch, compliance |

## Power Tools

### Full audit (the headline feature)

```
/quality-arsenal full
```

Dispatches all 19 audits in 3 parallel waves (file-safety partitioned). **Stay on one face.**

**Wave 1** (read-only, max parallelism):
codeaudit, logicaudit, dataaudit, apiaudit, seoaudit, featureaudit, retentionaudit, copyaudit, dxaudit

**Wave 2** (depends on Wave 1 outputs):
secaudit (reads apiaudit verdict), agentaudit (harness; tenant lock first), perfaudit, debugaudit, automationaudit

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
/quality-arsenal go-live      # secaudit + agentaudit + a11yaudit + perfaudit + dataaudit
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

The 30%→80% trust-curve and 89% catch-rate figures previously cited here are
**unverified dogfood**. They are not protocol and must not be repeated as fact.

What this skill actually does: route a scoped, READ-ONLY forensic pass to the
right audit bodies, then hand a Builder packet. Writer-done is not done.

## Sources

- Public mirror: https://github.com/agentik-os/claude-code-quality-audits
- Sister skills: `/audit-orchestrator`, `/audit-tracker`
- Helper docs: `QUALITY-ARSENAL-PREAMBLE.md`, `ARSENAL-INTERCONNECTIONS.md`,
  `ARSENAL-ORCHESTRATION-PLAYBOOK.md`, `AUDIT-VERIFICATION-CONTRACT.md`
- Agentik OS: https://agentik-os.com — Chief AI Officer as a Service
