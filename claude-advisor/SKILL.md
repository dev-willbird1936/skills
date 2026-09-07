---
name: claude-advisor
description: Run a read-only Fable 5.1 advisor consultation, xhigh effort for one consult and high for checkpoints. A
  question after the trigger means one consult; a bare trigger or a task means session checkpoints; `-i` forces one
  consult, `-chk` forces checkpoints. Native Agent tool in Claude Code, Claude CLI elsewhere. Aliases /claude-advisor, /claudvisor.
---

# /claude-advisor (alias: /claudvisor) — Fable 5.1 consultation

## Non-negotiables

- Advisor = Fable 5.1. Effort by mode: `xhigh` for one consult, `high` for every checkpoint consult.
- Executor = current session's main model, read from context; never hardcode.
- Advisor is read-only: it supplies input; you do every `Write`, `Edit`, `Bash` step.
- In Claude Code use only the named agent per [references/native-claude-consult.md](references/native-claude-consult.md); in any other harness use the Claude CLI per [references/cli-fallback.md](references/cli-fallback.md). Never invent a tool call or substitute another model. Neither route available: report route unavailable, skip the consult.
- Skill adds no wall-clock timeout of its own.

## Trigger

1. Before other work, scan the whole user message, including trailing lines.
2. Activate only for `/claude-advisor`, `/claudvisor`, or an explicit Claude/Fable advisor request. Unqualified "advisor mode" or a legacy model name is not a trigger.
3. Run the skill before the rest of the request; the flag decides whether checkpoints continue.

## Mode

Look at the token directly after the command, case-insensitive, then at what follows:

| After the command | Mode |
|---|---|
| `-i` (individual call) | One consult, always |
| `true`, `-chk`, `-checkpoints` | Session checkpoints, always |
| a question or a specific decision | One consult on it |
| nothing, or a task description without a question | Session checkpoints |

- Only the very next token can be a flag; `-i` or `true` elsewhere, or another command's argument, does not count. Strip a flag before interpreting the rest.
- Question vs task: a question asks for an answer now ("should X or Y?", "why does Z fail?"); a task asks for work ("refactor the parser", "hunt bugs in this repo"). Unsure: treat as a question and say which reading you took.
- One consult: exactly one consult now on the current request (or the attached question); read it, act as executor; consult again only if the user invokes the skill again. Checkpoint rules do not apply.
- Checkpoints: on for the rest of the session; frequency per "Checkpoint mode" and [references/checkpoints.md](references/checkpoints.md).
- Model, mechanism, no-timeout rule, prompt structure: identical in both modes. Effort differs: one consult `xhigh`, checkpoints `high`.

## Transport

1. Claude Code (the `Agent` tool exists): read [references/native-claude-consult.md](references/native-claude-consult.md). Agent by mode: `claude-advisor-xhigh` for one consult, `claude-advisor` for checkpoints. Verify the agent definition is present with its pinned effort; take that from the definition, never from an old note or prompt wording alone.
2. Any other harness (Codex, Pi, Cursor, other): read [references/cli-fallback.md](references/cli-fallback.md) and shell out to `claude -p` with `--effort` set by mode. Never run both routes for one consult.
3. Native ambient advisor features are a separate host capability; verify their availability and settings when relevant. This skill requests an explicit consult with a named model and pinned effort.
4. Read [references/checkpoints.md](references/checkpoints.md) only in checkpoint mode.

## Run the consult

- Ask one concrete, narrow question on a specific decision, not an exhaustive plan. Each consult is a real, billed Fable 5.1 call at `xhigh` (one consult) or `high` (checkpoint) effort.
- A consult ends only when: (1) advisor returns a final message; (2) the `Agent` call or CLI process returns an explicit error; (3) the user explicitly cancels.
- Keep waiting whatever the elapsed time; silence in a synchronous `Agent` call or a running CLI process is not a hang. Never stop, discard, or mark a consult failed because time passed. The skill cannot override an external platform or server process-lifetime limit; it adds no deadline.
- One advisor at a time; no duplicate while the call or process runs.
- User cancels: interrupt that exact call or process, report cancellation. Unrelated user input does not cancel.

## Use the advice

- Serious weight, not binding.
- Suggested step fails empirically, or primary-source evidence contradicts a claim (file says X, advisor assumed Y): adapt.
- Evidence points one way, advisor another: surface the conflict in one more short consult ("found X, you suggested Y — which constraint breaks the tie?") instead of picking a side. This tie-break is part of the same consult: allowed in one-time mode, not a new checkpoint.

## Checkpoint mode (flag only)

- Consult only when the advisor can materially improve a consequential decision; own reasoning and direct validation for routine, reversible or low-risk work.
- Batch related evidence and decisions into one consult; no call per tool result, probe or minor step; never as a progress or status check.
- No overlapping or duplicate consults. Re-consult only when new evidence, an error, or a changed constraint materially changes the decision.
- Checkpoint timing: [references/checkpoints.md](references/checkpoints.md).

## On activation

State the mode in one line, then act:

- One consult: "One-time Fable 5.1 consult (`xhigh` effort via synchronous `Agent(subagent_type: "claude-advisor-xhigh")`, or `claude -p --effort xhigh` outside Claude Code; no skill-imposed timeout); session checkpoints off." Run the single consult, continue as executor.
- Checkpoints: "Advisor checkpoints active for this session (Fable 5.1 at `high` reasoning effort via synchronous `Agent(subagent_type: "claude-advisor")`, or `claude -p --effort high` outside Claude Code; no skill-imposed wall-clock timeout, executor = current session model)." Continue the user's request, consulting per "Checkpoint mode" and [references/checkpoints.md](references/checkpoints.md).

Check before acting: trigger matched, mode from the flag or question/task reading, transport chosen by harness, advisor = Fable 5.1 at the mode's effort.

## Credits

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
