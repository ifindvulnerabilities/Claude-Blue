---
name: defensive-<surface-or-task>
description: <What it reviews or explains, for whom.> Use when <concrete triggers: what the user pastes and the phrases they use>. <One clause on what it won't decide.>
license: MIT
metadata:
  category: <soc | detection | ir | intel | hardening | people>
  human_role: <who owns the decision this skill informs>
  attack: "<ATT&CK IDs, if any>"
  pairs_with: <related claude-red skill, if any>
---

# <Skill Title>

## Why this skill exists
<The real defender need, and evidence for it if you have any.>

## Human authority
- **Claude does:** <explain / review / organise / question>
- **Claude does not:** <decide / act / invent>

## Before you start
<Inputs to ask for, only when missing. Data-handling reminder: redaction, no secrets.>

## Method
1. <Steps a careful senior defender would follow>

## Output format
```
OBSERVED
MEANING (with confidence)
GAPS
NEXT CHECKS
YOUR CALL
```

## Learning mode
<What changes when the user says "coach me".>

## Pitfalls
- <Where LLMs and people typically go wrong on this task>

## References
- <Authoritative, linkable sources>
