---
name: codex-advisor
description: Run a read-only GPT-6 Astra advisor consultation, xhigh effort for one consult and high for checkpoints, using native delegation in Codex or the
  documented CLI fallback. A question after the trigger means one consult; a bare trigger or a task means session
  checkpoints; `-i` forces one consult, `-chk` forces checkpoints. Aliases /codex-advisor, /codevisor.
---

# /codex-advisor (alias: /codevisor) — GPT-6 Astra consultation

## Trigger

Before other work, scan the whole user message, trailing lines included. Activate only on `/codex-advisor`, `/codevisor`, or an explicit Codex/GPT-6 Astra advisor request; an unqualified advisor request or legacy model name does not count. Consult before the rest of a matching request.

## Mode

Token directly after the trigger (`/codex-advisor <token>` / `/codevisor <token>`), case-insensitive, then what follows:

| After the trigger | Mode |
|---|---|
| `-i` (individual call) | One consult, always |
| `true`, `-chk`, `-checkpoints` | Session checkpoints, always |
| a question or a specific decision | One consult on it |
| nothing, or a task description without a question | Session checkpoints |

Only the very next token can be a flag; `-i` or `true` elsewhere, or another command's argument, does not count. Strip a flag before interpreting the rest. Question vs task: a question asks for an answer now; a task asks for work. Unsure: treat as a question and say which reading you took.

- One consult: exactly one consult now on the current request or attached question; act on it as executor; consult again only when the user invokes the skill again. [checkpoint policy](references/checkpoints.md) does not apply.
- Checkpoints: on for the rest of the session. Read [checkpoint policy](references/checkpoints.md); it plus "Checkpoint frequency" below govern when to consult.

Model, transport, no-timeout rule, prompt structure and safety are identical in both modes. Effort differs: one consult `xhigh`, checkpoints `high`.

## Fixed roles

- Advisor: GPT-6 Astra. Effort by mode: `xhigh` for one consult, `high` for every checkpoint consult.
- Transport: native Codex subagent inside Codex; read-only Codex CLI in every other harness (Claude Code, Pi, Cursor, other).
- Executor: current session's main model, read from context; never hardcode.

## On activation

State the mode in one line, then act:

- One consult: "One-time GPT-6 Astra consult (`xhigh` effort, no skill-imposed timeout); session checkpoints off." Run the consult, continue as executor.
- Checkpoints: "Advisor checkpoints active for this session (GPT-6 Astra at `high` reasoning effort, native Astra subagent when available and read-only Codex CLI fallback otherwise, no skill-imposed wall-clock timeout, executor = current session model)." Continue the user's request, consulting per [checkpoint policy](references/checkpoints.md).

## Transport

Native: when the agent exposes `spawn_agent`/`wait_agent` and permits `gpt-6-astra` at the mode's effort. Needs no local Codex CLI; no shell-out, no temporary wrapper. Call `spawn_agent` once:

- `agent_type: "default"`
- `model: "gpt-6-astra"`
- `reasoning_effort: "xhigh"` for one consult, `"high"` for a checkpoint consult
- `fork_turns: "none"` (makes the model override valid)
- concrete task name
- self-contained read-only prompt (below)

CLI fallback: native unavailable → read [CLI fallback](references/cli-fallback.md) first; set `model_reasoning_effort` to the mode's effort. Check installed flags and permissions; do not evade a sandbox restriction.

Built-in `/advisor` reaches Claude-family models only (see `/claude-advisor`); shows no GPT-6 Astra route.

## Advisor prompt

Advisor has zero memory of this conversation. Include:

1. Decision or problem as a direct question.
2. Context: tried so far, current file/state, errors, evidence, constraints.
3. Framing: second opinion; direct, concise recommendation with reasoning, not an implementation; state disagreement plainly.
4. Prohibition: no editing files, state-changing commands, commit, push, deploy, messages, or other external actions.

No secrets, credentials, SSH keys, browser profiles, cookies or `.env` contents in the prompt.

## Waiting: no skill-imposed timeout

The skill adds no wall-clock deadline (external platform/process limits may exist). Exactly three end states: advisor returns a final message; advisor/subprocess exits with an explicit error; user cancels.

- Wait with repeated bounded `wait_agent` calls (or bounded polls of the CLI process). Poll without update = still running; keep waiting. Elapsed time (six minutes, ten, any) never means failed.
- Inform the user at least once per minute.
- Track the exact advisor task name/ID; match completion/error notifications to it (wakes may come from other input or agents). Ambiguous wake → inspect `list_agents`, keep waiting while active.
- One advisor per consult while the original is alive.
- User cancels → `interrupt_agent` that exact advisor, confirm stopped, report.
- Final message → continue as executor. Explicit error → surface it. Never fabricate advice.

## Using the advice

- Serious weight, not binding. Step fails empirically, or primary-source evidence contradicts a claim (file says X, advisor assumed Y) → adapt.
- Evidence and advisor disagree → one short tie-break follow-up ("found X, you suggested Y — which constraint breaks the tie?"); part of the same consult, allowed in one-time mode.
- Small, focused decisions. Each consult is a real GPT-6 Astra call at `xhigh` or `high`: slow, not free.

## Safety

- Read-only on both transports: CLI via `--sandbox read-only`, native via the prompt prohibition. Keep it so; Codex-driven edits belong to the sibling `codex-reviewer` skill.
- Commits, pushes, deploys, production config, DNS, external messages, payments, broad deletion from a consult response: explicit user approval first.

## Checkpoint frequency (session-checkpoint mode)

- Consult only when the advisor can materially improve a consequential decision; own reasoning and direct validation for routine, reversible or low-risk work.
- Batch related evidence and decisions into one focused consult, one narrow question. One per decision; none per tool result, probe, minor step, or as a progress check.
- Re-consult only on new evidence, an error, or a changed constraint that materially changes the decision.

## Credits

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
