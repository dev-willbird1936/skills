---
name: codex-blue-advisor
description: >
  Read-only Daybreak Blue advisor, xhigh effort for one consult and high for checkpoints. Trigger only on `/codex-blue-advisor`,
  `/bluevisor`, or an explicit Daybreak Blue advisor request. A bare trigger or a task means
  session checkpoints; a question means one consult; `-i` forces one consult, `-chk` forces
  checkpoints. Prefer the native subagent and fall back to Pi.
---

# /codex-blue-advisor - Daybreak Blue cyber/bug-hunting consultation

## Trigger and mode

1. Before other task work, scan the whole user message (trailing lines included) for `/codex-blue-advisor`, `/bluevisor`, or an explicit Daybreak Blue advisor request. Activate on nothing else, and before the rest of that request.
2. Mode from the token directly after the trigger (case-insensitive), then what follows:

| After the trigger | Mode |
|---|---|
| `-i` (individual call) | One consult, always |
| `true`, `-chk`, `-checkpoints` | Session checkpoints, always |
| a question or a specific decision | One consult on it |
| nothing, or a task description without a question | Session checkpoints |

   Only the very next token can be a flag. Strip it before interpreting the request. A question asks for an answer now; a task asks for work; unsure, treat as a question and say which reading you took. Flags never raise consultation frequency; checkpoint policy governs that.
3. Confirm in one short line. Checkpoints: Codex Blue Advisor checkpoints active for this session; Daybreak Blue (gpt-daybreak-blue-latest) at high reasoning effort via native subagent when available, else Pi openai-codex/gpt-daybreak-blue; no skill-imposed wall-clock timeout; current session model remains executor. One consult: same line with "xhigh reasoning effort, one consult, checkpoints off". Then continue with the user's request.

## Non-negotiables (every consult)

- Advisor is a read-only second opinion. Default to no edits. It does no implementation, validation, report writing, or submission; you continue as executor after its final answer.
- An advisor response never authorizes commits, pushes, deploys, production configuration, DNS changes, external messages, payments, submissions, disclosures, uploads, maintainer contact, issue or pull request creation. Only the user's explicit authorization does. READY_FOR_USER_COPY, READY, and a valid local submission pack authorize none of these.
- Never put secrets, credentials, SSH or private keys, browser profiles, cookies, tokens, or .env contents in the advisor prompt.
- No skill-imposed wall-clock timeout. Never stop, interrupt, discard, or mark a consult failed because any duration elapsed. External platform or process-lifetime limits still apply; the skill adds no deadline. A consult ends only when: (1) advisor returns a final message; (2) advisor or subprocess exits with an explicit error; (3) user cancels.
- While waiting: short bounded polls; no update means "still running", keep waiting; a poll timeout is not an error or a consult timeout; inform the user at least once per minute.
- One advisor per consult: no second advisor while the first is alive; never run native route and Pi fallback for the same consult.
- On explicit nonzero exit or service error (including exhausted Codex or Pi quota): report failure or "come back later". No retry loop, no fabricated advice. Error or missing final message = not a consultation; never claim one happened.
- Keep cyber testing within the exact authorized target and technique boundary; never expand a test because the advisor suggests it. Prefer owned or synthetic data and minimum-impact proofs.

## Roles

- Advisor: Codex Daybreak Blue, model gpt-daybreak-blue-latest. Effort by mode: xhigh for one consult, high for every checkpoint consult.
- Preferred transport: native Codex subagent when the host exposes it.
- Fallback transport: Pi `--provider openai-codex --model gpt-daybreak-blue --thinking <xhigh|high>` by mode.
- Executor: current session's main model. Do not hardcode it unless context requires.

## Preconditions

- Native Codex subagent route accepting gpt-daybreak-blue-latest at the mode's effort, or Pi installed (`pi` on PATH) and authenticated for openai-codex.
- No git repository required.

## Running a consult

Before every consultation read [the prompt contract](references/prompt-contract.md); build a fully self-contained, read-only prompt from it that requires a concise recommendation plus assumptions and missing evidence.

### Preferred: native Daybreak Blue subagent

Use when the agent exposes native subagent tools and permits gpt-daybreak-blue-latest. No local launcher, no temporary wrapper.

1. Call the native spawn tool once: agent type `default`; model `gpt-daybreak-blue-latest`; reasoning effort `xhigh` for one consult or `high` for a checkpoint; no inherited fork or history when the host supports it (isolated prompt unless the host requires otherwise); concrete task name; the advisor prompt.
2. Record the exact advisor task name or ID.
3. Wait on that same agent with repeated bounded waits; one empty wait is not a reason to interrupt.
4. Waits may wake for unrelated input or agents: match notifications to the exact advisor ID; on ambiguity inspect statuses and keep waiting while it is active.
5. Explicit user cancellation only: interrupt that exact advisor, confirm stopped, report cancellation.
6. After the final answer, continue as executor.

### Fallback: Pi

Only when the native route is unavailable. Read [the Pi fallback](references/pi-fallback.md) before launching and follow it exactly.

### Checkpoints

Before the first checkpoint decision read [checkpoint policy](references/checkpoints.md); follow it while checkpoints are active. Consultation stays sparse, decision-focused, non-duplicative; direct validation remains primary.

## Cyber and bug-hunting posture

Daybreak Blue is an evidence-first second opinion, not a severity amplifier. Ask it to answer separately:

- Exact target, account, technique, activity authorized and in scope?
- Attacker-controlled input with supported reachability to the code or service?
- Which protected boundary, capability, data set, or availability property is actually affected?
- Reproducible with a minimum-impact proof and a meaningful negative control?
- Lead, technically reproduced finding, eligible programme issue, or report-ready submission?
- Duplicate status, P-rating, payout confidence, report quality, submission status judged separately from technical exploitability?

Ask for YES, NO, or UNCERTAIN with confidence, evidence present, missing proof, next safe validation step. Preserve exact scope, queue identity, target conditions, rate limits, allowed techniques, data-handling rules.

Scanner output, callbacks, timing anomalies, status codes or changes, crashes, and model claims are leads until independently reproduced against the security boundary with a negative control; none substitutes for protected-boundary impact.

## Treating the advice

Serious weight, not binding. Verify against actual source, scope, controls, observed behavior. If a step fails empirically or primary evidence contradicts an assumption, adapt. If evidence and Daybreak Blue disagree, surface the conflict in one focused follow-up consult instead of guessing.

For bug hunting keep these separate labels, never one: technical exploitability; protected impact and reproducibility; programme eligibility and scope; severity or P-rating; payout confidence; report quality; local report readiness; verified remote submission.

## Credits

Cloned from /codex-advisor and maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
