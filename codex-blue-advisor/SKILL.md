---
name: codex-blue-advisor
description: >
  Enable session-wide, read-only Daybreak Blue advisor checkpoints at max effort.
  Trigger only on `/codex-blue-advisor`, `/codeblue-advisor`, `/bluevisor`, or an
  explicit Daybreak Blue advisor request. Prefer the native subagent and fall back to Pi.
---

# /codex-blue-advisor (aliases: /codeblue-advisor, /bluevisor) - Daybreak Blue cyber/bug-hunting consultation (max effort)

## Trigger detection

Before other task work, scan the entire user message, including trailing lines in compound requests. Activate only for `/codex-blue-advisor`, `/codeblue-advisor`, `/bluevisor`, or an explicit Daybreak Blue advisor request. Invoke it before the rest of that request; checkpoint policy still controls later consultation frequency.

## Mode: session checkpoints (explicit flag supported)

This skill remains session-oriented: a bare trigger enables checkpoints for the rest of the
session, preserving its existing behavior. The token directly after the trigger may explicitly
select the same mode: `true`, `-chk`, or `-checkpoints`. Matching is case-insensitive; the token
counts only when it immediately follows the trigger, and the flag is stripped before interpreting
the request. The explicit flag does not increase consultation frequency.

## Read by route

- Before every consultation, read [the prompt contract](references/prompt-contract.md).
- Before the first checkpoint decision, read [checkpoint policy](references/checkpoints.md).
- If the native route is unavailable, read [the Pi fallback](references/pi-fallback.md) before launching anything.

## Roles for the rest of this session

- Advisor = Codex Daybreak Blue, model gpt-daybreak-blue-latest, pinned at max reasoning effort.
- Preferred transport = the native Codex subagent when the host exposes it.
- Fallback transport = Pi with --provider openai-codex --model gpt-daybreak-blue
  and --thinking max.
- Executor = the current session's main model, whatever it is right now. Do not hardcode the
  executor model unless the context requires it.

## No skill-imposed consultation timeout

An advisor consult has no skill-imposed wall-clock timeout. Never stop, interrupt, discard, or
classify a consult as failed because six minutes, ten minutes, or any other duration elapsed.
The skill cannot override an external platform or server process-lifetime limit, but it must not
add its own total deadline. Completion has only three terminal states:

1. The advisor returns a final message.
2. The advisor or subprocess exits with an explicit error.
3. The user cancels it.

Keep the user informed at least once per minute while waiting. Use short polling waits so the
session stays responsive, but do not confuse a poll timeout with a consultation timeout. A poll
that returns no update means only "still running"; continue waiting. Never create a new advisor
for the same consult while the original remains alive.

## Cyber and bug-hunting posture

Use Daybreak Blue as an evidence-first second opinion, not as an automatic severity amplifier.
For cyber-security and bug-hunting decisions, ask it to keep these questions separate:

- Is the exact target, account, technique, and activity authorized and in scope?
- Is there attacker-controlled input and supported reachability to the relevant code or service?
- What protected boundary, capability, data set, or availability property is actually affected?
- Is the effect reproducible with a minimum-impact proof and a meaningful negative control?
- Is the result a lead, a technically reproduced finding, an eligible programme issue, or a
  report-ready submission?
- Are duplicate status, P-rating, payout confidence, report quality, and submission status
  being evaluated separately from technical exploitability?

Prefer direct YES, NO, or UNCERTAIN recommendations with confidence, evidence present, missing
proof, and the next safe validation step. Preserve exact scope, queue identity, target
conditions, rate limits, allowed techniques, and data-handling rules. Use owned or synthetic
data where possible. Do not let a scanner hit, callback, crash, timing anomaly, or status
change stand in for protected-boundary impact.

## Preconditions

- A native Codex subagent route is available and accepts model gpt-daybreak-blue-latest with
  max reasoning effort, or Pi is installed (`pi` on PATH) and authenticated for openai-codex.
- No git repository is required for the consultation. The native route should use an isolated
  prompt with no inherited task context unless the host requires otherwise.
- The Codex or Pi quota may be temporarily exhausted. If the consult fails with an explicit
  nonzero exit or service error, surface that as a failure or "come back later" state. Do not
  retry in a loop and do not fabricate advice.
- Never place secrets, credentials, browser profiles, cookies, private keys, or .env contents
  in the advisor prompt.

## Preferred route: native Daybreak Blue subagent

When the current agent exposes native subagent tools and permits
gpt-daybreak-blue-latest, use that route. Do not shell out to the local launcher for the same
consult and do not create a temporary wrapper.

Call the native spawn tool once with:

- agent type: default
- model: gpt-daybreak-blue-latest
- reasoning effort: max
- no inherited conversation fork or history when the host supports that option
- a concrete task name
- a fully self-contained, read-only advisor prompt using the linked prompt contract

The prompt must say that the advisor must not edit files, run state-changing commands, commit,
push, deploy, send messages, submit or disclose findings, or take other external actions. The
prompt should require a concise recommendation and identify assumptions and missing evidence.

Track the exact spawned advisor task name or ID. Wait for that same agent using repeated bounded
wait calls for responsiveness; do not impose a total deadline and do not interrupt a healthy
advisor because one wait call returned without an update.

A wait may wake for unrelated user input or another agent. Match completion or error
notifications to the exact advisor ID. On an ambiguous wake, inspect the agent statuses and
continue waiting if the advisor remains active. Only explicit user cancellation ends a healthy
consult; interrupt that exact advisor, confirm it stopped, and report cancellation.

After the final answer arrives, continue the task yourself as executor. The advisor supplies a
second opinion; it does not perform the implementation, validation, report writing, or
submission.

## Fallback route: local Daybreak Blue via Pi

Use only when the native route is unavailable. Follow [the Pi fallback](references/pi-fallback.md) exactly; do not run both routes or add a total consultation timeout.

## Advisor prompt contract

Before each consultation, follow [the prompt contract](references/prompt-contract.md). Continue as executor after a verified final response; an explicit error or missing final message is not a completed consultation.

## Checkpoint use

When checkpoints are active, follow [checkpoint policy](references/checkpoints.md). It keeps consultation sparse, decision-focused and non-duplicative; direct validation remains primary.

## How to treat the advice

Give the advice serious weight, but it is not binding. Verify its claims against the actual
source, scope, controls, and observed behavior.

If a suggested step fails empirically, or primary evidence contradicts a specific assumption,
adapt rather than forcing the recommendation. If the evidence points one way and Daybreak Blue
points another, surface the conflict in one focused follow-up consult instead of guessing.

For bug hunting, never collapse these into one label:

- technical exploitability
- protected impact and reproducibility
- programme eligibility and scope
- severity or P-rating
- payout confidence
- report quality
- local report readiness
- verified remote submission

READY_FOR_USER_COPY, READY, and a valid local submission pack do not authorize disclosure,
upload, maintainer contact, issue creation, pull request creation, or submission.

## Safety

- Default to no edits. The advisor is a read-only second opinion, not an implementation agent.
- No commits, pushes, deploys, production configuration, DNS changes, external messages,
  payments, submissions, or disclosures may be triggered by an advisor response without the
  user's explicit authorization.
- Keep cyber testing within the exact authorized target and technique boundary. Prefer
  owned or synthetic data and minimum-impact proofs. Do not expand a test because the advisor
  suggests it.
- Do not print or leak secrets, credentials, SSH keys, browser profiles, cookies, tokens, or
  .env contents into the prompt sent to Daybreak Blue.
- Treat scanner output, callbacks, timing, status codes, crashes, and model claims as leads
  until independently reproduced against the relevant security boundary with an appropriate
  negative control.

## On activation

Confirm in one short line that Codex Blue Advisor checkpoints are active for this session:
Daybreak Blue (gpt-daybreak-blue-latest) at max reasoning effort via the native subagent when
available, Pi openai-codex/gpt-daybreak-blue fallback otherwise, no skill-imposed wall-clock timeout,
and the current session model remains executor. Then continue with whatever the user asked for.

## Credits

Cloned from /codex-advisor and maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
