---
name: defensive-timeline-review
description: Reviews an investigator's incident timeline or attack narrative for gaps, ordering errors, timezone problems, unsupported links between events, and alternative explanations. Use when someone shares an incident timeline, super-timeline extract, kill-chain reconstruction or "here's what I think happened" and asks for a sanity check or what they might be missing.
license: MIT
metadata:
  category: ir
  human_role: investigator owns the reconstruction and conclusions
  attack: ""
  pairs_with: offensive-advanced-redteam
---

# Timeline Review

## Why this skill exists
Long investigations accumulate evidence faster than anyone can hold it in mind, and LLMs working alone are known to miss small but critical details over long tasks. Used as a reviewer, though, a model is good at checking an investigator's reconstruction for internal consistency and for gaps the investigator can then go and examine.

## Human authority
- **Claude does:** check ordering and timezones, mark which links are evidenced vs inferred, point out gaps in the attack lifecycle, and offer alternative explanations to test.
- **Claude does not:** fill gaps with invented events, declare the root cause, or attribute the attack to an actor.

## Before you start
- The timeline (any format), with sources for each entry if available.
- The timezone each source uses. Mixed local/UTC timestamps are the most common timeline error.
- What the investigator currently believes happened, in a sentence or two.

## Method
1. **Normalise times.** Convert to UTC where the source timezone is known; mark entries where it isn't.
2. **Classify each entry**: *observed* (directly in a log/artifact), *derived* (computed, e.g. from file system timestamps that can be altered), or *inferred* (investigator's interpretation).
3. **Check ordering and causality.** Flag effects that precede causes, implausible gaps, and links stated as fact that are only inferred ("the attacker then moved to SRV02" — what shows it was the same actor?).
4. **Walk the lifecycle.** Compare against stages (initial access, execution, persistence, privilege escalation, credential access, discovery, lateral movement, collection, exfiltration, impact). For each empty stage, ask whether it didn't happen, wasn't logged, or wasn't looked for.
5. **Timestamp caveats.** File timestamps can be modified (timestomping); $MFT `$STANDARD_INFORMATION` vs `$FILE_NAME` discrepancies are worth checking; log retention gaps look like quiet periods.
6. **Alternative explanations.** Offer at least one competing reading of the key links, and the evidence that would separate them.
7. **Dwell time and first-evidence check.** Is the earliest entry really the beginning, or just the edge of available logs?

## Output format
```
NORMALISED TIMELINE (UTC)
| time | event | source | observed/derived/inferred |

ORDERING & TIMEZONE ISSUES
- …

LINKS THAT ARE INFERRED, NOT SHOWN
- <A → B>: what would confirm it …

LIFECYCLE GAPS
- <stage>: not observed — possible reasons …, where to look …

ALTERNATIVE READINGS
- …

YOUR CALL
Which gaps do you want to chase first?
```

## Learning mode
On "coach me": ask the investigator to mark each entry observed/derived/inferred themselves, then compare.

## Pitfalls
- Don't treat absence of evidence as evidence of absence; retention and logging gaps are common.
- Never add events from assumption to "complete" a story.
- Avoid attribution; similarity to a known actor's TTPs is not attribution.

## References
- NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response
- MITRE ATT&CK Enterprise tactics: https://attack.mitre.org/tactics/enterprise/
