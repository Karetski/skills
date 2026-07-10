---
name: wire-drift-check
description: Verify that every mirror, generated artifact, golden fixture, and both sides of a duplicated contract were updated together. Use when changing a wire format, serialization schema, API contract, shared constant, or code-generated mirror — anything duplicated across a boundary (two languages, client/server, generated plus hand-written) — when asking "did I update both sides" or "regenerate the bindings", or before opening a PR that touches a shared contract. Checks codegen freshness, golden fixtures, roundtrip (encode/decode) coverage, both-sides handling, and discriminant/field-order stability.
---

# wire-drift-check

Contract drift is the most common silent failure in projects with a
duplicated boundary: two sides can compile clean while disagreeing on
the wire, and the bug surfaces only when a real payload hits the
disagreeing side. This skill mechanizes the checklist. It applies to
any boundary where one source of truth is mirrored elsewhere:
client/server protocols, a schema shared across languages, generated
bindings, shared constants, config duplicated into multiple runtimes.

Two ideas ground it. One source of truth: exactly one file is
authoritative and every other copy is *derived* from it — so naming
which file is authoritative is the first step. Verify mechanically, not
by convention: an unenforced mirror is a future drift, so a missing
check is itself a finding. The roundtrip coverage in step 3 is
black-box behavioral testing applied to the boundary.

## What this skill does

First, identify the boundary the change touches and its source of
truth: which file is authoritative, and which artifacts are *derived*
from it (generated code, mirrors in another language, golden/snapshot
fixtures, documentation). Then verify, in order:

1. **Generated mirrors are fresh.**
   If the project has a codegen step (a `generate`/`gen`/`build`
   target, a `verify --check` mode, a snapshot updater), run its check
   mode. Deterministic codegen should re-run in check mode and refuse
   stale output. If the check complains, the contributor forgot to
   regenerate — name the exact stale generator and the command to run.

2. **Golden / snapshot fixtures regenerated.**
   Any serialized fixture that captures the on-the-wire bytes (golden
   files, recorded snapshots, `.snap` files) must be re-generated for
   every new or changed message/type. Compare the working tree's
   fixtures against the change and confirm they were rewritten, not
   left stale.

3. **Roundtrip / encode-decode coverage.**
   Every variant or field that crosses the boundary should be exercised
   by a roundtrip test (encode → decode → assert equal). A lexical
   "did you register the type" guard is not enough — semantic coverage
   is the roundtrip test's job. Flag new types with no roundtrip.

4. **Both sides handle the message.**
   For each new variant/message, confirm there is a real handler on
   **each** side of the boundary — a consumer on the receiving side and
   a producer on the sending side. A fallthrough no-op, a default arm,
   or a TODO handler is drift: dead code at best, protocol fiction at
   worst.

5. **Discriminants / field order / tags are stable.**
   If the encoding numbers variants or fields by declaration order (as
   many binary codecs do), reordering an existing type silently breaks
   every peer. Adding a new variant at the end is usually safe;
   reordering or removing is a breaking change. Confirm no existing
   discriminant, tag, or field position moved.

6. **Shared constants agree across every mirror.**
   If a constant lives in one source-of-truth file and is mirrored into
   other languages/runtimes, confirm every mirror moved together. A
   number bumped in one place and not the other breaks the contract as
   surely as a schema change.

## Output

A pass/fail per check, with file paths. If any check fails, name the
exact command to run to fix it (the regenerate command, the golden
updater, the specific mirror to edit). If the project has no codegen or
check tooling for a duplicated artifact, flag that gap — an unenforced
mirror is a future drift.

## See also

Stands alone — the skills below are optional companions, not dependencies:
`architecture-canon` (the single-source-of-truth principle behind it),
`behavioral-testing` (the roundtrip test tier), and `principle-review` (the
general review this specializes).
