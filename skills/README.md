# Skills — Cursor / Grok Bot wrappers

This directory is the **second surface** of the Quality Arsenal. Claude Code still installs `audits/*.md` as slash commands. Cursor and Grok Bot load these `SKILL.md` files.

## Contract

- YAML frontmatter: `name` + `description` (when-to-use lives in the description).
- Body: short recipe only. **Do not duplicate** the forensic protocols — Read `audits/<id>.md`.
- One face: **AGK Audit** (`quality-arsenal`). Do not create 18 auditor chats.
- Grok Bot hard-caps **50 agents**.
- Default: **READ-ONLY**. `--fix` is never implied.

## Install

```bash
# Cursor project
mkdir -p .cursor/skills
cp -R skills/* .cursor/skills/

# Cursor user
mkdir -p ~/.cursor/skills
cp -R skills/* ~/.cursor/skills/
```

Keep a clone of this repo on disk so the face agent can Read `audits/*.md`.

Grok Bot: attach this folder as a skill pack on the single AGK Audit face.

## Pack

| Skill | Role |
|---|---|
| `quality-arsenal` | Face / router |
| `audit-pilot` | Chooser (diff/PR → audits) |
| 18 original audits | Domain protocols |
| `agentaudit` | Harness / MCP / injection / tenancy |

`audit-orchestrator`, `audit-tracker`, and `newcmd` remain Claude command files under `audits/`. The face routes to them when needed; they are not extra chat agents.
