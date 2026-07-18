#!/usr/bin/env bash
# wire-drift-reminder
#
# PostToolUse hook. Reads the tool-call JSON on stdin; if the file just written
# or edited looks like a contract / wire-format / schema source, emits a single
# non-blocking reminder to run the wire-drift-check skill. It never blocks and
# never fails a tool call — it only nudges, because contract drift is the kind
# of silent failure a human forgets to check by hand.
#
# Safe on any project: if the edited path doesn't match a wire-format pattern
# (the common case), the script exits silently. To stop the nudge, remove the
# PostToolUse block (from hooks/settings.hook.example.json) from your
# ~/.claude/settings.json.

set -eu
shopt -s nocasematch          # match .PROTO / SCHEMA.SQL regardless of case

input="$(cat)"

# Pull tool_input.file_path out of the hook JSON without a JSON dependency.
# Paths with embedded double-quotes are not supported (and effectively never
# occur); everything else is handled.
file="$(printf '%s' "$input" \
  | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' \
  | head -1 \
  | sed -E 's/.*:[[:space:]]*"([^"]*)"/\1/')"

[ -z "${file:-}" ] && exit 0

case "$file" in
  *.proto|*.thrift|*.fbs|*.avsc|*.avro|*.capnp|*.graphql|*.gql|*.prisma \
  |*schema.*|*.schema.json|*openapi*|*swagger*|*.sql|*.ddl)
    printf '{"systemMessage": "wire-drift: you edited a contract/schema source (%s). Run /wire-drift-check to confirm generated mirrors, golden fixtures, and both sides of the boundary moved together — and prefer a CI check for the deterministic parts."}\n' "$file"
    ;;
  *)
    : # not a wire-format source — stay silent
    ;;
esac

exit 0
