/**
 * aptus: append SKILL.compact.md to Pi's system prompt on every
 * turn (before_agent_start). Idempotent via marker comments.
 * Install: symlink this file into ~/.pi/agent/extensions/aptus.ts.
 * Source file: ../../SKILL.compact.md relative to the real
 * location of this file, or $APTUS_COMPACT.
 */
import { existsSync, readFileSync, realpathSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const HERE = dirname(realpathSync(fileURLToPath(import.meta.url)));
const SRC = process.env.APTUS_COMPACT || join(HERE, "..", "..", "SKILL.compact.md");
const START = "<!--aptus-->";
const END = "<!--/aptus-->";
const BLOCK_RE = /\n?<!--aptus-->[\s\S]*?<!--\/aptus-->/g;

function load(): string | undefined {
  if (!existsSync(SRC)) return undefined;
  const body = readFileSync(SRC, "utf8").replace(/^﻿/, "").replace(/^---[\s\S]*?\n---\r?\n/, "").trim();
  return body || undefined;
}

export default function (pi: ExtensionAPI) {
  pi.on("before_agent_start", (event) => {
    const body = load();
    const base = event.systemPrompt.replace(BLOCK_RE, "").trimEnd();
    if (!body) return base === event.systemPrompt ? undefined : { systemPrompt: base };
    return { systemPrompt: `${base}\n\n${START}\n# Aptus (always-on working style)\n${body}\n${END}` };
  });
}
