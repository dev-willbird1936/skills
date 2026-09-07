# Cli fallback

Read only for the route identified by [SKILL.md](../SKILL.md). Commands and bare paths still resolve from the skill root. The procedures and acceptance constraints below remain authoritative for their stage.

## Preconditions

- `[EFFORT]` is `xhigh` for an individual consult and `high` for a checkpoint consult, from the parent skill's Mode section.

- Codex CLI is installed and authenticated (ChatGPT/subscription login). Verify with
  `"$(command -v codex || command -v codex.cmd)" --version` — see the binary-resolution note
  below for why the fallback matters.
- No git repo required — the consult mechanism below passes `--skip-git-repo-check`, so it
  works from any working directory, not just inside a repo.
- Codex enforces a rolling ChatGPT usage quota that can be temporarily exhausted. If so, the
  consult below fails fast (nonzero exit / empty output file) — that's a "come back later"
  state, not a bug. Don't retry in a loop; surface it to the user instead.

## CLI fallback: cross-device shell selection

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
    '--model', 'gpt-6-astra',
    '--config', 'model_reasoning_effort="[EFFORT]"',
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

## CLI fallback mechanism

Use this only when the native Astra-subagent route is unavailable. Claude Code's `Agent` tool, for
example, accepts Claude-family models only, so shell out to Codex CLI there.

Do not attach a fixed timeout to the consultation. If the host shell tool can keep a foreground
process alive indefinitely, use it. If the host tool enforces a per-call maximum, launch the
exact command as a durable background process and poll that same process/result until it exits.
Each poll may be bounded; total consultation lifetime must not be bounded. A tool-level poll
timeout is not advisor failure.

POSIX command:

```bash
codex_bin="$(command -v codex || command -v codex.cmd)"
tmp="$(mktemp)"
"$codex_bin" exec --cd "$(pwd)" --skip-git-repo-check --ignore-user-config \
  --sandbox read-only --color never \
  -m gpt-6-astra -c model_reasoning_effort=[EFFORT] -o "$tmp" - <<'PROMPT_EOF' >/dev/null
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
- `-m gpt-6-astra -c model_reasoning_effort=[EFFORT]`: pins the model and effort explicitly, so
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

