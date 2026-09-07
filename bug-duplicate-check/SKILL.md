---
name: bug-duplicate-check
description: >-
  Run an exhaustive, read-only duplicate and prior-art investigation for one
  supplied bug. Trigger only when asked whether it is known, reported, fixed,
  disclosed, duplicated, a variant or bypass, or plausibly new before triage,
  filing, disclosure, or submission; not for ordinary bug fixing or discovery.
---

# Bug Duplicate Check

Determine whether the same underlying bug already exists anywhere relevant. Optimize for avoiding false novelty claims, not speed.

## Non-negotiables

- Read-only: never file, comment, disclose, edit repositories, or mutate trackers. Writes are limited to the local durable artifact and the canonical-registry row described below.
- Decide from tools and current primary sources (canonical trackers, commits, patches, advisories, vendor records, release notes). Never from memory, one database, or a title/snippet; a search hit is discovery evidence only until its primary record is opened. Current external facts require browsing.
- Compare bug identity, not labels. Same CWE, symptom, endpoint, component, or impact alone never establishes duplication.
- Every record state is prior art: open, closed, merged, reverted, duplicate, wontfix, invalid, archived, historical versions. Search security and non-security prior art: issue, fix, regression test, release note, support thread, commit, advisory, duplicate closure, private tracker item.
- Answer two questions: **same bug?** and **already fixed?** Filing eligibility is separate: only when asked, appended as a context-specific disposition after the verdict. Bounty eligibility, severity, payout, disclosure status never alter identity analysis.
- Never promise absolute novelty; private or inaccessible corpora may exist. `NO_DUPLICATE_FOUND` only after every accessible critical source passes the coverage gate; `INCONCLUSIVE` when a critical source is blocked.
- Timestamp results: novelty is an as-of claim.
- Cite every duplicate claim with a direct URL/file. Log zero-result searches with exact query and scope; absence is meaningful only then.
- Stop only at the coverage gate, never at the first "no result".

## Inputs

Accept: finding/bug ID, filename, path, issue URL, advisory ID, partial title; local write-up or source checkout; natural-language description; two records to compare directly.

Resolve ambiguous local matches before external search. Without a write-up, obtain or derive: (1) target product/repository and affected version, (2) trigger or entry point, (3) observed or expected behavior, (4) distinguishing mechanism/root cause if known. Mark missing identity fields `unknown`, never invent; unresolved core identity lowers confidence and may force `INCONCLUSIVE`.

## Progress ledger

Maintain during execution:

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

Search local context first with `rg`/`rg --files`: findings folders, issue exports, reports, duplicate checks, rejected findings, audit notes, changelogs, source checkouts. Exclude generated/dependency trees unless evidence points there.

Record: canonical ID/title and source file or URL; target product/repo/package/plugin/service/fork/deployment; audited commit, release, build, platform, configuration, affected range; existing issue/CVE/GHSA/advisory/report IDs and links; existing duplicate assessments with evidence; comparison scope (local workspace, one tracker, one product, upstream/downstream, one disclosure program, global public prior art).

Prefer the most complete primary record. Reports, PoCs, validation notes, duplicate assessments are supporting artifacts of one bug unless they describe a distinct root cause.

## Phase 1 - Build canonical bug fingerprint

Fill before any web search:

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

- **Identity sentence:** actor + trigger + mechanism + sink + result, one sentence.
- **Exclusion sentence:** nearest similar behavior that is *not* this bug.
- **Alias set:** old/new product names, package/module names, endpoint variants, symbol names, error strings, protocol terms, CWE/general terms, abbreviations, translations where relevant.
- **Candidate-killing facts:** facts that immediately prove a hit is a different bug.

Start from specific identity terms; generic terms (`SSRF`, `crash`, `IDOR`) give noisy similarity without identity.

## Phase 2 - Build source coverage map

Read [source-catalog.md](references/source-catalog.md), select every applicable source class, mark each `REQUIRED`, `SUPPORTING`, `NOT_APPLICABLE`, or `BLOCKED`.

Universal source classes:

1. Local workspace prior art.
2. Canonical project tracker: issues, bugs, PRs/MRs, discussions, comments, duplicate chains.
3. Repository history: all branches/tags, commits, blame, tests, changelog, release notes.
4. Vendor/product support and known-issue records.
5. Security/advisory databases when security-relevant.
6. Ecosystem/package/fork/upstream/downstream records.
7. General web, research, mailing lists, forums, specialist sources.
8. Program/private/internal report corpus when relevant and authorized.

Critical sources:

- Source-available project: canonical tracker and code/release history.
- Closed-source product: vendor known-issues/support and release history.
- Security bug: advisory databases. Run the `vuln-intel` MCP first when connected (`search_vulns`, `verify_cve_claim`, `enrich_cve`, `search_public_code`), then open every primary record it surfaces. Add research-lab disclosures, security mailing lists, code search engines, distribution security trackers per the catalog; a CVE database alone is one source, not coverage.
- Question "duplicate in this bounty/internal tracker?": the intended report corpus.
- Vendored, forked, generated, or dependency-owned code: upstream records.
- A blocked critical source prevents a high-confidence novelty claim. Record it `BLOCKED`; never downgrade to `NOT_APPLICABLE`.

Record visibility limits explicitly: public search cannot enumerate private bounty reports, embargoed advisories, private Jira projects, deleted posts, unindexed comments, unpublished fixes.

## Phase 3 - Execute search matrix

Parallelize independent source classes; serialize candidate expansion when new aliases emerge. Keep a query ledger.

Run every applicable family against canonical sources:

1. **Exact identifiers:** symbols, endpoints, file paths, route names, error strings, exception types, config keys, protocol fields.
2. **Behavior phrase:** plain-language trigger -> result, with synonym permutations.
3. **Root cause/invariant:** missing ownership check, stale cache key, integer truncation, duplicate state transition, wrong auth header, etc.
4. **Symptom/impact:** crash signature, status-code mismatch, data corruption, leak, overwrite, hang, wrong UI state.
5. **Fix-oriented:** validation, guard, bounds, sanitize, authorize, preserve exception, clear cache, race, revert, regression.
6. **Version/alias:** old product names, renamed modules, package names, forks, upstream dependency, platform-specific terms.
7. **Related-ID expansion:** every issue, PR, commit, CVE, GHSA, advisory, or duplicate target referenced by a candidate.
8. **Negative/inverse wording:** "allow X," "prevent Y," "handle malformed Z," "avoid crash," and maintainer euphemisms: hardening, robustness, cleanup, correctness, edge case.

Minimum depth when source capabilities allow (the coverage gate checks this list):

- At least three materially different query families in the canonical tracker; punctuation or word-order variants do not count as separate searches.
- Both exact-symbol and behavior/root-cause searches.
- Open and closed/archived states.
- Issues/bugs plus PRs/MRs/commits; fixes often have no issue.
- Exact and semantic web searches.
- One query using the expected fix shape.
- One query using old/alternate names.

Expansion loop, which matters more than query count: for each plausible hit, open the primary record; extract new aliases, IDs, affected versions, fix commits, linked duplicates, terminology; add to the matrix; search again until no candidate adds a new high-signal term or link.

## Phase 4 - Compare every plausible candidate

Read issue body, comments, linked duplicates, patch, tests, final disposition. One row per candidate:

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

Identity tests:

- **Same-fix test:** Would the candidate's minimal correct fix necessarily close this bug? Strongest duplicate signal.
- **Same-failure test:** Do both fail because the same invariant is broken at the same ownership layer?
- **Coexistence test:** Can one be fixed while the other remains? If yes, likely distinct or a variant.
- **Counterfactual test:** If the candidate never existed, would this bug still arise unchanged from a different cause?
- **Scope test:** Does the prior record explicitly or logically subsume this trigger/version/path?
- **Bypass test:** Does this bug defeat a prior fix through a materially different mechanism or unguarded path?
- **Regression test:** Is the behavior a reintroduction of an already documented and fixed bug? Regressions are prior-art duplicates unless tracker policy treats recurrence separately; report both facts.

Interpretation rules:

- Same CWE/class only -> not duplicate evidence.
- Same component or endpoint only -> related, not enough.
- Same symptom with different root cause/fix -> distinct bug.
- Different symptom from same root cause and same fix -> usually duplicate/subsumed.
- Different endpoint sharing one missing central invariant and one fix -> often duplicate/subsumed.
- Same path after incomplete prior fix, with a distinct bypass mechanism -> `NOVEL_BYPASS` or `RELATED_VARIANT`, not automatically duplicate.
- A prior issue need not contain a PoC, severity claim, or perfect explanation to be a duplicate.
- Candidate status does not erase prior art.

## Phase 5 - Inspect history and current state

Search source and release history for silent prior art:

- `git log --all --oneline --decorate -- <path>`
- `git log --all -p -S '<exact token>' -- <path>`
- `git log --all -p -G '<regex>' -- <path>`
- `git blame`, tags, maintenance branches, reverted commits, backports, release branches.
- Tests named after symptoms, issue IDs, regressions, edge cases.
- Changelog/release-note wording: fix, harden, validate, prevent, robustness, cleanup, security.
- Package/plugin version diffs and upstream/downstream patches.

Determine separately: present on latest default branch? in latest stable release? fixed only on another branch/version? reintroduced after a prior fix? mitigated by default configuration but still present? silent fix with no public issue?

An already-fixed bug can still be a duplicate. A current bug can still be duplicate prior art.

## Phase 6 - Adversarial second pass

Before any non-duplicate verdict, assume the tentative conclusion is wrong and run a fresh pass that:

- Uses aliases and terminology learned from candidates, not original wording.
- Searches expected patch code and invariant-restoring language.
- Searches old names, forks, upstreams, downstreams, package mirrors, moved trackers.
- Follows duplicate closures to canonical issues and canonical issues back through related records.
- Searches commits with no issue link and issues with no code link.
- Searches comments/attachments where the tracker permits.
- Checks localized or ecosystem-specific terminology when the target community uses it.
- Revisits the closest three candidates and writes the decisive non-match fact for each.

If independent agents are available, give one only the canonical fingerprint and target, withhold the tentative verdict and candidates, ask for a fresh duplicate check. Reconcile its evidence; never average conclusions.

## Phase 7 - Coverage gate and verdict

A duplicate is established when any holds:

- Primary evidence describes the same root cause/invariant and trigger/scope.
- The prior record explicitly subsumes the current path.
- Same-fix and same-failure tests both pass with no decisive scope difference.

One authoritative record suffices once its identity and state are confirmed from primary material; continue far enough to identify the canonical record and fix history.

`NO_DUPLICATE_FOUND` requires all of:

- Fingerprint has no unresolved identity-critical field.
- Every applicable critical source checked and logged.
- Phase 3 minimum depth met: exact, semantic, root-cause, fix, version/alias, historical searches.
- Every plausible candidate opened and its Phase 4 comparison completed.
- Phase 5 code/release history check complete where available.
- Phase 6 pass finds no unresolved high-overlap candidate.
- Limitations stated.

`INCONCLUSIVE` when any holds:

- A critical private/inaccessible source could contain duplicates.
- Target/version/root cause too uncertain to compare.
- Search/index/API failures materially reduce coverage.
- A high-overlap candidate cannot be inspected.
- Current code/history unobtainable and version identity decisive.

### Verdict taxonomy

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

Report the technical relationship separately: `same-root-cause`, `same-symptom-different-cause`, `same-component`, `fix-bypass`, `regression`, `upstream-shared`, or `unrelated`.

Confidence, reported as these words, never as a numeric probability:

- **High:** primary records and patches inspected; critical sources covered; no material ambiguity.
- **Medium:** good public evidence but one noncritical gap or identity uncertainty.
- **Low:** indirect evidence, blocked source, unresolved candidate, or incomplete fingerprint.

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

Examples (exact duplicate, distinct variant, blocked private corpus): [examples.md](references/examples.md).

## Durable artifact

When the caller needs persistence or another skill will consume the result, write the required output to:

`Findings/<repo-or-software>/DUPLICATE-CHECK-<finding-id>.md`

Hashes:

- `finding_sha256`: lowercase SHA-256 of the raw canonical finding bytes. If no canonical file exists, hash the exact normalized input record and state that in limitations.
- `fingerprint_sha256`: SHA-256 of the UTF-8, LF-normalized canonical fingerprint values in this exact order, one `key=value` per line:

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

Validator rules:

- For `DUPLICATE_EXACT`, `DUPLICATE_SUBSUMED`, or `LIKELY_DUPLICATE`: `closest_prior_art` is a direct primary URL, and the candidate-comparison row for that URL holds the decisive identity evidence.
- Every evidence-ledger row has exactly six columns and a primary URL or a sibling evidence file.
- Ledger: at least one row per checked critical source and at least that many distinct source classes; coverage checklist: the same number of distinct checked source classes.
- The validator rebuilds the ordered fingerprint text from the twelve `key=value` lines and requires its SHA-256 to match `fingerprint_sha256`.

Validate every durable result before another skill consumes it:

```powershell
python "$env:USERPROFILE\.brain\skills\bug-duplicate-check\scripts\validate_duplicate_record.py" "<duplicate-record>"
```

A downstream skill may reuse the artifact only when schema, finding hash, fingerprint hash, target/version, critical coverage, and check freshness still match.

## Canonical registry

If this check changes a finding or hunt row, use the Google Workspace MCP against the spreadsheet in `System/registry.md`. Canonical finding records live at `Findings/<program>/<software>/<id>/`. Local CSV files are derived views, not authority.
