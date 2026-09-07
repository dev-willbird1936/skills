# Pi fallback

Read only when the native Daybreak Blue subagent route is unavailable. The parent skill's model, effort, read-only, safety, identity, and no-total-timeout rules remain mandatory.

Pi is authoritative for the model and effort pin: `openai-codex/gpt-daybreak-blue` with `--thinking xhigh`. Run exactly one Pi process for one consult, wait for it to finish, and do not start a duplicate while it is alive. Do not use `omp` unless Pi is unavailable.

## Windows PowerShell

```powershell
$pi = Get-Command pi,pi.cmd -CommandType Application -ErrorAction SilentlyContinue |
  Select-Object -First 1 -ExpandProperty Source
if (-not $pi) {
  $pi = Join-Path $env:APPDATA 'npm\pi.cmd'
}
if (-not (Test-Path -LiteralPath $pi)) {
  throw "pi not found. Install @earendil-works/pi-coding-agent, then retry."
}

$prompt = @'
<fully self-contained prompt - use the parent skill's prompt contract>
'@

& $pi --provider openai-codex --model gpt-daybreak-blue --thinking xhigh --approve --no-session -p $prompt
$status = $LASTEXITCODE
if ($status -ne 0) {
  throw "Daybreak Blue advisor consult failed (exit code $status). Do not fabricate advice."
}
```

Use the available PowerShell or shell tool's normal foreground execution if it can keep the process alive. If it imposes a per-call maximum, launch the exact command as a durable background process and poll that same process and result until it exits. Each poll may be bounded; the total consultation lifetime may not be bounded.

## POSIX shell

```bash
PI="$(command -v pi)"
"$PI" --provider openai-codex --model gpt-daybreak-blue --thinking xhigh --approve --no-session -p "$PROMPT"
status=$?
if [ "$status" -ne 0 ]; then
  echo "Daybreak Blue advisor consult failed (exit code $status). Do not fabricate advice." >&2
  exit "$status"
fi
```

The fallback returns Pi's final output as the consultation result. Preserve explicit stderr or process errors for diagnosis. Empty output or a nonzero exit means the consult failed; report that plainly instead of proceeding as if advice was received.

Do not attach a fixed timeout to the advisor process. A host-tool poll timeout is not advisor failure. Do not run both the native route and fallback for one consult.
