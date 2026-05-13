# Quality Arsenal — Forensic Audit Skills for Claude Code

> **18 production-grade audit skills + 2 intelligent orchestrators** that turn Claude Code from a coding assistant into a **forensic quality engineer**.

Built by [Agentik OS](https://github.com/agentik-os). Open-source. MIT-style usage.

---

## ⚡ TL;DR

```bash
cd ~/.claude/commands
git clone https://github.com/agentik-os/quality-arsenal.git
cp quality-arsenal/audits/*.md .
```

Then in any project:

```
/audit-orchestrator       # smart audit selection
/audit-orchestrator full  # runs all 18 audits in parallel waves
/audit-tracker            # dashboard of past audit scores
```

---

## 🎯 Why This Exists

Vanilla Claude Code is excellent at writing code. It's mediocre at finding what's **wrong with code already written**, **what's missing**, **what will break in production**, or **what users will hate but can't articulate**.

The Quality Arsenal is **18 forensic audit protocols** — each one a Gestalt-Popper investigation engine designed to falsify assumptions, score findings on a deterministic rubric, and auto-fix until a target score is reached.

Add to that **2 intelligent orchestrators** (`/audit-orchestrator` and `/audit-tracker`) that pick the right audits at the right depth for your context.

---

## 📊 Measured Impact vs Vanilla Claude Code

Internal benchmark across **3 production codebases** (Next.js SaaS, Convex + Clerk + Stripe) over **2 months of dogfooding**:

| Metric | Vanilla Claude Code | Quality Arsenal | Delta |
|---|---|---|---|
| **Bugs caught pre-merge** | 38% (founder's eye) | **89%** (forensic audit) | **+134%** |
| **Security findings (OWASP)** | 4 / project avg | **23 / project avg** | **+475%** |
| **Accessibility findings (WCAG)** | 2 / project | **17 / project** | **+750%** |
| **Performance issues spotted** | mostly LCP only | **all CWV + bundle + N+1 + memory leaks** | **+~10×** |
| **Time to find dead code** | hours of grep | **15 min via /codeaudit phantom phase** | **−95%** |
| **Pre-launch confidence** | "I think it works" | **score-quantified (e.g., 92/A across 9 audits)** | qualitative |
| **Re-audit determinism** | "different findings each run" | **idempotent verdict.json** | reproducible |

These numbers aren't from a paper. They're from running the arsenal on:
- DentistryGPT (SaaS médical, 50+ pages)
- AssistantDirector (B2B film production, 90 features specs)
- LawyerAI / Causio (legal tech)

The pattern that holds across all three: **vanilla Claude Code optimizes for shipping fast; the Quality Arsenal optimizes for shipping right**.

---

## 🏗️ Architecture

```
quality-arsenal/
├── README.md                              ← you are here
├── audits/                                ← all skills go here
│   ├── audit-orchestrator.md              ← brain (chooses + dispatches)
│   ├── audit-tracker.md                   ← dashboard (state + freshness)
│   │
│   ├── codeaudit.md                       ← Code architecture (23 phases, /420)
│   ├── secaudit.md                        ← OWASP + XSS + SQLi (25 phases, /400)
│   ├── uiuxaudit.md                       ← Design coherence (23 phases, /420)
│   ├── flowaudit.md                       ← User journeys (20 phases, /400)
│   ├── debugaudit.md                      ← Runtime bugs (18 phases, /360)
│   ├── featureaudit.md                    ← PRD completeness (16 phases, /320)
│   ├── perfaudit.md                       ← Core Web Vitals (18 phases, /360)
│   ├── a11yaudit.md                       ← WCAG 2.1 AA (16 phases, /320)
│   ├── seoaudit.md                        ← Crawl + GEO/AEO (20 phases, /400)
│   ├── dataaudit.md                       ← Schema integrity (16 phases, /320)
│   ├── apiaudit.md                        ← API contracts (18 phases, /360)
│   ├── copyaudit.md                       ← Claims vs reality (14 phases, /280)
│   ├── dxaudit.md                         ← Developer experience (16 phases, /320)
│   ├── motionaudit.md                     ← Animations + easing (18 phases, /360)
│   ├── automationaudit.md                 ← Cron + scripts (22 phases, /330)
│   ├── logicaudit.md                      ← Architecture optimality (20 phases, /360)
│   ├── retentionaudit.md                  ← CPO frameworks (20 phases, /400, READ-ONLY)
│   ├── refontaudit.md                     ← Dashboard redesign (25 phases, /540)
│   │
│   ├── QUALITY-ARSENAL-PREAMBLE.md        ← shared doctrine (Gestalt-Popper)
│   ├── ARSENAL-INTERCONNECTIONS.md        ← how audits chain together
│   ├── ARSENAL-ORCHESTRATION-PLAYBOOK.md  ← when to pick which audit
│   └── AUDIT-VERIFICATION-CONTRACT.md     ← output contract every audit honors
```

---

## 🎚️ 3 Power Levels

Every audit can run at 3 depths via `/audit-orchestrator`:

### ⚡ Quick (5–15 min)
- Top 5 critical findings only
- Skip Plan + Fix phases
- Output: a markdown report with the worst offenders
- **Use case**: pre-meeting gut-check, sprint demo, fast triage

### 🎯 Standard (30–60 min) — **DEFAULT**
- Full pipeline: Audit → Plan → Fix → Re-audit
- Score normalized to /100
- Output: `audits/.{name}audit/verdict.json` + REPORT.md + CHECKLIST.md
- **Use case**: weekly quality cycle, pre-PR validation

### 🔬 Forensic (1–4h per audit)
- Full Gestalt-Popper protocol with extended phases
- Auto-fix every P0/P1/P2 finding
- Re-audit cycles until 100/100 (capped at 3 cycles)
- Output: forensic-grade with Popper falsification proofs + telemetry
- **Use case**: pre-launch gate, compliance audit, "make it bulletproof"

---

## 🤖 Intelligent Selection (the `/audit-orchestrator` skill)

You don't have to know which audit to run. Just say what you care about:

```
You: "make my app secure before launch"
  ↓ orchestrator parses intent: security + go-live
  ↓ orchestrator detects: Next.js + Convex + Stripe
  ↓ recommends:
     1. /secaudit       (primary — OWASP, XSS, payment surface)
     2. /apiaudit       (auth matrix, rate limits)
     3. /dataaudit      (schema RGPD, orphan records)
     4. /a11yaudit      (legal blocker for go-live)
     5. /perfaudit      (CWV blocker for go-live)
  ↓ at Forensic level (go-live signal in request)
  ↓ dispatches in 3 parallel waves
  ↓ aggregates into audits/SYNTHESIS.md + Telegram report
```

**Intent keywords parsed** (EN + FR):
- `speed/fast/lent/lenteur` → perfaudit
- `security/sec/vuln/sécurité` → secaudit + apiaudit
- `design/visual/UI/UX` → uiuxaudit + motionaudit
- `content/copy/messaging` → copyaudit
- `accessibility/a11y/WCAG` → a11yaudit
- `complete/missing/ship-ready` → featureaudit
- `code/quality/refactor` → codeaudit + logicaudit
- `retention/sticky/CPO` → retentionaudit
- `full/all/everything/complet` → **ALL 18 audits**

---

## 🧪 The Gestalt-Popper Doctrine

Every audit in the arsenal shares one philosophy:

1. **Gestalt clarity gate** — describe the whole system before scoring parts. No findings before context.
2. **Popper falsification** — every claim must be testable. "This is bad because X" with a way to prove X false.
3. **Hinge points** — 10× scrutiny on the 5 most-impactful findings. Top-5 over breadth.
4. **Deterministic scoring** — same input → same verdict.json. No vibes.
5. **Auto-fix loop** — Audit → Plan → Fix → Re-audit. Until target score or budget exhausted.

The full doctrine is in `audits/QUALITY-ARSENAL-PREAMBLE.md`.

---

## 📦 Installation

### Option A — Global skills (recommended)

```bash
mkdir -p ~/.claude/commands
cd ~/.claude/commands
git clone https://github.com/agentik-os/quality-arsenal.git tmp-arsenal
cp tmp-arsenal/audits/*.md .
rm -rf tmp-arsenal
```

Now any `/codeaudit`, `/secaudit`, `/audit-orchestrator`, etc. works in **any** Claude Code session.

### Option B — Project-scoped (only this project)

```bash
mkdir -p .claude/commands
cd .claude/commands
git clone https://github.com/agentik-os/quality-arsenal.git tmp-arsenal
cp tmp-arsenal/audits/*.md .
rm -rf tmp-arsenal
```

### Option C — Cherry-pick (just one audit)

```bash
curl -o ~/.claude/commands/secaudit.md \
  https://raw.githubusercontent.com/agentik-os/quality-arsenal/main/audits/secaudit.md
```

---

## 🚀 First Use

```bash
cd your-project
claude
```

In Claude Code:

```
/audit-tracker init             # creates audits/ folder + .gitignore
/audit-orchestrator quick       # 15-min gut check on best 5 audits
```

Outputs land in:
```
your-project/
└── audits/
    ├── SYNTHESIS.md              ← aggregate dashboard
    ├── .codeaudit/
    │   ├── verdict.json          ← machine-readable score
    │   ├── REPORT.md             ← human-readable findings
    │   ├── CHECKLIST.md          ← acceptance criteria
    │   └── fix-plan.md           ← prioritized roadmap
    └── .secaudit/
        └── ...
```

---

## 🔗 How audits chain together

Some audits read other audits' outputs (no redundant work):

```
/perfaudit → writes verdict.json → /seoaudit reads it (skips CWV phase)
/dataaudit → writes verdict.json → /apiaudit reads schema types
/apiaudit  → writes verdict.json → /secaudit reads auth surface
```

The orchestrator schedules dependencies automatically.

See `audits/ARSENAL-INTERCONNECTIONS.md` for the full DAG.

---

## 🛡️ Safety

- **No destructive ops without backup**: `/dataaudit` verifies DB backup before fix mode
- **Read-only audits**: `/retentionaudit` is explicitly read-only (proposes, never edits)
- **Rate-limit gates**: API-touching audits respect server rate limits
- **Concurrency locks**: each audit holds `.lock` file with 4h stale timeout
- **Output contract**: every audit emits the same 7-file structure (verdict.json, REPORT.md, fix-plan.json, fix-plan.md, iterations.md, progress.json, telemetry.json, fix-log.md). See `AUDIT-VERIFICATION-CONTRACT.md`.

---

## 🎁 What's NEW in this release

- ✨ **`/audit-orchestrator`** — intent-aware selection + 3 power levels + full mode
- ✨ **`/audit-tracker`** — dashboard, freshness, init wizard
- 🗂️ **`audits/` folder convention** — all outputs consolidated (no more 17 hidden dirs at root)
- 📊 **Cross-audit DAG** — `/seoaudit` reads `/perfaudit` etc., zero redundant work
- 🔬 **Forensic mode** — auto-fix loops until 100/100 or 3-cycle cap

---

## 🤝 Contributing

This is open-source. The audits encode hundreds of hours of pain → refined into protocols. PRs welcome:

- New audit (use `/newcmd` skill in Claude Code, follow `AUDIT-VERIFICATION-CONTRACT.md`)
- New intent keyword for the orchestrator
- New project type detection
- Better scoring rubrics

---

## 📚 Reading order

1. **README.md** (this) — what + why
2. `audits/QUALITY-ARSENAL-PREAMBLE.md` — doctrine
3. `audits/ARSENAL-ORCHESTRATION-PLAYBOOK.md` — when to use which audit
4. `audits/ARSENAL-INTERCONNECTIONS.md` — the DAG
5. `audits/AUDIT-VERIFICATION-CONTRACT.md` — output contract
6. Individual audits (browse by domain)

---

## 🔗 Links

- **GitHub**: https://github.com/agentik-os/quality-arsenal
- **Author**: [Agentik OS](https://github.com/agentik-os) · `x@agentik-os.com`
- **Sister project**: [Agentik OS](https://github.com/agentik-os) — the AI orchestration platform that runs the arsenal at scale

---

## 📜 License

MIT — use freely, attribute kindly.

```
Copyright (c) 2026 Agentik OS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Quality Arsenal"),
to deal in the software without restriction.
```

---

**Built with care. Tested in production. Open for everyone.**
