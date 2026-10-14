---
name: defensive-post-incident-review
description: Helps a team prepare, facilitate and write up a blameless post-incident review (lessons learned, retrospective, after-action review) by structuring the discussion, separating contributing factors from blame, and turning findings into owned actions. Use when someone is planning or writing a post-incident review, retro or after-action report for a security incident or near miss.
license: MIT
metadata:
  category: ir
  human_role: team draws conclusions and owns actions
  attack: ""
  pairs_with: offensive-reporting
---

# Blameless Post-Incident Review

## Why this skill exists
The lessons from an incident live in the people who handled it. AI can make the review easier to run and the write-up clearer, but the insight has to come from the team's own discussion. This skill supports that discussion and protects its blameless character.

## Human authority
- **Claude does:** propose an agenda and questions, organise the team's input, rephrase blaming language, and check that every action has an owner and a date.
- **Claude does not:** decide root cause, assign fault to individuals, or produce findings the team didn't reach.

## Before you start
- The incident summary and timeline.
- Who will attend, and the time available.
- Whether the output goes to leadership, auditors, or only the team.

## Method
1. **Prepare.** Draft a 45–60 minute agenda: facts recap (10 min), what went well (10), what was hard (15), contributing factors (15), actions (10). Suggest the facilitator not be the incident lead.
2. **Questions that avoid blame.** Use "what" and "how", not "who" and "why didn't you":
   - What did you know at that moment, and what were you trying to achieve?
   - What made that step harder or slower than it should have been?
   - Where did tools, alerts or documentation help or mislead?
   - What would have made the right action the easy action?
3. **Contributing factors, not a single root cause.** Organise input into: detection, tooling, process, communication, staffing and fatigue, knowledge, and external factors.
4. **Rewrite blaming language.** Turn "Bob failed to patch" into "The patch was available for 40 days; the patch process had no alert for internet-facing systems." Point out such rewrites to the author.
5. **Actions.** Each has an owner, a due date, and a way to tell it's done. Prefer fixes to systems over "be more careful" or "retrain staff".
6. **Recognise the work.** Include what responders did well and the effort they put in.

## Output format
```
AGENDA
…

DISCUSSION QUESTIONS
…

WRITE-UP STRUCTURE
- Summary · Timeline · What went well · Contributing factors · Actions (owner, date, done-when)

LANGUAGE NOTES
- "<original>" → "<blameless rewrite>"

YOUR CALL
The conclusions and actions are the team's. Shall I help format what you agreed?
```

## Learning mode
On "coach me" (e.g. a new facilitator): ask them to draft three discussion questions first, then review those questions together for blaming language and openness.

## Pitfalls
- Don't collapse a complex incident into one "root cause".
- Never name individuals as the cause; describe conditions and decisions in context.
- Avoid producing metrics that rank responders.

## References
- Google SRE Book, "Postmortem Culture: Learning from Failure"
- NIST SP 800-61 Rev. 3, post-incident activity
