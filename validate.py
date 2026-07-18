#!/usr/bin/env python3
"""Validate this config repo against the invariants it promises.

The repo is a dotfiles-style source of truth for Claude Code: a `skills/`
directory you symlink into `~/.claude/skills/`, plus a `hooks/` script you wire
into `settings.json`. Its own rule is "verify mechanically, not by convention",
so the properties that make it correct are enforced here rather than trusted to
review. Run before publishing or after edits:

    python3 validate.py            # validate the repo this script lives in
    python3 validate.py <dir>      # validate a different repo

Exits non-zero if any ERROR is found (suitable for CI). No third-party deps.

What it checks
  Each skill (skills/<name>/SKILL.md):
    - frontmatter delimited by --- / ---, with non-empty `name` and `description`
    - name: <=64 chars, ^[a-z0-9-]+$, no reserved word (anthropic|claude), and
      equals the skill's directory name (the /command a user types)
    - description (+ when_to_use, which shares the cap): non-empty, combined
      <=1536 chars (Claude Code's skill-listing truncation point), no XML-ish
      tag, no [[wikilink]]
    - body <=500 lines; no [[wikilink]] anywhere in the file
    - every referenced references/X.md exists; orphan reference files warn
    - references one level deep (no reference links to another references/*.md)
    - no [[wikilink]] in any reference file
  Hooks:
    - every hooks/*.sh script is executable
    - hooks/settings.hook.example.json is valid JSON
  Note: cross-skill *name mentions* are allowed. These skills are installed
  together, so a soft pointer from one to another (letting shared canon live in
  one place) is a feature, not coupling.
"""
import json, os, re, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(REPO, "skills")
HOOKS_DIR = os.path.join(REPO, "hooks")
NAME_RE = re.compile(r"^[a-z0-9-]+$")
RESERVED = ("anthropic", "claude")
NAME_MAX, DESC_MAX, BODY_MAX = 64, 1536, 500

errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

def parse_frontmatter(text, label):
    if not text.startswith("---"):
        err(f"{label}: no frontmatter start marker"); return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        err(f"{label}: no frontmatter end marker"); return {}, text
    fm, key = {}, None
    for line in text[3:end].strip("\n").split("\n"):
        m = re.match(r"^([a-zA-Z0-9_-]+):\s?(.*)$", line)
        if m:
            key = m.group(1); fm[key] = m.group(2)
        elif key and line.strip():                       # folded continuation
            fm[key] += " " + line.strip()
    return fm, text[end + 4:]

def validate_skill(skill):
    label = f"skills/{skill}"
    sp = os.path.join(SKILLS_DIR, skill, "SKILL.md")
    text = open(sp, encoding="utf-8").read()
    fm, body = parse_frontmatter(text, label)

    for field in ("name", "description"):
        if not fm.get(field, "").strip():
            err(f"{label}: missing/empty frontmatter field '{field}'")

    name = fm.get("name", "")
    if name != skill:
        err(f"{label}: name '{name}' != directory name '{skill}'")
    if len(name) > NAME_MAX:
        err(f"{label}: name is {len(name)} chars (>{NAME_MAX})")
    if name and not NAME_RE.match(name):
        err(f"{label}: name has characters outside [a-z0-9-]")
    if any(r in name.lower() for r in RESERVED):
        err(f"{label}: name contains a reserved word ({'/'.join(RESERVED)})")

    combined = len(fm.get("description", "")) + len(fm.get("when_to_use", ""))
    if combined > DESC_MAX:
        err(f"{label}: description+when_to_use is {combined} chars (>{DESC_MAX})")
    if re.search(r"<[a-zA-Z/]", fm.get("description", "")):
        err(f"{label}: description contains an XML-ish tag")
    if "[[" in fm.get("description", ""):
        err(f"{label}: description contains a [[wikilink]]")

    n = body.count("\n")
    if n > BODY_MAX:
        err(f"{label}: body is {n} lines (>{BODY_MAX})")
    if "[[" in text:
        err(f"{label}: SKILL.md contains a [[wikilink]]")

    mentioned = set(re.findall(r"references/([a-z0-9-]+\.md)", text))
    refdir = os.path.join(SKILLS_DIR, skill, "references")
    on_disk = set(os.listdir(refdir)) if os.path.isdir(refdir) else set()
    for m in sorted(mentioned - on_disk):
        err(f"{label}: names references/{m} which does not exist")
    for d in sorted(on_disk - mentioned):
        warn(f"{label}: references/{d} exists but is not named in SKILL.md (orphan)")
    for d in sorted(on_disk):
        rtext = open(os.path.join(refdir, d), encoding="utf-8").read()
        if "[[" in rtext:
            err(f"{label}/references/{d}: contains a [[wikilink]]")
        if re.search(r"references/[a-z0-9-]+\.md", rtext):
            err(f"{label}/references/{d}: links to another references/*.md (nested > 1 deep)")

def validate_hooks():
    if not os.path.isdir(HOOKS_DIR):
        return
    for f in sorted(os.listdir(HOOKS_DIR)):
        path = os.path.join(HOOKS_DIR, f)
        if f.endswith(".sh") and not os.access(path, os.X_OK):
            err(f"hooks/{f}: script is not executable (chmod +x)")
        if f.endswith(".json"):
            try:
                json.load(open(path, encoding="utf-8"))
            except Exception as e:
                err(f"hooks/{f}: invalid JSON ({e})")

# --- run ---
if not os.path.isdir(SKILLS_DIR):
    err("no skills/ directory found")
    skills = []
else:
    skills = sorted(d for d in os.listdir(SKILLS_DIR)
                    if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")))
for s in skills:
    validate_skill(s)
validate_hooks()

refcount = sum(len(os.listdir(os.path.join(SKILLS_DIR, s, "references")))
               for s in skills if os.path.isdir(os.path.join(SKILLS_DIR, s, "references")))
print(f"Validated {len(skills)} skill(s) ({refcount} reference files): {', '.join(skills)}\n")
print("ERRORS: none ✓" if not errors else f"ERRORS ({len(errors)}):")
for e in errors:
    print("  ✗", e)
print("WARNINGS: none ✓" if not warnings else f"WARNINGS ({len(warnings)}):")
for w in warnings:
    print("  ⚠", w)
sys.exit(1 if errors else 0)
