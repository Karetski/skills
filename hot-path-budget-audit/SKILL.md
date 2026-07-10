---
name: hot-path-budget-audit
description: Static audit of a latency-critical path for blocking IO, allocations, unbounded work, and budget violations — the performance specialist of the review family. Grounded in [[architecture-canon]]'s Acton star (data layout is the design) and Observability star (hot-path silence); its allocation and budget claims are pinned as [[behavioral-testing]] invariants (`references/invariants.md`). Triggers — adding or changing code on a hot path (a game/simulation tick, a render frame, a request handler, an event-loop callback, an inner loop), or investigating gradual performance degradation. A per-iteration time budget is one of the hardest invariants to maintain, because violating it rarely fails a test; it degrades under load.
---

# hot-path-budget-audit

A hot path runs on a fixed budget: N milliseconds per tick, per frame,
per request, per callback. Violations don't surface as test failures —
they surface as gradual stutter, tail-latency creep, or throughput
collapse that only appears under real load, after which they're
expensive to root-cause. Static audit is cheaper than reactive
profiling.

This audit is the enforcement arm of two [[architecture-canon]] stars:
Acton (choose the data layout so hot walks are allocation-free —
[[architecture-canon]] `references/acton.md`) and Observability (no span
belongs on a hot path without re-running its allocation invariant —
[[architecture-canon]] `references/observability.md`). The
green/yellow/red verdict below is a static estimate; the durable proof
is a [[behavioral-testing]] invariant test (a counting-allocator pin, a
bounded-depth pin — [[behavioral-testing]] `references/invariants.md`)
that fails the build when the property breaks.

## What this skill does

1. **Establish the budget and the path.** State the budget explicitly
   (e.g. "20 Hz tick = 50 ms/tick", "60 fps = 16 ms/frame", "p99 target
   = 100 ms/request"). Then enumerate the hot path: start from its
   entry point and walk every function called per iteration — including
   callbacks, observers, systems, and indirect dispatch. List them in
   execution order with their file paths.

2. **Per function, flag forbidden operations.** Many projects catch
   some of these at compile/lint time (a disallowed-methods lint, a
   `no-blocking-in-async` rule); humans still slip in the equivalents:
   - **Blocking / synchronous IO**: filesystem, network, DB queries,
     blocking HTTP clients, `acquire`/`lock` on a shared poolable
     resource. On an async hot path, none of these belong inline.
   - **Allocations in the inner loop**: fresh collections, string
     building, boxing inside an iteration over the working set. Hoist
     or reuse buffers.
   - **Unbounded iteration**: scanning the whole world/table/dataset
     when the work only needs a bounded neighbourhood, a spatial cell,
     an index lookup, or the subscribers of one channel.
   - **Locks held across `await` / yield points**: on an async path
     there should ideally be no awaits at all in the hot section; flag
     both the await and any lock that spans it.
   - **Awaiting a full channel / backpressure inline**: a send that
     blocks when the queue is full stalls the whole path. Prefer a
     non-blocking `try_send` and count drops via a metric.
   - **Work that could be amortized**: anything rebuilt from scratch
     every iteration that could be cached and invalidated, or moved off
     the hot path entirely (to a background flusher / worker).

3. **Bound every new unit of work.** Interest/visibility work must use
   a spatial or indexed bound, not a full scan. Broadcasts must
   enumerate subscribers, never the whole population. Any per-iteration
   work must be provably bounded by something other than total dataset
   size.

4. **Estimate worst-case cost.** For each new or changed unit, write
   the worst case as "for N items, this is O(...) operations." Divide
   the budget by expected N to get a per-item ceiling, and check the
   estimate against it. Anything O(N²) on the working-set size is a
   yellow flag at small N and a red flag as N grows.

5. **Output a verdict per unit.**
   - 🟢 Green: bounded, allocation-free in the inner loop, no blocking
     IO.
   - 🟡 Yellow: bounded but allocates, or has a documented "runs once
     per interval, not per iteration" exception.
   - 🔴 Red: unbounded, blocking, or does IO on the hot path. Must be
     fixed before merge.

## What earns a "must be fixed before merge"

A red verdict is non-negotiable. The remediation is almost always the
same: move the work off the hot path — behind a non-blocking queue to a
background worker, into a cache invalidated out-of-band, or into a
bounded index lookup — so the per-iteration budget is preserved.
