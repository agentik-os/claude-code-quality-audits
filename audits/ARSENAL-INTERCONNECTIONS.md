---
name: ARSENAL-INTERCONNECTIONS
description: >
  Complete interconnection map for the 14 Quality Arsenal audits. Defines ownership
  boundaries (no duplicate findings), dispatch-order constraints, input/output contracts
  between audits, shared finding types with routing rules, and parallel-dispatch groups.
  Referenced by /aisb, /metaudit, rule 43 Linear pipeline, and Oracle orchestrators.
  NOT a user-invokable skill — shared source of truth, like QUALITY-ARSENAL-PREAMBLE.md.
---

# Quality Arsenal — Interconnections Map v1.0

> *"Each audit is a lens. Together they must focus, not interfere."*

---

## 1. WHAT EACH AUDIT OWNS (single-source ownership — no duplicates)

| Audit | Primary question | Owns exclusively |
|-------|-----------------|-------------------|
| `/codeaudit` | Is the code SOLID? | SOLID violations, phantom imports, circular deps, dead code, contract drift, git safety, fix-gate smoke tests for integrations |
| `/debugaudit` | What is BROKEN right now? | Runtime console errors, network failures mid-flow, visual regressions, chaos-mode fuzzing, authenticated-state behavior |
| `/uiuxaudit` | Is the interface COHERENT? | Visual coherence (color/typography/spacing), Gestalt principles, design-system adherence, AI-generic smells, dark-mode parity |
| `/flowaudit` | Does the EXPERIENCE work? | User journeys, state-machine integrity, dead ends, promise-vs-experience (runtime), error recovery paths, onboarding |
| `/featureaudit` | Is the product COMPLETE? | PRD coverage, feature parity with competitors, inferred-vs-explicit PRD fallback, WebSearch-bounded parity research |
| `/perfaudit` | Is it FAST enough? | Core Web Vitals measurement, bundle size, render timing, memory profiling, perf regressions vs baseline |
| `/secaudit` | Is it SECURE? | OWASP Top 10 exploitation, XSS/SQLi/SSRF/IDOR probes, auth bypass, privilege escalation, rate-limit-safe fuzzing |
| `/a11yaudit` | Is it ACCESSIBLE? | WCAG 2.1 AA, keyboard nav, ARIA, screen-reader automation, RTL/i18n layout, reduced-motion |
| `/seoaudit` | Is it DISCOVERABLE? | Crawlability, indexability, meta tags, Schema.org markup, GEO (AI-search optimization), content decay |
| `/copyaudit` | Is the COPY clear? | Word-level tone, claim clarity (static), CTA text, jargon, banned-phrase scan, i18n wrapping |
| `/dxaudit` | Is the DX smooth? | README quality (20-item rubric), setup time (external runner), error messages, dev-loop UX |
| `/motionaudit` | Is motion PURPOSEFUL? | CSS/JS/WebGL/P5/Lottie/video/GIF animation audit, purpose classification, reduced-motion compliance |
| `/dataaudit` | Is the DATA intact? | Schema validation, migration safety (DB backup gate), orphan records, referential integrity, data sampling |
| `/apiaudit` | Is the API solid? | REST/GraphQL contract compliance, auth middleware presence, rate-limit specs, inference-mode labeling |

**Rule:** A given finding has exactly ONE owner. If two audits disagree, the ownership table wins.

---

## 2. OWNERSHIP CONFLICTS & RESOLUTIONS

Cases where the boundary was fuzzy — now formally resolved:

| Concern | Conflict | Resolution |
|---------|---------|------------|
| **Core Web Vitals** | `/perfaudit` measures, `/seoaudit` cares about ranking impact | `/perfaudit` MEASURES + OWNS REMEDIATION. `/seoaudit` READS `audits/.perfaudit/verdict.json` (if <24h old) and scores only the SEO-ranking-impact dimension. No re-measurement. |
| **Auth security** | `/apiaudit` static-checks auth middleware, `/secaudit` exploits it | `/apiaudit` owns STATIC auth correctness. `/secaudit` owns RUNTIME exploitation. Shared finding if both agree = CRITICAL elevation. |
| **Promise vs experience** | `/flowaudit` checks runtime, `/copyaudit` checks static text | `/copyaudit` owns WORD-level (tone, jargon, 5-second test). `/flowaudit` owns LABEL-vs-ACTION at runtime. Duplicate file:line → prefer `/flowaudit` (behavior > text). |
| **i18n wrapping** | `/a11yaudit` + `/copyaudit` both care | `/copyaudit` owns wrapping detection (hardcoded string regex). `/a11yaudit` owns rendered-locale verification (RTL, pluralization). |
| **Dead ends** | `/flowaudit` owns, `/uiuxaudit` sometimes notices | `/flowaudit` exclusively. If `/uiuxaudit` notices a dead end, emit as a `/flowaudit`-routed finding (cross-audit hand-off). |
| **Banned phrases** | `/copyaudit` scans copy, `/metaudit` scans commands | `/copyaudit` scans user-facing copy. `/metaudit` scans `.md` configuration files. No overlap (different target surfaces). |
| **Error messages** | `/dxaudit` (helpful?), `/copyaudit` (clear?), `/debugaudit` (accurate?) | `/dxaudit` owns HELPFULNESS (actionable, diagnosable). `/copyaudit` owns CLARITY (plain language). `/debugaudit` owns ACCURACY (matches actual error). Rare 3-way overlap = same underlying error string — elevate to CRITICAL. |
| **Non-UI contexts** | Who audits a CLI? | `/codeaudit`, `/dxaudit` (primary), `/copyaudit` (help text), `/secaudit`, `/perfaudit`, `/dataaudit`, `/apiaudit`. ABORT list: `/uiuxaudit`, `/flowaudit`, `/motionaudit`, `/seoaudit`. |

---

## 3. DISPATCH ORDER CONSTRAINTS

Some audits depend on others' outputs. Dispatch order matters when running them together.

### Strict ordering (dependent audits)

```
/perfaudit   →  /seoaudit         (/seoaudit reads audits/.perfaudit/verdict.json for CWV scoring)
/apiaudit    →  /secaudit         (/secaudit exploits the contract /apiaudit documented)
/codeaudit   →  /debugaudit       (fix code phantoms before looking for runtime bugs)
/dataaudit   →  /apiaudit         (schema defines API response shape)
/codeaudit   →  /dataaudit        (model types define schema)
```

### Independent (can run in parallel)

Any audit not in the strict chain above can run in parallel with others, subject to concurrency locks (preamble §3) and distinct `.{audit}/` output directories.

### The Rule-43 Quadruple (Linear ticket pipeline)

For Linear ticket resolution (per `~/.claude/docs/rules-archive/43-linear-ticket-pipeline.md` Step 8):

```
Parallel dispatch (same ticket, same files_modified, same page_url):
  /codeaudit  --files={files} --ticket={T} --url={url}
  /uiuxaudit  --files={files} --ticket={T} --url={url}
  /flowaudit  --files={files} --ticket={T} --url={url}
  /debugaudit --files={files} --ticket={T} --url={url}

Each writes to: .linear-fix/{TICKET}/{audit}.json
Threshold: each = 100/100 (rule 43 step 8b fix-and-reaudit until 100)
```

The dynamic audit chain (4-12 audits selected by audit-selector.py) is safe to parallelize because:
- Each writes to a ticket-specific distinct path (no output collision)
- Each concurrency-locks its own `.{audit}/.lock` (no same-audit collision)
- No output dependency between them (CWV deferral rule applies elsewhere)

### The `/aisb full` / `/godmode` octad (broad verification)

For comprehensive verification across a project, run 8 parallel audits grouped by independence:

```
Group 1 (independent): /codeaudit, /perfaudit, /secaudit, /a11yaudit
Group 2 (depends on Group 1): /debugaudit, /seoaudit, /dataaudit, /apiaudit
Group 3 (independent of 1+2): /uiuxaudit, /flowaudit, /featureaudit, /motionaudit, /copyaudit, /dxaudit
```

Dispatch: Group 1 → wait for /codeaudit + /perfaudit + /apiaudit + /dataaudit completion → Group 2. Group 3 runs parallel to 1+2.

---

## 4. INPUT / OUTPUT CONTRACTS BETWEEN AUDITS

Machine-readable handoffs documented here:

| Producer | Consumer | File | Contents |
|----------|---------|------|----------|
| `/perfaudit` | `/seoaudit` | `audits/.perfaudit/verdict.json` | `{phases: [{id: 6, name: "CWV", metrics: {lcp, fid/inp, cls, ttfb}}]}` — /seoaudit reads `metrics` and scores ranking impact |
| `/apiaudit` | `/secaudit` | `audits/.apiaudit/verdict.json` | `{findings: [{type: "auth_check_missing", endpoint: "..."}]}` — /secaudit elevates to CRITICAL if exploit confirmed |
| `/codeaudit` | `/debugaudit` | `audits/.codeaudit/verdict.json` | `{findings: [{type: "phantom_import", file: "..."}]}` — /debugaudit skips console-error findings already covered |
| `/dataaudit` | `/apiaudit` | `audits/.dataaudit/verdict.json` | Schema type info — /apiaudit validates REST/GraphQL response shape matches |
| Any audit | `/metaudit` | `.{audit}/verdict.json` | `preamble_version`, `compliance_score`, `skill_used` — /metaudit's Phase 1 compliance check |

**Contract violation** (e.g., /seoaudit running without /perfaudit's output despite expecting it) → /seoaudit either runs its own CWV measurement (fallback) or emits a warning in verdict.md. Never fails silently.

---

## 5. SHARED FINDING TYPES & ROUTING

Some finding types appear across multiple audits. Routing rules:

| Finding type | Audits that detect | Routing rule |
|-------------|-------------------|--------------|
| **Banned phrase (rule 46)** | `/copyaudit` (user copy), `/metaudit` (command config) | `/copyaudit` owns user-facing copy. `/metaudit` owns `.md` configuration. Different targets = no dedupe. |
| **Stale Skill() ref** | `/metaudit` (exclusively) | Only `/metaudit` scans command files. |
| **Dead end in flow** | `/flowaudit` (exclusively) | `/uiuxaudit` notices → forward to `/flowaudit` queue. |
| **Auth bypass** | `/apiaudit` (static), `/secaudit` (runtime) | Both can emit. Shared agreement = CRITICAL. |
| **Regression vs baseline** | `/perfaudit` (perf), `/debugaudit` (visual), `/seoaudit` (ranking) | Each owns its own baseline file. |
| **Integration broken post-fix** | ANY code-touching audit via Phase 23 smoke gate | First audit to detect aborts the fix + reverts. Others inherit revert state. |
| **Broken screenshot / 4xx-5xx page** | `/debugaudit` ABORTS (preamble §5) | NEVER marked as "pass with warning" — ABORT is the only correct response. |

---

## 6. HANDOFF LIFECYCLE (what flows between audits during a full run)

```
                 ┌──────────────────┐
                 │   /aisb / Oracle │
                 └────────┬─────────┘
                          │ dispatch
                          ▼
          ┌──────────────────────────────────┐
          │  Group 1 (no deps, parallel)     │
          │  /codeaudit  /perfaudit          │
          │  /secaudit   /a11yaudit          │
          │  /dataaudit  /apiaudit (partial) │
          └───┬────────┬─────┬────────┬──────┘
              │        │     │        │
              ▼        ▼     ▼        ▼
          ┌──────────────────────────────────┐
          │  Handoff files                   │
          │  audits/.codeaudit/verdict.json         │
          │  audits/.perfaudit/verdict.json (CWV)   │
          │  audits/.dataaudit/verdict.json (types) │
          │  audits/.apiaudit/verdict.json (partial)│
          └───┬──────────────────────────────┘
              │ consumed by
              ▼
          ┌──────────────────────────────────┐
          │  Group 2 (depends on Group 1)    │
          │  /debugaudit (reads codeaudit)   │
          │  /seoaudit   (reads perfaudit)   │
          │  /apiaudit   (reads dataaudit)   │
          │  /secaudit   (reads apiaudit)    │
          └──────────────────────────────────┘

          ┌──────────────────────────────────┐
          │  Group 3 (fully independent,     │
          │  runs parallel to 1+2)           │
          │  /uiuxaudit  /flowaudit          │
          │  /featureaudit /motionaudit      │
          │  /copyaudit   /dxaudit           │
          └──────────────────────────────────┘
                          │
                          ▼
          ┌──────────────────────────────────┐
          │  /metaudit (compliance check)    │
          │  Verifies all 14 wrote verdicts  │
          │  with preamble_version="1.0"     │
          └──────────────────────────────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Final verdict   │
                 │  to Oracle/User  │
                 └──────────────────┘
```

---

## 7. ANTI-PATTERNS (what NOT to do)

1. **Never run audits sequentially when they're independent** — wastes days instead of hours.
2. **Never dispatch a dependent audit before its producer** — `/seoaudit` before `/perfaudit` = duplicate CWV work.
3. **Never combine audits into a single "audit" worker** — per rule 001, always invoke specific skills.
4. **Never interpret 403/401 as a pass** — preamble §5 ABORT rule is absolute.
5. **Never mark an audit "done" without output-gate verification** — check files exist with valid schemas.
6. **Never run without scoped flags when rule 43 requires them** — `--url`, `--ticket`, `--files` are MANDATORY for Linear pipeline.
7. **Never duplicate findings across audits** — ownership table (§1) wins, cross-forward if one audit notices another's turf.
8. **Never skip `/metaudit` after touching any command `.md` file** — drift starts immediately.
9. **Never run a `/uiuxaudit` / `/flowaudit` / `/motionaudit` / `/seoaudit` on a non-UI project** — ABORT per preamble §5.
10. **Never run two instances of the same audit simultaneously on the same project** — concurrency lock blocks, but don't even try.

---

## 8. HOW /aisb AND ORACLES PICK AUDITS

When a task arrives, Oracle classifies it and picks the minimal audit set:

| Task signal | Audits to dispatch |
|-------------|-------------------|
| "fix this bug" + specific file | `/codeaudit --files=... --focus=<area>` + `/debugaudit --url=... --files=...` |
| "build is slow" | `/perfaudit` (solo) |
| "security concern" on endpoint | `/apiaudit --url=... --focus=auth` → if findings → `/secaudit --url=...` |
| "redesign the dashboard" | `/uiuxaudit` + `/flowaudit` + `/a11yaudit` (parallel) |
| "audit everything" / "full audit" / "audit complet" | All 14 via Group 1→2 + Group 3 parallel |
| "check accessibility" | `/a11yaudit` (solo) |
| "SEO review" | `/perfaudit` then `/seoaudit` |
| Linear ticket (rule 43) | Quadruple: `/codeaudit` + `/uiuxaudit` + `/flowaudit` + `/debugaudit` — all --ticket-scoped |
| "audit the commands" / "audit the audits" | `/metaudit` (solo) |
| "check if my CLI has UX issues" | `/dxaudit` + `/copyaudit` (NEVER `/uiuxaudit` on a CLI) |

Full routing table: `~/.claude/commands/ARSENAL-ORCHESTRATION-PLAYBOOK.md`.

---

## 9. THE META-LAW

> **One doctrine, fourteen implementations, zero drift, fifteen lenses when /metaudit is included.**

- One `QUALITY-ARSENAL-PREAMBLE.md` (shared doctrine)
- Fourteen audit `.md` files (each with compliance block + 100/100 certificate)
- One `ARSENAL-INTERCONNECTIONS.md` (this file — relationships)
- One `ARSENAL-ORCHESTRATION-PLAYBOOK.md` (how to dispatch)
- One `/metaudit` command (compliance enforcement)

Together: **a coherent Quality Arsenal, not 14 isolated tools.**

---

*v1.0 — 2026-04-14. Referenced by all audits, /metaudit, /aisb, /godmode, rule 43, rule 001.*

---

## 10. SIGNAL-BASED AUTO-DISPATCH (intelligence upgrade — preamble v1.1 §16)

Beyond keyword matching, Oracle reads project signals before dispatching:

```
package.json deps detected → auto-focus
  convex       → /dataaudit (Convex schema), /apiaudit (Convex functions)
  @clerk/*     → /secaudit --focus=auth, /flowaudit --focus=auth-flow
  stripe       → /flowaudit --focus=payment, /secaudit --focus=payment-security
  next-intl    → /copyaudit --focus=i18n, /a11yaudit --focus=rtl
  framer-motion → /motionaudit relevant
  prisma       → /dataaudit + /apiaudit (schema → contract chain)
  no react/vue → ABORT UI audits, route to /dxaudit + /copyaudit
```

Emit `project_signals_detected` in every verdict.json (preamble v1.1 §16).

## 11. ARSENAL EXPANSION CANDIDATES

Three gaps no current audit covers:

| Proposed | Owns | Gap between |
|----------|------|-------------|
| /i18naudit | String extraction, locale completeness, date/number format, full RTL | /copyaudit (hardcoded strings) ↔ /a11yaudit (rendered locale) |
| /cicdaudit | Build trends, DORA metrics, secret management, artifact caching | /dxaudit (static CI config) → runtime CI health |
| /costaudit | Unbounded API calls, spend caps, runaway crons, serverless waste | No current audit covers billing exposure |

Build when a project hits the gap. Not mandated.

---

*v1.1 — 2026-04-14. Added §10 signal-based dispatch + §11 expansion candidates.*
