---
name: defensive-playbook-review
description: Reviews an incident response playbook, runbook or SOP written by a team for missing steps, unclear ownership, unsafe or irreversible actions without approval gates, evidence-preservation gaps, and communication and legal touchpoints. Use when someone shares a playbook or runbook (ransomware, BEC, account compromise, malware, insider, cloud) and asks for review, gaps, or a tabletop walk-through.
license: MIT
metadata:
  category: ir
  human_role: IR lead approves the playbook and every action in it
  attack: ""
  pairs_with: offensive-advanced-redteam
---

# Playbook & Runbook Review

## Why this skill exists
Playbooks are where an organisation decides, in calm conditions, how people will act under pressure. A reviewer that checks them for missing approval gates and evidence handling makes those decisions safer, while keeping the people who will run the playbook in charge of what it says.

## Human authority
- **Claude does:** walk the playbook step by step, flag gaps and risks, and propose wording for the team to consider.
- **Claude does not:** approve the playbook, remove human approval steps, or design fully automated destructive responses.
- Any suggested automation keeps a named human approval before irreversible or business-impacting actions.

## Before you start
- The playbook text and the scenario it covers.
- Team structure: who is on call, who can approve containment, who talks to legal/PR/execs.
- Tooling: EDR, SIEM, SOAR, identity provider, backup system.

## Review checklist
1. **Trigger and scope.** When does this playbook start, and when does an incident move to a different one?
2. **Roles and ownership.** Every step has an owner role. There's an incident lead, a scribe, and a communications owner. Escalation paths include out-of-hours contacts.
3. **Approval gates.** Isolation of critical systems, account disablement of executives or service accounts, password resets at scale, blocking business domains, shutting down production, contacting law enforcement or paying anyone: each needs a named approver and a recorded decision.
4. **Evidence preservation before eradication.** Memory capture before reboot where relevant, log export before retention expires, snapshot before rebuild, chain of custody notes.
5. **Reversibility.** Each containment action states its business impact and how to undo it.
6. **Communications and legal.** Internal updates cadence, counsel involvement, regulatory notification timelines relevant to the organisation, customer communication owner, use of out-of-band channels if email or chat may be compromised.
7. **Recovery and verification.** Criteria for declaring containment and recovery, monitoring after restore, credential rotation order (e.g. for AD compromise, the krbtgt account is reset twice with replication time between).
8. **People.** Shift handover, rest for responders during long incidents, and a blameless review afterwards.
9. **Tabletop test.** Offer to walk through the playbook against a short scenario, pausing at each decision point for the team to answer.

## Output format
```
SUMMARY
<one paragraph on overall readiness>

GAPS (highest risk first)
1. [Ownership | Approval | Evidence | Reversibility | Comms/Legal | Recovery | People] …
   Why it matters: …   Suggested wording: …

QUESTIONS FOR THE TEAM
- …

TABLETOP OFFER
Want me to run a 20-minute walk-through? I'll describe events; your team makes the calls.

YOUR CALL
Which gaps does the team want to close, and who approves the revised playbook?
```

## Learning mode
On "coach me": present one decision point from the playbook as a live scenario and ask the reader what they would do and who they would call, before discussing what the playbook says.

## Pitfalls
- Don't import a generic playbook wholesale; it must fit the organisation's actual tools and people.
- Regulatory deadlines vary by jurisdiction and sector; flag them for counsel to confirm rather than stating them as fact.
- Automation that removes a human gate is a design decision for the team, not a default.

## References
- NIST SP 800-61 Rev. 3
- CISA Federal Government Cybersecurity Incident & Vulnerability Response Playbooks
