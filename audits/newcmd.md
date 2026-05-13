---
name: newcmd
description: >
  Skill engineering lab. Creates production-grade commands with Quality DNA: Gestalt clarity gate,
  strong identity, scope detection, input/output contracts, verification gates, and full Omega
  registration (Oracle, Telegram, SMITH). For audits: adds Popper falsification + scoring.
  Use when user says "/newcmd", "create a command", "new skill", "new audit", "forge".
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Agent"]
---

# /newcmd — Skill Engineering Lab

> *"A mediocre skill is worse than no skill — it teaches the system bad habits."*

---

## PHILOSOPHY: THE QUALITY DNA

Every skill created by /newcmd carries the same DNA. Not because of bureaucracy — because it works.

**Gestalt Clarity** applies to ALL skills (not just audits):
- Understand BEFORE acting. A skill that jumps into execution without understanding context produces generic garbage.
- Every skill has a HINGE MOMENT — the single decision/output that determines if the entire skill succeeded or failed. Identify it. Nail it.
- One question resolves more than ten assumptions.

**Popper Falsification** applies to AUDIT skills only:
- Don't verify. Falsify. Prove it lies.
- Every claim is a hypothesis. Test it.

**The result:** Skills that feel like they were written by a domain expert who's done this 1000 times, not an AI following a template.

---

## SKILL TYPES & QUALITY DNA

### TYPE 1: FORENSIC AUDIT (scored, multi-phase, auto-fix)

```
Examples: /codeaudit, /debugaudit, /perfaudit, /secaudit
DNA: Gestalt + Popper
Structure: 15-25 phases, scoring /300-450, auto-fix, re-audit
```

### TYPE 2: CREATIVE PIPELINE (multi-stage, iterative)

```
Examples: /gestalt, /deepux, /brand-identity, /vision
DNA: Gestalt (clarity → research → structure → polish)
Structure: 3-5 sequential stages, each gate-checked
```

### TYPE 3: WORKFLOW ORCHESTRATOR (multi-step, dependencies)

```
Examples: /build, /new, /planner, /linear-fix
DNA: Gestalt (understand → plan → execute → verify)
Structure: Sequential steps, rollback plan, completion gate
```

### TYPE 4: FOCUSED TOOL (single purpose, fast)

```
Examples: /reader, /tunnel, /switch, /prompt
DNA: Gestalt-lite (scope detection, clear output)
Structure: Input → Process → Output, minimal ceremony
```

---

## THE UNIVERSAL QUALITY DNA (ALL skills MUST have)

Every skill, regardless of type, MUST have these 8 elements:

### DNA-1: IDENTITY (who am I?)
```markdown
# /name — Title

> *"Punchy one-liner that captures the skill's mindset"*

## IDENTITY
You are not a {generic role}. You are a {specific expert persona}.
{2-3 sentences establishing expertise, taste, and standards.}
```

**Why:** Without identity, the skill behaves like a generic assistant. With it, it behaves like a specialist.

### DNA-2: SCOPE DETECTION (what does the user want?)
```markdown
## SCOPE DETECTION (automatic from user prompt)
Parse the user's intent. No clarification needed for common patterns.

"/{name}"              → Full pipeline, default scope
"/{name} [target]"     → Scoped to specific target
"/{name} [problem]"    → Focused on the described problem
"/{name} --focus {area}"  → Narrower scope with full depth (rule 46: no --quick)
```

**Why:** A skill that always asks "what do you want?" wastes the user's time. Parse intent, ask only when genuinely ambiguous.

### DNA-3: HINGE MOMENT (what's the ONE thing that matters most?)
```markdown
## HINGE MOMENT
Before executing, identify the single output/decision/element
that determines if this skill succeeded or failed.
Allocate 50% of effort to the hinge moment, 50% to everything else.
```

**Why:** Equal effort across all steps produces mediocre everything. Concentrated effort on the hinge produces excellence where it matters.

### DNA-4: INPUT/OUTPUT CONTRACT (what goes in, what comes out?)
```markdown
## OUTPUT CONTRACT
Clearly define:
- What files/artifacts are created
- Where they're saved
- What format they use
- What the user should do with them
```

**Why:** A skill that produces output the user can't find or use is useless.

### DNA-5: PROGRESSIVE DEPTH (simple → advanced)
```markdown
## USAGE
Simple:   /{name}                → Default behavior, sensible defaults
Targeted: /{name} [scope]        → Focused on specific area  
Advanced: /{name} --deep [scope] → Maximum depth, all options
```

**Why:** New users need simplicity. Power users need depth. Both from the same command.

### DNA-6: VERIFICATION GATE (did it actually work?)
```markdown
## VERIFICATION
Before reporting done:
- [ ] Output exists and is well-formed
- [ ] Build/compile/import passes (if code was changed)
- [ ] The hinge moment was nailed (not just attempted)
```

**Why:** "Done" without verification is a lie. Every skill self-checks.

### DNA-7: INTEGRATION (how does it connect to the ecosystem?)
```markdown
## ECOSYSTEM INTEGRATION
- When to use BEFORE this skill: {prerequisites}
- When to use AFTER this skill: {next steps}
- Related skills: {complementary commands}
```

**Why:** Skills in isolation are tools. Skills in context are a system.

### DNA-8: DOMAIN EXPERTISE (not generic — specific)
```
The skill must contain domain-specific knowledge that a generic 
assistant wouldn't have. Specific checks, specific patterns, 
specific best practices, specific anti-patterns.

BAD:  "Check if the code is good"
GOOD: "Check if N+1 queries exist by scanning for loops that 
       call database queries. Pattern: for item in items: db.get(item.related_id)"
```

**Why:** Generic instructions produce generic results. Specific instructions produce expert results.

---

## ADDITIONAL DNA FOR AUDIT SKILLS (Type 1 only)

On top of the 8 universal DNA elements, audit skills add:

### AUDIT-DNA-1: POPPER FALSIFICATION
```
Don't verify it works. Prove it LIES.
Every phase asks: "where does this claim diverge from reality?"
Falsification categories specific to the domain.
```

### AUDIT-DNA-2: SCORING MATRIX
```
Each phase scored 0-10, weighted by user impact.
Total 300-450 points. Normalized to /100. Letter grade S-F.
```

### AUDIT-DNA-3: AUTO-FIX PIPELINE
```
Phase N+1: Generate fix plan (prioritized by severity)
Phase N+2: Execute fixes (sequential, with rollback)  
Phase N+3: Re-audit (verify fixes, detect regressions)
```

### AUDIT-DNA-4: PARALLEL EXECUTION
```
Group phases into 4-5 waves for maximum parallelism.
Wave 1: Discovery (sequential)
Wave 2-3: Analysis (parallel agents)
Wave 4: Verdict + Fix (sequential)
```

---

## PROCESS

### Step 1: UNDERSTAND
Ask 1-2 questions max. Determine:
- Domain and purpose
- Type (audit / creative / workflow / tool)
- Expected output

### Step 2: RESEARCH
Before writing a single line:
- Read 2-3 existing skills of the same type for structural reference
- Identify domain best practices (what would a world expert check?)
- Identify the HINGE MOMENT for this domain

### Step 3: GENERATE
Write the skill file applying ALL Quality DNA elements.
File should be:
- Audit: 500-800 lines (comprehensive, forensic)
- Creative: 300-500 lines (stages, examples, quality gates)
- Workflow: 200-400 lines (steps, dependencies, verification)
- Tool: 100-200 lines (focused, fast, clear)

### Step 4: REGISTER IN OMEGA

**Mandatory for ALL skills:**

1. **Oracle routing** — `~/.claude/rules/001-smart-routing.md`
   Add to Key Routes table with trigger patterns

2. **CLAUDE.md** — `~/CLAUDE.md`
   Add to appropriate table

3. **AISB Telegram bot** — 3 files:
   - `bot/aisb/handlers.py` → SKILL_COMMANDS dict + aliases
   - `bot/aisb/commands.py` → help text
   - `bot/aisb/prompts.py` → oracle skills list

4. **AISB docs** (audits only):
   - `~/.aisb/docs/ARCHITECTURE.md` → command table
   - `~/.aisb/docs/ORCHESTRATION.md` → command table

5. **Verify:**
   ```bash
   cd ~/VibeCoding/work/agentik-monitor/bot && source venv/bin/activate
   python -c "from aisb.handlers import SKILL_COMMANDS; print('{name}' in SKILL_COMMANDS)"
   ```

### Step 5: QUALITY GATE

Before reporting done:
- [ ] File exists and contains ALL applicable DNA elements
- [ ] Identity is specific (not generic)
- [ ] Scope detection handles 3+ patterns
- [ ] Hinge moment is identified and emphasized
- [ ] Domain expertise is specific (not "check if good")
- [ ] Output contract is clear
- [ ] Verification gate exists
- [ ] Bot imports pass after registration
- [ ] At least 2 trigger phrases in description

### Step 6: REPORT

```
Command: /{name}
Type:    {audit | creative | workflow | tool}
DNA:     {8/8 universal + N/4 audit-specific}
Hinge:   {the ONE thing that determines success}
File:    ~/.claude/commands/{name}.md ({N} lines)
Omega:   Oracle ✓ | CLAUDE.md ✓ | Telegram ✓ | Docs ✓
```

---

## ANTI-PATTERNS (what NOT to do)

| Anti-Pattern | Why it's bad | What to do instead |
|-------------|-------------|-------------------|
| Generic identity ("You are a helpful assistant") | Produces bland output | Specific expert persona with taste |
| No scope detection ("What would you like?") | Wastes user time | Parse intent from prompt |
| Equal effort on all steps | Mediocre everywhere | 50% effort on hinge moment |
| "Check if it's good" | Generic, unverifiable | Specific checks with specific criteria |
| No verification gate | "Done" is unverified | Self-check before reporting |
| No ecosystem integration | Isolated tool | References related skills |
| Copy-paste template | Soulless skill | Domain-specific expertise |

---

## SMITH INTEGRATION

SMITH improves skills over time by:
1. Reading results from repeated use across projects
2. Identifying phases/steps that consistently produce weak output → strengthen them
3. Identifying domain patterns not covered → propose new checks
4. Adjusting scoring weights based on real-world severity distribution
5. Proposing new skills based on frequently requested capabilities

---

*"/newcmd — Engineer skills, don't template them. Quality DNA in every command."*
