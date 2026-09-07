# Hook registration snippets

Replace `[APTUS]` with the absolute path of your clone, for example `/home/you/.claude/skills/aptus` or `C:/Users/you/.claude/skills/aptus`. Forward slashes work on Windows. Back up the config file before editing it. Merge into existing `hooks` objects; do not replace other hooks.

## Claude Code: `~/.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          { "type": "command", "command": "node [APTUS]/hooks/inject.cjs claude SessionStart", "timeout": 5 }
        ]
      }
    ],
    "SubagentStart": [
      {
        "hooks": [
          { "type": "command", "command": "node [APTUS]/hooks/inject.cjs claude SubagentStart", "timeout": 5 }
        ]
      }
    ]
  }
}
```

## Codex: `~/.codex/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          { "type": "command", "command": "node [APTUS]/hooks/inject.cjs codex", "timeout": 5 }
        ]
      }
    ]
  }
}
```

After saving, run `/hooks` inside Codex and trust the new definition. Codex does not run untrusted hooks.

## Cursor: `~/.cursor/hooks.json`

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      { "command": "node [APTUS]/hooks/inject.cjs cursor" }
    ]
  }
}
```

Cursor injects context only at session start. Subagents do not receive it.

## Pi: `~/.pi/agent/extensions/aptus.ts`

Symlink the extension. Pi loads every file in that directory.

```bash
ln -s [APTUS]/hooks/pi/aptus.ts ~/.pi/agent/extensions/aptus.ts
```

PowerShell:

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.pi\agent\extensions\aptus.ts" -Target "[APTUS]\hooks\pi\aptus.ts"
```

## Verify

```bash
node [APTUS]/hooks/inject.cjs claude
```

Prints a JSON envelope whose `additionalContext` begins with `# Aptus`. An empty `{}` means the compact file was not found.
