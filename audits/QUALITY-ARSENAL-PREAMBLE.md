---
name: QUALITY-ARSENAL-PREAMBLE
description: >
  Shared doctrine, invariants, and contracts for Quality Arsenal forensic
  audits (18 originals + /agentaudit). Dual runtime: Claude Code commands AND
  Cursor / Grok Bot SKILL.md wrappers under skills/. Default is READ-ONLY.
  Referenced by /metaudit for compliance verification.
  NOT a user-invokable skill — this is a shared source of truth.
---

# Quality Arsenal Preamble v2.0

> *"One doctrine, nineteen implementations, one face, zero same-session self-fix."*

Every Gestalt-Popper forensic audit in the Quality Arsenal inherits the contracts below. Deviations are either (a) declared explicitly with rationale, or (b) a bug caught by `/metaudit`.

**v2.0 (2026-08-24) — late-2026 agentic reality.** Auditor ≠ fixer. Dual surface (Claude commands + Cursor/Grok skills). One tenant per run. One `AGK Audit` face (Grok Bot hard-caps 50 agents). Unverified README percentages are not doctrine.

---

## 0A. AUDITOR ≠ FIXER (universal, 2026) — ADR-001

**AGK Audit is READ-ONLY findings.** The audit produces `verdict.json` + a Builder packet (`fix-plan.json`). It does **not** edit product code or schema.

- Auto-fix-in-the-same-session is a **conflict of interest**. The model that missed the bug must not certify the patch.
- **There is no `--fix` flag on AGK Audit.** A flag or a chat “yes” is not authorization to mutate. Destructive apply needs a **different agent**.
- **Fix** is a handoff to a **Builder**: Omega workers `claude` | `codex` | `glm`, or **Cursor Cloud on CLIENT**. That agent is not this skill pack.
- **Re-audit is a FRESH session.** Same chat continuing to score its own diffs is invalid.
- `/retentionaudit` is **always** READ-ONLY (proposals only). Do not attach an apply path to it.
- `--no-fix` is redundant; the only mode is readonly.

`verdict.json.mode` is always `"readonly"`.

Skills that say “Read and follow `audits/<id>.md`” must obey the **AGK-AUDIT-OVERRIDE-V2** block in the first 100 lines of that file. Later FIX EXECUTION text, if any remnant exists, is void.

---

## 0B. DUAL RUNTIME + ONE FACE

| Surface | Artifacts | Invocation |
|---|---|---|
| Claude Code | `audits/*.md` copied to `~/.claude/commands/` | `/secaudit` |
| Cursor / Grok Bot | `skills/<id>/SKILL.md` | Face agent loads the skill; recipe Reads `audits/<id>.md` |

**Do not design 18 auditor chats.** Integration target: one face named **AGK Audit** (`/quality-arsenal`) plus skills. Grok Bot **hard-caps 50 agents** — treat that as a ceiling, not a staffing plan.

Writer saying done is **not** done. AGK loop: **Review** (fresh, reasons not to merge) → **Audit** (this arsenal, scoped by `/audit-pilot`) → **Afterwork** packet.

---

## 0C. TENANCY (universal)

**One tenant per run.** Never load sibling-client secrets.

| Tenant | Runtime rule |
|---|---|
| AGK | Omega / Agentik infra OK |
| CLIENT | **Never on Omega.** Cursor Cloud or the client's own host |
| LEVERAGE | Isolated leverage workspace only |
| PERSONAL | Operator personal runtime only |

If tenant is unset (`--tenant=` or `AGK_TENANT`) → **ABORT**. Do not guess.

---

## 0D. RED RULE (secaudit + agentaudit, inherited by any security-touching phase)

Findings + evidence + impact + recommendation. **Never emit exploit PoCs, working payloads, or jailbreak recipes.** Label each finding `tool-backed` | `llm-judgment` | `inventory-only`.

---

## 0. THE FIRST LAW (universal, above all others)

> **Code lies. Comments lie. Only runtime tells the truth.**

Before any finding, any fix, any conclusion: **observe the actual runtime behavior**. Reading code reveals what the author *intended*. Reading logs, traces, outputs, network dumps, file states reveals what *actually happens*. When they disagree, reality wins.

**Applied to every audit:**
- Before claiming "X is broken" → show the runtime evidence (log line, trace, output, screenshot).
- Before claiming "X works" → verify at runtime, not by reading the code.
- Before the 3rd code change on the same bug → add logging, reproduce, observe.
- When a comment says "X is required" but X's purpose is unclear → test the alternative in isolation.
- When a fix "should work" but symptoms persist → runtime observation is mandatory before the next attempt.

**Anti-pattern catastrophe (2026-04-14):** 2h35 wasted on `tmux paste-buffer -p` because the comment said "-p is required". Runtime test with and without `-p`: only *without* worked. The comment lied for years. See `~/.claude/projects/-home-hacker/memory/feedback_live_debug_first.md` for the full protocol.

---

## 1. GESTALT-POPPER DOCTRINE (universal)

- **Gestalt clarity gate** — Before any phase runs, identify the *hinge point* of the system under audit (the one element that, if broken, makes everything else worthless). Audit the hinge with 10x scrutiny. Proportional scrutiny elsewhere.
- **Popper falsification** — Every claim gets a test that could disprove it. A claim that can't be falsified is not a finding, it's an opinion.
- **Evidence chain** — Every finding has: file:line → what's wrong → why it matters → blast radius → suggested fix. Missing any link = invalid finding.
- **Adversarial thinking** — For every component: "How would I break this? What if the inputs lie?"
- **The target is guilty until proven innocent.**
- **Runtime > code > comments.** When the three disagree, trust them in that order.

---

## 2. SCOPED INVOCATION FLAGS (MANDATORY across all audits)

Every audit parses these flags identically. Rule 43 (Linear pipeline) depends on this compatibility.

| Flag | Effect | Required when |
|------|--------|---------------|
| `--url={page_url}` | Scope URL-based walkthroughs to this page | Linear ticket audits |
| `--files={comma-separated-paths}` | Scope code-side checks to these files | Targeted reviews |
| `--scope={1-line description}` | Free-text scope note in outputs | Multi-audit orchestration |
| `--ticket={TICKET_ID}` | Link audit to Linear ticket, write results to `.linear-fix/{TICKET}/{audit}.json` | Rule 43 pipeline |
| `--tenant={AGK\|CLIENT\|LEVERAGE\|PERSONAL}` | Tenant lock | Always, unless `AGK_TENANT` is already set |
| `--no-fix` | Redundant confirm of READ-ONLY (the only AGK Audit mode) | Optional |
| `--fix` / `--fix-only` | **Forbidden on AGK Audit.** Do not parse as apply. Tell the user to dispatch a Builder. | Never |
| `--focus={area}` | Per-audit narrower scope with FULL phase depth | Targeted concerns |

**FORBIDDEN (rule 46):** `--quick`, `--streamlined`, `--lightweight`, `--light`, `--fast`, `--custom`. If present in user prompt → REFUSE with reference to rule 46. Narrower scope uses `--focus` with full depth per phase.

**Mandatory combinations:**
- `--ticket=X` requires `--url=Y` (can't audit a ticket without knowing the page)
- Rule 43 dispatches MUST provide `--files`, `--url`, `--ticket`

---

## 3. CONCURRENCY LOCK (MANDATORY)

Every audit acquires a lock at Phase 0 to prevent simultaneous runs from stomping outputs.

```bash
LOCKFILE=".{audit}/.lock"
mkdir -p ".{audit}"
if [ -f "$LOCKFILE" ]; then
  LOCK_AGE=$(($(date +%s) - $(stat -c %Y "$LOCKFILE" 2>/dev/null || echo 0)))
  if [ $LOCK_AGE -lt 14400 ]; then  # 4h max; rule 46 allows long audits
    echo "ABORT: another /{audit} holds $LOCKFILE (age ${LOCK_AGE}s, PID $(cat $LOCKFILE))."
    echo "Wait or rm $LOCKFILE if stale."
    exit 1
  fi
  echo "WARNING: stale lockfile (>4h), reclaiming"
fi
echo $$ > "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT
```

Rule 43's parallel DYNAMIC audit chain (`/codeaudit` + `/uiuxaudit` + `/flowaudit` + `/debugaudit` on the same ticket) uses distinct `.{audit}/` directories, so locks don't collide across different audits — only duplicate invocations of the same audit are blocked.

---

## 4. PHASE RE-AUDIT CAP (MANDATORY)

**READ-ONLY only:** no apply loop. Emit the Builder packet and stop. `iterations.md` records `cycles=0 mode=readonly`.

Re-audit after a Builder lands is a **fresh session** (cap 3 fresh sessions). AGK Audit never applies patches between those sessions.

Zero tolerance for silent infinite loops. Same-session auto-fix is **forbidden**, not merely discouraged.

---

## 5. NON-UI CONTEXT HANDLING (MANDATORY per audit)

Not every project has UI/URLs/flows. Each audit declares its compatibility:

| Project type | /codeaudit | /debugaudit | /uiuxaudit | /flowaudit | /featureaudit | /perfaudit | /secaudit | /a11yaudit | /seoaudit | /copyaudit | /dxaudit | /motionaudit | /dataaudit | /apiaudit |
|--------------|-----------|-------------|-----------|-----------|---------------|-----------|-----------|-----------|-----------|-----------|----------|--------------|-----------|-----------|
| Web app (URLs) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (if DB) | ✅ (if API) |
| Mobile (RN/Expo) | ✅ | partial | ✅ | mobile mode | ✅ | ✅ | ✅ | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | ✅ |
| CLI tool | ✅ | ⚠️ (log-based) | **ABORT** | **ABORT** | ✅ | ✅ (startup/CPU) | ✅ | ✅ (output text) | N/A | ✅ | ✅ (primary!) | **ABORT** | ✅ (if DB) | N/A |
| Library / SDK | ✅ | N/A | **ABORT** | **ABORT** | ✅ | ✅ | ✅ | N/A | N/A | ✅ (docs) | ✅ | **ABORT** | N/A | ✅ (if API) |
| Backend-only API | ✅ | partial | **ABORT** | **ABORT** | ✅ | ✅ | ✅ | N/A | N/A | ✅ (docs) | ✅ | **ABORT** | ✅ | ✅ (primary!) |
| Headless service | ✅ | log-based | **ABORT** | **ABORT** | ✅ | ✅ | ✅ | N/A | N/A | ✅ | ✅ | **ABORT** | ✅ | ✅ |

**ABORT behavior**: exit with clear error naming the detected project type and suggesting alternative audits. Never hallucinate findings for missing surfaces.

---

## 6. OUTPUT CONTRACT VERIFICATION (MANDATORY)

Every audit declares outputs. Before reporting success, verify they exist with valid schema.

### Required outputs per audit

```
.{audit}/
├── session.log              # timestamps, scope, args, duration
├── verdict.json             # machine-readable score + findings (schema below)
├── verdict.md               # human-readable final report
├── fix-plan.json            # prioritized fix tasks (schema below)
├── fix-plan.md              # human-readable fix plan
├── iterations.md            # score trajectory (iteration 1..N)
├── progress.json            # live progress (for watchers)
├── telemetry.json           # cost + duration (schema below)
├── fix-log.md               # append-only fix execution log
└── discovery/               # audit-specific inventories
```

### verdict.json schema (MANDATORY)

```json
{
  "audit": "<audit-name>",              // e.g. "codeaudit"
  "version": "<audit-version>",         // e.g. "v2.1"
  "preamble_version": "2.0",            // MUST match this file's version
  "skill_used": "<audit-name>",         // for rule 43 gate compliance
  "mode": "readonly",                   // AGK Audit is always readonly
  "tenant": "CLIENT",                   // AGK | CLIENT | LEVERAGE | PERSONAL
  "runtime": "agk-audit",               // claude-code | cursor | grok-bot | agk-audit
  "score": 95,                          // /100 normalized
  "raw_score": 395,                     // raw score
  "raw_max": 420,                       // applicable max (N/A phases excluded)
  "grade": "A",                         // S/A/B/C/D/F
  "scope": {
    "url": "...",                       // if --url provided
    "files": ["..."],                   // if --files provided
    "ticket": "...",                    // if --ticket provided
    "free_text": "..."                  // if --scope provided
  },
  "phases": [
    {"id": 1, "name": "...", "score": 30, "max": 30, "applicable": true}
  ],
  "findings": [
    {
      "id": "F-001",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "phase": 3,
      "file": "src/auth.ts",
      "line": 42,
      "description": "...",
      "evidence": "...",
      "blast_radius": "...",
      "suggested_fix": "...",
      "cross_audit_confirmations": []   // see below
    }
  ],
  "cross_audit_confirmations": [        // ELEVATION MECHANISM
    {
      "finding_id": "F-001",           // this audit's finding
      "confirmed_by": "secaudit",      // which other audit confirmed
      "confirmed_finding_id": "F-012", // that audit's corresponding finding
      "elevation": "CRITICAL",         // elevated severity (both agree = CRITICAL)
      "evidence_path": "audits/.secaudit/verdict.json"
    }
  ],
  "iterations": 3,                      // how many fix-and-reaudit loops
  "needs_review": [],                   // findings that hit 5-iter cap
  "project_signals_detected": [],       // auto-detected from package.json (see §16)
  "timestamp_start": "...",
  "timestamp_end": "..."
}
```

### Cross-audit finding elevation (ENFORCEMENT)

When two audits produce findings on the same file:line or same concern:
1. The later-running audit checks `.{producer_audit}/verdict.json` for matching findings
2. If match found: add a `cross_audit_confirmations` entry to its own verdict.json
3. Both audits agreeing on same file:line = automatic elevation to CRITICAL
4. /metaudit verifies elevation consistency in its Phase 1 compliance check

### telemetry.json schema (MANDATORY)

```json
{
  "audit": "<name>",
  "version": "<version>",
  "duration_sec": 12840,
  "tokens_used": {"input": 450000, "output": 120000},
  "phases_completed": 23,
  "phases_skipped": [14, 18],
  "phases_applicable": 21,
  "fixes_applied": 47,
  "fix_reverts": 3,
  "telegram_notifications_sent": 9,
  "model": "claude-opus-4-6",
  "preamble_version": "2.0"
}
```

### fix-plan.json schema (MANDATORY)

```json
{
  "audit": "<name>",
  "generated_at": "...",
  "tasks": [
    {
      "id": "FIX-001",
      "finding_id": "F-001",
      "severity": "HIGH",
      "file": "src/auth.ts",
      "line": 42,
      "description": "...",
      "fix": "...",
      "status": "pending|applied|reverted|needs_review",
      "depends_on": ["FIX-000"],
      "attempts": 0
    }
  ]
}
```

### Output gate (MANDATORY, runs at end of audit)

```
1. For each file in the required outputs list:
   - Does it exist? (fail-stop)
   - Does it parse? (JSON: schema check; MD: non-empty)
   - verdict.json.score is a number 0-100
   - verdict.json.skill_used == <audit-name>
   - verdict.json.preamble_version == "2.0"
   - verdict.json.mode is "readonly" or "fix"
   - verdict.json.tenant is set
2. If any check fails:
   - Do NOT report success
   - Write .{audit}/OUTPUT_GATE_FAILED.md with details
   - Exit non-zero, Telegram SOS
3. Only mark audit "complete" when all checks pass.
```

---

## 7. TELEGRAM PROGRESS CHANNEL (MANDATORY)

Every audit sends structured notifications. Use helper: `~/.aisb/bin/audit-notify.sh <audit> <event> <details>`.

| Event | Timing | Content |
|-------|--------|---------|
| `start` | Phase 0 begin | `🚦 /{audit} started on {project} — scope: {scope}` |
| `progress` | Every 3 phases completed | `📊 /{audit} phase {N}/{total} complete — {phase_name}` |
| `iteration` | Each fix-and-reaudit cycle | `🔁 /{audit} iteration {N}/5 — score trajectory: {prev} → {curr}` |
| `verdict` | Phase 21 (final score) | `🎯 /{audit} done — score {X}/100 — see {verdict.md path}` |
| `abort` | Any ABORT condition | `🛑 /{audit} aborted — reason: {reason}` |
| `sos` | 5-iter cap, lock collision, output-gate fail, unrecoverable error | `🆘 /{audit} SOS — {diag_file_path}` |

---

## 8. DISCOVERY-DRIFT CHECK (MANDATORY on resumed audits)

If `.{audit}/discovery/` exists and is older than 1h:
1. Re-run light discovery pass
2. Diff against existing inventory
3. If diff detected: flag as DRIFT, abort or user-confirm
4. Never trust stale discovery — the codebase moves

---

## 9. SELF-TELEMETRY (MANDATORY)

Emit `.{audit}/telemetry.json` at completion (schema in §6). Used by `/metaudit` + capacity planning.

---

## 10. DEPRECATION REGISTRY

Check `~/.claude/DEPRECATED.md` for deprecated skill/command names before invoking cross-references. If an audit references a deprecated name, surface it as a finding.

Current known deprecations (as of 2026-04-14):
- `/hunt` → `/debugaudit` (renamed 2026-03-26)
- `/delegate` → route via `/ceo`, `/cto`, `/cmo`, `/cpo` (never implemented as standalone)
- `/remotion` → removed (no replacement; use `/creative_director` pipeline instead)
- `/head_of_marketing` → `/cmo` or `/content-strategy` skill
- `/landing_page_analysis` → `/market landing`
- `/website_brand_analysis` → `/market brand`
- `/ad_creative_analysis` → `/ads_analyst`
- `/performance_marketer` → `/market` suite skills
- `/bmad` → removed

---

## 11. INTEGRATION SMOKE TEST (MANDATORY in fix gate for code-touching audits)

Any audit that modifies code (/codeaudit, /debugaudit, /uiuxaudit, /flowaudit, /featureaudit, /perfaudit, /a11yaudit, /apiaudit, /dataaudit, /copyaudit, /seoaudit, /motionaudit) MUST run integration smoke tests in Phase 23 fix gate:

```
1. Detect integrations from package.json + env vars:
   - Composio: @composio/sdk, COMPOSIO_API_KEY
   - MCP: @modelcontextprotocol/*, MCP server configs
   - Stripe: stripe, STRIPE_SECRET_KEY
   - Clerk: @clerk/*, CLERK_SECRET_KEY
   - Convex: convex, CONVEX_URL
   - Trigger.dev: @trigger.dev/sdk, TRIGGER_SECRET_KEY
   - Linear: LINEAR_API_KEY
2. For each detected integration, run smoke test:
   - Stripe: fetch account.retrieve() with test key
   - Clerk: verify JWT template exists
   - Convex: npx convex dev --once (dry validate)
   - Composio: npx composio ping
   - MCP: test handshake
3. Post-fix, re-run the same smoke tests
4. If any integration breaks post-fix → revert → mark NEEDS_REVIEW
5. Memory basis: "fixes must NEVER break working integrations"
```

Read-only audits (/copyaudit text-only mode, /secaudit in dry-run) may skip this gate.

---

## 12. RATE-LIMIT SAFETY (MANDATORY for audits that fuzz or hit APIs)

/secaudit + /apiaudit make external requests. They MUST respect:

```
- Max 10 req/s default (override: --rate-limit-override=<N> for authorized tests)
- Abort on 3 consecutive 429 or 503 responses
- Never run against production without explicit --prod flag + confirmation
- Self-pentest (target = own audit infra) ABORT with "not supported — manual review required"
```

---

## 13. SCORE NORMALIZATION (MANDATORY)

Each audit has its own raw max (varies 280–540 across family; `/secaudit` full max is **460**). All report to /100:

```
normalized = round((raw_score / applicable_raw_max) * 100)
```

Where `applicable_raw_max` excludes phases marked N/A for the project type.

Grade boundaries:
- 90-100: S (Fortress)
- 80-89: A (Solid)
- 70-79: B (Good)
- 60-69: C (Acceptable)
- 50-59: D (Risky)
- <50: F (Condemned)

---

## 14. RULE-46 COMPLIANCE (MANDATORY)

No audit may:
- Offer `--quick` / `--streamlined` / `--lightweight` / `--light` / `--fast` / `--custom` modes
- Substitute "lighter" protocols for phases
- Skip phases "to save time"
- Accept "streamlined" instructions from orchestrators — REFUSE and raise alert

Narrower scope is achieved via `--focus` flag with FULL phase depth, never degraded depth.

---

## 15. AUDIT REGISTRY

| Audit | Max | Phases | Non-UI ABORT | Code-touching | External-fetch | Specialty |
|-------|-----|--------|-------------|---------------|----------------|-----------|
| /codeaudit | 420 | 24 | No | Never (AGK Audit) | No | SOLID, phantoms, deps |
| /debugaudit | 360 | 23 | Partial | Never (AGK Audit) | No | Runtime bugs, console |
| /uiuxaudit | 420 | 25 | Yes | Never (AGK Audit) | No | Visual coherence |
| /flowaudit | 400 | 25 | Yes | Never (AGK Audit) | No | User journeys |
| /featureaudit | 320 | 19 | No | Never (AGK Audit) | Yes (WebSearch) | PRD completeness |
| /perfaudit | 360 | 23 | No | Never (AGK Audit) | No | Core Web Vitals |
| /secaudit | 460 (400 if LLM phases N/A) | 20 + 3 | No | **Never (AGK Audit)** | Inventory; **no PoCs** | OWASP 2021 + LLM 2025 surfaces |
| /agentaudit | 360 | 16 | No | **Never** | No | Harness / MCP / tenancy / gates |
| /a11yaudit | 320 | 21 | Partial | **Never (AGK Audit)** | No | WCAG 2.2 AA |
| /seoaudit | 400 | 25 | Partial | Never (AGK Audit) | Yes (crawl) | Crawlability, GEO/AEO |
| /copyaudit | 280 | 19 | No | Never (AGK Audit) | No | Claims vs reality |
| /dxaudit | 320 | 21 | No | Never (AGK Audit) | No | Developer onboarding |
| /motionaudit | 360 | 23 | Yes | Never (AGK Audit) | No | Motion purpose |
| /dataaudit | 320 | 21 | No | **Never (AGK Audit). Builder may write only with backup + separate dispatch** | No | Schema + integrity |
| /apiaudit | 360 | 23 | No | Never (AGK Audit) | Yes (inventory) | REST/GraphQL contracts |
| /retentionaudit | 400 | — | No | **Never** | No | Product/CPO (proposal only) |
| /automationaudit | 330 | 22 | No | Never (AGK Audit) | No | Cron / daemons |
| /logicaudit | 360 | 20 | No | Never (AGK Audit) | No | Architecture |
| /refontaudit | 540 | 25 | Yes | Never (AGK Audit) | No | Dashboard redesign |

---

## 16. PROJECT SIGNAL DETECTION (auto-dispatch intelligence)

Before dispatching audits based on keyword matching alone, Oracle/AISB SHOULD read the project's actual signals to auto-suggest relevant audit focuses:

```bash
# Auto-detect from package.json + env vars + file structure
has_convex   = grep -q "convex" package.json          → /dataaudit relevant
has_clerk    = grep -q "@clerk" package.json           → /secaudit --focus=auth
has_stripe   = grep -q "stripe" package.json           → /flowaudit --focus=payment
has_i18n     = grep -qE "next-intl|i18next|lingui"     → /copyaudit --focus=i18n + /a11yaudit --focus=rtl
has_prisma   = test -d prisma/                         → /dataaudit + /apiaudit
has_graphql  = test -f schema.graphql                  → /apiaudit --mode=graphql
has_ci       = test -f .github/workflows/*.yml         → /dxaudit --focus=cicd
has_motion   = grep -qE "framer-motion|gsap|three"     → /motionaudit relevant
has_tailwind = test -f tailwind.config.*               → /uiuxaudit relevant
has_mcp      = test -f .mcp.json -o -f mcp.json -o -d .cursor   → /agentaudit + /secaudit --focus=mcp
has_skills   = test -d skills -o -d .cursor/skills     → /agentaudit
has_providers= test -f providers.toml                  → /agentaudit --focus=secrets + tenant lock
no_ui        = ! grep -qE "react|vue|svelte|next"      → ABORT /uiuxaudit /flowaudit /motionaudit
```

Emit detected signals in verdict.json as `project_signals_detected: ["convex", "clerk", "stripe", ...]`.

This makes dispatch SMARTER than keyword-only routing. Example: user says "audit everything" on a Convex+Clerk+Stripe project → system auto-focuses /dataaudit on Convex schema, /secaudit on Clerk auth, /flowaudit on Stripe payment flows — without the user having to specify.

---

## 17. PREAMBLE SELF-CHECK (auto-drift detection)

Every audit invocation runs a lightweight Phase 0 pre-flight that verifies its OWN preamble compliance before starting the full pipeline:

```bash
# 10-second pre-flight (negligible cost)
AUDIT_FILE="~/.claude/commands/${AUDIT_NAME}.md"
PREAMBLE="~/.claude/commands/QUALITY-ARSENAL-PREAMBLE.md"

# Check preamble exists
test -f "$PREAMBLE" || { echo "ABORT: Preamble missing. Run /metaudit."; exit 1; }

# Check own file declares preamble_version (v2.0 as of 2026-08-24; v1.x still warn)
grep -qE 'preamble_version.*(2\.0|1\.0)' "$AUDIT_FILE" || { echo "WARN: ${AUDIT_NAME} may not be preamble-compliant. Run /metaudit --focus preamble."; }

# Check own compliance_score
grep -q '"compliance_score": 100' "$AUDIT_FILE" || { echo "WARN: ${AUDIT_NAME} compliance < 100. Run /metaudit --focus arsenal."; }
```

This catches drift at the moment it matters — when an audit is about to execute — rather than waiting for a manual /metaudit invocation.

---

*Preamble v1.1 — 2026-04-14. Added §16 (project signal detection) + §17 (preamble self-check).*
*Preamble v2.1 — 2026-08-24. ADR-001: AGK Audit has no `--fix` path. Auditor ≠ fixer in the bodies skills follow. Dual runtime, tenancy, AGK Audit face, /agentaudit, RED (catalogs removed). Unverified catch-rate/trust-curve numbers are not doctrine.*
*Referenced by all 19 audits + /metaudit compliance scanner.*
*One doctrine, nineteen implementations, one face.*
