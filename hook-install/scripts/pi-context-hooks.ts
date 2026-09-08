/**
 * hook-install: append every *.md in the context directory to Pi's system prompt
 * on every turn (before_agent_start). Idempotent via marker comments.
 * Install: symlink this file into ~/.pi/agent/extensions/context-hooks.ts.
 * Context dir: $CONTEXT_HOOKS_DIR, else ~/.brain/hooks/context if ~/.brain exists, else ~/.context-hooks
 */
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const START = "<!--context-hooks-->";
const END = "<!--/context-hooks-->";
const BLOCK_RE = /\n?<!--context-hooks-->[\s\S]*?<!--\/context-hooks-->/g;

function contextDir(): string {
  if (process.env.CONTEXT_HOOKS_DIR) return process.env.CONTEXT_HOOKS_DIR;
  const brain = join(homedir(), ".brain");
  return existsSync(brain) ? join(brain, "hooks", "context") : join(homedir(), ".context-hooks");
}

function load(): string {
  const dir = contextDir();
  if (!existsSync(dir)) return "";
  const blocks: string[] = [];
  for (const f of readdirSync(dir).filter((n) => n.endsWith(".md")).sort()) {
    const raw = readFileSync(join(dir, f), "utf8").replace(/^﻿/, "").replace(/^---[\s\S]*?\n---\r?\n/, "").trim();
    if (!raw) continue;
    blocks.push(raw.startsWith("# ") ? raw : `# ${f.replace(/\.md$/, "")}\n${raw}`);
  }
  return blocks.join("\n\n");
}

export default function (pi: ExtensionAPI) {
  pi.on("before_agent_start", (event) => {
    const body = load();
    const base = event.systemPrompt.replace(BLOCK_RE, "").trimEnd();
    if (!body) return base === event.systemPrompt ? undefined : { systemPrompt: base };
    return { systemPrompt: `${base}\n\n${START}\n${body}\n${END}` };
  });
}
