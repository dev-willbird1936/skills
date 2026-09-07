---
name: codex-advisor
description: Run a read-only GPT-6 Astra advisor consultation at high effort, using native delegation when available or the
  documented CLI fallback. One consultation by default; checkpoints only when selected.
---

# /codex-advisor (alias: /codevisor) — GPT-6 Astra consultation (high effort)

## Read by transport and mode

Prefer the native route below when the host supports the required model and effort. Native delegation does not require a locally authenticated Codex CLI.

- Native transport unavailable: read [CLI fallback](references/cli-fallback.md) before using it. Check installed flags and permissions; do not evade a sandbox restriction.
- Explicit session-checkpoint mode: read [checkpoint policy](references/checkpoints.md). A one-time consult does not activate continuing checkpoints.
- Preserve the configured model/effort, read-only scope and no skill-imposed total timeout. Inspect actual child status; a bounded wait timing out is not a completed or failed consult.

## Trigger detection

Before other task work, scan the entire user message, including trailing lines in compound requests. Activate only for `/codex-advisor`, `/codevisor`, or an explicit Codex/GPT-6 Astra advisor request. Do not treat an unqualified advisor request or a legacy model name as this trigger. Invoke it before the rest of a matching request; the mode flag controls later checkpoints.

## Mode: one-time consult (default) or session checkpoints (flag)

Parse the token that comes **directly after** the trigger (`/codex-advisor <token>` or
`/codevisor <token>`), if any:

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

The advisor model, effort, transport, no-timeout rule, prompt structure, and safety rules are
identical in both modes.

## Conservative checkpoint usage

When checkpoint mode is active, use consultations sparingly and only when the advisor can
materially improve a consequential decision. Prefer the executor's reasoning and direct
validation for routine, reversible, or low-risk work. Batch related evidence and decisions into
one focused consultation; do not spend a separate call on each tool result, probe, or minor step.
Ask a concrete, narrow question, avoid overlapping or duplicate consultations, and do not use the
advisor as a progress or status check. Re-consult only when new evidence, an error, or a changed
constraint materially changes the decision.

**Roles (this consult; and for the rest of the session in checkpoint mode):**
- **Advisor = GPT-6 Astra at `high` reasoning effort**, always, regardless of what else changes.
- **Transport = native Codex subagent when available; read-only Codex CLI otherwise.**
- **Executor = the current session's main model**, whatever that is right now (don't hardcode a
  specific model — read it from context if it matters, otherwise it's just "you").

## No skill-imposed consultation timeout

An advisor consult has **no skill-imposed wall-clock timeout**. Never stop, interrupt, discard,
or classify a consult as failed because six minutes, ten minutes, or any other duration elapsed.
The skill cannot override an external platform or server process-lifetime limit, but it must not
add its own total deadline. Completion has only three terminal states:

1. the advisor returns a final message;
2. the advisor/subprocess exits with an explicit error; or
3. the user cancels it.

Keep the user informed at least once per minute while waiting. Use short polling waits so the
session stays responsive, but do not confuse a poll timeout with a consultation timeout. A poll
that returns no update means only "still running". Continue waiting. Never create a new advisor
for the same consult while the original remains alive.

Claude Code also has a real, built-in `/advisor` command (a server-side tool — see
`/claude-advisor`'s notes for the full detail), but its own docs only show Claude-family models
as the advisor (e.g. `/advisor opus`), with no indication it can reach an external CLI/model
like GPT-6 Astra. This skill exists for that gap, not as a workaround for anything broken.

## Preferred Codex route: native Astra subagent

When the current agent exposes `spawn_agent`/`wait_agent` and permits `gpt-6-astra` as a model,
use that route. Do not shell out to Codex CLI and do not create a temporary wrapper.

Call `spawn_agent` once with:

- `agent_type: "default"`
- `model: "gpt-6-astra"`
- `reasoning_effort: "high"`
- `fork_turns: "none"` so the explicit model override is valid
- a concrete task name
- a fully self-contained, read-only advisor prompt using the structure below

The prompt must say that the advisor must not edit files, run state-changing commands, commit,
push, deploy, send messages, or take other external actions. Then wait for that same agent. Use
repeated bounded `wait_agent` calls for responsiveness; do not impose a total deadline and do not
interrupt a healthy advisor because a wait call returned without an update.

Track the exact spawned advisor task name or ID. A wait may wake for unrelated user input or
another agent, so match completion/error notifications to that exact advisor. On an ambiguous
wake, inspect `list_agents` and continue waiting if the advisor remains active. Only explicit user
cancellation ends a healthy consult: call `interrupt_agent` for that exact advisor, confirm it
stopped, and report cancellation.

After the final answer arrives, continue the task yourself as executor. If the agent reports an
explicit error, surface it. Never fabricate advice.

## How to treat the advice

Give it serious weight, but it isn't binding. If a suggested step fails empirically, or there's
primary-source evidence contradicting a specific claim (the file says X, the advisor assumed Y),
adapt rather than force it. If evidence already gathered points one way and the advisor points
another, don't silently pick a side — surface the conflict in one more short consult ("found X,
you suggested Y — which constraint breaks the tie?") instead of guessing. A tie-break follow-up
like this is part of the same consult and is allowed in one-time mode; it is not a new checkpoint.

Keep consults focused on small decisions rather than asking for an exhaustive plan every time.
Each consult is a real GPT-6 Astra call at `high` effort — slower than a default-effort call and
not free — don't spam it.

## Safety

- Default to no edits — the `--sandbox read-only` flag enforces this; don't loosen it just to
  get a consult to "fix it directly" — that's not this skill's job (see the sibling
  `codex-reviewer` skill if actual Codex-driven edits are wanted instead of advice).
- No commits, pushes, deploys, production config, DNS, external messages, payments, or broad
  deletion triggered from a consult response without explicit user approval.
- Do not print or leak secrets, credentials, SSH keys, browser profiles, cookies, or `.env`
  file contents into the prompt sent to Codex.

## On activation

State the mode in one short line, then act:

- **Default (no flag):** "One-time GPT-6 Astra consult (`high` effort, no skill-imposed
  timeout); session checkpoints off." Then run the single consult and continue as executor.
- **Flag present (`true` / `-chk` / `-checkpoints`):** "Advisor checkpoints active for this
  session (GPT-6 Astra at `high` reasoning effort, native Astra subagent when available and
  read-only Codex CLI fallback otherwise, no skill-imposed wall-clock timeout, executor = current
  session model)." Then continue with whatever the user asked for, consulting per the
  "When to consult" rules.

## Credits

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
