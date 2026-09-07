# Native claude consult

Read only for the route identified by [SKILL.md](../SKILL.md). Commands and bare paths still resolve from the skill root. The procedures and acceptance constraints below remain authoritative for their stage.

## How to consult (the actual mechanism)

Call the `Agent` tool with:
- `subagent_type` by mode: `"claude-advisor-xhigh"` for one consult, `"claude-advisor"` for a
  checkpoint consult. Each is a dedicated agent definition in `~/.claude/agents/` that pins
  `model: claude-fable-5-1` and `effort: xhigh` or `effort: high` respectively in its own
  frontmatter (`effort` is a documented, supported frontmatter field — values `low`/`medium`/
  `high`/`xhigh`/`max` — confirmed against current official Claude Code docs). This is the REAL
  reasoning-effort lever: the generic `Agent` tool call has no per-call effort parameter for
  Claude models, but a custom subagent *definition* can pin one. **Don't also pass a `model`
  param** alongside `subagent_type` — `model` overrides the definition's pinned model for that
  one call and would silently defeat the point.
- `run_in_background: false` — this must block with no added total deadline. You need the answer
  before continuing; a background consult that reports back after you've already acted defeats
  the point. Current Claude Code documentation states that
  `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` applies only to background subagents and does not apply
  to synchronous subagents. Do not switch this consult to background mode to work around slow
  reasoning.
- `description`: short label, e.g. `"Advisor consult: <topic>"`
- `prompt`: fully self-contained. The subagent has zero memory of this conversation — it only
  sees what you write here. Include:
  1. The decision or problem, stated plainly, as a direct question.
  2. Relevant context: what's been tried, current file/state, errors seen, evidence gathered so
     far, constraints that matter.
  3. An explicit framing: *"Act as a second opinion / advisor on this decision. Give a direct,
     concise recommendation with your reasoning — not an implementation. If you disagree with the
     current approach, say so plainly and explain why."*
  4. A reinforcing effort line, in these or similar words: *"Use a high level of reasoning
     effort for this consult — think carefully and thoroughly before answering."* The agent
     definition already pins the real effort, so this line is redundant reinforcement, not the
     only lever — if it's ever the only thing pinning the effort level, that means the agent
     definition got lost or renamed; fix that instead of leaning on prompt text alone.

Verify the configured model and effort in the actual agent definition before the consult. A bare model-only call can inherit the host's current effort setting; prompt text does not establish the runtime parameter. Preserve the named agent's pin and report if the host cannot support it.

After the call returns, read the guidance, then continue the task yourself as the executor —
the consult only supplies input; you still do the actual Write/Edit/Bash work.

