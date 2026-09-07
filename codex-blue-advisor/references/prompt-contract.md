# Advisor prompt contract

Read before every Daybreak Blue consultation. The prompt must be fully self-contained because the advisor may have no memory of this conversation.

Include:

1. The decision or problem, stated plainly as a direct question.
2. Relevant context: current file or state, what has been tried, errors seen, evidence gathered, and constraints that matter.
3. The exact question the executor wants answered, rather than a request for an exhaustive implementation.
4. This explicit framing: "Act as a second opinion / advisor on this decision. Give a direct, concise recommendation with your reasoning - not an implementation. If you disagree with the current approach, say so plainly and explain why."
5. For a cyber or bug-hunting task, the authorization and scope boundary, attacker-control claim, reachability, protected-impact claim, reproduction status, negative control, duplicate status, and the distinction between technical, programme, payout, report, and submission decisions.
6. A request to identify assumptions, missing proof, and the safest next validation step.

The prompt must say that the advisor must not edit files, run state-changing commands, commit, push, deploy, send messages, submit or disclose findings, or take other external actions. Require a concise recommendation and identification of assumptions and missing evidence. Never include secrets, credentials, browser profiles, cookies, private keys, tokens, or `.env` contents.

After the call returns, read the guidance and continue as executor. Do not claim that a consultation happened if the advisor returned an explicit error or no final message.
