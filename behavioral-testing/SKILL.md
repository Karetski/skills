---
name: behavioral-testing
description: How tests are shaped and where they live — sister skill to [[architecture-canon]], [[function-shape]], [[coding-discipline]]. Use when writing or moving any test, when adding a new public API and deciding what to verify, when a co-located unit-test block appears in a diff (it shouldn't), when a test wants to reach into an internal item (decide promote-to-public / drive-through-public-API / delete), or when picking between a behavioral scenario and a physical invariant. The black-box rule and `given_…_when_…_then_…` naming are hard. Load only the `references/<topic>.md` files relevant to the question.
---

# behavioral testing

Tests are **black-box** and **behavioral**. They live outside the source tree,
call only the public contract, and read as scenarios.

## The three rules (always apply)

1. **No co-located unit-test blocks inside the source tree.** Tests live in a
   dedicated tests directory outside the source. A new co-located block in a
   diff is a regression — call it out.
2. **Public contract only.** A test that runs outside the source tree can only
   see what's public. If a test needs an internal item: drive it through the
   public entry point that already uses it, promote the item to public (it's
   really part of the contract), or delete the test (it was pinning a
   structural detail).
3. **Scenario names, sectioned bodies.** `given_<setup>_when_<action>_then_<outcome>`
   (or `when_…_then_…` when there's no precondition). Bodies sectioned with
   `// Given` / `// When` / `// Then` headers.

Plain built-in assertions. No snapshot, property, parameterized, or
pretty-diff libraries by default — those are separate decisions, not defaults.

## Layout

```
<tests-dir>/                      ← outside the source tree
  behaviors_<area>              ← scenarios for one public subsystem
  behaviors_<flow>_pipeline     ← end-to-end input→state→output flows
  invariants_<name>             ← perf / alloc / depth pins
  common/ (shared fixtures)     ← a shared-fixtures module
<benches-dir>/                   ← bench-harness hot-path benches
```

One `behaviors_*` file per public subsystem, not one per source file.

**Language-adapter note.** Where each top-level test file is its own compiled
test binary (the common case for compiled languages with an out-of-tree test
convention), fewer files keep link/build time bounded — so group by subsystem,
not by source file. The shared-fixtures module is imported by each behavior
file. Adapt the file-per-binary framing to whatever your toolchain's test unit
is; the grouping rule holds regardless.

## Topic → reference

Pick the row that matches the work in front of you. Don't pre-load all references.

| Question | Reference |
|---|---|
| How do I shape a single behavioral test? Body shape, table-driven cases, red flags. | `references/behaviors.md` |
| When is a pipeline test the right tier? Which seams does it catch? | `references/pipelines.md` |
| When is something a physical invariant, not a behavior? Allocation counters, depth pins. | `references/invariants.md` |
| Where do benches live? Two tiers, harness setup, CI smoke. | `references/benches.md` |
| How do I migrate a co-located unit-test block out of the source tree? | `references/migration.md` |

For observability / span placement and its interaction with allocation
invariants, see `references/invariants.md` (the "instrumentation" section).

## Scope

This skill applies to tests in any project. The black-box rule and scenario
naming are language- and tool-neutral. The mechanics — where the tests
directory sits, how test binaries are compiled, how internal visibility works —
are the language-adapter layer: map them onto your toolchain, keep the spine
intact.

Two **review** skills lean on the test tiers here. [[hot-path-budget-audit]]
turns its green/yellow/red verdicts into durable proof via the invariant tier
(`references/invariants.md` — counting-allocator and bounded-depth pins).
[[wire-drift-check]] relies on the roundtrip (encode → decode → assert equal)
coverage that the behavior and pipeline tiers provide across a duplicated
boundary.
