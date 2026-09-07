#!/usr/bin/env node
// aptus: emit ../SKILL.compact.md as session context.
// Usage: node inject.cjs <claude|codex|cursor> [event]
// Source file: ../SKILL.compact.md, or $APTUS_COMPACT.
// Fail-open: any error prints an empty envelope and exits 0.
'use strict';
const fs = require('fs');
const path = require('path');

const harness = (process.argv[2] || 'claude').toLowerCase();
const event = process.argv[3] || 'SessionStart';
const SRC = process.env.APTUS_COMPACT ||
  path.join(__dirname, '..', 'SKILL.compact.md');

function load() {
  const raw = fs.readFileSync(SRC, 'utf8').replace(/^﻿/, '');
  const body = raw.replace(/^---[\s\S]*?\n---\r?\n/, '').trim();
  return '# Aptus (always-on working style)\n' + body;
}

function emit(obj) { process.stdout.write(JSON.stringify(obj)); }

try {
  const ctx = load();
  if (harness === 'cursor') emit({ additional_context: ctx });
  else emit({ hookSpecificOutput: { hookEventName: event, additionalContext: ctx } });
} catch (e) {
  emit({});
}
process.exit(0);
