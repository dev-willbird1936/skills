---
name: codex-advisor
description: >
  Turn on reliable GPT-5.6 Sol advisor consultation, via Codex CLI at high reasoning effort,
  for the rest of THIS session. Same role/mechanism as /claude-advisor, but the advisor is
  GPT-5.6 Sol (Codex CLI, `-m gpt-5.6-sol -c model_reasoning_effort=high`) instead of Fable 5,
  invoked as a read-only, no-edit `codex exec` subprocess via Bash rather than the Agent tool
  (Codex isn't a selectable Agent-tool model). Use when the user says "/codex-advisor" or its
  alias "/codevisor", "turn on codex advisor mode", "consult sol this session", "consult codex
  this session", or wants a GPT-5.6 Sol second opinion checked in on reliably rather than left
  to default timing. For the Fable 5 equivalent, see /claude-advisor (alias /claudvisor).
---

# /codex-advisor (alias: /codevisor) — GPT-5.6 Sol (Codex CLI) consultation for this session (high effort)

## Do not miss this trigger — scan the whole message, not just the first command

This trigger is frequently **appended** to the end of a longer, compound instruction — e.g. a
`/goal` command that ends with `/codex-advisor` (or the sibling `/claude-advisor`) on its own
trailing line. When that happens, it is easy to get absorbed into executing the earlier, larger
request and never reach the trailing invocation. That is a real failure mode that has happened
before with the sibling `/claude-advisor` skill: a long `/goal` command ending in
`/claude-advisor` was processed by diving straight into the technical setup work described
earlier in the message, and the trailing advisor invocation was never fired at all until the
user asked why. The same risk applies here.

To prevent that: before doing anything else in response to a new user message — before any
`Read`, `Bash`, `Glob`, or other tool call — scan the **entire** message top to bottom for this
skill's trigger phrases (`/codex-advisor`, `/codevisor`, "turn on codex advisor mode", "consult
sol this session", etc.), including text buried after other slash commands, appended on a
trailing line, or mixed into a larger paragraph. If found anywhere, invoke this skill
immediately, before starting the rest of the requested work — not after, not "when convenient,"
not folded into a later checkpoint. This is about not losing the invocation itself, not about
consulting the advisor more often once the session is active — the "When to consult" /
"When NOT to consult" guidance below is unchanged and still governs actual consult frequency
during the rest of the session.

**Roles for the rest of this session:**
- **Advisor = GPT-5.6 Sol via Codex CLI, at `high` reasoning effort**, always, regardless of
  what else changes.
- **Executor = the current session's main model**, whatever that is right now (don't hardcode a
  specific model — read it from context if it matters, otherwise it's just "you").

Claude Code also has a real, built-in `/advisor` command (a server-side tool — see
`/claude-advisor`'s notes for the full detail), but its own docs only show Claude-family models
as the advisor (e.g. `/advisor opus`), with no indication it can reach an external CLI/model
like GPT-5.6 Sol. This skill exists for that gap, not as a workaround for anything broken.

## Preconditions

- Codex CLI is installed and authenticated (ChatGPT/subscription login). Verify with
  `"$(command -v codex || command -v codex.cmd)" --version` — see the binary-resolution note
  below for why the fallback matters.
- No git repo required — the consult mechanism below passes `--skip-git-repo-check`, so it
  works from any working directory, not just inside a repo.
- Codex enforces a rolling ChatGPT usage quota that can be temporarily exhausted. If so, the
  consult below fails fast (nonzero exit / empty output file) — that's a "come back later"
  state, not a bug. Don't retry in a loop; surface it to the user instead.

## Cross-device shell selection

The reference command below is POSIX/Bash syntax. Use it unchanged on Linux/macOS VPS
terminals and Git Bash. On Windows Codex Desktop, use the PowerShell equivalent below when
the available shell/tool is PowerShell or `exec_command`; do not paste Bash syntax such as
`$(...)`, `mktemp`, or a Bash heredoc into PowerShell. Both recipes have the same behavior:
read-only execution, isolated user config, a clean final-message file, explicit working
directory, and failure on a nonzero exit or empty result.

When PowerShell is the available shell, the PowerShell recipe below is authoritative for that
invocation; the existing Bash-tool wording and Bash command remain authoritative on Bash hosts.

### Windows PowerShell equivalent

```powershell
$codex = Get-Command codex,codex.cmd,codex.exe -CommandType Application -ErrorAction SilentlyContinue |
  Select-Object -First 1 -ExpandProperty Source
if (-not $codex) {
  throw "Codex CLI not found. Install/authenticate Codex CLI, then retry."
}

$tmp = [System.IO.Path]::GetTempFileName()
$prompt = @'
<fully self-contained prompt - use the same prompt structure described below>
'@

try {
  $codexArgs = @(
    'exec',
    '--cd', $PWD.Path,
    '--skip-git-repo-check',
    '--ignore-user-config',
    '--sandbox', 'read-only',
    '--color', 'never',
    '--model', 'gpt-5.6-sol',
    '--config', 'model_reasoning_effort="high"',
    '--output-last-message', $tmp,
    '-'
  )

  # Suppress Codex event/noise on stdout; leave stderr visible for diagnostics.
  $prompt | & $codex @codexArgs 1> $null
  $status = $LASTEXITCODE
  if ($status -ne 0) {
    throw "Codex advisor consult failed (exit code $status). Do not fabricate advice."
  }
  if (-not (Test-Path -LiteralPath $tmp) -or (Get-Item -LiteralPath $tmp).Length -eq 0) {
    throw "Codex advisor consult returned no final message. Do not fabricate advice."
  }
  Get-Content -Raw -LiteralPath $tmp
}
finally {
  Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
}
```

Replace the placeholder between `@'` and `'@` with the same fully self-contained advisor
prompt required by the Bash example. If the desktop exposes Git Bash instead, use the Bash
example; if it exposes only PowerShell, use this recipe. Do not run both recipes for one
consult.

## How to consult (the actual mechanism)

There's no Claude-Code `Agent`-tool model slot for GPT-5.6 Sol (the `Agent` tool's `model`
param only takes Claude models). Consult it instead by shelling out to Codex CLI directly with
the `Bash` tool, in the foreground, with an extended timeout (pass `timeout: 600000` on the
`Bash` call — its 120000ms default can be too short for a `high`-effort consult, which can take
several minutes):

```bash
codex_bin="$(command -v codex || command -v codex.cmd)"
tmp="$(mktemp)"
"$codex_bin" exec --cd "$(pwd)" --skip-git-repo-check --ignore-user-config \
  --sandbox read-only --color never \
  -m gpt-5.6-sol -c model_reasoning_effort=high -o "$tmp" - <<'PROMPT_EOF' >/dev/null
<fully self-contained prompt — see structure below>
PROMPT_EOF
cat "$tmp"
rm -f "$tmp"
```

- `codex_bin="$(command -v codex || command -v codex.cmd)"`: resolves the binary portably.
  Confirmed live: on this Windows install, bare `codex` does NOT resolve in Claude Code's Git
  Bash (no extensionless shim, and bash doesn't apply `PATHEXT`) — only `codex.cmd` does. On
  Linux (this repo's skills also sync to a VPS) bare `codex` resolves fine; the fallback covers
  both without branching per-OS.
- `--sandbox read-only`: advisory only — Codex cannot edit files. Treat this as a strong
  default, not an absolute guarantee: Codex CLI's sandbox enforcement on Windows is newer and
  weaker than on macOS/Linux.
- Do **not** add `--ask-for-approval` — confirmed it doesn't exist on the currently installed
  CLI (`error: unexpected argument '--ask-for-approval' found`); `codex exec` is already
  non-interactive and defaults to never-approve on its own.
- `--skip-git-repo-check`: lets this run in any directory, including non-repo ones (this very
  repo, `.brain`, isn't a git repo, and the consult must still work from inside it).
- `--ignore-user-config`: skips loading `~/.codex/config.toml`. Without it, the advisor call
  also loads the user's full MCP fleet (retell/phone, resend/email, bank, github, roblox,
  serena, playwright, chrome-devtools, node_repl) under `approval: never`, and fires the user's
  Codex session-start/prompt-submit hooks — pure side-effect surface for a call that's supposed
  to be read-only analysis, and measured ~2.4x slower startup (~20s vs ~8.4s) because of it.
  Authentication is unaffected; `-m`/`-c` still pin model/effort regardless of the now-ignored
  config defaults.
- `-m gpt-5.6-sol -c model_reasoning_effort=high`: pins the model and effort explicitly, so
  the consult stays correct even if `~/.codex/config.toml`'s defaults ever drift.
- `--color never`: keeps the captured output free of ANSI escape codes.
- `-o "$tmp"`, with stdout suppressed (`>/dev/null`, stderr kept) and read back from `$tmp`
  after: `codex exec` interleaves reasoning/tool-call noise on stdout and isn't clean to parse
  directly, so capture the clean final message separately via `--output-last-message` (`-o`)
  instead. Same pattern `claude-codex-proxy.js` uses elsewhere in this repo.
- The heredoc (`<<'PROMPT_EOF'`, quoted delimiter) pipes the prompt over stdin (the trailing
  `-` tells `codex exec` to read it from there) — this sidesteps shell-quoting/escaping issues
  entirely for prompts containing quotes, backticks, or code snippets. Don't inline the prompt
  as a quoted CLI argument instead; long or code-bearing prompts will break shell escaping.
- **Empty `$tmp` or a nonzero exit code means the consult failed — do not fabricate advice.**
  Report the failure plainly (quota exhaustion is a common cause) instead of proceeding as if a
  consult happened.

The prompt (inside the heredoc) must be fully self-contained — the Codex subprocess has zero
memory of this conversation. Include:
1. The decision or problem, stated plainly, as a direct question.
2. Relevant context: what's been tried, current file/state, errors seen, evidence gathered so
   far, constraints that matter.
3. An explicit framing: *"Act as a second opinion / advisor on this decision. Give a direct,
   concise recommendation with your reasoning — not an implementation. If you disagree with the
   current approach, say so plainly and explain why."*

After the call returns, read `$tmp`'s contents, then continue the task yourself as the
executor — the consult only supplies input; you still do the actual Write/Edit/Bash work.

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
Each consult is a real Codex CLI subprocess call at `high` effort — slower than a default-effort
call and not free — don't spam it.

## Safety

- Default to no edits — the `--sandbox read-only` flag enforces this; don't loosen it just to
  get a consult to "fix it directly" — that's not this skill's job (see the sibling
  `codex-reviewer` skill if actual Codex-driven edits are wanted instead of advice).
- No commits, pushes, deploys, production config, DNS, external messages, payments, or broad
  deletion triggered from a consult response without explicit user approval.
- Do not print or leak secrets, credentials, SSH keys, browser profiles, cookies, or `.env`
  file contents into the prompt sent to Codex.

## On activation

Confirm in one short line that advisor checkpoints are active for this session (GPT-5.6 Sol at
`high` reasoning effort via `codex exec -m gpt-5.6-sol -c model_reasoning_effort=high`,
executor = current session model), then continue with whatever the user asked for.

## Credits

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
