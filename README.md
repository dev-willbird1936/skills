# Skills

Reusable agent skills. Each top-level folder is one skill with a `SKILL.md` at its root, so the repo installs directly into a skills directory.

```bash
npx skills add dev-willbird1936/skills -g            # all
npx skills add dev-willbird1936/skills --skill aptus -g
```

## Install Reimagine

Reimagine includes its restructure and compress guides, so it needs no other skills:

```bash
npx skills add dev-willbird1936/skills --skill reimagine -g
```

Restructure and Compress remain separate, independently installable skills. Add them when you also want their standalone commands:

```bash
npx skills add dev-willbird1936/skills --skill restructure compress -g
```

## Skills

| Skill | Purpose |
|---|---|
| [`aptus`](aptus/SKILL.md) | Always-on working style: Karpathy thinking, Minto and ADHD-shaped replies, caveman wording, ponytail implementation. Ships session hooks for Claude Code, Codex, Cursor and Pi. |
| [`babysit`](babysit/SKILL.md) | Supervise a separate agent task through verified completion. |
| [`caveman`](caveman/SKILL.md) | Unofficial reimagined fork of JuliusBrussee/caveman: ultra-compressed replies, levels lite, full, ultra and wenyan. |
| [`bug-duplicate-check`](bug-duplicate-check/SKILL.md) | Exhaustive, read-only duplicate and prior-art investigation for one bug. |
| [`claude-advisor`](claude-advisor/SKILL.md) | Consult Fable 5.1 as a read-only second opinion from Claude Code. |
| [`codex-advisor`](codex-advisor/SKILL.md) | Consult GPT-6 Astra through Codex as a read-only advisor. |
| [`codex-blue-advisor`](codex-blue-advisor/SKILL.md) | Consult GPT Daybreak Blue at max effort through Codex. |
| [`compress`](compress/SKILL.md) | Compress any text or file: `lossless`, `lossy`, or `maximum`. |
| [`hook-install`](hook-install/SKILL.md) | Make any instruction text always-on: `/compress maximum` it, then inject it at session start in every harness found (Claude Code, Codex, Cursor, Pi). |
| [`ponytail`](ponytail/SKILL.md) | Unofficial reimagined fork of DietrichGebert/ponytail: the laziest solution that works, levels lite, full, ultra. |
| [`restructure`](restructure/SKILL.md) | Reword and reorder instruction text for adherence, research-backed. |
| [`reimagine`](reimagine/SKILL.md) | Self-contained restructure-and-compress workflow with backups, main and compact outputs. Bundles both guides; standalone skills remain available. |
| [`qualverloop`](qualverloop/SKILL.md) | Quality verification loop: review until the result stops improving. |

## Maintain bundled guides

`restructure/SKILL.md` and `compress/SKILL.md` are the source of truth. Do not edit their generated copies in `reimagine/references/`. After changing either source, run these commands from the repository root before publishing:

```bash
python reimagine/scripts/sync-references.py
python reimagine/scripts/sync-references.py --check
```

The check fails if either bundled guide is missing or differs from its source. This Python helper is for maintainers with a full repository checkout; installing or using Reimagine does not require running it.

Maintained by [dev-willbird1936](https://github.com/dev-willbird1936).
