---
name: babysit
description: Supervise a user-requested agent task or session through status inspection, targeted steering and verified completion.
  Reuse an existing task unless the user asks to launch a new one.
---

# Babysit

## Meaning

Treat **babysit** as active supervision:

1. Read what the worker is doing: its new messages, reasoning summaries, tool calls, command output, errors, tests, and current status.
2. Understand its present approach, progress, next step, and risks.
3. Compare that evidence with the user's goal and completion criteria.
4. Send targeted steering whenever you judge it relevant or beneficial. This includes proactive advice, useful context, better approaches, risk warnings, and quality improvements—not only corrections after failure.
5. Keep reading and steering until the outcome is verified.

Do not merely launch and wait. Exercise supervisory judgment. Intervene when a message is reasonably likely to improve alignment, quality, safety, efficiency, or completion odds. Do not duplicate the worker's work or send low-value noise.

## 1. Define the contract

Extract:

- one concrete objective;
- one concise, specific base name derived from the objective (for example, `Checkout Regression`);
- observable completion criteria;
- relevant project, files, constraints, and context;
- any explicitly requested agent/model, reasoning effort, isolation mode, or token budget.

Use the text after `/babysit` or `$babysit` as the job. If no objective exists in the request or usable conversation context, ask one concise question before launch. Do not invent materially different scope.

## 2. Launch the worker

Use the current host's native tools for the named existing task. Create a separate user-visible task only when the user asks to launch one; supervision alone is not a request for a duplicate. Tool names vary by host. Use capabilities equivalent to:

- create a new chat/task/session;
- read its transcript, status, and outputs;
- send it follow-up messages;
- wait for or monitor new activity.

Prefer a user-visible persistent session over a hidden subagent. If the host cannot create, inspect, and steer another session, state that limitation instead of pretending to babysit.

Choose the correct project or general context before launch. Follow the host's default isolation/worktree behavior unless the user specifies otherwise. Preserve the user's configured agent/model and explicit reasoning effort.

Open the worker with a self-contained prompt containing:

- objective, completion criteria, context, and constraints;
- an instruction to create/set the active goal immediately using the host's native goal mechanism;
- when no native goal mechanism exists, a persistent `GOAL` and `DONE WHEN` block that the worker must track in every progress/final update;
- no token budget unless the user supplied one;
- instructions to inspect before editing, work autonomously, preserve unrelated changes, continue past planning, and verify proportionately;
- instructions to mark the goal complete only after verification and blocked only after the same blocker persists across three consecutive attempts/turns;
- instructions to report evidence, residual risks, and changed artifacts.

Capture the worker's session identifier or handle. Name it clearly when supported. Set the goal inside the worker session, not the supervisor session. If the worker begins without a goal, immediately correct it and confirm the goal is recorded.

### Name both sessions

When the host supports task/chat/session naming:

- rename the current supervisor session to `[base name] Parent`;
- name the created worker session `[base name] Baby`.

Replace `[base name]`; do not include the square brackets in the actual titles. For example, use `Checkout Regression Parent` and `Checkout Regression Baby`. Use the same relevant base name for both, keep it short enough for the host's title limits, and prefer the objective's subject over generic names such as `Babysit`. Rename the supervisor as soon as the base name is known. Set the worker title during creation when supported; otherwise rename it immediately after creation. If either naming capability is unavailable, skip only that rename and continue babysitting. Never claim a rename succeeded without tool confirmation.

## 3. Run the babysitting loop

At each checkpoint:

1. Read all new worker activity since the previous checkpoint. Include raw outputs when errors, tests, diffs, or tool evidence matter.
2. Determine: what it is doing now, why, what changed, what evidence exists, what remains, and whether its next move is sound.
3. Compare current state against every contract item.
4. Steer through the host's follow-up-message capability whenever you judge intervention relevant or materially useful.
5. Resume monitoring. If nothing new exists, wait briefly with the host's native wait/monitor mechanism; never busy-loop.

Use judgment; the following are examples, not an exhaustive trigger list. Intervene proactively whenever guidance could materially improve the result, and especially when the worker:

- drifts from scope or ignores a constraint;
- stops at a plan, summary, or partial implementation;
- overlooks a failing test, stack trace, user change, security issue, or required check;
- makes an unsupported completion claim;
- asks something answerable from available context;
- repeats an unproductive approach;
- becomes idle while safe in-scope work remains.

Send one precise steering message: observation, evidence, and required next action. Avoid duplicate prompts and avoid interrupting productive work. Keep the user informed during long supervision according to the host's update cadence.

If the worker ends early, tell it to continue and list unmet criteria. Resolve questions from explicit context when safe; otherwise ask the user one concise question, then resume supervision.

## 4. Verify

Do not accept the worker's final claim alone. Read its latest activity and evidence. Where accessible, independently inspect resulting files, diffs, tests, builds, logs, or artifacts.

Finish only when:

- the requested result exists;
- each completion criterion has evidence;
- required checks pass, or an unavoidable external/pre-existing failure is evidenced;
- no requested work remains;
- the worker marked its native goal complete or clearly recorded completion in its goal/status block.

If a gap remains, send the exact failing criterion back and keep babysitting. Report blocked only after the same blocker persists for three consecutive attempts/turns and no safe in-scope alternative remains.

## 5. Hand off

Return a self-contained supervisor summary: outcome, verification evidence, changed artifacts, and residual risk or blocker. Include the worker-task link, identifier, or host-required created-task directive when supported.

## Credits

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
