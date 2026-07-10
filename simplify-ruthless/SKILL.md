---
name: simplify-ruthless
description: Ruthless deletion audit — the action form of [[coding-discipline]]'s "simplicity first", enforcing [[architecture-canon]] (Hickey) and [[function-shape]]. Output is a ranked deletion list, never additions. Triggers — "simplify this", "is this overkill", "tighten this module", "can we delete X", "this feels heavy", "is this over-engineered", trimming a feature, or auditing an abstraction for its keep. Back off if the request is "make this work" (a debugging session), not "make this smaller".
---

# simplify-ruthless

Most refactors drift toward additive cleverness whenever the request is
ambient ("clean this up") rather than explicit ("delete this"). This
skill exists so the user can invoke "delete more" as a first-class
request. The bias is **delete first**.

This is the action form of [[coding-discipline]] §2 (*Simplicity
first*): that skill states the default while you write; this one is the
audit you run against code that already exists. Its deletion triggers
enforce [[architecture-canon]]'s Hickey star (a complected type is
un-braided by deletion, not addition) and [[function-shape]] (a helper
that doesn't earn its existence is a deletion, not a rename).

## What this skill does

1. Read the named code (a file, a module, a function, or the most
   recent diff).

2. If the project states its own anti-patterns — a "what we
   deliberately do not do" section, a non-goals list, a style guide —
   read it and test each abstraction against it. Otherwise apply the
   general over-engineering smells below.

3. Test each non-trivial abstraction against the usual deletion
   triggers:
   - **Abstractions for hypothetical future needs.** Rule of Three:
     wait for the third concrete caller before generalizing. One or two
     call sites don't earn an abstraction.
   - **Optimizations without a measured cost they reduce.** Structural
     performance work is fine; speculative micro-optimization that
     complicates the code without a benchmark is not.
   - **Generic-over-T parameters with one caller.**
   - **Early extraction "for testability"** when the test would be the
     same shape inlined.
   - **Wrapper types that pass through every method unchanged.**
   - **Indirection through an interface/trait that has one
     implementation** and is not a genuine test seam or boundary.
   - **Config knobs, feature flags, or parameters** that only ever take
     one value in practice.
   - **Dead branches, unreachable arms, and commented-out code.**

4. For each abstraction that fails the test, output:
   - **Path + line range.**
   - **What to delete** (one sentence).
   - **Which principle or smell it violates.**
   - **What concrete pain would re-introduce it.** If the answer is
     "none I can name," recommend deletion. If the answer is "actually
     this prevents X," keep it and say so.

5. Rank the deletion list by lines removed, descending. Five concrete
   deletions beats fifty hand-wavy ones.

## What this skill must not do

- Never propose new abstractions. This skill subtracts.
- Never propose renames or formatting changes. Style is not the job.
- Never recommend "just add a comment to clarify." If a name is
  unclear, rename the symbol; do not annotate it.
- Never flag load-bearing sanity checks (assertions, invariant guards,
  debug-only assertion checks) for deletion just because they look
  redundant — they encode an invariant. Only cut them if you can show
  the invariant is enforced elsewhere.

## When to back off

If the user has framed the request as "make this work" rather than
"make this smaller," do nothing and say so. Forced simplification
during a debugging session is how regressions ship.
