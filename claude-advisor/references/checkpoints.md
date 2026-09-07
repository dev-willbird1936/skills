# Checkpoints

Read only for the route identified by [SKILL.md](../SKILL.md). Commands and bare paths still resolve from the skill root. The procedures and acceptance constraints below remain authoritative for their stage.

## When to consult (session-checkpoint mode only)

This section applies only when the checkpoint flag was present. In default one-time mode there is
exactly one consult and it has already happened.

- **Before your first `Write`, `Edit`, or state-changing `Bash` call** on a non-trivial task
  (installs, migrations, commits, deploys, anything that mutates state). Read-only orientation —
  `Read`, `Glob`, `Grep`, `git status`, `git diff`, `git log`, `ls`, `cat` — doesn't count and
  doesn't need a prior consult.
- **When stuck**: an error keeps recurring, the approach isn't converging, or a result doesn't
  fit what was expected.
- **Before declaring a task complete.** Make the deliverable durable first — write the file, save
  the result, commit — then consult. The call takes time; if the session ends mid-call, a durable
  result survives and an unwritten one doesn't.
- **Before committing to an approach** on anything longer than a few steps.
- **For design, architecture, and risk questions with no tool calls involved** — if the response
  would be pure analysis or a recommendation with nothing to Read/Write/Bash, consult first. That
  judgment call is exactly where a second opinion is highest-value.

## When NOT to consult (session-checkpoint mode only)

- Simple factual lookups or arithmetic — answer those directly.
- Short reactive steps where the next action is dictated by tool output just read — the advisor
  adds most of its value before the approach crystallizes, not on every step after.
- Don't re-consult on the same decision unless something material changed (new error, new
  evidence, or genuinely reconsidering the approach).

