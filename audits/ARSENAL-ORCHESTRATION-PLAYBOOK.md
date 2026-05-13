---
name: ARSENAL-ORCHESTRATION-PLAYBOOK
description: >
  Operational playbook for AISB (ORACLE-led orchestration) and project Oracles to
  dispatch Quality Arsenal audits correctly. Translates user intent into specific
  audit invocations with proper flags, ordering, and parallelism. Complements
  ARSENAL-INTERCONNECTIONS.md (the what) with the how.
  NOT a user-invokable skill — AISB/Oracle reference doc.
---

# Quality Arsenal — Orchestration Playbook v1.0

> *"Given a mission, which audits fire, in what order, with what scope?"*

---

## 1. ORACLE'S AUDIT SELECTION ALGORITHM

When Oracle receives a task (from AISB / direct user / rule 43 / godmode), it follows this decision tree:

```
1. Parse user intent. Extract:
   - Action verb (fix / audit / verify / check / review / redesign / speed up / etc.)
   - Target noun (page URL / file paths / module / feature / "everything")
   - Domain signals (UI / code / perf / sec / a11y / SEO / data / API / flow / motion / copy / DX)

2. Consult AUDIT KEYWORD DETECTION table in ~/.claude/CLAUDE.md §"AUDIT KEYWORD DETECTION":
   - Each keyword maps to a specific /audit skill
   - Multiple keywords = multiple audits in PARALLEL (rule 001 enforced)

3. Consult ARSENAL-INTERCONNECTIONS.md §3 (dispatch order):
   - If selected audits have ordering constraints (e.g., perfaudit → seoaudit):
     batch by dependency group
   - Within a group: dispatch in parallel

4. Consult ARSENAL-INTERCONNECTIONS.md §5 (non-UI gates):
   - If project is CLI/library/backend-only/headless:
     remove incompatible audits (/uiuxaudit, /flowaudit, /motionaudit, /seoaudit)
     emit "aborted — non-UI context" for user visibility
     route to alternatives (/dxaudit, /copyaudit)

5. Apply scoping flags based on signals:
   - URL detected → --url=<URL>
   - File paths detected → --files=<paths>
   - Linear ticket ID (rule 43) → --ticket=<ID> + --url + --files
   - "just this page" → --scope="single page"

6. Enforce concurrency + locks (preamble §3):
   - Check .{audit}/.lock for each selected audit before dispatch
   - If lock held < 4h: wait or abort per user intent
   - If stale > 4h: reclaim, proceed

7. Dispatch via Agent() / TeamCreate() / direct Skill() per task complexity:
   - SIMPLE (1 audit, single-file) → direct Skill()
   - MEDIUM (2-3 audits, parallel, independent) → parallel Agent() calls
   - COMPLEX (4+ audits, groups) → /team with tmux + dependency tracking
   - EPIC (all 14) → /aisb full or /godmode orchestration

8. Monitor progress via Telegram channel + .{audit}/progress.json files

9. On completion:
   - Verify all verdict.json files exist + preamble_version="1.0" (output gate)
   - Aggregate findings by severity
   - Run /metaudit IF any .md config file was edited during audits
   - Report to user with cross-audit dedupe per INTERCONNECTIONS.md §5
```

---

## 2. INTENT → AUDIT-SET TRANSLATION TABLE

Machine-usable routing from natural language to dispatch:

| User input (en/fr, case-insensitive substring match) | Dispatch plan |
|------|---------------|
| `audit complet`, `full audit`, `toutes les audits`, `all audits`, `tout auditer` | All 14 via the octad pattern (INTERCONNECTIONS §3). `/metaudit` as final step. |
| `audit code`, `code audit`, `audit this code` | `/codeaudit --files=<detected>` solo |
| `audit ui`, `audit ux`, `design audit`, `audit design`, `audit visuel` | `/uiuxaudit --url=<detected>` solo (add `/a11yaudit` if user says "accessible" too) |
| `audit flow`, `user flow`, `audit parcours`, `workflow audit` | `/flowaudit --url=<detected>` solo |
| `audit perf`, `performance audit`, `core web vitals`, `audit rapidité` | `/perfaudit --url=<detected>` solo |
| `audit sec`, `security audit`, `owasp`, `audit sécurité` | `/apiaudit` (static auth) → `/secaudit` (exploit) — STRICT order |
| `audit a11y`, `accessibility audit`, `wcag`, `audit accessibilité` | `/a11yaudit --url=<detected>` solo |
| `audit seo`, `seo audit`, `audit référencement`, `crawlability` | `/perfaudit --url=<detected>` → `/seoaudit --url=<detected>` — STRICT order (CWV handoff) |
| `audit api`, `api audit`, `audit contrats api` | `/dataaudit` → `/apiaudit` — STRICT order (schema → contract) |
| `audit data`, `data audit`, `data integrity`, `audit données` | `/dataaudit` solo |
| `audit feature`, `feature audit`, `audit complétude`, `prd gap` | `/featureaudit` solo |
| `audit copy`, `copy audit`, `messaging audit`, `audit texte`, `audit messages` | `/copyaudit --url=<detected>` solo |
| `audit dx`, `dx audit`, `developer experience`, `onboarding dev`, `audit dev` | `/dxaudit` solo |
| `audit motion`, `motion audit`, `animation audit`, `audit animations` | `/motionaudit --url=<detected>` solo |
| `debugaudit`, `hunt`, `runtime bug`, `chaos`, `audit bugs`, `find bugs` | `/codeaudit` → `/debugaudit` — STRICT order |
| `meta audit`, `audit the audits`, `audit commands`, `quality arsenal compliance` | `/metaudit` solo |
| `redesign dashboard`, `refonte dashboard`, `comme linear`, `comme vercel`, `dashboard senior` | `/refontaudit` (not Quality Arsenal, separate dashboard skill) |
| Linear ticket phrase per rule 43 | QUADRUPLE: `/codeaudit` + `/uiuxaudit` + `/flowaudit` + `/debugaudit` all --ticket-scoped in parallel |
| Vague (`review`, `check it out`) | ASK user which domain — do NOT pick arbitrarily |

**Multiple keywords in one prompt** (e.g., "audit UX et code on /cases"):
- Launch each matching audit in PARALLEL with the scope derived from the URL
- Never combine into a single generic worker (rule 001, §AUDIT KEYWORD DETECTION)

---

## 3. SCOPE FLAGS — HOW TO APPLY THEM

Per preamble §2 (scoped invocation flags), every audit accepts these flags uniformly:

```
--url={URL}          Apply URL-based walkthroughs to this page only.
                     Required for: /uiuxaudit, /flowaudit, /debugaudit, /perfaudit,
                     /a11yaudit, /seoaudit, /motionaudit, /copyaudit (for page-specific copy)
                     when scope is specific.

--files={paths}      Apply code-side checks to these files only.
                     Required for: /codeaudit, /apiaudit, /dataaudit when targeting specific
                     modules. Used by rule 43 (Linear pipeline) with git diff output.

--scope={1-liner}    Free-text scope note in output.
                     Always include for clarity. Example: --scope="checkout success page only".

--ticket={ID}        Link audit to Linear ticket.
                     Writes results to .linear-fix/{TICKET}/{audit}.json.
                     MANDATORY for rule 43 pipeline (Step 8 dynamic chain).
                     Requires --url and --files to be present.

--no-fix             Dry-run scoring only; skip fix execution.
                     Use when user wants to review the fix plan before authorize.

--focus={area}       Per-audit narrower phase selection with FULL depth.
                     Examples:
                       /codeaudit --focus=security → phases 4+5+6+9+10 at full depth
                       /uiuxaudit --focus=typography → phase 2 at full depth
                     NOT a "quick mode". Full protocol, narrower surface.

--set-baseline       Write current measurements as new baseline (regression comparison).
                     Applies to /perfaudit, /debugaudit (visual), /seoaudit (rankings).
                     Use sparingly — only for intentional baseline resets.
```

**FORBIDDEN flags** (rule 46): `--quick`, `--streamlined`, `--lightweight`, `--light`, `--fast`, `--custom`. If user requests, REFUSE with rule-46 explanation. Suggest `--focus <area>` for narrower scope at full depth.

---

## 4. PARALLELIZATION STRATEGY

Multiple audits in the same dispatch:

### Rule-43 Quadruple (Linear ticket)
```
Parallel dispatch (4 work sessions or Agent Teams):
  /codeaudit  --files=$FILES --ticket=$T --url=$URL
  /uiuxaudit  --files=$FILES --ticket=$T --url=$URL
  /flowaudit  --files=$FILES --ticket=$T --url=$URL
  /debugaudit --files=$FILES --ticket=$T --url=$URL

Wait for all 4 to produce .linear-fix/$T/{audit}.json with score=100.
If any < 100: fix-and-reaudit loop per rule 43 step 8b.
```

### Octad (full audit)
```
Phase A (parallel, no dependencies):
  /codeaudit  — full run, produces audits/.codeaudit/verdict.json
  /perfaudit  — full run, produces audits/.perfaudit/verdict.json (CWV measurements)
  /a11yaudit  — full run
  /dataaudit  — full run, produces audits/.dataaudit/verdict.json (schema types)

Phase B (after Phase A completes — reads Phase A outputs):
  /debugaudit   — reads audits/.codeaudit/ (skip phantom-covered findings)
  /seoaudit     — reads audits/.perfaudit/verdict.json for CWV (skip re-measurement)
  /apiaudit     — reads audits/.dataaudit/verdict.json for schema types, produces audits/.apiaudit/verdict.json
  /secaudit     — reads audits/.apiaudit/verdict.json for auth surfaces to exploit

NOTE: /apiaudit runs in Phase B (NOT Phase A) because it consumes /dataaudit output.
      /secaudit also runs in Phase B because it consumes /apiaudit output.
      This is a strict dependency chain: dataaudit → apiaudit → secaudit (sequential within Phase B).

Phase C (parallel, independent of A+B, starts immediately with A):
  /uiuxaudit /flowaudit /featureaudit /motionaudit /copyaudit /dxaudit

Final: /metaudit (if any .md edited).
```

### Non-UI project audit
```
Parallel dispatch (only UI-compatible audits ABORT):
  /codeaudit /dxaudit /copyaudit /perfaudit /secaudit /a11yaudit-partial
  /apiaudit (if API project) /dataaudit (if DB project)

ABORTED (emit graceful skip notices):
  /uiuxaudit /flowaudit /motionaudit /seoaudit

Inform user: "This is a {CLI/library/backend-only/headless} project.
4 audits not applicable, skipped gracefully."
```

---

## 5. AISB (ORACLE-led) FULL-PIPELINE TEMPLATE

When `/aisb full <task>` is invoked:

```
STEP 0: kill-switch + state init (aisb.md)
STEP 1: reformulate prompt (aisb.md §STEP 1)
STEP 2: dispatch ORACLE (aisb.md §STEP 2)

ORACLE then:
  a. Classifies task (SIMPLE/MEDIUM/COMPLEX/EPIC)
  b. Reads ARSENAL-ORCHESTRATION-PLAYBOOK.md §2 routing table
  c. Reads ARSENAL-INTERCONNECTIONS.md §3 for dispatch order
  d. Builds .orchestrator/dispatch-plan.json with:
     - audits_to_run: [...]
     - dispatch_groups: [[group_A], [group_B], [group_C]]
     - scope_flags_per_audit: {...}
     - wait_conditions: {...}
  e. Creates TeamCreate + TaskCreate per audit
  f. Dispatches per group, waiting on dependencies
  g. Monitors .{audit}/progress.json + Telegram channel
  h. On all complete: aggregates verdicts, dedupes per INTERCONNECTIONS §5, reports

STEP 3: report results (aisb.md §STEP 3)
POST-TASK: /debugaudit verification (aisb.md §POST-TASK)
```

---

## 6. GODMODE AUDIT HANDLING

`/godmode` is fully autonomous. When it spawns audits:

```
godmode Phase 2 cycle step 4 (EXECUTE):
  - For each planned audit task:
    - Pre-inline into the agent prompt:
      - Audit name + scope flags
      - References to preamble + interconnections
      - Expected output path (.{audit}/verdict.json)
      - Stop criteria: score >= 80 (solo) or 100 (rule 43)
    - Spawn Agent(subagent_type=<specialist or generic>) or invoke Skill() directly
  - Concurrent audits: use TeamCreate for visibility + SendMessage for coordination
  - Track in ~/.godmode/audits-status.json

godmode Phase 2 cycle step 8 (STUCK DETECTION):
  - If same audit fails 3× with same finding pattern → root cause analysis,
    not more retries (already enforced by 5-iter cap per preamble §4)

godmode Phase 2 cycle step 10 (REPORT):
  - Include audit scores in Telegram milestone updates
  - Highlight any NEEDS_REVIEW items that hit the 5-iter cap
```

---

## 7. METAUDIT INVOCATION TRIGGERS

Run `/metaudit` automatically when:

1. **After any `.md` file in `~/.claude/commands/` is edited** (drift prevention)
2. **At the end of `/aisb full`** (final compliance check)
3. **At rule 43 pipeline step 9** (before moving ticket to "In Review")
4. **On-demand** when user invokes `/metaudit` directly

Metaudit scope flags:
- `/metaudit` — full 20-phase scan
- `/metaudit --focus arsenal` — 14 audits compliance only (fast)
- `/metaudit --focus preamble` — Phase 1 only (hinge point)
- `/metaudit --focus deprecation` — stale refs only
- `/metaudit --focus banned-phrases` — rule 46 scan
- `/metaudit --focus skills` — Skill() call validity

---

## 8. ORACLE DISPATCH CONTRACT

When Oracle dispatches an audit work session, the prompt MUST:

1. **Start with the exact skill invocation on line 1**:
   ```
   /codeaudit --files=src/auth.ts,src/middleware.ts --url=https://example.com/dashboard --scope="auth flow regression" --ticket=DEN-42
   ```
2. **Never paraphrase the audit protocol** — rule 001 enforces this (AUDIT KEYWORD DETECTION).
3. **Include expected output gate**: "On completion, verify `audits/.codeaudit/verdict.json` exists with `score >= 100` and `preamble_version: \"1.0\"`."
4. **Include the interconnections context**: "See ARSENAL-INTERCONNECTIONS.md §1 for ownership boundaries. Do not duplicate findings owned by other audits."
5. **Reference the preamble**: "All contracts in QUALITY-ARSENAL-PREAMBLE.md apply. Emit `preamble_version` in verdict.json."
6. **Pass scope boundaries explicitly**: "Do not expand beyond the specified --files / --url / --scope."

---

## 9. USER COMMUNICATION TEMPLATES

When Oracle reports audit results back to the user:

### Success (single audit)
```
✅ /codeaudit complete — score 100/100 (S, Fortress)
   Scope: 3 files, 1 page
   Findings: 0 CRITICAL, 0 HIGH, 2 MEDIUM, 5 LOW (all auto-fixed)
   Iterations: 2 (fix-and-reaudit loop)
   Duration: 18min
   Report: audits/.codeaudit/verdict.md
   Next: /debugaudit for runtime verification (same scope)
```

### Partial (NEEDS_REVIEW)
```
⚠️ /flowaudit completed with 3 NEEDS_REVIEW items (hit 5-iter cap)
   Score: 92/100 (A, solid)
   Hinge flow intact. Remaining items need human decision:
     1. Onboarding step 3 ambiguity (design choice, not fixable in code)
     2. Payment retry UX (needs business policy)
     3. Dead-end on /settings/advanced (intentional? confirm)
   Report: audits/.flowaudit/verdict.md
   Telegram SOS sent.
```

### Group dispatch (Linear DYNAMIC audit chain)
```
✅ Rule-43 DYNAMIC audit chain complete for DEN-42 (selector chose 5 of 16):
   /codeaudit    100/100 (3 fixes applied)
   /uiuxaudit    100/100 (1 fix applied)
   /flowaudit    100/100 (0 fixes needed)
   /debugaudit   100/100 (2 console warnings silenced)
   /logicaudit   100/100 (1 redundant path removed)
   Adversarial:  confirmed (5 attack attempts blocked)
   Intent Q1-Q5: PASS
   Gate passed:  ticket ready for "In Review: Gareth"
   Comment posted with Before/After screenshots.
```

### Failure (ABORT)
```
🛑 /uiuxaudit aborted — non-UI context detected
   Project type: CLI tool (no visual UI surface)
   Alternatives dispatched automatically:
     /dxaudit (primary for CLIs)
     /copyaudit (help text, error messages)
   Preamble §5 ABORT gate enforced per design.
```

---

## 10. QUICK REFERENCE — "WHICH AUDIT FOR WHAT?"

One-line answer per common question:

| Question | Audit |
|---------|-------|
| "The button doesn't work" | `/debugaudit` + `/flowaudit` |
| "The design looks off" | `/uiuxaudit` + `/a11yaudit` (if contrast/readability) |
| "Site feels slow" | `/perfaudit` |
| "Users can't find what they need" | `/flowaudit` + `/seoaudit` |
| "Can someone hack us?" | `/secaudit` (must follow `/apiaudit` for auth surfaces) |
| "Google isn't ranking us" | `/perfaudit` → `/seoaudit` |
| "Form fields lost data" | `/flowaudit` (Phase 8 data integrity through flow) + `/dataaudit` |
| "API returning wrong shape" | `/apiaudit` |
| "Screen reader doesn't work" | `/a11yaudit` |
| "This animation is distracting" | `/motionaudit` |
| "Headline is unclear" | `/copyaudit` |
| "New devs struggle to onboard" | `/dxaudit` |
| "Database is corrupting" | `/dataaudit` |
| "Is our command system healthy?" | `/metaudit` |

---

*v1.0 — 2026-04-14. Referenced by /aisb, /godmode, /team, rule 43, rule 001-smart-routing.md.*
