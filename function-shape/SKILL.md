---
name: function-shape
description: How an individual function or small module should be shaped — sister skill to [[architecture-canon]] (architecture) and [[coding-discipline]] (agent behavior). Use when writing or reviewing a single function, helper, or tiny owner type; when a function busts ~10 real branches and the question is extract-or-contain; when picking between panic / empty-absent value / typed error / encoded-protocol-failure; when naming a `prepare_x` / `execute_prepared_x` / `finalize_executed_x` pipeline; or when deciding whether a comment earns its line. Phase-flow and cyclomatic ceiling are hard — bust them only inside a named containment zone. Load only the `references/<topic>.md` files relevant to the question.
---

# function shape

Architecture-level rules: [[architecture-canon]]. Agent self-discipline: [[coding-discipline]]. This skill speaks only to what a single function looks like.

## Question → reference

Pick the row that matches the decision in front of you. Don't pre-load all references.

| Question | Reference |
|---|---|
| Does this function read as one concept? Is it past the branch ceiling? | `references/phase-flow.md` |
| Should this failure be a panic, a typed error, or an encoded protocol failure? | `references/error-handling.md` |
| What do I name the steps of a multi-step pipeline? | `references/pipeline-names.md` |
| Where should this mutation live? Does this owner earn its existence? | `references/mutation-owners.md` |
| Does this comment earn its line? Doc comment or inline? | `references/comments.md` |

## Style choices inside the line

These are short enough to live in the index, not a separate file.

- Prefer explicit loops when state evolves across records.
- Prefer chained transforms (map / filter / flat-map / collect) for pure projections.
- Use closures only when they capture a tiny invariant better than a detached helper would.
- Read top-to-bottom without a mental trampoline park.

## Scope

This skill applies to a single function, helper, or tiny owner type in any project and any language. The examples are language-neutral; where an idiom is shown, it is illustrative, not a mandate to use that language. Generated code, parsers, layout walkers, and other containment zones are exempt from the cyclomatic ceiling — but only those.

When a review finds a helper or owner type that doesn't earn its existence (`references/mutation-owners.md`), the fix is a deletion — hand it to [[simplify-ruthless]], the review skill that outputs a ranked deletion list rather than a rename.
