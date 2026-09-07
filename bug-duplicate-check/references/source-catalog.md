# Bug Duplicate Check — Source Catalog

Use this catalog to build a target-specific coverage map. Search every applicable critical class; skip irrelevant sources deliberately and record why.

## Contents

1. Local workspace and authoritative record
2. Canonical project trackers
3. Source, commit, release, and fix history
4. Security and advisory sources
5. Ecosystem and package sources
6. Vendor, product, support, and community sources
7. Internal and private corpora
8. Bounty and disclosure platforms
9. Product-specific routing
10. Query templates and coverage rules

## 1. Local workspace and authoritative record

Search before external research. Local notes often contain old IDs, rejected variants, private links, duplicate assessments, or source terminology absent from public pages.

Preferred commands:

```bash
rg --files -g '!node_modules' -g '!vendor' -g '!dist' -g '!build' -g '!coverage'
rg -n -i '{bug-id}|{symbol}|{endpoint}|{error phrase}|duplicate|wontfix|fixed|reported' . \
  -g '*.md' -g '*.json' -g '*.yaml' -g '*.yml' -g '*.txt'
rg -l -i '{distinctive phrase}' . -g '!**/source/**'
```

Check:

- Dedicated findings/bugs/issues folders.
- Reports, PoCs, runtime evidence, validation notes, duplicate checks.
- Rejected, closed, invalid, informative, or wontfix records.
- Project master indexes and migration/import artifacts.
- Existing issue exports, mail archives, Slack/Teams exports, release notes.
- Source checkout and its remotes, branches, tags, submodules, vendored dependencies.

Do not count multiple artifacts for one canonical bug as separate bugs.

## 2. Canonical project trackers

### GitHub

Search issues and PRs in all states. Use several query families; GitHub indexing can miss comments, old records, symbols, or punctuation-heavy terms.

```bash
gh search issues "repo:{owner}/{repo} {query}" --limit 100
gh search prs "repo:{owner}/{repo} {query}" --limit 100
gh issue list -R {owner}/{repo} -S "{query} in:title,body" --state all -L 100
gh pr list -R {owner}/{repo} -S "{query} in:title,body" --state all -L 100
gh api --method GET repos/{owner}/{repo}/issues --paginate -f state=all -f per_page=100
gh api graphql -f q='repo:{owner}/{repo} {query}' -f query='query($q:String!){search(query:$q,type:DISCUSSION,first:100){nodes{... on Discussion{number title url createdAt updatedAt}}}}'
```

Web fallbacks:

```text
https://github.com/{owner}/{repo}/issues?q={query}
https://github.com/{owner}/{repo}/pulls?q={query}
https://github.com/{owner}/{repo}/discussions?discussions_q={query}
https://github.com/search?q=repo%3A{owner}%2F{repo}+{query}&type=issues
https://github.com/search?q=repo%3A{owner}%2F{repo}+{query}&type=commits
```

For each candidate, inspect:

- Body, comments, labels, timeline, linked PRs/commits, duplicate target.
- Cross-referenced issues and transferred/moved records.
- Security advisories and private-fork merge references when public.
- Reactions or maintainer summaries only as supporting evidence.

Do not assume `gh search` covers issue comments. Follow candidate timelines and use API endpoints to fetch comments when relevant.

### GitLab

Search open/closed issues, merge requests, epics, snippets, releases, and commit history.

```text
https://gitlab.com/{namespace}/{project}/-/issues?search={query}&scope=all&state=all
https://gitlab.com/{namespace}/{project}/-/merge_requests?search={query}&scope=all&state=all
https://gitlab.com/{namespace}/{project}/-/commits/{branch}?search={query}
```

Use GitLab API when available:

```text
GET /projects/:id/issues?search={query}&scope=all&state=all
GET /projects/:id/merge_requests?search={query}&scope=all&state=all
```

### Jira / Linear / YouTrack / Azure DevOps

If connected and authorized, search:

- Summary/title and full text.
- Closed/resolved/duplicate/wontfix records.
- Comments, attachments, linked commits, parent/child issues.
- Old project keys, moved teams, archived projects, imported IDs.
- Fix version, affected version, component, labels, stack traces.

Private tracker access is critical when deciding whether a new internal ticket is a duplicate. If inaccessible, verdict cannot exceed `INCONCLUSIVE` for that tracker.

### Bugzilla

Search quicksearch and advanced fields, including resolved/verified/duplicate bugs:

```text
https://bugzilla.mozilla.org/buglist.cgi?quicksearch={query}
https://issues.chromium.org/issues?q={query}
```

Follow duplicate chains to canonical bug. Restricted/security bugs create unavoidable blind spots; record them.

### Other canonical trackers

- Launchpad bugs and merge proposals.
- Gerrit changes and review comments.
- Phabricator/Maniphest tasks and differentials.
- SourceForge trackers and mailing lists.
- Vendor public issue portals.
- WordPress Trac, plugin support forums, SVN logs.
- Browser issue trackers, standards repositories, WPT issues.

Canonical tracker is determined by project governance, not repository host alone.

## 3. Source, commit, release, and fix history

Search current and historical code even when trackers are clean. Fix-only commits and regression tests are common prior art.

### Local Git

```bash
git remote -v
git branch -a
git tag --sort=-creatordate | head -100
git log --all --oneline --decorate -- {path}
git log --all -p -S '{exact token}' -- {path}
git log --all -p -G '{regex or behavior term}' -- {path}
git log --all --grep='{behavior phrase}' -i
git blame -L {start},{end} {path}
git show {candidate-commit}
git branch -a --contains {candidate-commit}
git tag --contains {candidate-commit}
```

Use both `-S` and `-G`:

- `-S` finds changes to exact token count.
- `-G` finds diffs matching a regex, useful when symbols were renamed.

Inspect:

- Default, release, maintenance, security, and backport branches.
- Reverts and partial reverts.
- Tests introduced with fixes.
- Commit trailers (`Fixes`, `Closes`, `Refs`, CVE/GHSA IDs).
- Blame origin and moved/renamed files (`git log --follow`).
- Submodule or vendored-code update commits.

### Hosted history

- GitHub/GitLab commit search.
- Blame and file history UI.
- Releases and tags.
- Compare views between affected and fixed versions.
- CI/test names and failure logs where public.

### Release and distribution history

Check:

- `CHANGELOG*`, `HISTORY*`, `NEWS*`, `RELEASE_NOTES*`.
- GitHub/GitLab releases.
- Package registry release metadata.
- Plugin/app-store version histories.
- Vendor bulletins and update notes.
- Documentation snapshots and migration guides.

Search euphemisms: hardening, robustness, validation, edge case, cleanup, correctness, improve error handling, avoid crash, preserve state, prevent overwrite, normalize, sanitize, authorization, race, bounds, lifecycle.

## 4. Security and advisory sources

Use for vulnerabilities and security-relevant defects. Search by product/package, component, symbol, technique, affected version, and related identifiers.

### Primary/global

| Source | Entry point |
|---|---|
| Repository advisories | `https://github.com/{owner}/{repo}/security/advisories` |
| GitHub Advisory Database | `https://github.com/advisories?query={query}` |
| OSV | `https://osv.dev/list?q={package-or-product}` |
| CVE.org | `https://www.cve.org/CVERecord/SearchResults?query={query}` |
| NVD | `https://nvd.nist.gov/vuln/search/results?query={query}` |
| Vendor security center | Product-specific |
| CERT/CC and national CERTs | Product/technique search |

Useful API/CLI routes:

```bash
gh api repos/{owner}/{repo}/security-advisories --paginate
gh api --method GET /advisories -f ecosystem='{ecosystem}' -f affects='{package}' --paginate
```

When the `vuln-intel` MCP is connected, run it first over the advisory class: `search_vulns` (keyword, semantic, and seed-CVE mechanism search fused across NVD, KEV, EPSS, OSV, GHSA), `verify_cve_claim` (does a cited CVE exist and cover this version), `enrich_cve` (references, fix commits, PoCs), and `search_public_code` (repos carrying the same code string, for vendored or copied bugs). Its output is discovery evidence; still open the primary advisory and fix.

Research and vendor-lab disclosures (often precede or replace CVEs):

- Google Project Zero issue tracker and blog.
- Zero Day Initiative advisories (`zerodayinitiative.com/advisories`), Cisco Talos, Trend Micro, Checkmarx, Snyk research, GitHub Security Lab.
- oss-security list (`openwall.com/lists/oss-security`), Full Disclosure and Bugtraq archives on seclists.org.
- syzbot dashboard for Linux kernel crashes; OSS-Fuzz and ClusterFuzz issues for fuzzed projects.
- Wayback Machine for deleted advisories, issues, or posts referenced by ID.

Code search across ecosystems, for fixed or unfixed copies of the same code:

- GitHub code search (`https://github.com/search?q={snippet}&type=code`), Sourcegraph (`sourcegraph.com/search`), grep.app.
- `deps.dev` for package dependents and cross-referenced OSV records.

Distribution security trackers, which often record fixes and CVE splits before upstream does:

- Debian security tracker, Ubuntu CVE tracker, Red Hat CVE database and Bugzilla, SUSE CVE pages, Alpine secdb, Gentoo GLSA, Arch security tracker.

Additional databases:

- Snyk vulnerability DB.
- GitLab Advisory Database.
- CISA KEV (impact/exploitation context, not comprehensive duplicate corpus).
- VulnCheck, Tenable, Rapid7, vendor PSIRTs.
- CNVD, CNNVD, JVN/JPCERT, CERT-EU where relevant.
- Exploit-DB, Packet Storm, Metasploit modules after disclosure.

Read original advisory and fix references. Aggregators often collapse distinct variants or repeat incorrect descriptions.

### Ecosystem-specific security sources

- RustSec / `cargo audit` database.
- Go Vulnerability Database / `govulncheck`.
- npm advisories and package release notes.
- PyPI package advisories, OSV, pip-audit data.
- Maven Central ecosystem advisories.
- NuGet/MSRC/.NET announcements.
- RubySec.
- Linux kernel CVE records, stable backports, mailing lists.
- OSS-Fuzz issue references and ClusterFuzz/Testcase records when public.
- Android Security Bulletins, Apple security releases, browser advisories.

Same CVE class is not enough. Compare affected code, trigger, root cause, and fix.

## 5. Ecosystem, dependency, fork, and downstream sources

Determine code ownership:

- Is buggy code authored here, vendored, generated, copied, forked, or dependency-provided?
- Does downstream modify the relevant path?
- Is the bug caused by integration/configuration rather than upstream code?

Search:

- Upstream repository tracker and commits.
- Downstream distro/vendor bug trackers.
- Fork issue trackers and synchronization PRs.
- Package manager metadata and mirrors.
- Distribution patches: Debian, Ubuntu, Red Hat, Alpine, Arch, Homebrew, Nixpkgs.
- Browser/OS vendor downstream fixes.
- Container image and Helm-chart release notes.

Relation rules:

- Same vulnerable upstream code and same fix → upstream-shared duplicate/prior art.
- Independent reimplementation with same bug class → not duplicate merely by similarity.
- Downstream-only integration bug → distinct unless prior record explicitly covers integration.
- Existing upstream bug may make downstream report duplicate or redirect-worthy; state tracker-specific disposition separately.

## 6. Vendor, product, support, and community sources

For closed-source products these may be the only public evidence.

Search:

- Vendor support KB and known-issues pages.
- Release notes, status pages, incident postmortems, update bulletins.
- Product forums, community discussions, feature-request portals.
- App-store reviews and version histories as weak discovery signals.
- Stack Overflow/Stack Exchange.
- Mailing lists, Discourse, Google Groups, project chat archives.
- Maintainer/researcher blogs, conference talks, papers, podcasts/transcripts.
- Reddit/Hacker News/social posts only as leads; corroborate with primary evidence.
- Documentation changes describing new constraints or workarounds.

Web query families:

```text
"{exact error string}" "{product}"
"{symbol or endpoint}" {behavior phrase}
"{product}" {root-cause phrase} fixed
"{product}" {symptom} regression
site:{canonical-domain} {exact identifier}
site:github.com/{owner}/{repo} {behavior phrase}
site:stackoverflow.com "{error string}"
"{old product name}" {same trigger}
"{expected fix phrase}" "{component}"
```

Use date/version filters carefully; old reports can still be duplicates.

## 7. Internal and private corpora

When authorized and connected, search:

- Jira, Linear, Azure Boards, ServiceNow, Bugzilla private groups.
- Slack, Teams, email, support tickets, incident systems.
- Notion/Confluence/Google Drive/SharePoint engineering docs.
- Private GitHub/GitLab issues, advisories, forks, security incidents.
- Bounty platform submissions and duplicate closures available to the user.

Protect secrets and private data. Return only evidence necessary for duplicate identity.

Visibility rule:

- If user asks “is this duplicate in our tracker?” and tracker cannot be searched, verdict is `INCONCLUSIVE`.
- If private corpus is only a theoretical global blind spot, public result may be `NO_DUPLICATE_FOUND` with explicit limitation, but never “absolutely novel.”

## 8. Bounty and disclosure platforms

Use only when finding is bounty/security-disclosure related. Platform status affects filing, but duplicate identity still uses fingerprint tests.

| Context | Sources | Visibility caveat |
|---|---|---|
| Huntr/Protect AI | Repo page, report pages, hacktivity, guidelines, linked CVEs/GHSAs | Pending/private data may be incomplete |
| HackerOne | Program hacktivity, disclosed reports, vendor advisories | Most reports private |
| Bugcrowd | CrowdStream, program brief, vendor advisories | Most reports private |
| Intigriti/YesWeHack | Public disclosures, program brief, vendor advisories | Private corpus unavailable |
| Google/Microsoft/vendor VRPs | Rules, public acknowledgements, advisories, issue trackers | Report corpus generally private |
| Direct coordinated disclosure | Vendor advisories, security page, CVE records | Embargoed reports invisible |

Public absence on a bounty platform is not proof of no duplicate. If the actual report corpus is critical and inaccessible, use `INCONCLUSIVE` for platform-specific novelty.

### WordPress global prior art

For WordPress core/plugin/theme bugs, search all:

- Patchstack vulnerability database.
- Wordfence Intelligence vulnerability database.
- WPScan vulnerability database.
- WordPress.org plugin support forum.
- Plugin/theme `readme.txt` changelog.
- WordPress.org SVN/Trac history and version diffs.
- Vendor changelog/support site.

Search exact plugin slug and aliases. Compare vulnerable/fixed ranges and callback/action names; generic “missing authorization” matches are insufficient.

## 9. Product-specific routing

### OSS repository

Critical: local prior art, canonical tracker all states, PR/MR/commit history, releases, advisories if security, upstream/dependencies.

### Closed-source SaaS/web service

Critical: vendor known issues/support, release notes, status incidents, public research, intended private report corpus if platform-specific verdict requested. Expect `INCONCLUSIVE` when private corpus is inaccessible.

### Desktop/mobile application

Critical: app release notes, OS-specific trackers, crash signatures, store versions, vendor advisories, upstream framework/dependency history.

### Browser/OS

Critical: canonical Bugzilla/Chromium/vendor tracker, restricted-bug caveat, security bulletins, regression ranges, platform tests, stable/backport branches.

### API/service integration

Critical: both provider and consumer trackers, API changelogs, protocol specs, auth/version/config differences, SDK issues.

### Parser/file format/model loader

Critical: parser implementation history, format spec, fuzzing corpora/issues, sibling language implementations, CVE/advisory databases, exact crash signature and malformed structure.

### Fork/vendored dependency

Critical: upstream and downstream trackers/history, divergence point, local modifications, synchronization releases.

### Internal product

Critical: internal tracker, incident/support history, private source history, release/deployment records. Public web is supporting only.

## 10. Query ledger and coverage rules

Record each meaningful query:

| Source | Query | State/version scope | Date | Result count | Plausible candidates | Notes |
|---|---|---|---|---:|---|---|

Zero results must include exact query and source. “Searched GitHub” is not auditable.

Coverage status:

- `CHECKED`: source queried with multiple identity families and candidates inspected.
- `PARTIAL`: source available but indexing/API limits or only one search path used.
- `BLOCKED`: inaccessible, auth failure, rate limit, private, deleted, or query failure.
- `NOT_APPLICABLE`: source cannot reasonably contain this target's prior art; state reason.

Critical coverage gate:

```text
Any critical BLOCKED/PARTIAL source capable of containing the same bug?
  yes -> INCONCLUSIVE or lower-confidence direct candidate verdict
  no  -> continue

Any unresolved plausible candidate?
  yes -> INCONCLUSIVE / LIKELY_DUPLICATE
  no  -> continue

Exact + semantic + root-cause + fix + history + alias searches complete?
  no  -> continue searching
  yes -> adversarial second pass, then NO_DUPLICATE_FOUND if clean
```
