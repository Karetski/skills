# agentkit

A personal **source of truth for Claude Code configuration** — kept as a
plain, symlink-friendly repo (dotfiles style), not a plugin. It holds more than
a list of skills: reusable `skills/` you drop into `~/.claude/skills/`, a
canonical `CLAUDE.md` of always-on conduct you import into `~/.claude/CLAUDE.md`,
and a `hooks/` script you wire into `settings.json`. Room to grow into `agents/`
and `output-styles/` as the config expands.

```
.
├── CLAUDE.md             # always-on coding conduct (single source)
├── skills/               # knowledge + workflows, loaded on demand
│   └── <name>/SKILL.md   #   (+ optional references/ for detail)
├── hooks/
│   ├── wire-drift-reminder.sh        # a PostToolUse nudge
│   └── settings.hook.example.json    # how to wire it into settings.json
├── .github/workflows/    # CI: runs validate.py on every push
├── validate.py           # mechanical checks over the repo
└── README.md
```

No install flow, no namespacing: skills are invoked as `/principle-review`,
`/architecture-canon`, and so on, and Claude auto-loads one when its description
matches the work.

## Install

This repo is its own installer: open Claude Code **in this directory** and ask it
to wire everything up — symlink every `skills/` directory into `~/.claude/skills/`,
import this repo's `CLAUDE.md` into `~/.claude/CLAUDE.md` (an `@`-import line, not a
copy), and merge the `hooks/` snippet into `~/.claude/settings.json` with the hook
command pointed at this repo. Run `python3 validate.py` first, then restart Claude
Code so it picks up the new skills and hook.

## Choosing the right mechanism

The reason this is more than a skills list: **not every rule should be a skill.**
Claude Code offers several mechanisms, and the durable value is knowing which to
reach for ([source](https://code.claude.com/docs/en/features-overview)):

| Mechanism | Use it for | Loads | Determinism | Here |
|---|---|---|---|---|
| **CLAUDE.md** | "Always do X" conduct and conventions that apply to *all* work | Every session | Model interprets | this repo's `CLAUDE.md` |
| **Skill** | On-demand knowledge or a workflow you trigger with `/name` | When invoked or matched | Model interprets | `skills/*` |
| **Subagent** (`context: fork`) | Work that reads many files but should return only a verdict, keeping your main context clean | When delegated | Model interprets, isolated | the four review verbs |
| **Hook** | A guardrail or reaction that must fire *every* time, no thinking required | On its event | Guaranteed | `wire-drift-reminder` |

Rule of thumb, quoting the docs: *"Put it in CLAUDE.md if Claude should always
know it… Put it in a skill if it's reference material Claude needs sometimes or a
workflow you trigger. If a rule must hold every time, make it a hook rather than
a prompt instruction."* That's why the drift check is a hook, the conduct is
CLAUDE.md, and the audits are `context: fork` skills — each on the
mechanism that fits it.

## The skills

Conduct that governs *all* work is always-on in [`CLAUDE.md`](CLAUDE.md), not a skill (see *Making conduct always-on*). The skills below load on demand.

**Standards** — ambient guidance on what good code looks like, while you write and review:

| Skill | Governs | Applies to |
|---|---|---|
| [`architecture-canon`](skills/architecture-canon/SKILL.md) | Ten borrowed design north-stars, each with a *forbids* clause and quotable red flags. | Hickey/SICP/MLIR anywhere; the rest labeled by habitat |
| [`function-shape`](skills/function-shape/SKILL.md) | One function's shape — phase flow, branch ceiling, error-handling moves, pipeline naming, mutation ownership, comments. | any codebase |
| [`behavioral-testing`](skills/behavioral-testing/SKILL.md) | Behavioral, scenario-named tests (given/when/then), the four tiers, black-box-first — placement treated as a per-ecosystem convention. | any codebase |

**Workflows** — on-demand methodologies you follow *while* working:

| Skill | Governs | Applies to |
|---|---|---|
| [`debugging-methodology`](skills/debugging-methodology/SKILL.md) | Diagnosis discipline — reproduce first, hypothesize before patching, bisect to the change, fix the root cause not the symptom. | any codebase |
| [`commit-discipline`](skills/commit-discipline/SKILL.md) | Commit & PR shape — atomic commits, refactor split from behavior, message shape, reviewable slices, bisectable history. | any project under version control |

**Review verbs** — on-demand audits you run against a change before merging. Each
declares `context: fork`, so it runs in an isolated subagent and returns just its
verdict, keeping the files it reads out of your main conversation:

| Skill | Checks |
|---|---|
| [`principle-review`](skills/principle-review/SKILL.md) | Walks a change against the project's own stated principles; falls back to a built-in rubric. Ends in ship / revise / reject. |
| [`simplify-ruthless`](skills/simplify-ruthless/SKILL.md) | Deletion-only audit — a ranked removal list, never additions. |
| [`wire-drift-check`](skills/wire-drift-check/SKILL.md) | Confirms mirrors, generated artifacts, golden fixtures, and both sides of a duplicated contract moved together. |
| [`hot-path-budget-audit`](skills/hot-path-budget-audit/SKILL.md) | Audits a latency-critical path for blocking IO, unbounded work, and budget violations — across GC and no-GC languages. |

**Hook** — [`hooks/wire-drift-reminder.sh`](hooks/wire-drift-reminder.sh): a
non-blocking `PostToolUse` nudge that fires the moment you edit a contract/schema
source (`.proto`, `.graphql`, `schema.*`, …), reminding you to run
`/wire-drift-check`. The "verify mechanically, not by convention" principle
applied to the collection itself.

## When each skill fires

| Situation | Skill |
|---|---|
| Starting any coding task; handing off a diff | always-on via `CLAUDE.md` |
| Proposing a new type / module / interface / config key | `architecture-canon` |
| Writing/reviewing one function; picking an error strategy | `function-shape` |
| Writing/placing a test | `behavioral-testing` |
| Diagnosing a failing test, crash, or regression | `debugging-methodology` |
| Shaping commits / opening a PR | `commit-discipline` |
| "Does this change fit our design?" before merge | `principle-review` |
| "Simplify / is this over-engineered / can we delete X?" | `simplify-ruthless` |
| Changing a wire format / schema / generated mirror | `wire-drift-check` (+ the hook nudges you) |
| Touching a tick/frame/request/inner-loop path | `hot-path-budget-audit` |

## Making conduct always-on

The coding conduct governs *all* work, so it lives always-on in this repo's
[`CLAUDE.md`](CLAUDE.md) rather than as a maybe-loaded skill. Import it — don't
copy it — into your `~/.claude/CLAUDE.md` (all projects) or a project `./CLAUDE.md`
(shared with the team) by adding a single `@`-import line pointing at this repo's
`CLAUDE.md`. One canonical file, imported wherever it's needed, so the conduct
can't drift into two copies — the docs' rule is "always do X" belongs in
CLAUDE.md, reference and workflows in skills.

## Extending this repo

Because it mirrors `~/.claude/`, every future artifact has an obvious home — this
is what makes it a source of truth rather than a pile:

| Add | Put it in | Wire it up |
|---|---|---|
| a skill | `skills/<name>/SKILL.md` (+ `references/`) | symlink into `~/.claude/skills/` |
| a subagent | `agents/<name>.md` | symlink into `~/.claude/agents/` |
| a hook | `hooks/<script>` + a settings snippet | merge into `~/.claude/settings.json` |
| always-on conduct | `CLAUDE.md` | import (`@`-line) into `~/.claude/CLAUDE.md` |

## Applying the skills to a project

The skills aim to be project-neutral, but neutral is not the same as universal —
and the collection is honest about the difference. It was genericized from a Rust
TUI and a systems project, and some content is native to that habitat:

- **Universally applicable:** the always-on conduct, `function-shape`,
  `debugging-methodology`, `commit-discipline`, `simplify-ruthless`,
  `principle-review`, and the Hickey / SICP / MLIR stars of `architecture-canon`
  bite on any codebase — web, backend, mobile, data, systems.
- **Habitat-bound (labeled as such):** the Acton / Plan 9 / Erlang / Smalltalk /
  Observability stars of `architecture-canon`, the allocation-invariant tier of
  `behavioral-testing`, and the systems half of `hot-path-budget-audit` earn their
  keep only where the code has the surface they describe. If the habitat isn't
  there, the star simply doesn't apply — don't manufacture a violation.
- **Conditional-but-correct:** `wire-drift-check` fires only when a project has a
  duplicated boundary (client/server protocol, codegen, cross-language mirror); it
  stays quiet otherwise, which is a feature.

The `architecture-canon` red flags bite hardest when restated in the adopting
project's own vocabulary — translate "node kind", "event bus", "namespace", "hot
path" into whatever those concepts are actually called. The principle is the
durable artifact; the implementation under it can change without the skill changing.

## Verifying the repo

```sh
python3 validate.py
```

`validate.py` enforces the repo's promises: skill frontmatter (name = directory,
only documented fields, description + `when_to_use` under the 1,536-char cap),
body ≤500 lines, references one level deep, no `[[wikilinks]]`, a non-empty
canonical `CLAUDE.md`, README↔skills link parity (every skill is linked, and
every link resolves), every hook script executable, the hook snippet valid JSON, and no concrete
home path hardcoded in it. Run it before publishing or after edits — and CI runs
it on every push.

## License

[MIT](LICENSE).
