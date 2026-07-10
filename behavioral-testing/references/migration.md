# Migrating a co-located unit-test block out of the source tree

A co-located unit-test block is any test that sits *inside* a source file,
compiled together with the code it tests: a conditionally-compiled test module,
a test class next to the class under test, tests appended to the implementation
file. When you find one in a source file you're touching:

1. Open the `behaviors_<area>` file for that subsystem in the out-of-tree tests
   directory (create it if no scenarios for that subsystem exist yet).
2. For each test inside the co-located block, decide:
   - **Calls only public items** → move, rename to `given_…_when_…_then_…`, add
     `// Given` / `// When` / `// Then` section comments.
   - **Calls internal items** → drive through the public API, OR promote to
     public if it's really contract, OR delete if it was pinning a structural
     detail.
3. Delete the entire co-located block and any test-only imports at the top of
   the source file.
4. Run the affected subsystem's tests and confirm the green set.
5. Record the count delta in the commit message:
   `tests before: N, after: M, deleted: K (reasons: …)`.

A drop in count is the win. A *silent* drop is not.

## Verifying no co-located tests remain

Search the source tree for whatever marks a co-located test block in your
language (the conditional-compilation attribute, the test annotation, the
test-framework import). After migrating a subsystem, that search must come back
empty.

## Red flags

- **Internal visibility widened only for testing.** A test outside the source
  tree still can't see it, so the widened visibility is a lie. Either promote
  it fully to public (it's contract) or delete the test (it's pinning
  structure).
- **A migrated test still named `collection_add_works`.** The migration is
  half-done; rename to `given_…_when_…_then_…`.
- **The block was deleted without recording the count delta.** Future
  archaeology can't tell whether tests were lost or consolidated. Always note.
