# Aptus

One always-on working style for coding agents, in one skill and one hook.

Aptus merges five instruction sets and keeps their names so the model can call on the concepts:

- Thinking: Karpathy guidelines, run autonomously (no clarifying questions).
- Communication: Minto pyramid, ADHD-shaped replies, caveman wording in ASD-STE100 Simplified Technical English.
- Implementation: ponytail, the lazy senior developer who reads first and ships the shortest working diff.

Two modes. `/aptus full` (default) is caveman ultra plus ponytail ultra. `/aptus lite` is caveman full plus ponytail full. Thinking and communication rules apply in both.

## Layout

| Path | Purpose |
|---|---|
| `SKILL.md` | Full skill. Loads on `/aptus` and its trigger phrases. |
| `SKILL.compact.md` | Minimum version. The hook injects this one into every session. |
| `hooks/inject.cjs` | Emits the compact skill as session context for Claude Code, Codex and Cursor. |
| `hooks/pi/aptus.ts` | Pi extension. Appends the compact skill to the system prompt each turn. |
| `hooks/snippets.md` | Exact JSON blocks to register the hook in each harness. |

## Install

The repo root is the skill folder, so clone it straight into your skills directory. Paste this into your agent:

> Clone https://github.com/dev-willbird1936/aptus into my skills directory as `aptus` (for example `~/.claude/skills/aptus`). Back up my hook config, then register `hooks/inject.cjs` from that clone on session start using the block for this harness in `hooks/snippets.md`. For Pi, symlink `hooks/pi/aptus.ts` into `~/.pi/agent/extensions/`. Tell me which files you changed, then I will restart you.

Skill directories: `~/.claude/skills`, `~/.codex/skills`, `~/.cursor/skills`, `~/.pi/agent/skills`. One clone can serve several agents; symlink it into the others. Codex users must also run `/hooks` and trust the new definition.

Skill only, no hook, any agent the `skills` CLI supports:

```bash
npx skills add dev-willbird1936/aptus -g
```

Without the hook, Aptus loads on demand when you type `/aptus` or a trigger phrase, and is not always on.

## Manual install

1. Clone the repo into your skills directory as `aptus`.
2. Apply the matching block from `hooks/snippets.md`, with `[APTUS]` set to that clone path.
3. Restart the agent. Run `node hooks/inject.cjs claude` to check the envelope.

## Editing

The compact file is the single source for injection. Edit it and every harness picks up the change at the next session start (Pi: next turn). Keep the full and compact files in step by hand; there is no build step.

## Credits

Built from [caveman](https://github.com/JuliusBrussee/caveman), [ponytail](https://github.com/ponytail-ai/ponytail), i-have-adhd, minto-pyramid and Karpathy's coding guidelines. MIT.
