#!/usr/bin/env node
// hook-install: emit every *.md in the context directory as session context.
// Usage: node inject.cjs <claude|codex|cursor> [event]
// Context dir: $CONTEXT_HOOKS_DIR, else ~/.brain/hooks/context if ~/.brain exists, else ~/.context-hooks
// Fail-open: any error, or no files, prints an empty envelope and exits 0.
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');

const harness = (process.argv[2] || 'claude').toLowerCase();
const event = process.argv[3] || 'SessionStart';

function contextDir() {
  if (process.env.CONTEXT_HOOKS_DIR) return process.env.CONTEXT_HOOKS_DIR;
  const brain = path.join(os.homedir(), '.brain');
  return fs.existsSync(brain) ? path.join(brain, 'hooks', 'context') : path.join(os.homedir(), '.context-hooks');
}

function load() {
  const dir = contextDir();
  if (!fs.existsSync(dir)) return '';
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.md')).sort();
  const blocks = [];
  for (const f of files) {
    let raw = fs.readFileSync(path.join(dir, f), 'utf8').replace(/^﻿/, '');
    raw = raw.replace(/^---[\s\S]*?\n---\r?\n/, '').trim(); // drop frontmatter
    if (!raw) continue;
    const title = f.replace(/\.md$/, '');
    blocks.push(raw.startsWith('# ') ? raw : `# ${title}\n${raw}`);
  }
  return blocks.join('\n\n');
}

function emit(obj) { process.stdout.write(JSON.stringify(obj)); }

try {
  const ctx = load();
  if (!ctx) emit({});
  else if (harness === 'cursor') emit({ additional_context: ctx });
  else emit({ hookSpecificOutput: { hookEventName: event, additionalContext: ctx } });
} catch (e) {
  emit({});
}
process.exit(0);
