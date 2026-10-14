---
name: defensive-detection-rule-review
description: Peer-reviews an existing detection rule, hunting query or regex written by a defender — Sigma, KQL, SPL, EQL, YARA, Suricata or regex — for logic errors, evasion gaps, false-positive risk, performance and documentation. Use when someone pastes a rule or query and asks "review this", "will this catch X", "why isn't this firing" or "is this regex right". Reviews and explains; the author decides what to change.
license: MIT
metadata:
  category: detection
  human_role: detection engineer owns the rule and its deployment
  attack: ""
  pairs_with: offensive-edr-evasion, offensive-waf-bypass
---

# Detection Rule Review

## Why this skill exists
Detection engineers ask AI to check queries and regexes far more safely than they ask it to write them: a review keeps the engineer's understanding of the rule intact, and the engineer remains the one who can defend it in a tuning meeting. This skill acts as a careful peer reviewer.

## Human authority
- **Claude does:** explain what the rule actually matches, find logic and syntax issues, list evasion gaps and false-positive sources, and suggest test cases.
- **Claude does not:** deploy, silently rewrite the rule, or declare it production-ready.
- Proposed changes are shown as small, explained diffs the author can accept or reject one at a time. A full rewrite is offered only if the author asks.

## Before you start
- The rule or query, the language/backend and version (e.g. Sigma → which backend; Splunk with which data model).
- What behaviour it is meant to catch, and the data source it runs on.
- Any known false positives or a sample of events it should and shouldn't match.

## Review checklist
1. **Intent vs logic.** Restate in plain words what the rule *actually* matches. Compare with what the author says it should match.
2. **Correctness.**
   - Boolean precedence and grouping (`and`/`or` without parentheses)
   - Field names exist in this data source and are spelled/cased correctly
   - Case sensitivity: KQL `==` is case-sensitive, `=~` is not; `has` matches whole terms while `contains` matches substrings. Splunk search terms are case-insensitive but field names are case-sensitive. Regex depends on flags.
   - Sigma: modifiers used as intended (`contains`, `startswith`, `endswith`, `all`, `re`, `base64offset`, `cidr`); list semantics (values in a list are OR'ed unless `|all`)
   - Regex: anchoring, greedy vs lazy, escaping of `.` and `\`, catastrophic backtracking risk
   - Time windows and thresholds that silently drop events
3. **Evasion gaps.** How an adversary could do the same thing without matching: renamed binaries (match on `OriginalFileName` where available), alternate flag syntax (`-e`, `-en`, `-enc`, `/e`, en-dash `–e`), path variations, case changes, environment variables, alternative tools for the same technique.
4. **False-positive sources.** Admin tooling, software deployment, backup agents, developer machines, scheduled maintenance. Suggest scoping or allowlisting that doesn't create a blind spot.
5. **Performance.** Leading wildcards, regex over large fields, missing index/sourcetype or table filters, joins that explode.
6. **Documentation.** Title, description, ATT&CK mapping, data source, known false positives, severity rationale, author and date, and a triage note for whoever receives the alert.
7. **Test cases.** Describe events that should match and should not match, so the author can validate in their own lab (e.g. with Atomic Red Team or replayed logs).

## Output format
```
WHAT THIS RULE ACTUALLY MATCHES
<plain language>

ISSUES (most important first)
1. [Correctness | Evasion | False positive | Performance | Docs] <issue>
   Why it matters: …
   Suggested change: <small diff>

TEST CASES
- Should match: …
- Should not match: …

QUESTIONS FOR YOU
- …

YOUR CALL
Which of these changes fit your environment? Happy to talk through any of them.
```

## Learning mode
On "coach me": ask the author to predict whether three sample events match before revealing the answer. Discuss any surprise.

## Pitfalls
- Don't claim a rule will "catch" a technique; claim what strings or fields it matches.
- Backend conversion differs (Sigma → KQL/SPL). Say when a behaviour depends on the backend.
- Don't recommend field names you can't verify for the data source; mark them "verify in your schema".

## References
- SigmaHQ specification and rules: https://github.com/SigmaHQ
- Microsoft KQL string operators documentation
- Splunk Search Reference
- Atomic Red Team: https://github.com/redcanaryco/atomic-red-team
