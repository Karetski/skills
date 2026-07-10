# skills

A cross-project collection of reusable [Claude Code](https://docs.claude.com/en/docs/claude-code)
skills for engineering work. Each skill is a self-contained folder with a `SKILL.md` and,
where the topic is large, a `references/` directory loaded on demand.

Two things every skill here holds to:

- **Self-contained.** A skill works installed on its own — no skill depends on another
  being present. Where skills relate, each names the others under a `See also` footer as
  optional, non-load-bearing pointers.
- **Project-independent.** They were genericized from project-specific skills (originally
  a Rust TUI and a systems project) into language- and domain-neutral form. Where a rule
  has a mechanical layer (test-file location, error-signalling idiom, codegen format), the
  text flags it as a **language-adapter** point — map it onto your toolchain and keep the
  durable principle intact.

## The skills

**Standards** — ambient guidance on what good code looks like, useful while you write and review:

| Skill | What it governs |
|---|---|
| [`coding-discipline`](coding-discipline/SKILL.md) | Agent conduct — think before coding, simplicity first, surgical changes, goal-driven execution, with a final calibration checklist. |
| [`architecture-canon`](architecture-canon/SKILL.md) | Ten borrowed architectural north stars, each answering one design question, with *forbids* clauses and quotable red flags. |
| [`function-shape`](function-shape/SKILL.md) | How one function or helper is shaped — phase flow, branch ceiling, error-handling moves, pipeline naming, mutation ownership, comments. |
| [`behavioral-testing`](behavioral-testing/SKILL.md) | Black-box behavioral tests — scenario naming, the four-tier taxonomy, public-contract-only, migration discipline. |

**Reviews** — on-demand audit verbs you run against a change before merging:

| Skill | What it checks |
|---|---|
| [`principle-review`](principle-review/SKILL.md) | Walks a change against the project's own stated principles one at a time; falls back to a built-in rubric when the project has none. Ends in a ship / revise / reject verdict. |
| [`simplify-ruthless`](simplify-ruthless/SKILL.md) | Ruthless deletion audit — outputs a ranked deletion list, never additions. |
| [`wire-drift-check`](wire-drift-check/SKILL.md) | Verifies mirrors, generated artifacts, golden fixtures, and both sides of a duplicated contract were updated together. |
| [`hot-path-budget-audit`](hot-path-budget-audit/SKILL.md) | Static audit of a latency-critical path (tick / frame / request / loop) for blocking IO, allocations, unbounded work, and budget violations. |

The two groups complement each other — a review verb applies, against a finished change, a
property the matching standard describes while you write — but each skill is independent.
Install one, a few, or all.

## Install

Claude Code discovers skills one level deep under a skills directory — `<skills-dir>/<name>/SKILL.md`.
That is why every skill folder sits at the repo root: drop the folders in directly, no nesting.

- **Global** (all your projects): copy or symlink the skill folders into `~/.claude/skills/`.
- **Per-project** (checked in for the team): copy or symlink them into `<project>/.claude/skills/`.

```sh
# Global, all skills, via symlink (edits here track upstream):
for d in */ ; do [ -f "$d/SKILL.md" ] && ln -s "$PWD/${d%/}" ~/.claude/skills/ ; done

# Or copy a single skill into a project:
cp -R architecture-canon /path/to/project/.claude/skills/
```

Restart Claude Code (or start a new session) so it picks up the new skills. Each is then
invocable directly by name (`/architecture-canon`, `/wire-drift-check`, …) and auto-loads
when its `description` matches the work at hand.

## Verifying the collection

`validate.py` mechanically enforces the invariants these skills promise — valid frontmatter
(name, ≤1024-char description), no cross-skill wikilink coupling, references one level deep,
and no reference file depending on another skill. Run it before publishing or after edits:

```sh
python3 validate.py
```

## Applying them to a project

The skills are neutral by design. The `architecture-canon` red flags bite hardest when
restated in the adopting project's own vocabulary — translate "node kind", "event bus",
"namespace", "hot path" into whatever those concepts are actually called in your codebase.
The principle is the durable artifact; the implementation under it can change without the
skill changing.

## License

[MIT](LICENSE).
