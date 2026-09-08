#!/usr/bin/env node
// hook-install: register the context injector in every harness found on this machine.
// Usage: node register.cjs [--dry-run] [--only claude,codex,cursor,pi]
// Idempotent: an existing registration that points at this script is left alone.
// Every edited config is backed up beside itself as <file>.bak-<timestamp> first.
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');

const HOME = os.homedir();
const HERE = __dirname;
const INJECT = path.join(HERE, 'inject.cjs').replace(/\\/g, '/');
const PI_EXT = path.join(HERE, 'pi-context-hooks.ts');
const args = process.argv.slice(2);
const dry = args.includes('--dry-run');
const onlyIdx = args.indexOf('--only');
const only = onlyIdx >= 0 ? args[onlyIdx + 1].split(',') : null;
const ts = new Date().toISOString().replace(/[-:]/g, '').replace(/\..*/, '').replace('T', '-');
const report = [];
const did = dry ? 'would register' : 'registered';

function want(h) { return !only || only.includes(h); }
function readJson(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }
function backup(p) { if (!dry) fs.copyFileSync(p, `${p}.bak-${ts}`); return `${p}.bak-${ts}`; }
function writeJson(p, obj) { if (!dry) fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n'); }
function has(groups, needle) { return JSON.stringify(groups || []).includes(needle); }

// Claude Code: ~/.claude/settings.json, SessionStart + SubagentStart
if (want('claude')) {
  const p = path.join(HOME, '.claude', 'settings.json');
  if (fs.existsSync(p)) {
    const s = readJson(p); s.hooks = s.hooks || {};
    const cmd = (ev) => `node ${INJECT} claude ${ev}`;
    let changed = false;
    if (!has(s.hooks.SessionStart, INJECT)) {
      s.hooks.SessionStart = [...(s.hooks.SessionStart || []), { matcher: 'startup|resume|clear|compact', hooks: [{ type: 'command', command: cmd('SessionStart'), timeout: 5 }] }]; changed = true;
    }
    if (!has(s.hooks.SubagentStart, INJECT)) {
      s.hooks.SubagentStart = [...(s.hooks.SubagentStart || []), { hooks: [{ type: 'command', command: cmd('SubagentStart'), timeout: 5 }] }]; changed = true;
    }
    if (changed) { const b = backup(p); writeJson(p, s); report.push(`claude: ${did} SessionStart + SubagentStart in ${p} (backup ${b})`); }
    else report.push(`claude: already registered in ${p}`);
  } else report.push('claude: not found (no ~/.claude/settings.json)');
}

// Codex: ~/.codex/hooks.json, SessionStart
if (want('codex')) {
  const dir = path.join(HOME, '.codex');
  if (fs.existsSync(dir)) {
    const p = path.join(dir, 'hooks.json');
    const s = fs.existsSync(p) ? readJson(p) : { hooks: {} }; s.hooks = s.hooks || {};
    if (!has(s.hooks.SessionStart, INJECT)) {
      s.hooks.SessionStart = [...(s.hooks.SessionStart || []), { matcher: 'startup|resume|clear|compact', hooks: [{ type: 'command', command: `node ${INJECT} codex`, timeout: 5 }] }];
      const b = fs.existsSync(p) ? backup(p) : '(new file)'; writeJson(p, s);
      report.push(`codex: ${did} SessionStart in ${p} (backup ${b}); run /hooks inside Codex and trust it`);
    } else report.push(`codex: already registered in ${p}`);
  } else report.push('codex: not found (no ~/.codex)');
}

// Cursor: ~/.cursor/hooks.json, sessionStart
if (want('cursor')) {
  const dir = path.join(HOME, '.cursor');
  if (fs.existsSync(dir)) {
    const p = path.join(dir, 'hooks.json');
    const s = fs.existsSync(p) ? readJson(p) : { version: 1, hooks: {} }; s.hooks = s.hooks || {};
    if (!has(s.hooks.sessionStart, INJECT)) {
      s.hooks.sessionStart = [...(s.hooks.sessionStart || []), { command: `node ${INJECT} cursor` }];
      const b = fs.existsSync(p) ? backup(p) : '(new file)'; writeJson(p, s);
      report.push(`cursor: ${did} sessionStart in ${p} (backup ${b})`);
    } else report.push(`cursor: already registered in ${p}`);
  } else report.push('cursor: not found (no ~/.cursor)');
}

// Pi: symlink extension into ~/.pi/agent/extensions
if (want('pi')) {
  const dir = path.join(HOME, '.pi', 'agent', 'extensions');
  if (fs.existsSync(path.join(HOME, '.pi', 'agent'))) {
    const link = path.join(dir, 'context-hooks.ts');
    let ok = false;
    try { ok = fs.realpathSync(link) === fs.realpathSync(PI_EXT); } catch (_) {}
    if (ok) report.push(`pi: already linked at ${link}`);
    else if (!dry) {
      fs.mkdirSync(dir, { recursive: true });
      try { fs.unlinkSync(link); } catch (_) {}
      try { fs.symlinkSync(PI_EXT, link, 'file'); report.push(`pi: linked ${link} -> ${PI_EXT}`); }
      catch (e) { fs.copyFileSync(PI_EXT, link); report.push(`pi: copied (symlink failed: ${e.code}) ${PI_EXT} -> ${link}`); }
    } else report.push(`pi: would link ${link} -> ${PI_EXT}`);
  } else report.push('pi: not found (no ~/.pi/agent)');
}

console.log((dry ? '[dry-run]\n' : '') + report.join('\n'));
