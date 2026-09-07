# Bug Duplicate Check — Examples

These examples demonstrate identity reasoning. URLs/IDs are illustrative unless explicitly verified during a real check.

## Contents

1. Exact duplicate
2. Related variant, not duplicate
3. Novel bypass
4. Non-security regression
5. Inconclusive private-corpus check

## 1. Exact duplicate

```markdown
# Bug Duplicate Check: API export accepts foreign workspace object ID

**As of:** 2026-07-12T14:30:00Z

## Verdict

| Field | Result |
|---|---|
| Duplicate status | DUPLICATE_EXACT |
| Technical relationship | same-root-cause |
| Confidence | High |
| Coverage | 5/5 critical; 7/8 total |
| Closest prior art | issue #1842 |
| Current state | affected on main; fixed on unreleased branch |
| Critical blind spots | none |

## Canonical fingerprint

- Target/version: example/export-service 4.8.0 and main
- Actor/preconditions: authenticated member of workspace A
- Trigger/entry: POST /exports with object_id from workspace B
- Source → sink: caller object_id → global ORM lookup → export serializer
- Broken invariant/root cause: lookup omits active_workspace_id predicate
- Observable result/impact: cross-workspace document export
- Expected fix shape: bind object query to active workspace before serialization
- Identity sentence: Workspace-A member supplies workspace-B object ID to export route; global ID lookup omits tenant predicate and serializes foreign document.
- Excludes: issue #1660 concerns guessing export job IDs after creation, not source-object lookup.

## Candidate comparison

| Candidate | Trigger | Root cause/invariant | Sink | Fix shape | Relation | Decisive evidence |
|---|---|---|---|---|---|---|
| #1842 | foreign object_id in /exports | same missing workspace predicate | same serializer | same scoped query | exact | Patch adds active_workspace_id to exact lookup |
| #1660 | foreign export_job_id in download | job ownership check | download handler | authorize job owner | variant | One fix leaves other reachable |

## Conclusion

Issue #1842 is exact duplicate: same entry, missing predicate, data flow, sink, result, and minimal fix. Current bug adds a stronger PoC but no distinct identity.
```

Why: matching class/impact was not enough; matching invariant and patch established duplication.

## 2. Related variant, not duplicate

```markdown
# Bug Duplicate Check: image upload crashes when type query parameter is absent

**As of:** 2026-07-12T15:00:00Z

## Verdict

| Field | Result |
|---|---|
| Duplicate status | RELATED_VARIANT |
| Technical relationship | same-component |
| Confidence | High |
| Coverage | 4/4 critical; 6/7 total |
| Closest prior art | issue #9210: malformed image bytes crash decoder |
| Current state | affected |
| Critical blind spots | private support tickets not searchable |

## Candidate comparison

| Candidate | Trigger | Root cause/invariant | Sink | Fix shape | Relation | Decisive evidence |
|---|---|---|---|---|---|---|
| #9210 | corrupt image bytes | decoder exception not caught | image decoder | catch decode error | variant | Missing query parameter never reaches decoder |
| current | absent `type` query | local variable assigned only in conditional | response formatter | initialize/validate parameter | variant | Decoder fix does not initialize variable |

## Conclusion

Same endpoint and same 500 response, but different trigger, root cause, sink, and fix. Not duplicate of #9210. Global result remains `RELATED_VARIANT`, not absolute novelty, because private support tickets are unavailable.
```

Why: same symptom and component can conceal independent bugs.

## 3. Novel bypass

```markdown
# Bug Duplicate Check: redirect allowlist bypass via gzip-wrapped body URL

**As of:** 2026-07-12T15:30:00Z

## Verdict

| Field | Result |
|---|---|
| Duplicate status | NOVEL_BYPASS |
| Technical relationship | fix-bypass |
| Confidence | High |
| Coverage | 6/6 critical; 8/8 total |
| Closest prior art | GHSA-xxxx: redirect destination validation |
| Current state | affected after prior fix |
| Critical blind spots | none known |

## Candidate comparison

| Candidate | Trigger | Root cause/invariant | Sink | Fix shape | Relation | Decisive evidence |
|---|---|---|---|---|---|---|
| GHSA-xxxx | HTTP Location redirect | redirect target not revalidated | redirect follower | validate each redirect | prior sibling | Fix fully closes redirect path |
| current | URL decoded from gzip response body | body-derived fetch skips allowlist | secondary fetch | validate decoded body URL | bypass | Redirect validation never sees body URL |

## Conclusion

Prior advisory establishes same broad SSRF objective but not same data flow or missing guard. Its fix can be present while current body-derived fetch remains exploitable. Classify as a distinct bypass, not a duplicate restatement.
```

Why: “same endpoint + same impact” did not override coexistence and same-fix tests.

## 4. Non-security regression

```markdown
# Bug Duplicate Check: search test endpoint returns HTTP 200 on backend failure

**As of:** 2026-07-12T16:00:00Z

## Verdict

| Field | Result |
|---|---|
| Duplicate status | DUPLICATE_SUBSUMED |
| Technical relationship | regression |
| Confidence | High |
| Coverage | 4/4 critical; 5/6 total |
| Closest prior art | commit 9f31d2a + regression test `test_backend_error_status` |
| Current state | regressed in 3.2.1 |
| Critical blind spots | none |

## History and current-state analysis

Commit 9f31d2a changed the endpoint from a returned `{status: error}` object to raised HTTP 502 and added a regression test. Refactor 70bc81e deleted the exception path and test while consolidating providers. Current behavior is the same documented defect reintroduced.

## Conclusion

No open issue uses current wording, but commit and deleted test are authoritative prior art. This is a regression of the same bug and therefore duplicate/subsumed for novelty tracking.
```

Why: duplicate checks must search fixes and tests, not only issue titles.

## 5. Inconclusive private-corpus check

```markdown
# Bug Duplicate Check: Calendar assistant performs action from quoted email text

**As of:** 2026-07-12T16:30:00Z

## Verdict

| Field | Result |
|---|---|
| Duplicate status | INCONCLUSIVE |
| Technical relationship | no public match found |
| Confidence | Low |
| Coverage | 3/4 critical; 7/8 total |
| Closest prior art | public indirect-prompt-injection research; no same action chain |
| Current state | affected in tested build; latest server state unknown |
| Critical blind spots | vendor's private VRP report corpus inaccessible |

## Conclusion

Public tracker, release notes, research, vendor security posts, and local prior art contain no same trigger/action chain. However, intended VRP corpus is private and capable of containing the exact report. Correct result is `INCONCLUSIVE`, not `NO_DUPLICATE_FOUND` or “absolutely novel.”
```

Why: honesty about inaccessible sources prevents false certainty.
