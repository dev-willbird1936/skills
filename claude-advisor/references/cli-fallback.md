# Claude CLI fallback

Read only when the host is not Claude Code, so the `Agent` tool and the `claude-advisor` agent definitions are unavailable (Codex, Pi, Cursor, any other harness). The parent skill's model, effort-by-mode, read-only, and no-total-timeout rules remain mandatory.

## Preconditions

- Claude Code CLI installed and authenticated. Verify with `claude --version`.
- No git repository required.
- `[EFFORT]` is `xhigh` for an individual consult and `high` for a checkpoint consult, from the parent skill's Mode section.

## POSIX shell

```bash
tmp="$(mktemp)"
claude -p --model claude-fable-5-1 --effort [EFFORT] \
  --disallowedTools Edit Write NotebookEdit Agent \
  --output-format text - <<'PROMPT_EOF' > "$tmp"
<fully self-contained prompt - use the parent skill's prompt structure>
PROMPT_EOF
status=$?
if [ "$status" -ne 0 ] || [ ! -s "$tmp" ]; then
  echo "Claude advisor consult failed (exit code $status). Do not fabricate advice." >&2
  rm -f "$tmp"; exit 1
fi
cat "$tmp"; rm -f "$tmp"
```

## Windows PowerShell

```powershell
$claude = Get-Command claude,claude.cmd,claude.exe -CommandType Application -ErrorAction SilentlyContinue |
  Select-Object -First 1 -ExpandProperty Source
if (-not $claude) { throw "Claude Code CLI not found. Install and authenticate it, then retry." }

$prompt = @'
<fully self-contained prompt - use the parent skill's prompt structure>
'@

$out = $prompt | & $claude -p --model claude-fable-5-1 --effort [EFFORT] `
  --disallowedTools Edit Write NotebookEdit Agent --output-format text -
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace(($out -join "`n"))) {
  throw "Claude advisor consult failed (exit code $LASTEXITCODE). Do not fabricate advice."
}
$out -join "`n"
```

## Rules

- The prompt goes over stdin (trailing `-`), never as a quoted argument; long or code-bearing prompts break shell escaping.
- `--disallowedTools` keeps the consult read-only. Do not add `--dangerously-skip-permissions`.
- Do not attach a fixed timeout. If the host tool enforces a per-call maximum, launch the exact command as a durable background process and poll that same process until it exits; each poll may be bounded, the total lifetime may not.
- Nonzero exit or empty output means the consult failed. Report it; never fabricate advice. Do not run this and the native route for one consult.
- The final text is the consultation result. Continue as executor afterwards.
