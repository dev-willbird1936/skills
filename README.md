# Skills

Reusable agent skills. Each top-level folder is one skill with a `SKILL.md` at its root, so the repo installs directly into a skills directory.

```bash
npx skills add dev-willbird1936/skills -g            # all
npx skills add dev-willbird1936/skills --skill aptus -g
```

| Skill | Purpose |
|---|---|
| [`aptus`](aptus/SKILL.md) | Always-on working style: Karpathy thinking, Minto and ADHD-shaped replies, caveman wording, ponytail implementation. Ships session hooks for Claude Code, Codex, Cursor and Pi. |
| [`babysit`](babysit/SKILL.md) | Supervise a separate agent task through verified completion. |
| [`bug-duplicate-check`](bug-duplicate-check/SKILL.md) | Exhaustive, read-only duplicate and prior-art investigation for one bug. |
| [`claude-advisor`](claude-advisor/SKILL.md) | Consult Fable 5.1 as a read-only second opinion from Claude Code. |
| [`codex-advisor`](codex-advisor/SKILL.md) | Consult GPT-6 Astra through Codex as a read-only advisor. |
| [`codex-blue-advisor`](codex-blue-advisor/SKILL.md) | Consult GPT Daybreak Blue at max effort through Codex. |
| [`compress`](compress/SKILL.md) | Compress any text or file: `lossless`, `lossy`, or `maximum`. |
| [`restructure`](restructure/SKILL.md) | Reword and reorder instruction text for adherence, research-backed. |
| [`reimagine`](reimagine/SKILL.md) | `/restructure` then `/compress lossy`, with backup and in-place replace. |
| [`qualverloop`](qualverloop/SKILL.md) | Quality verification loop: review until the result stops improving. |

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
