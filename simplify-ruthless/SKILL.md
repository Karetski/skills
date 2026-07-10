---
name: simplify-ruthless
description: Ruthless deletion audit whose output is a ranked deletion list, never additions. Use when asked to "simplify this", "tighten this module", "can we delete X", when something "feels heavy", "is this overkill / over-engineered", when trimming a feature, or when auditing an abstraction for whether it earns its keep. Tests each abstraction against over-engineering smells (rule of three, speculative flexibility, one-caller generics, pass-through wrappers, single-implementation interfaces) and ranks deletions by lines removed. Backs off when the request is "make this work" (a debugging session), not "make this smaller".
---

# simplify-ruthless

Most refactors drift toward additive cleverness whenever the request is
ambient ("clean this up") rather than explicit ("delete this"). This
skill exists so the user can invoke "delete more" as a first-class
request. The bias is **delete first**.

Where a write-time discipline states "simplicity first" as a default,
this is the audit you run against code that already exists. Two ideas
ground it: a complected type — one that braids state, identity,
lifecycle, and behavior — is un-braided by deletion, not addition; and
a helper that doesn't earn its existence is a deletion, not a rename.

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

## See also

Stands alone — the skills below are optional companions, not
dependencies: `coding-discipline` (the write-time "simplicity first"
default), `architecture-canon` (the design-level case against complected
types), and `function-shape` (when a helper earns its existence).
