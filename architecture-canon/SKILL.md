---
name: architecture-canon
description: Apply ten borrowed architectural north stars when designing, proposing, auditing, or reviewing anything that adds public surface — a new public type, module, interface, event kind, config key, or extension point. Sister skill to [[coding-discipline]] (agent behavior), [[function-shape]] (per-function shape), and [[behavioral-testing]] (tests). Triggers — proposing a subsystem or surface, "should we add X" / "how should we structure Y", designing an extension or contribution surface, reviewing a PR, auditing hot-path data layout, or fixing a bug whose proper resolution introduces public surface. The principles are hard constraints with explicit *forbids* clauses, not stylistic preferences. Load only the `references/<star>.md` files relevant to the questions in front of you.
---

# architecture canon

Ten borrowed ideas, each answering one specific design question. This skill is the operational form: each star lives in `references/<star>.md` with its forbids clause and concrete red flags reviewers can quote. Architecture rules live here; agent behavior in [[coding-discipline]]; per-function shape in [[function-shape]]; test shape in [[behavioral-testing]].

## Question → star lookup

When a design choice is up in the air, find the question, load the reference, walk the forbids.

| Question | Star | Reference |
|---|---|---|
| What is this thing? | MLIR, Plan 9 | `references/mlir.md`, `references/plan9.md` |
| How is it addressed? | Plan 9 | `references/plan9.md` |
| How is it bound? | Smalltalk | `references/smalltalk.md` |
| How does it lay out in memory? | Acton | `references/acton.md` |
| What happens when it fails? | Erlang | `references/erlang.md` |
| How is it observed? | Observability | `references/observability.md` |
| How does an extension reach it? | LSP, VS Code | `references/lsp.md`, `references/vscode.md` |
| Is it doing one thing? | Hickey | `references/hickey.md` |
| Does it have primitives, combination, and abstraction? | SICP | `references/sicp.md` |

## How to apply

Three modes:

**Proposing a feature.** Walk the table top-to-bottom; load each reference and name the star's answer for the proposal. A row with no answer means the proposal isn't ready — say so, name the missing piece, don't paper over it.

**Auditing existing code.** Each reference has a *red flags* section. If the code matches a red flag, the violation is real — name the star, quote the forbids clause.

**Reviewing a PR.** Both: place the change against the relevant rows, then scan the touched files against the red flags for those stars. An extension-surface review loads four references (MLIR + Plan 9 + LSP + VS Code); a hot-path data refactor loads two (Acton + Hickey); a span-placement audit loads two (Observability + Erlang). Pick from the table, not all ten.

Don't pre-load all ten references. Pick from the lookup table; load only what the work needs.

## Finding the canonical pattern

References are deliberately abstract — they don't pin to specific files or symbols, because anchors rot when code moves and stale anchors teach the wrong lesson. When you need a concrete example of how a star is realized in *this* codebase, search for the relevant concept directly and read the live code. The principle is the durable artifact; the implementation under it can change without the skill changing.

## Tone

The principles are direct. Apply them directly. "This violates Plan 9 — two resource kinds share one namespace already, and you're proposing a second registry with its own lookup" is the right phrasing. Hedged "maybe consider possibly using…" is not. The principles are the bar; either a proposal clears it or it doesn't. Name the violation, quote the forbids, and point at the relevant existing concept when describing what right looks like.

When two stars conflict on a design (rare, but it happens — e.g., a late-bound message bus that obscures memory layout), name both and the tradeoff explicitly. Don't pretend it's clean. The user decides which star wins; record the reasoning.

## Scope

This skill is the architecture-review layer for design work in any project. It sits alongside [[coding-discipline]] (agent behavior), [[function-shape]] (per-function shape), and [[behavioral-testing]] (tests). Load only the `references/<star>.md` files the current decision needs.

Two **review** skills operationalize these stars against a finished change: [[principle-review]] walks a whole change against the project's principles (and falls back to this canon when none exist), and [[hot-path-budget-audit]] enforces the Acton (`references/acton.md`) and Observability (`references/observability.md`) stars on a latency-critical path. [[wire-drift-check]] enforces the Plan 9 single-source-of-truth (`references/plan9.md`) across a duplicated boundary.
