#!/usr/bin/env python3
"""Validate every skill in this collection against the invariants it promises.

The collection's own rule is "verify mechanically, not by convention" — so the
properties that make these skills correct and self-contained are enforced here
rather than trusted to review. Run before publishing or installing:

    python3 validate.py            # validate the repo this script lives in
    python3 validate.py <dir>      # validate a different skills directory

Exits non-zero if any ERROR is found (suitable for CI). No third-party deps.

Per SKILL.md it checks:
  - YAML frontmatter is present and delimited by --- / ---
  - required fields `name` and `description` are present and non-empty
  - name: <=64 chars, matches ^[a-z0-9-]+$, no reserved word (anthropic|claude),
    and equals the skill's directory name (the /command a user types)
  - description: non-empty, <=1024 chars, contains no XML-ish tag, no [[wikilink]]
  - body is <=500 lines
  - no [[wikilink]] anywhere in the file
Cross-file / structural (self-containment):
  - every `references/X.md` named in a SKILL.md exists on disk
  - every reference file on disk is named by its SKILL.md (no orphans) [warning]
  - references are one level deep: no reference file links to another references/*.md
  - no cross-skill coupling: no reference file names another skill, and no
    [[wikilink]] appears in any reference file
"""
import os, re, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
SKILLS = sorted(d for d in os.listdir(REPO)
                if os.path.isfile(os.path.join(REPO, d, "SKILL.md")))
SKILL_NAMES = set(SKILLS)
RESERVED = ("anthropic", "claude")
NAME_MAX, DESC_MAX, BODY_MAX = 64, 1024, 500

errors, warnings = [], []

def parse_frontmatter(text, path):
    if not text.startswith("---"):
        errors.append(f"{path}: no frontmatter start marker"); return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        errors.append(f"{path}: no frontmatter end marker"); return {}, text
    fm, key = {}, None
    for line in text[3:end].strip("\n").split("\n"):
        m = re.match(r"^([a-zA-Z0-9_-]+):\s?(.*)$", line)
        if m:
            key = m.group(1); fm[key] = m.group(2)
        elif key and line.strip():                       # folded continuation line
            fm[key] += " " + line.strip()
    return fm, text[end + 4:]

for skill in SKILLS:
    sp = os.path.join(REPO, skill, "SKILL.md")
    text = open(sp, encoding="utf-8").read()
    fm, body = parse_frontmatter(text, skill)

    for field in ("name", "description"):
        if not fm.get(field, "").strip():
            errors.append(f"{skill}: missing/empty frontmatter field '{field}'")

    name = fm.get("name", "")
    if name != skill:
        errors.append(f"{skill}: name '{name}' != directory name '{skill}'")
    if len(name) > NAME_MAX:
        errors.append(f"{skill}: name is {len(name)} chars (>{NAME_MAX})")
    if name and not re.match(r"^[a-z0-9-]+$", name):
        errors.append(f"{skill}: name has characters outside [a-z0-9-]")
    if any(r in name.lower() for r in RESERVED):
        errors.append(f"{skill}: name contains a reserved word ({'/'.join(RESERVED)})")

    desc = fm.get("description", "")
    if len(desc) > DESC_MAX:
        errors.append(f"{skill}: description is {len(desc)} chars (>{DESC_MAX})")
    if re.search(r"<[a-zA-Z/]", desc):
        errors.append(f"{skill}: description contains an XML-ish tag")
    if "[[" in desc:
        errors.append(f"{skill}: description contains a [[wikilink]]")

    n = body.count("\n")
    if n > BODY_MAX:
        errors.append(f"{skill}: body is {n} lines (>{BODY_MAX})")
    if "[[" in text:
        errors.append(f"{skill}: SKILL.md contains a [[wikilink]]")

    mentioned = set(re.findall(r"references/([a-z0-9-]+\.md)", text))
    refdir = os.path.join(REPO, skill, "references")
    on_disk = set(os.listdir(refdir)) if os.path.isdir(refdir) else set()
    for m in sorted(mentioned - on_disk):
        errors.append(f"{skill}: SKILL.md names references/{m} which does not exist")
    for d in sorted(on_disk - mentioned):
        warnings.append(f"{skill}: references/{d} exists but is not named in SKILL.md (orphan)")

    for d in sorted(on_disk):
        rtext = open(os.path.join(refdir, d), encoding="utf-8").read()
        if "[[" in rtext:
            errors.append(f"{skill}/references/{d}: contains a [[wikilink]]")
        if re.search(r"references/[a-z0-9-]+\.md", rtext):
            errors.append(f"{skill}/references/{d}: links to another references/*.md (nested > 1 deep)")
        for other in SKILL_NAMES - {skill}:
            if re.search(rf"(?<![\w-]){re.escape(other)}(?![\w-])", rtext):
                errors.append(f"{skill}/references/{d}: names another skill '{other}' (cross-skill coupling)")

refcount = sum(len(os.listdir(os.path.join(REPO, s, "references")))
               for s in SKILLS if os.path.isdir(os.path.join(REPO, s, "references")))
print(f"Validated {len(SKILLS)} skills ({refcount} reference files): {', '.join(SKILLS)}\n")
print(f"ERRORS: none ✓" if not errors else f"ERRORS ({len(errors)}):")
for e in errors:
    print("  ✗", e)
print(f"WARNINGS: none ✓" if not warnings else f"WARNINGS ({len(warnings)}):")
for w in warnings:
    print("  ⚠", w)
sys.exit(1 if errors else 0)
