---
name: principle-review
description: Review a substantial change against the project's own stated principles, one principle at a time — the catch-all front door of the review family, dispatching to the specialists ([[wire-drift-check]], [[hot-path-budget-audit]], [[simplify-ruthless]]) for their domains and falling back to the standards canon ([[architecture-canon]], [[coding-discipline]], [[function-shape]], [[behavioral-testing]]) when the project has no principles doc of its own. Triggers — reviewing a new feature / module / subsystem before merge, "does this fit our design", "review this against our principles", "is this the right shape", auditing a PR for convention alignment, or onboarding a change into an unfamiliar codebase. Reads the design doc and walks the change against it; defer domain-specific concerns to the specialist reviews.
---

# principle-review

A project's principles document is only useful if it is consulted.
Without an explicit invocation, principles and conventions documents
become read-once artifacts that drift out of everyone's memory. This
skill makes principle alignment a step you take before merging, not a
hope. It is the catch-all of the review family: it grounds itself in
the project's own rubric first, the shared standards canon second, and
hands off to a specialist review whenever the change enters that
specialist's domain.

## What this skill does

1. **Locate and re-read the project's principles at the start of each
   review.** Look, in order, for the project's stated conventions:
   `docs/principles.md`, `PRINCIPLES.md`, `ARCHITECTURE.md`,
   `CONTRIBUTING.md`, `docs/playbook.md`, `CLAUDE.md`, or whatever the
   repo points to as its design rubric. The written principles are the
   rubric, not your memory of them. If the project has **no** stated
   principles, say so and fall back to the standards canon in this
   collection — [[architecture-canon]] for design, [[coding-discipline]]
   for how the change was made, [[function-shape]] for the shape of the
   code, [[behavioral-testing]] for its tests — plus widely-held
   principles (deep modules, least surprise, single source of truth,
   verify-mechanically). Flag that the project would benefit from
   writing its own principles down.

2. **For the change under review, walk every principle by name.** For
   each principle the change actually engages with, write one short
   paragraph: does the change uphold it, bend it, or break it? Skip
   principles the change doesn't touch. Common lenses worth checking
   even when unstated:
   - **Performance / responsiveness budgets.** Does the change stay
     inside whatever budget the hot path is held to? If it claims a
     perf win, where is the measurement?
   - **Simplicity.** Does the change make the call site simpler or more
     complex? If it adds an abstraction, what concrete pain does it
     absorb (Ousterhout's deep-module test — small interface, powerful
     behaviour)?
   - **Predictability over cleverness.** Any new implicit dispatch,
     order-dependent registration, or context-sensitive behaviour?
     Name it.
   - **Source of truth / authority boundaries.** Does the change
     respect where authoritative state lives? Does it let an untrusted
     or downstream layer influence state it shouldn't own?
   - **Verify mechanically, not by convention.** Does the change
     introduce a rule the build cannot enforce? If yes, propose where
     the enforcement belongs (a lint config, a CI check, a codegen
     check, a golden/snapshot test). "Remember to X" comments are a
     smell.
   - **Architect from prior pain, not from prior glory.** What specific
     past pain motivates this abstraction? If the answer is vague, the
     abstraction is premature.

3. **Module-boundary direction.** Reconstruct the project's dependency
   direction (its module / package / layer DAG). Any import that runs
   against the intended direction is a smell — name it with the file
   path.

4. **Doc-shape check.** New durable architectural decisions belong
   wherever the project keeps durable decisions (its principles doc, a
   changelog/ADR entry). They do **not** belong buried in module-level
   prose or scattered into new ad-hoc docs. If the project has
   deliberately kept its docs surface small, respect that — it is
   usually load-bearing.

5. **Defer specialist concerns.** When the change touches a domain that
   has its own dedicated review skill, run that skill instead of
   duplicating it here:
   - A duplicated contract, wire format, schema, or generated mirror →
     [[wire-drift-check]].
   - A latency-critical path (tick / frame / request / inner loop) →
     [[hot-path-budget-audit]].
   - A request to trim, delete, or judge whether something is
     over-engineered → [[simplify-ruthless]].

   `principle-review` is the catch-all; if a specialist exists, defer to
   it.

## Output

A principle-anchored review, one short paragraph per principle the
change actually engages with. Skip principles that don't apply. End
with a single-line verdict: ship / revise / reject.
