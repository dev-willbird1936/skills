---
name: claude-advisor
description: >
  Turn on an explicit, guaranteed-xhigh-effort Fable 5 advisor consultation for the rest of
  THIS session. Claude Code has a real, built-in `/advisor` command (a server-side tool,
  confirmed via official docs — invisible to ToolSearch/tool-list checks by design, which is
  why an earlier check wrongly concluded it was absent) that runs ambiently once
  `advisorModel` is set in settings.json (already `"fable"` here): Claude decides on its own
  when to consult it, at some default effort level you don't control. This skill is a
  deliberate complement, not a workaround for something broken: spawn a Fable 5 subagent via
  the Agent tool using a dedicated `claude-advisor` subagent definition
  (`~/.claude/agents/claude-advisor.md`, pinned `model: fable` + `effort: xhigh`) for an
  explicit, on-demand second opinion at key checkpoints, with full control over exactly what's
  asked — while the current session's main model (whatever is selected — Sonnet, Opus, Haiku,
  etc.) continues to do the actual implementation. Use when the user says "/claude-advisor" or
  its alias "/claudvisor", "turn on advisor mode", "consult fable this session", "make the
  advisor actually fire", or wants a guaranteed-xhigh-effort Fable consult rather than leaving
  it to native /advisor's opaque default timing/effort. For the same mechanism against GPT-5.6
  Sol via Codex CLI instead (native /advisor is Claude-model-only), see /codex-advisor (alias
  /codevisor).
---

# /claude-advisor (alias: /claudvisor) — explicit, guaranteed-xhigh-effort Fable 5 consultation for this session

## Do not miss this trigger — scan the whole message, not just the first command

This trigger is frequently **appended** to the end of a longer, compound instruction — e.g. a
`/goal` command that ends with `/claude-advisor` on its own trailing line. When that happens,
it is easy to get absorbed into executing the earlier, larger request and never reach the
trailing invocation. That is a real failure mode that has happened before: a long `/goal`
command ending in `/claude-advisor` was processed by diving straight into the technical setup
work described earlier in the message, and the trailing `/claude-advisor` was never invoked at
all until the user asked why.

To prevent that: before doing anything else in response to a new user message — before any
`Read`, `Bash`, `Glob`, or other tool call — scan the **entire** message top to bottom for this
skill's trigger phrases (`/claude-advisor`, `/claudvisor`, "turn on advisor mode", "consult
fable this session", etc.), including text buried after other slash commands, appended on a
trailing line, or mixed into a larger paragraph. If found anywhere, invoke this skill
immediately, before starting the rest of the requested work — not after, not "when convenient,"
not folded into a later checkpoint. This is about not losing the invocation itself, not about
consulting the advisor more often once the session is active — the "When to consult" /
"When NOT to consult" guidance below is unchanged and still governs actual consult frequency
during the rest of the session.

Claude Code's native `/advisor` command is real — a **server-side tool** (confirmed via
official docs at `code.claude.com/docs/en/advisor.md`), which is exactly why checking the
top-level tool list or `ToolSearch` for it finds nothing: server-side tools are invisible at
that layer *by design*, regardless of whether they're working. An earlier version of this
skill concluded "no callable tool exists" from that check — that conclusion was wrong; the
check simply couldn't see the right layer either way. This install is fully compatible (Claude
Code 2.1.198 ≥ the v2.1.98 base requirement and the v2.1.170 Fable-specific requirement; direct
Anthropic API, not Bedrock/Vertex/Foundry) and `advisorModel: "fable"` is already set in
`~/.claude/settings.json`.

**This skill is not a workaround for something broken — it's a deliberate complement.** Native
`/advisor` runs *ambiently*: once configured, Claude decides on its own when to consult it, at
some default reasoning effort you neither see nor control, and (per the docs' own examples,
`/advisor opus`) it appears to only support Claude-family models as the advisor. This skill
gives you an *explicit*, on-demand consult instead — guaranteed `effort: xhigh`, fired exactly
when you or the executor decides, with full control over what's actually asked. Use native
`/advisor` for background checkpoints; use `/claude-advisor` when you want a guaranteed
xhigh-effort second opinion on a specific decision, right now, in your own words.

**Roles for the rest of this session:**
- **Advisor = Fable 5, pinned at `xhigh` reasoning effort**, always, regardless of what else
  changes.
- **Executor = the current session's main model**, whatever that is right now (don't hardcode a
  specific model — read it from context if it matters, otherwise it's just "you").

## How to consult (the actual mechanism)

Call the `Agent` tool with:
- `subagent_type: "claude-advisor"` — a dedicated agent definition at
  `~/.claude/agents/claude-advisor.md` that pins `model: fable` and `effort: xhigh` in its own
  frontmatter (`effort` is a documented, supported frontmatter field — values `low`/`medium`/
  `high`/`xhigh`/`max` — confirmed against current official Claude Code docs). This is the REAL
  reasoning-effort lever: the generic `Agent` tool call has no per-call effort parameter for
  Claude models, but a custom subagent *definition* can pin one. **Don't also pass a `model`
  param** alongside `subagent_type` — `model` overrides the definition's pinned model for that
  one call and would silently defeat the point.
- `run_in_background: false` — this must block. You need the answer before continuing; a
  background consult that reports back after you've already acted defeats the point.
- `description`: short label, e.g. `"Advisor consult: <topic>"`
- `prompt`: fully self-contained. The subagent has zero memory of this conversation — it only
  sees what you write here. Include:
  1. The decision or problem, stated plainly, as a direct question.
  2. Relevant context: what's been tried, current file/state, errors seen, evidence gathered so
     far, constraints that matter.
  3. An explicit framing: *"Act as a second opinion / advisor on this decision. Give a direct,
     concise recommendation with your reasoning — not an implementation. If you disagree with the
     current approach, say so plainly and explain why."*
  4. A reinforcing high-effort line, in these or similar words: *"Use a high level of reasoning
     effort for this consult — think carefully and thoroughly before answering."* The
     `claude-advisor` agent definition already pins real `xhigh` effort, so this line is
     redundant reinforcement, not the only lever — if it's ever the only thing pinning the
     effort level, that means the agent definition got lost or renamed; fix that instead of
     leaning on prompt text alone.

**Why the agent definition, not just a prompt instruction:** the session-level effort setting in
this environment defaults to `low` (`effortLevel` in `~/.claude/settings.json`), and a bare
`Agent(model:"fable")` call with no `subagent_type` inherits that default — so a pinned effort
level via prompt text alone was cosmetic, not real. This was caught by a live consult and fixed
by pinning `effort: xhigh` in the `claude-advisor` agent definition instead. Don't regress to a
bare `model:"fable"` call.

After the call returns, read the guidance, then continue the task yourself as the executor —
the consult only supplies input; you still do the actual Write/Edit/Bash work.

## When to consult

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

## When NOT to consult

- Simple factual lookups or arithmetic — answer those directly.
- Short reactive steps where the next action is dictated by tool output just read — the advisor
  adds most of its value before the approach crystallizes, not on every step after.
- Don't re-consult on the same decision unless something material changed (new error, new
  evidence, or genuinely reconsidering the approach).

## How to treat the advice

Give it serious weight, but it isn't binding. If a suggested step fails empirically, or there's
primary-source evidence contradicting a specific claim (the file says X, the advisor assumed Y),
adapt rather than force it. If evidence already gathered points one way and the advisor points
another, don't silently pick a side — surface the conflict in one more short consult ("found X,
you suggested Y — which constraint breaks the tie?") instead of guessing.

Keep consults focused on small decisions rather than asking for an exhaustive plan every time.
Each consult is a real, billed Fable 5 subagent call, run at real `xhigh` effort — don't spam it.

## On activation

Confirm in one short line that advisor checkpoints are active for this session (Fable 5 at real
`xhigh` reasoning effort via `Agent(subagent_type: "claude-advisor")`, executor = current
session model), then continue with whatever the user asked for.

## Credits

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
