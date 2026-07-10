# Physical invariants

Invariants answer **"does this code obey a physical property the design
depends on?"** — zero allocations on a hot walk, bounded recursion depth,
branch-free dispatch, log pruning, a recovery byte sequence. These are
non-functional properties: the user never sees them directly, but the design
collapses if they break.

The archetype (illustrative): a counting-allocator hook installed for the test,
with allocation deltas asserted to be zero across the hot operation. New
invariant tests follow that shape and are recorded alongside the design
principle they protect.

Kinds of invariant worth pinning:

- A hot data-structure walk performs zero allocations.
- A segmenter / parser allocates only its bounded working set.
- A reentrant dispatch's depth counter returns to zero after draining.
- A log or buffer prunes to its bound instead of growing unboundedly.
- A recovery/teardown path emits an exact byte or call sequence.

**Run the matching invariant after touching a hot path or adding an
instrumentation span.** A failing invariant means your change is wrong, not the
invariant.

## Instrumentation: how spans interact with invariants

Spans/logs go through a structured instrumentation layer, gated by the app's
log env var (only emitting when it's set). When adding instrumentation, pick
the level by how often the code runs:

- **INFO and above**: cold paths (process start, plugin/module load, connection
  or file open). Always-on cost is acceptable; cardinality is low.
- **DEBUG**: medium paths invoked per-request / per-frame at most (request
  handler, render, event dispatch).
- **TRACE**: per-inner-loop work (per-row render, per-record walk, per-segment
  scan). These run under the zero-allocation invariants — verify those tests
  still pass after the span lands. A failing invariant means the span placement
  is wrong, not the invariant.

## Red flags

- **A behaviors file that imports allocation counters or installs a counting
  allocator.** That's an invariant, not a behavior. Move it.
- **An invariant test asserting on user-visible state (rendered text, visible
  numbers).** That's a behavior. Demote.
- **A new hot-path function (a walk, a segmenter, a dispatch) without an
  invariant pinning its physical property.** Add one before the regression
  lands.
- **Don't mix tiers in one file.** A behavior scenario that *also* checks an
  allocation count is two tests in one body — split.
