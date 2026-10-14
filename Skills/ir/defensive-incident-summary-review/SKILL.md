---
name: defensive-incident-summary-review
description: Reviews an analyst-written incident summary, report or executive brief against the investigation notes and evidence, checking for omitted facts, unsupported claims, contradictions, unclear impact and audience fit. Use when someone shares a draft incident report, case summary, post-incident write-up or stakeholder update and asks for a review, a check, or help making it clearer.
license: MIT
metadata:
  category: ir
  human_role: incident lead owns the report and its conclusions
  attack: ""
  pairs_with: offensive-reporting
---

# Incident Summary Review

## Why this skill exists
A Google study of 18 analysts and 50 real incidents found that fully autonomous LLM summaries omitted critical details in 35% of cases and introduced factual errors in 42%, while collaborative use reduced effort and improved readability. So the right role for AI is the one this skill takes: the analyst writes, Claude checks the draft against the evidence.

## Human authority
- **Claude does:** compare the draft with the source notes, flag omissions and unsupported claims, check consistency of times and counts, and suggest clearer wording.
- **Claude does not:** add facts that aren't in the notes, change conclusions, assign blame, or produce the final report unasked.
- Every suggested addition cites the note or evidence it comes from.

## Before you start
- The draft, and the source material it summarises (case notes, timeline, ticket history). Without source material, say the review can only cover clarity and internal consistency.
- The audience: executives, legal, auditors, technical peers, regulators, affected customers.
- Any reporting obligations or templates the organisation uses.
- Data handling: incident material is often privileged or regulated. Remind the analyst to follow legal/counsel guidance on what may be shared with an AI tool.

## Review checklist
1. **Completeness against the notes.** Does the summary cover:
   - What happened and how it was detected
   - Timeline with timezone (first evidence, detection, containment, eradication, recovery)
   - Scope: systems, accounts, data types, number of records/people affected — or an explicit "not yet determined"
   - Root cause or initial access vector, and confidence in it
   - Actions taken and their status
   - Remaining risk and open questions
   - Lessons and follow-ups with owners
2. **Unsupported claims.** Flag any sentence the notes don't support, especially absolute claims ("no data was exfiltrated", "fully contained"). Suggest wording that matches the evidence ("we found no evidence of exfiltration in the proxy and DLP logs reviewed").
3. **Consistency.** Times, counts, hostnames and account names agree throughout.
4. **Relationships, not just facts.** Check that the links between facts survive: e.g. that the compromised account *was* the one with access to the affected database. Summaries can keep every fact and still lose the connection that matters.
5. **Audience fit.** Executives need impact, decisions needed and risk; technical readers need indicators and the sequence. Flag jargon for non-technical readers.
6. **Tone.** Factual and blameless; no speculation about individuals' motives.

## Output format
```
OMISSIONS (in notes, missing from draft)
- <fact> — source: <note/line>

UNSUPPORTED OR OVERSTATED
- "<quoted sentence>" → evidence shows … Suggested: "…"

INCONSISTENCIES
- …

CLARITY & AUDIENCE
- …

QUESTIONS BEFORE THIS GOES OUT
- …

YOUR CALL
Which edits do you want to take? The conclusions are yours.
```

## Learning mode
On "coach me": ask the analyst to list the five facts a reader must not miss, then check the draft for them together.

## Pitfalls
- Never fill a gap with a plausible guess. Missing information is reported as missing.
- Don't soften findings to make them comfortable; accuracy is the point.
- Legal/regulatory wording (e.g. "breach") may have specific meaning; flag it for counsel instead of editing it.

## References
- Kramer et al., *Integrating Large Language Models into Security Incident Response*, SOUPS 2025: https://www.usenix.org/conference/soups2025/presentation/kramer
- NIST SP 800-61 Rev. 3, Incident Response Recommendations
