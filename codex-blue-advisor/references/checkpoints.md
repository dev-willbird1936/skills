# Session checkpoint policy

Read only when session checkpoints are active. Apply these rules together with the parent skill's no-total-timeout, read-only, safety, and duplicate-consult rules.

## When to consult

- Before the first Write, Edit, or state-changing Bash call on a non-trivial task such as an install, migration, commit, deploy, or other mutation.
- Before committing to a multi-step design or routing decision.
- Before choosing or reprioritizing a bug-hunting target, capability, account condition, or validation path when the choice materially affects scope, risk, or time.
- When a lead may be promoted to a finding: ask specifically whether attacker control, reachability, protected-boundary impact, reproducibility, and negative-control evidence are sufficient.
- When stuck: an error keeps recurring, the approach is not converging, or the result does not fit the expected protected behavior.
- Before declaring a non-trivial task complete, after the deliverable is durable.
- Before finalizing local report wording when severity, programme eligibility, duplicate status, P-rating, payout confidence, or submission readiness is uncertain.

## When not to consult

- Simple factual lookups or arithmetic.
- Short reactive steps where the next action is dictated by the tool output just read.
- Routine file inspection that does not change the decision.
- Every individual probe in a bug hunt. Batch meaningful evidence and consult at the decision boundary.
- Do not re-consult on the same decision unless new evidence, a new error, or a genuinely changed constraint makes the question materially different.

## Conservative use

Use checkpoints sparingly and only when Daybreak Blue can materially improve a consequential security or routing decision. Prefer direct validation and the executor's reasoning for routine, reversible, or low-risk work. Batch related evidence and questions into one focused consultation; do not spend a separate call on each probe, tool result, or minor step. Ask a concrete question, avoid overlapping or duplicate consultations, and never use the advisor as a progress or status check. Re-consult only when new evidence, an error, or a changed constraint materially changes the decision.
