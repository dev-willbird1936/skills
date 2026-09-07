---
name: bug-duplicate-check
description: >-
  Run an exhaustive, read-only duplicate and prior-art investigation for one
  supplied bug. Trigger only when asked whether it is known, reported, fixed,
  disclosed, duplicated, a variant or bypass, or plausibly new before triage,
  filing, disclosure, or submission; not for ordinary bug fixing or discovery.
---

# Bug Duplicate Check

## Canonical registry

If this check changes a finding or hunt row, use the Google Workspace MCP
against the spreadsheet in `System/registry.md`. Canonical finding records
live at `Findings/<program>/<software>/<id>/`. Local CSV files are derived
views, not authority.

Determine whether the same underlying bug already exists anywhere relevant. Optimize for avoiding false novelty claims, not for producing a fast answer.

## Operating contract

- Keep the investigation read-only. Do not file, comment, disclose, edit repositories, or mutate trackers.
- Use tools and current sources. Never decide from memory, search snippets, titles alone, or one database.
- Search security and non-security prior art. A bug can be documented as an issue, fix, regression test, release note, support thread, commit, advisory, duplicate closure, or private tracker item.
- Compare bug identity, not labels. Same CWE, symptom, endpoint, component, or impact alone does not establish duplication.
- Treat open, closed, merged, reverted, duplicate, wontfix, invalid, and archived records as prior art.
- Separate three questions: **same bug?**, **already fixed?**, and **eligible to file here?** This skill answers the first two. Discuss filing eligibility only when requested.
- Never promise absolute novelty. Proving nonexistence is impossible when relevant private or inaccessible corpora may exist. Use `NO_DUPLICATE_FOUND` only after all accessible critical sources pass the coverage gate; use `INCONCLUSIVE` when a critical source is blocked.
- Timestamp results. Novelty is an as-of claim.

## Inputs and invocation

Accept any of:

- Finding/bug ID, filename, path, issue URL, advisory ID, or partial title.
- Local write-up or source checkout.
- Natural-language bug description.
- Two records to compare directly.

Resolve ambiguous local matches before searching externally. If no write-up exists, obtain or derive at least:

1. target product/repository and affected version;
2. trigger or entry point;
3. observed or expected behavior;
4. distinguishing mechanism/root cause, if known.

Do not invent missing identity fields. Mark them `unknown`; unresolved core identity lowers confidence and may force `INCONCLUSIVE`.

## Required progress ledger

Maintain this checklist during execution:

```text
Bug duplicate check:
- [ ] 0. Resolve authoritative bug record and scope
- [ ] 1. Build canonical bug fingerprint and aliases
- [ ] 2. Build target-specific source coverage map
- [ ] 3. Execute lexical, semantic, historical, and fix-oriented searches
- [ ] 4. Open and compare every plausible candidate
- [ ] 5. Inspect code, version, release, and fix history
- [ ] 6. Run adversarial second pass against the tentative verdict
- [ ] 7. Apply coverage gate and issue evidence-bounded verdict
```

## Phase 0 - Resolve authoritative bug record

Search local context first with `rg`/`rg --files`. Include dedicated findings folders, issue exports, reports, duplicate checks, rejected findings, audit notes, changelogs, and source checkouts. Exclude generated/dependency trees unless evidence points there.

Record:

- Canonical ID/title and source file or URL.
- Target product, repo, package, plugin, service, fork, or deployment.
- Audited commit, release, build, platform, configuration, and affected range.
- Existing issue/CVE/GHSA/advisory/report IDs and links.
- Existing duplicate assessments and their evidence.
- Whether comparison scope is local workspace, one tracker, one product, upstream/downstream, one disclosure program, or global public prior art.

Prefer the most complete primary record. Treat reports, PoCs, validation notes, and duplicate assessments as supporting artifacts, not separate bugs unless they describe a distinct root cause.

## Phase 1 - Build canonical bug fingerprint

Create this fingerprint before web searching:

| Dimension | Required content |
|---|---|
| Target identity | Product/repo/package, upstream/downstream/fork relation |
| Version window | First known affected, tested, latest affected, fixed/reintroduced |
| Surface | UI flow, route, API, parser, file format, protocol, workflow, function |
| Actor/preconditions | Auth role, permissions, config, platform, feature flags, attacker control |
| Trigger/input | Exact action, payload shape, state transition, malformed object, sequence |
| Source/data flow | Where attacker/user-controlled state originates and transformations |
| Sink/operation | Failing or dangerous operation, symbol/path/line when available |
| Broken invariant | Security, correctness, lifecycle, bounds, ownership, transaction, or state rule violated |
| Root cause | Missing/wrong guard, stale state, overflow, race, wrong key, bad normalization, etc. |
| Observable result | Error, crash, overwrite, disclosure, wrong response, state corruption, bypass |
| Impact | User-visible and security consequence without inflation |
| Fix shape | Smallest invariant-restoring change expected to close the bug |

Then write:

- **Identity sentence:** one sentence containing actor + trigger + mechanism + sink + result.
- **Exclusion sentence:** nearest similar behavior that is *not* this bug.
- **Alias set:** old/new product names, package/module names, endpoint variants, symbol names, error strings, protocol terms, CWE/general terms, abbreviations, translations where relevant.
- **Candidate-killing facts:** facts that would immediately prove a search hit is a different bug.

Do not begin with generic terms such as `SSRF`, `crash`, or `IDOR`; they create noisy similarity without identity.

## Phase 2 - Build source coverage map

Read [source-catalog.md](references/source-catalog.md), select every applicable source class, and mark each `REQUIRED`, `SUPPORTING`, `NOT_APPLICABLE`, or `BLOCKED`.

Universal source classes:

1. Local workspace prior art.
2. Canonical project tracker: issues, bugs, PRs/MRs, discussions, comments, duplicate chains.
3. Repository history: all branches/tags, commits, blame, tests, changelog, release notes.
4. Vendor/product support and known-issue records.
5. Security/advisory databases when security-relevant.
6. Ecosystem/package/fork/upstream/downstream records.
7. General web, research, mailing lists, forums, and specialist sources.
8. Program/private/internal report corpus when relevant and authorized.

Critical-source rules:

- Canonical tracker and code/release history are critical for source-available projects.
- Vendor known-issues/support and release history are critical for closed-source products.
- Advisory databases are critical for security bugs.
- The intended report corpus is critical when the question is "duplicate in this bounty/internal tracker?"
- Upstream records are critical when code is vendored, forked, generated, or dependency-owned.
- A blocked critical source prevents a high-confidence novelty claim.

Record visibility limits explicitly. Public search cannot enumerate private bounty reports, embargoed advisories, private Jira projects, deleted posts, unindexed comments, or unpublished fixes.

## Phase 3 - Execute search matrix

Search in parallel where possible, but preserve a query ledger. Search all states and historical records, not only open/current items.

### Query families

Run every applicable family against canonical sources:

1. **Exact identifiers:** symbols, endpoints, file paths, route names, error strings, exception types, config keys, protocol fields.
2. **Behavior phrase:** plain-language trigger -> result, with synonym permutations.
3. **Root cause/invariant:** missing ownership check, stale cache key, integer truncation, duplicate state transition, wrong auth header, etc.
4. **Symptom/impact:** crash signature, status-code mismatch, data corruption, leak, overwrite, hang, wrong UI state.
5. **Fix-oriented:** validation, guard, bounds, sanitize, authorize, preserve exception, clear cache, race, revert, regression.
6. **Version/alias:** old product names, renamed modules, package names, forks, upstream dependency, platform-specific terms.
7. **Related-ID expansion:** every issue, PR, commit, CVE, GHSA, advisory, or duplicate target referenced by a candidate.
8. **Negative/inverse wording:** "allow X," "prevent Y," "handle malformed Z," "avoid crash," and maintainer euphemisms such as hardening, robustness, cleanup, correctness, or edge case.

Minimum search depth when source capabilities allow:

- At least three materially different query families in the canonical tracker.
- Both exact-symbol and behavior/root-cause searches.
- Open and closed/archived states.
- Issues/bugs plus PRs/MRs/commits; fixes often have no issue.
- Exact and semantic web searches.
- One query using the expected fix shape.
- One query using old/alternate names.

Do not count minor punctuation or word-order changes as independent searches.

### Search expansion loop

For each plausible hit:

1. Open the primary record.
2. Extract new aliases, IDs, affected versions, fix commits, linked duplicates, and terminology.
3. Add them to the query matrix.
4. Search again until no candidate adds a new high-signal term or link.

This loop matters more than a fixed query count.

## Phase 4 - Compare every plausible candidate

Never classify from a title/snippet. Read issue body, comments, linked duplicates, patch, tests, and final disposition.

Create one row per candidate:

| Dimension | Current bug | Candidate | Match? |
|---|---|---|---|
| Target/version | | | |
| Actor/preconditions | | | |
| Entry/trigger | | | |
| Data/control flow | | | |
| Sink/operation | | | |
| Broken invariant/root cause | | | |
| Observable result/impact | | | |
| Fix/test shape | | | |

Apply these identity tests:

- **Same-fix test:** Would the candidate's minimal correct fix necessarily close this bug? Strongest duplicate signal.
- **Same-failure test:** Do both fail because the same invariant is broken at the same ownership layer?
- **Coexistence test:** Can one be fixed while the other remains? If yes, likely distinct or a variant.
- **Counterfactual test:** If candidate never existed, would this bug still arise unchanged from a different cause?
- **Scope test:** Does prior record explicitly or logically subsume this trigger/version/path?
- **Bypass test:** Does this bug defeat a prior fix through a materially different mechanism or unguarded path?
- **Regression test:** Is behavior a reintroduction of an already documented and fixed bug? Regressions are prior-art duplicates unless tracker policy treats recurrence separately; report both facts.

Interpretation rules:

- Same CWE/class only -> not duplicate evidence.
- Same component or endpoint only -> related, not enough.
- Same symptom with different root cause/fix -> distinct bug.
- Different symptom from same root cause and same fix -> usually duplicate/subsumed.
- Different endpoint sharing one missing central invariant and one fix -> often duplicate/subsumed.
- Same path after incomplete prior fix, with a distinct bypass mechanism -> `NOVEL_BYPASS` or `RELATED_VARIANT`, not automatically duplicate.
- Prior issue need not contain a PoC, severity claim, or perfect explanation to be a duplicate.
- Candidate status does not erase prior art.

## Phase 5 - Inspect history and current state

Search source and release history for silent prior art:

- `git log --all --oneline --decorate -- <path>`
- `git log --all -p -S '<exact token>' -- <path>`
- `git log --all -p -G '<regex>' -- <path>`
- `git blame`, tags, maintenance branches, reverted commits, backports, and release branches.
- Tests named after symptoms, issue IDs, regressions, or edge cases.
- Changelog/release-note wording such as fix, harden, validate, prevent, robustness, cleanup, and security.
- Package/plugin version diffs and upstream/downstream patches.

Determine separately:

- Present on latest default branch?
- Present in latest stable release?
- Fixed only on another branch/version?
- Reintroduced after a prior fix?
- Mitigated by default configuration but still present?
- Silent fix with no public issue?

An already-fixed bug can still be a duplicate. A current bug can still be duplicate prior art.

## Phase 6 - Adversarial second pass

Before issuing any non-duplicate verdict, assume the tentative conclusion is wrong.

Run a fresh pass that:

- Uses aliases and terminology learned from candidates, not original wording.
- Searches expected patch code and invariant-restoring language.
- Searches old names, forks, upstreams, downstreams, package mirrors, and moved trackers.
- Follows duplicate closures to canonical issues and follows canonical issues back through related records.
- Searches commits with no issue link and issues with no code link.
- Searches comments/attachments where the tracker permits it.
- Checks localized or ecosystem-specific terminology when target community uses it.
- Revisits the closest three candidates and writes the decisive non-match fact for each.

If independent agents are available, give one only the canonical fingerprint and target, ask it to perform a fresh duplicate check, and withhold tentative verdict/candidates. Reconcile its evidence; do not average conclusions.

## Coverage gate and stopping rules

### A duplicate is established when

- Primary evidence describes the same root cause/invariant and trigger/scope; or
- Prior record explicitly subsumes the current path; or
- Same-fix and same-failure tests both pass with no decisive scope difference.

One authoritative record is sufficient, but confirm its identity and state from primary material. Continue enough to identify canonical record and fix history.

### `NO_DUPLICATE_FOUND` is allowed only when

- Fingerprint contains no unresolved identity-critical field.
- Every applicable critical source is checked and logged.
- Query matrix covers exact, semantic, root-cause, fix, version/alias, and historical searches.
- Every plausible candidate is opened and comparison completed.
- Code/release history check is complete where available.
- Adversarial second pass finds no unresolved high-overlap candidate.
- Limitations are stated.

### Use `INCONCLUSIVE` when

- A critical private/inaccessible source could contain duplicates.
- Target/version/root cause is too uncertain to compare.
- Search/index/API failures materially reduce coverage.
- A high-overlap candidate cannot be inspected.
- Current code/history cannot be obtained and version identity is decisive.

Never silently downgrade a blocked source to `NOT_APPLICABLE`.

## Verdict taxonomy

| Verdict | Meaning |
|---|---|
| `DUPLICATE_EXACT` | Same bug identity: trigger/root cause/sink/scope align |
| `DUPLICATE_SUBSUMED` | Prior broader record necessarily covers this path or failure |
| `LIKELY_DUPLICATE` | Strong identity overlap, but decisive primary evidence is incomplete |
| `RELATED_VARIANT` | Shared component/class/ancestry, but distinct trigger, cause, or fix |
| `NOVEL_BYPASS` | Prior fix/record exists; this uses a materially distinct bypass and remains reachable |
| `NOT_DUPLICATE` | Direct comparison shows decisive identity mismatch; does not claim global novelty |
| `NO_DUPLICATE_FOUND` | Exhaustive accessible search found none; evidence-bounded, not absolute proof |
| `INCONCLUSIVE` | Coverage or identity gaps prevent reliable decision |

Also report technical relationship separately: `same-root-cause`, `same-symptom-different-cause`, `same-component`, `fix-bypass`, `regression`, `upstream-shared`, or `unrelated`.

Confidence levels:

- **High:** primary records and patches inspected; critical sources covered; no material ambiguity.
- **Medium:** good public evidence but one noncritical gap or identity uncertainty.
- **Low:** indirect evidence, blocked source, unresolved candidate, or incomplete fingerprint.

Do not convert confidence into fake mathematical probability.

## Durable artifact contract

When the caller needs persistence or another skill will consume the result, write:

`Findings/<repo-or-software>/DUPLICATE-CHECK-<finding-id>.md`

This local evidence write is allowed; all repository, tracker, program, and web investigation remains read-only.

Start the file with:

```yaml
---
schema_version: "bug-duplicate-check/v1"
finding_id: "FND-YYYYMMDD-CONTEXT-CLASS-NNNN-slug"
canonical_finding: "FND-YYYYMMDD-CONTEXT-CLASS-NNNN-slug.md"
finding_sha256: ""
fingerprint_sha256: ""
target: ""
tested_version: ""
duplicate_verdict: "INCONCLUSIVE"
technical_relationship: ""
confidence: "Low"
checked_at_utc: "YYYY-MM-DDTHH:MM:SSZ"
critical_coverage: ""
current_state: "unknown"
closest_prior_art: ""
---
```

Use lowercase SHA-256 of raw canonical finding bytes for `finding_sha256`. Build `fingerprint_sha256` from UTF-8, LF-normalized canonical fingerprint values in this exact order, one `key=value` per line:

```text
target_identity
version_window
surface
actor_preconditions
trigger_input
source_data_flow
sink_operation
broken_invariant
root_cause
observable_result
impact
fix_shape
```

If no canonical file exists, hash the exact normalized input record and state that in limitations. A downstream skill may reuse the artifact only when the schema, finding hash, fingerprint hash, target/version, critical coverage, and check freshness still match.

For `DUPLICATE_EXACT`, `DUPLICATE_SUBSUMED`, or `LIKELY_DUPLICATE`,
`closest_prior_art` must be a direct primary URL. The candidate-comparison row
must use that URL and contain the decisive identity evidence. Every evidence
ledger row must contain the exact six columns and a primary URL or a sibling
evidence file. The ledger must contain at least one row per checked critical
source and at least that many distinct source classes. The coverage checklist
must contain the same number of distinct checked source classes. The validator
rebuilds the ordered fingerprint text from the twelve `key=value` lines and
requires its SHA-256 to match `fingerprint_sha256`.

## Required output

```markdown
---
schema_version: "bug-duplicate-check/v1"
finding_id: "{finding ID}"
canonical_finding: "{canonical filename}"
finding_sha256: "{lowercase SHA-256}"
fingerprint_sha256: "{lowercase SHA-256}"
target: "{canonical target}"
tested_version: "{commit/release/build}"
duplicate_verdict: "{taxonomy verdict}"
technical_relationship: "{relationship}"
confidence: "High / Medium / Low"
checked_at_utc: "{UTC timestamp}"
critical_coverage: "{checked critical}/{applicable critical}"
current_state: "affected / fixed / regression / unknown"
closest_prior_art: "{primary URL, issue/advisory/commit ID, or none}"
---

# Bug Duplicate Check: {ID or short title}

**As of:** {UTC timestamp}

## Verdict

| Field | Result |
|---|---|
| Duplicate status | {taxonomy verdict} |
| Technical relationship | {relationship} |
| Confidence | High / Medium / Low |
| Coverage | {checked critical}/{applicable critical}; {checked total}/{applicable total} |
| Closest prior art | {ID/link or none found} |
| Current state | affected / fixed / regression / unknown |
| Critical blind spots | none / explicit list |

## Canonical fingerprint

```text
target_identity=
version_window=
surface=
actor_preconditions=
trigger_input=
source_data_flow=
sink_operation=
broken_invariant=
root_cause=
observable_result=
impact=
fix_shape=
```

- Identity sentence:
- Excludes:

## Candidate comparison

| Candidate | Trigger | Root cause/invariant | Sink | Fix shape | Relation | Decisive evidence |
|---|---|---|---|---|---|---|

## Evidence ledger

| # | Source | Query/scope | States/versions | Result | Primary URL/file |
|---|---|---|---|---|---|

## History and current-state analysis

{Code, commits, releases, silent fixes, regressions, affected ranges.}

## Adversarial second pass

{Alternative terms/sources used and closest candidates rechecked.}

## Coverage checklist

| Source class | Status | Notes |
|---|---|---|
| Local prior art | checked/blocked/N/A | |
| Canonical tracker | checked/blocked/N/A | |
| Code/release history | checked/blocked/N/A | |
| Vendor/support records | checked/blocked/N/A | |
| Advisories | checked/blocked/N/A | |
| Ecosystem/upstream/downstream | checked/blocked/N/A | |
| Web/research/community | checked/blocked/N/A | |
| Program/private/internal corpus | checked/blocked/N/A | |

## Conclusion

{Direct answer. State exactly why closest prior art is or is not same bug.}

## Not checked / limitations

- {Every inaccessible, failed, private, unindexed, or intentionally irrelevant source.}
```

For examples of exact duplicate, distinct variant, and blocked-private-corpus results, read [examples.md](references/examples.md).

## Execution requirements

- Use local read/search plus internet research when available. Current external facts require browsing.
- Validate every durable result before another skill consumes it:

```powershell
python "$env:USERPROFILE\.brain\skills\bug-duplicate-check\scripts\validate_duplicate_record.py" "<duplicate-record>"
```
- Prefer primary sources: canonical issue trackers, commits, patches, advisories, vendor records, release notes.
- Cite every duplicate claim with direct URL/file evidence.
- Log zero-result searches; absence is meaningful only with query and scope.
- Open every high-signal result. Search result snippets are discovery evidence only.
- Search all states and historical versions.
- Parallelize independent source classes; serialize candidate expansion when new aliases emerge.
- Do not stop at first "no result." Stop only at coverage gate.
- Do not let bounty eligibility, severity, payout, or disclosure status distort bug-identity analysis.
- If asked for filing advice, append a separate context-specific disposition after duplicate verdict.
