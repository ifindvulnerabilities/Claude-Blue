---
name: defensive-threat-intel-review
description: Helps a defender read and apply a threat intelligence report, vendor advisory, CISA alert or vulnerability bulletin — summarising key behaviours, proposing candidate ATT&CK mappings for analyst verification, extracting IOCs as data, and asking what is relevant to the organisation. Use when someone shares a threat report, blog, advisory or CVE and asks what it means for them, for a summary, or for ATT&CK mapping.
license: MIT
metadata:
  category: intel
  human_role: analyst verifies mappings and decides relevance and priority
  attack: ""
  pairs_with: offensive-osint-methodology
---

# Threat Intel Review

## Why this skill exists
Turning narrative threat reports into something actionable is slow, manual work. Studies show LLMs can reduce that effort, but they also confuse similar ATT&CK techniques and lose context. So this skill proposes mappings as *candidates with evidence*, and the analyst confirms them.

## Human authority
- **Claude does:** summarise behaviours, quote the sentences behind each candidate mapping, list IOCs, and ask relevance questions.
- **Claude does not:** confirm attribution, decide priority for the organisation, or present candidate mappings as verified.
- IOCs are extracted as defanged text. Claude never visits them.

## Before you start
- The report text or link content, and its date (intel ages quickly).
- The organisation's context: industry, key platforms (e.g. Windows/AD, M365, AWS, specific edge devices), internet-facing systems.
- What the analyst wants: briefing, detection gap check, hunt ideas, or patch prioritisation.

## Method
1. **One-paragraph summary** in your own words: who is targeted, how, and what the impact is. Note the source's confidence language and the report date.
2. **Behaviours first.** List the adversary behaviours described, each with the sentence it comes from (paraphrased, with a pointer to the section).
3. **Candidate ATT&CK mappings.** For each behaviour, propose a technique/sub-technique with:
   - the supporting text
   - confidence (*strong* / *plausible* / *weak*)
   - a commonly confused alternative if one exists (e.g. T1078 Valid Accounts vs T1110 Brute Force; T1059.001 PowerShell vs T1218 proxy execution)
   Mark the whole list "for analyst verification".
4. **IOCs as data.** Extract hashes, domains, IPs, URLs, file paths, registry keys, defanged. Note that atomic IOCs age fast and behaviour is more durable.
5. **Relevance questions.** Do we run the affected product/version? Is it internet-facing? Do we have logging for these behaviours? Have we seen any of these indicators?
6. **What the analyst could do next**: hunt ideas (as hypotheses), detection coverage to check, patches or mitigations to discuss with owners.
7. **CVE specifics** (if present): affected versions, exploitation status (e.g. listed in CISA KEV), vendor fix and workaround. Tell the analyst to confirm on the vendor's advisory; don't state version ranges you can't see in the input.

## Output format
```
SUMMARY (report dated …)
…

BEHAVIOURS & CANDIDATE MAPPINGS — verify before use
| behaviour | source section | candidate technique | confidence | often confused with |

IOCs (defanged, not checked)
- …

IS THIS RELEVANT TO US? — questions
- …

POSSIBLE NEXT STEPS
- Hunt hypothesis: …
- Coverage check: …
- Mitigation to discuss: …

YOUR CALL
Which of these matter for your environment, and what priority?
```

## Learning mode
On "coach me": give the analyst a behaviour and ask them to map it before showing the candidate, then discuss differences.

## Pitfalls
- Don't attribute to an actor because of overlapping tools; tools are shared.
- Don't amplify vendor hype; separate what is observed from what is speculated.
- Respect copyright: summarise reports; don't reproduce them.

## References
- MITRE ATT&CK: https://attack.mitre.org
- CISA Known Exploited Vulnerabilities Catalog
- MITRE TRAM (Threat Report ATT&CK Mapper)
