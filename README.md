# skills

A cross-project collection of reusable [Claude Code](https://docs.claude.com/en/docs/claude-code)
skills for engineering work. Each skill is a self-contained folder with a `SKILL.md` and,
where the topic is large, a `references/` directory loaded on demand.

Every skill is **project-independent**. They were extracted and genericized from
project-specific skills (originally authored against a Rust TUI codebase and a separate
systems project) into language- and domain-neutral form. Examples span web services, CLIs,
libraries, and games so no single stack owns the vocabulary. Where a rule has a mechanical
layer (test-file location, error-signalling idiom, codegen format), the text flags it as a
**language-adapter** point — map it onto your toolchain and keep the durable principle intact.

## The two families

The skills split into two families. **Standards** are ambient guidance — the shape of good
code, loaded while you write and review. **Reviews** are on-demand audit verbs — invoke one
against a change to check a specific property before merging. They cross-reference each other
with `[[skill-name]]` links and are designed to layer.

### Standards — what good code looks like

| Skill | Layer | What it governs |
|---|---|---|
| [`coding-discipline`](coding-discipline/SKILL.md) | base | How the agent behaves — think before coding, simplicity first, surgical changes, goal-driven execution. |
| [`architecture-canon`](architecture-canon/SKILL.md) | design | Ten borrowed architectural north stars, each answering one design question, with *forbids* clauses and quotable red flags. |
| [`function-shape`](function-shape/SKILL.md) | per-function | How a single function or small module is shaped — phase flow, branch ceiling, error-handling moves, pipeline naming, mutation owners, comments. |
| [`behavioral-testing`](behavioral-testing/SKILL.md) | tests | Black-box behavioral testing — scenario naming, the four-tier taxonomy, test-the-public-contract, migration discipline. |

`coding-discipline` is the base layer; the other three sit on top of it.

### Reviews — audit a change before merging

| Skill | What it checks | Grounded in |
|---|---|---|
| [`principle-review`](principle-review/SKILL.md) | Walks a substantial change against the project's own stated principles, one at a time; falls back to the standards canon when the project has none. The catch-all that dispatches to the specialists below. | all four standards |
| [`simplify-ruthless`](simplify-ruthless/SKILL.md) | Ruthless deletion audit — outputs a ranked deletion list, never additions. The action form of `coding-discipline`'s "simplicity first". | `[[coding-discipline]]`, `[[architecture-canon]]` (Hickey), `[[function-shape]]` |
| [`wire-drift-check`](wire-drift-check/SKILL.md) | Verifies mirrors, generated artifacts, golden fixtures, and both sides of a duplicated contract were updated together. | `[[architecture-canon]]` (Plan 9), `[[behavioral-testing]]` |
| [`hot-path-budget-audit`](hot-path-budget-audit/SKILL.md) | Static audit of a latency-critical path (tick / frame / request / loop) for blocking IO, allocations, unbounded work, and budget violations. | `[[architecture-canon]]` (Acton, Observability), `[[behavioral-testing]]` (invariants) |

### How they connect

`principle-review` is the front door: when a project has no principles doc of its own, it
falls back to the four standards and defers domain-specific concerns to `wire-drift-check`,
`hot-path-budget-audit`, and `simplify-ruthless`. Each review is grounded in the standard it
enforces — deleting is `coding-discipline` made actionable, drift is a `behavioral-testing`
roundtrip plus a Plan 9 single-source-of-truth, the hot-path audit is Acton + Observability
with its pins verified as `behavioral-testing` invariants.

## Install

Claude Code discovers skills one level deep under a skills directory — `<skills-dir>/<name>/SKILL.md`.
That is why every skill folder sits at the repo root: you drop the folders in directly, no
nesting. Two scopes:

- **Global** (all your projects): copy or symlink the skill folders into `~/.claude/skills/`.
- **Per-project** (checked in for the team): copy or symlink them into `<project>/.claude/skills/`.

```sh
# Global, all skills, via symlink (edits here track upstream):
for d in */ ; do ln -s "$PWD/${d%/}" ~/.claude/skills/ ; done

# Or copy a single skill into a project:
cp -R architecture-canon /path/to/project/.claude/skills/
```

Restart Claude Code (or start a new session) so it picks up the new skills. Each is then
invocable by name and auto-suggested when its `description` triggers match.

## Applying them to a project

The skills are neutral by design. The `architecture-canon` red flags bite hardest when
restated in the adopting project's own vocabulary — translate "node kind", "event bus",
"namespace", "hot path" into whatever those concepts are actually called in your codebase.
The principle is the durable artifact; the implementation under it can change without the
skill changing.

## License

[MIT](LICENSE).
