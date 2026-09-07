---
name: claude-advisor
description: Run a read-only Fable 5.1 advisor consultation at high effort through a compatible Claude-native agent. One
  consultation by default; session checkpoints only with an explicit flag.
---

# /claude-advisor (alias: /claudvisor) — explicit Fable 5.1 consultation with pinned high effort

## Read by transport and mode

Read [the Claude-native mechanism](references/native-claude-consult.md) before consulting. Verify that the active harness exposes the named Claude agent and its pinned effort. Do not translate that API into an invented tool call or silently substitute another model. Report an unavailable route when no supported transport exists.

Read [checkpoint policy](references/checkpoints.md) only when the user selects session-checkpoint mode. Otherwise run the requested one-time consult. Preserve its read-only role and no skill-imposed total timeout.

## Trigger detection

Before other task work, scan the entire user message, including trailing lines in compound requests. Activate only for `/claude-advisor`, `/claudvisor`, or an explicit Claude/Fable advisor request. Do not treat an unqualified "advisor mode" request or a legacy model name as this trigger. Invoke it before the rest of a matching request; the mode flag controls later checkpoints.

## Mode: one-time consult (default) or session checkpoints (flag)

Parse the token that comes **directly after** the trigger (`/claude-advisor <token>` or
`/claudvisor <token>`), if any:

| Token directly after the command        | Mode                          |
| -------------------------------------- | ----------------------------- |
| *(nothing, or anything else)*          | **One-time consult** (default) |
| `true`, `-chk`, or `-checkpoints`      | **Session checkpoints**       |

Matching is case-insensitive. The token only counts if it is the very next token after the
command; a `true` elsewhere in the message, or another command's argument, does not switch modes.
When the token is a flag, strip it from the request before interpreting the rest of the message.

- **One-time consult (default):** run exactly one advisor consult, now, about the current
  request (or the specific question the user attached to the command). Read the answer, act on it
  as executor, and do **not** consult again in this session unless the user explicitly invokes the
  skill again. The "When to consult" / "When NOT to consult" sections below do **not** apply.
- **Session checkpoints (flag present):** advisor checkpoints are on for the rest of the session
  and the "When to consult" / "When NOT to consult" sections govern consult frequency.

The advisor model, effort, mechanism, no-timeout rule, and prompt structure are identical in
both modes.

## Conservative checkpoint usage

When checkpoint mode is active, use consultations sparingly and only when the advisor can
materially improve a consequential decision. Prefer the executor's reasoning and direct
validation for routine, reversible, or low-risk work. Batch related evidence and decisions into
one focused consultation; do not spend a separate call on each tool result, probe, or minor step.
Ask a concrete, narrow question, avoid overlapping or duplicate consultations, and do not use the
advisor as a progress or status check. Re-consult only when new evidence, an error, or a changed
constraint materially changes the decision.

This skill requests an explicit consultation with a named model and pinned effort. Native ambient advisor features are a separate host capability; verify their current availability and settings when relevant. Do not infer runtime compatibility or effort from an old installation note or from prompt wording alone.

**Roles (this consult; and for the rest of the session in checkpoint mode):**
- **Advisor = Fable 5.1, pinned at `high` reasoning effort**, always, regardless of what else
  changes.
- **Executor = the current session's main model**, whatever that is right now (don't hardcode a
  specific model — read it from context if it matters, otherwise it's just "you").

## No skill-imposed consultation timeout

An advisor consult has **no skill-imposed wall-clock timeout**. Never stop, discard, or classify
a consult as failed because six minutes, ten minutes, or any other duration elapsed. The skill
cannot override an external platform or server process-lifetime limit, but it must not add its
own total deadline. Completion has only three terminal states:

1. the advisor returns a final message;
2. the `Agent` call returns an explicit error; or
3. the user explicitly cancels it.

Silence during a synchronous `Agent` call is not evidence of a hang. Do not start a duplicate
advisor while the original call remains active. If the user cancels, interrupt that exact active
`Agent` call and report cancellation; unrelated user input does not cancel the consult.

## How to treat the advice

Give it serious weight, but it isn't binding. If a suggested step fails empirically, or there's
primary-source evidence contradicting a specific claim (the file says X, the advisor assumed Y),
adapt rather than force it. If evidence already gathered points one way and the advisor points
another, don't silently pick a side — surface the conflict in one more short consult ("found X,
you suggested Y — which constraint breaks the tie?") instead of guessing. A tie-break follow-up
like this is part of the same consult and is allowed in one-time mode; it is not a new checkpoint.

Keep consults focused on small decisions rather than asking for an exhaustive plan every time.
Each consult is a real, billed Fable 5.1 subagent call, run at real `high` effort — don't spam it.

## On activation

State the mode in one short line, then act:

- **Default (no flag):** "One-time Fable 5.1 consult (`high` effort via synchronous
  `Agent(subagent_type: "claude-advisor")`, no skill-imposed timeout); session checkpoints
  off." Then run the single consult and continue as executor.
- **Flag present (`true` / `-chk` / `-checkpoints`):** "Advisor checkpoints active for this
  session (Fable 5.1 at real `high` reasoning effort via synchronous
  `Agent(subagent_type: "claude-advisor")`, no skill-imposed wall-clock timeout, executor =
  current session model)." Then continue with whatever the user asked for, consulting per the
  "When to consult" rules.

## Credits

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
