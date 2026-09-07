---
name: babysit
description: Supervise a user-requested agent task or session through status inspection, targeted steering and verified completion.
  Reuse an existing task unless the user asks to launch a new one.
---

# Babysit

Active supervision of a worker session: read its activity, compare with the contract, steer, verify the outcome yourself. Job = text after `/babysit` or `$babysit`.

## Non-negotiables

- Attach to the existing named task with the host's native tools. Create a new user-visible task only when the user asks to launch one; supervision alone is not a launch request.
- Prefer a user-visible persistent session over a hidden subagent. If the host cannot create, inspect, and steer another session, state that instead of pretending to babysit.
- Take the objective from the request or usable conversation context; if none, ask one concise question before launch. Never invent materially different scope.
- Preserve the user's configured agent/model, explicit reasoning effort, isolation mode and token budget. Follow the host's default isolation/worktree behaviour unless the user specifies otherwise. Give the worker no token budget unless the user supplied one.
- Accept no worker claim (completion, rename, anything) without tool evidence.
- Steer whenever a message is reasonably likely to improve alignment, quality, safety, efficiency or completion odds: proactive advice, context, better approaches, risk warnings, quality improvements. No low-value noise, duplicate prompts, or interrupting productive work. Never do the worker's work for it.

## 1. Contract

Extract:

- one concrete objective;
- one short, specific base name from the objective's subject (e.g. `Checkout Regression`), within host title limits, never generic like `Babysit`;
- observable completion criteria;
- relevant project, files, constraints, context;
- any explicitly requested agent/model, reasoning effort, isolation mode or token budget.

## 2. Attach or launch

Use host capabilities equivalent to: create a chat/task/session; read its transcript, status, outputs; send follow-up messages; wait for/monitor new activity. Pick the correct project or general context before launch.

When launching, give the worker a self-contained prompt with:

- objective, completion criteria, context, constraints;
- create/set the active goal immediately via the host's native goal mechanism; if none exists, keep a persistent `GOAL` and `DONE WHEN` block in every progress/final update;
- inspect before editing, work autonomously, preserve unrelated changes, continue past planning, verify proportionately;
- mark the goal complete only after verification, blocked only after the same blocker persists across three consecutive attempts/turns;
- report evidence, residual risks, changed artifacts.

Capture the worker's session identifier/handle. The goal lives in the worker session, not the supervisor's; if the worker starts without one, correct it immediately and confirm it is recorded.

### Name both sessions

When the host supports naming:

- rename the supervisor session `[base name] Parent` as soon as the base name is known;
- name the worker `[base name] Baby` at creation when supported, else rename it immediately after.

Without brackets: `Checkout Regression Parent`, `Checkout Regression Baby`. If either rename is unavailable, skip only that one and continue. Claim a rename succeeded only after tool confirmation.

## 3. Loop

Each checkpoint:

1. Read all new worker activity since the last checkpoint: messages, reasoning summaries, tool calls, command output, errors, tests, status. Read raw output when errors, tests, diffs or tool evidence matter.
2. Determine what it is doing, why, what changed, what evidence exists, what remains, its risks, whether its next move is sound.
3. Compare against every contract item.
4. Steer via the host's follow-up-message capability whenever intervention is relevant or materially useful.
5. Resume. If nothing new, wait briefly with the host's native wait/monitor mechanism; never busy-loop.

Intervene proactively whenever guidance could materially improve the result, including when the worker:

- drifts from scope or ignores a constraint;
- stops at a plan, summary or partial implementation;
- overlooks a failing test, stack trace, user change, security issue or required check;
- makes an unsupported completion claim;
- asks something answerable from available context;
- repeats an unproductive approach;
- idles while safe in-scope work remains.

One precise steering message: observation, evidence, required next action. If the worker ends early, tell it to continue and list unmet criteria. Answer its questions from explicit context when safe; else ask the user one concise question, then resume. Keep the user informed during long supervision per the host's update cadence.

## 4. Verify

Read the worker's latest activity and evidence. Where accessible, independently inspect resulting files, diffs, tests, builds, logs or artifacts. Finish only when:

- the requested result exists;
- each completion criterion has evidence;
- required checks pass, or an unavoidable external/pre-existing failure is evidenced;
- no requested work remains;
- the worker marked its native goal complete or clearly recorded completion in its goal/status block.

If a gap remains, send the exact failing criterion back and keep babysitting. Report blocked only after the same blocker persists for three consecutive attempts/turns and no safe in-scope alternative remains.

## 5. Hand off

Self-contained supervisor summary: outcome, verification evidence, changed artifacts, residual risk or blocker. Include the worker-task link, identifier or host-required created-task directive when supported.

## Credits

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
