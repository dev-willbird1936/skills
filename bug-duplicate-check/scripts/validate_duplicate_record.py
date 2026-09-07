#!/usr/bin/env python3
"""Validate a durable bug-duplicate-check record without external packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_FIELDS = {
    "schema_version",
    "finding_id",
    "canonical_finding",
    "finding_sha256",
    "fingerprint_sha256",
    "target",
    "tested_version",
    "duplicate_verdict",
    "technical_relationship",
    "confidence",
    "checked_at_utc",
    "critical_coverage",
    "current_state",
    "closest_prior_art",
}
VERDICTS = {
    "DUPLICATE_EXACT",
    "DUPLICATE_SUBSUMED",
    "LIKELY_DUPLICATE",
    "RELATED_VARIANT",
    "NOVEL_BYPASS",
    "NOT_DUPLICATE",
    "NO_DUPLICATE_FOUND",
    "INCONCLUSIVE",
}
RELATIONSHIPS = {
    "same-root-cause",
    "same-symptom-different-cause",
    "same-component",
    "fix-bypass",
    "regression",
    "upstream-shared",
    "unrelated",
}
REQUIRED_SECTIONS = {
    "## Verdict",
    "## Canonical fingerprint",
    "## Candidate comparison",
    "## Evidence ledger",
    "## History and current-state analysis",
    "## Adversarial second pass",
    "## Coverage checklist",
    "## Conclusion",
    "## Not checked / limitations",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FINDING_RE = re.compile(
    r"^(?:"
    r"FND-\d{8}-[a-z0-9]+(?:-[a-z0-9]+)*-\d{4}"
    r"|"
    r"FND-\d{8}-[A-Z]+-[A-Z]+-\d{4}-.+"
    r")$"
)
# Legacy records predate the lowercase software-key convention.
LEGACY_FINDING_RE = re.compile(
    r"^FND-\d{8}-[A-Z][A-Z0-9_]*(?:-[A-Z][A-Z0-9_]*)*-\d{4}(?:-[a-z0-9]+(?:-[a-z0-9]+)*)?$"
)
COVERAGE_RE = re.compile(r"^(\d+)/(\d+)$")
PLACEHOLDERS = ("YYYY-", "VERIFY", "TBD", "TODO", "<finding", "{finding")
FINGERPRINT_KEYS = (
    "target_identity",
    "version_window",
    "surface",
    "actor_preconditions",
    "trigger_input",
    "source_data_flow",
    "sink_operation",
    "broken_invariant",
    "root_cause",
    "observable_result",
    "impact",
    "fix_shape",
)


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["missing opening YAML frontmatter delimiter"]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, ["missing closing YAML frontmatter delimiter"]
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if (
            not line.strip()
            or line.lstrip().startswith("#")
            or line[:1].isspace()
            or ":" not in line
        ):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = strip_scalar(value)
    return fields, []


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section_content(text: str, heading: str) -> str:
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        return ""
    content: list[str] = []
    fence: str | None = None
    for line in lines[start + 1 :]:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            marker_match = re.match(r"^(`{3,})", stripped)
            marker = marker_match.group(1) if marker_match else "```"
            if fence is None:
                fence = marker
            elif stripped.startswith(fence):
                fence = None
            content.append(line)
            continue
        if fence is None and line.startswith("## "):
            break
        content.append(line)
    return "\n".join(content).strip()


def meaningful(content: str, minimum: int = 24) -> bool:
    cleaned = re.sub(r"[`#|:\-\[\]\s]", "", content)
    return len(cleaned) >= minimum


def table_data_rows(content: str, expected_columns: int | None = None) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        if cells[0].lower() in {"candidate", "#", "field", "source class"}:
            continue
        if expected_columns is not None and len(cells) != expected_columns:
            continue
        rows.append(cells)
    return rows


def is_findings_artifact(path: Path) -> bool:
    resolved = path.resolve()
    parts = list(resolved.parts)
    lower = [part.lower() for part in parts]
    if "findings" not in lower:
        return False
    index = len(parts) - 1 - lower[::-1].index("findings")
    workspace = Path(*parts[:index])
    return bool(
        len(parts) - index >= 3
        and (workspace / "AGENTS.md").is_file()
        and (workspace / "System" / "global-finding-naming-rating-system.md").is_file()
    )


def has_primary_reference(value: str, folder: Path) -> bool:
    if re.search(r"https?://[^\s)]+", value):
        return True
    cleaned = re.sub(r"[`*_]", "", value).strip()
    candidate = (folder / cleaned).resolve()
    return candidate.parent == folder.resolve() and candidate.is_file()


def valid_utc(value: str) -> bool:
    if not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def fingerprint_serialization(content: str) -> tuple[str, list[str]]:
    errors: list[str] = []
    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip() and not re.fullmatch(r"`{3,}(?:text)?", line.strip(), re.IGNORECASE)
    ]
    if len(lines) != len(FINGERPRINT_KEYS):
        errors.append(
            f"Canonical fingerprint must contain exactly {len(FINGERPRINT_KEYS)} ordered key=value lines"
        )

    values: list[str] = []
    for index, key in enumerate(FINGERPRINT_KEYS):
        if index >= len(lines):
            errors.append(f"Canonical fingerprint is missing ordered field {key}")
            values.append("")
            continue
        match = re.fullmatch(rf"{re.escape(key)}=(.+)", lines[index])
        if not match:
            errors.append(f"Canonical fingerprint line {index + 1} must be {key}=<value>")
            values.append("")
            continue
        value = match.group(1).strip()
        if not value:
            errors.append(f"Canonical fingerprint has an empty {key}")
        values.append(value)

    serialized = "\n".join(
        f"{key}={values[index] if index < len(values) else ''}"
        for index, key in enumerate(FINGERPRINT_KEYS)
    )
    return serialized, errors


def validate(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    fields, errors = parse_frontmatter(text)
    errors.extend(
        f"missing frontmatter field: {key}" for key in sorted(REQUIRED_FIELDS - fields.keys())
    )

    finding_id = fields.get("finding_id", "")
    if fields.get("schema_version") != "bug-duplicate-check/v1":
        errors.append("schema_version must be bug-duplicate-check/v1")
    if finding_id and "YYYY" not in finding_id and not (
        FINDING_RE.match(finding_id) or LEGACY_FINDING_RE.match(finding_id)
    ):
        errors.append("finding_id does not match workspace FND naming")
    if finding_id and path.name != f"DUPLICATE-CHECK-{finding_id}.md":
        errors.append("duplicate record filename does not match finding_id")
    if not is_findings_artifact(path):
        errors.append("duplicate record must be under Findings/<repo-or-software>/")

    canonical_value = fields.get("canonical_finding", "")
    if not canonical_value:
        errors.append("canonical_finding must name the sibling finding file")
    else:
        canonical = (path.parent / canonical_value).resolve()
        if canonical.parent != path.resolve().parent:
            errors.append("canonical_finding must be a sibling in the same finding folder")
        elif not canonical.is_file():
            errors.append("canonical_finding does not exist")
        elif sha256_file(canonical) != fields.get("finding_sha256"):
            errors.append("finding_sha256 does not match canonical_finding")
    if not SHA256_RE.match(fields.get("finding_sha256", "")):
        errors.append("finding_sha256 must be a lowercase SHA-256")
    if not SHA256_RE.match(fields.get("fingerprint_sha256", "")):
        errors.append("fingerprint_sha256 must be a lowercase SHA-256")

    verdict = fields.get("duplicate_verdict", "")
    if verdict not in VERDICTS:
        errors.append(f"invalid duplicate_verdict: {verdict}")
    if fields.get("technical_relationship") not in RELATIONSHIPS:
        errors.append("technical_relationship is missing or invalid")
    if fields.get("confidence") not in {"High", "Medium", "Low"}:
        errors.append("confidence must be High, Medium, or Low")
    if fields.get("current_state") not in {"affected", "fixed", "regression", "unknown"}:
        errors.append("current_state is missing or invalid")
    if not fields.get("target", "").strip() or not fields.get("tested_version", "").strip():
        errors.append("target and tested_version must be substantive")
    if not valid_utc(fields.get("checked_at_utc", "")):
        errors.append("checked_at_utc must be a valid ISO UTC timestamp")

    coverage_match = COVERAGE_RE.match(fields.get("critical_coverage", ""))
    if not coverage_match:
        errors.append("critical_coverage must use checked/applicable integer syntax")
    else:
        checked, applicable = map(int, coverage_match.groups())
        if applicable < 1 or checked > applicable:
            errors.append("critical_coverage values are invalid")
        if verdict == "NO_DUPLICATE_FOUND" and checked != applicable:
            errors.append("NO_DUPLICATE_FOUND requires complete critical coverage")

    for section in sorted(REQUIRED_SECTIONS):
        content = section_content(text, section)
        minimum = 4 if section == "## Not checked / limitations" else 24
        if not meaningful(content, minimum):
            errors.append(f"section is empty or non-substantive: {section}")

    evidence_rows = table_data_rows(section_content(text, "## Evidence ledger"), 6)
    if not evidence_rows:
        errors.append("Evidence ledger requires at least one source result row")
    elif any(not has_primary_reference(row[-1], path.parent) for row in evidence_rows):
        errors.append("every Evidence ledger row requires a primary URL or sibling evidence file")

    fingerprint, fingerprint_errors = fingerprint_serialization(
        section_content(text, "## Canonical fingerprint")
    )
    errors.extend(fingerprint_errors)
    if not fingerprint_errors:
        computed_fingerprint = hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()
        if computed_fingerprint != fields.get("fingerprint_sha256"):
            errors.append("fingerprint_sha256 does not match Canonical fingerprint")

    comparison_rows = table_data_rows(section_content(text, "## Candidate comparison"), 7)
    closest = fields.get("closest_prior_art", "").strip()
    if verdict in {"DUPLICATE_EXACT", "DUPLICATE_SUBSUMED", "LIKELY_DUPLICATE"}:
        if not meaningful(closest, 4) or closest.lower() in {"none", "unknown", "n/a"}:
            errors.append(f"{verdict} requires closest_prior_art")
        elif not re.fullmatch(r"https?://[^\s]+", closest):
            errors.append(f"{verdict} closest_prior_art must be a direct primary URL")
        if not comparison_rows:
            errors.append(f"{verdict} requires a candidate comparison row")
        elif not any(
            closest in row[0]
            and meaningful(row[-1], 16)
            and has_primary_reference(row[0], path.parent)
            for row in comparison_rows
        ):
            errors.append(
                f"{verdict} requires a closest-prior-art row with substantive decisive evidence"
            )

    if coverage_match:
        checked = int(coverage_match.group(1))
        if len(evidence_rows) < checked:
            errors.append("Evidence ledger has fewer rows than checked critical sources")
        distinct_sources = {row[1].strip().lower() for row in evidence_rows}
        if len(distinct_sources) < checked:
            errors.append("Evidence ledger has fewer distinct source classes than critical_coverage")

    coverage_rows = table_data_rows(section_content(text, "## Coverage checklist"), 3)
    checked_coverage_rows = {
        row[0].strip().lower()
        for row in coverage_rows
        if row[1].strip().lower() == "checked"
    }
    if not checked_coverage_rows:
        errors.append("Coverage checklist requires at least one checked source-class row")
    elif coverage_match and len(checked_coverage_rows) < int(coverage_match.group(1)):
        errors.append("Coverage checklist has fewer distinct checked classes than critical_coverage")

    for token in PLACEHOLDERS:
        if token.lower() in text.lower():
            errors.append(f"duplicate record contains placeholder token: {token}")
            break

    return {
        "path": str(path.resolve()),
        "valid": not errors,
        "duplicate_verdict": verdict,
        "errors": errors,
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if not args.record.is_file():
        result = {
            "path": str(args.record),
            "valid": False,
            "duplicate_verdict": None,
            "errors": ["record does not exist or is not a file"],
            "warnings": [],
        }
    else:
        result = validate(args.record)
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{'PASS' if result['valid'] else 'FAIL'}: {result['path']}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
