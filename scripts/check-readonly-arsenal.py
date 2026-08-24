#!/usr/bin/env python3
"""Fail if AGK Audit bodies regain Write/Edit/Bash defaults or payload catalogs.

This is a process gate (ADR-001). It does not claim eval scores.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDITS = ROOT / "audits"

# Orchestrators / doctrine are not forensic skill bodies.
SKIP = {
    "QUALITY-ARSENAL-PREAMBLE.md",
    "ARSENAL-ORCHESTRATION-PLAYBOOK.md",
    "ARSENAL-INTERCONNECTIONS.md",
    "AUDIT-VERIFICATION-CONTRACT.md",
    "newcmd.md",
    "quality-arsenal.md",
    "audit-pilot.md",
    "audit-orchestrator.md",
    "audit-tracker.md",
}

FORBIDDEN_TOOLS = re.compile(
    r"^allowed-tools:\s*\[([^\]]*)\]", re.M
)
PAYLOADS = [
    "<script>alert",
    "onerror=alert",
    "' OR '1'='1'",
    "javascript:alert",
]
FIX_HEADING = re.compile(r"^## .*FIX EXECUTION", re.M)
FIX_LEFTOVER = re.compile(r"FIX EXECUTION / RE-AUDIT phases below")
META_REQUIRE = re.compile(
    r"(?<![Nn]ot )(?<!not )Read `~/\.claude/audit-meta-protocol-v2\.md`"
)
A11Y_TRUNCATED = re.compile(r"contrast,\s*2\.\s*$", re.M)
RETENTION_UNLESS_FIX = re.compile(r"unless.{0,40}--fix", re.I)


def main() -> int:
    errors: list[str] = []
    files = sorted(p for p in AUDITS.glob("*.md") if p.name not in SKIP)
    if not files:
        errors.append("no audit bodies found")
    for path in files:
        text = path.read_text()
        rel = path.relative_to(ROOT)
        m = FORBIDDEN_TOOLS.search(text)
        if m:
            tools = m.group(1)
            for bad in ("Write", "Edit", "Bash"):
                if re.search(rf'"{bad}"', tools):
                    errors.append(f"{rel}: allowed-tools includes {bad}")
        if path.name.endswith("audit.md") or path.name in {
            "agentaudit.md",
            "refontaudit.md",
        }:
            head = "\n".join(text.splitlines()[:100])
            if "AGK-AUDIT-OVERRIDE-V2" not in head:
                errors.append(f"{rel}: missing AGK-AUDIT-OVERRIDE-V2 in first 100 lines")
        if FIX_HEADING.search(text):
            errors.append(f"{rel}: leftover FIX EXECUTION heading")
        if FIX_LEFTOVER.search(text):
            errors.append(f"{rel}: leftover FIX EXECUTION / RE-AUDIT apply loop")
        for needle in PAYLOADS:
            if needle in text:
                errors.append(f"{rel}: payload catalog remnant {needle!r}")
        for i, line in enumerate(text.splitlines(), 1):
            if "audit-meta-protocol-v2.md" in line and "not" not in line.lower():
                errors.append(f"{rel}:{i}: requires missing audit-meta-protocol-v2.md")
        if path.name == "secaudit.md":
            if "full raw max 460" not in text and "full applicable max  = 460" not in text:
                errors.append(f"{rel}: secaudit must declare full raw max 460")
            # 420 may appear only as the rejected number, never as this audit's max.
            for i, line in enumerate(text.splitlines(), 1):
                if "420" in line and "never" not in line.lower() and "do not use" not in line.lower() and "not use" not in line.lower():
                    if "max" in line.lower() or "raw" in line.lower():
                        errors.append(f"{rel}:{i}: secaudit still treats 420 as a live max")

    skills = ROOT / "skills"
    a11y = skills / "a11yaudit" / "SKILL.md"
    if a11y.exists():
        desc = a11y.read_text()
        if A11Y_TRUNCATED.search(desc) or "contrast, 2." in desc:
            errors.append("skills/a11yaudit/SKILL.md: description truncated mid-token")
    retention = skills / "retentionaudit" / "SKILL.md"
    if retention.exists():
        rtxt = retention.read_text()
        if RETENTION_UNLESS_FIX.search(rtxt):
            errors.append("skills/retentionaudit/SKILL.md: unless/--fix contradiction")
        if "ALWAYS READ-ONLY" not in rtxt:
            errors.append("skills/retentionaudit/SKILL.md: missing ALWAYS READ-ONLY")

    if errors:
        print("ADR-001 readonly gate FAILED:")
        for e in errors:
            print(" -", e)
        return 1
    print(f"ADR-001 readonly gate OK ({len(files)} bodies)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
