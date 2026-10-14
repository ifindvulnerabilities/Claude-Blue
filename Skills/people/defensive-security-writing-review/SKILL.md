---
name: defensive-security-writing-review
description: Improves the clarity, accuracy and tone of an analyst's own security writing — case notes, alert descriptions, shift handoffs, tickets, emails to users or clients, and updates to managers — without changing the technical facts. Use when someone pastes a security-related draft and asks to "make this better", "reword", "make it clearer", "make it shorter" or "make it less technical".
license: MIT
metadata:
  category: people
  human_role: analyst is the author and sends the message
  attack: ""
  pairs_with: offensive-reporting
---

# Security Writing Review

## Why this skill exists
Text editing was the second most common SOC use of LLMs in field research (about 22% of queries): rephrasing incident descriptions, fixing grammar, and adjusting tone for users and clients. The analyst stays the author; this skill helps them say what they mean clearly.

## Human authority
- **Claude does:** tighten wording, fix grammar, adjust tone and reading level, and point out ambiguity.
- **Claude does not:** add technical facts, change findings, strengthen or weaken conclusions, or send anything.
- If an edit would change meaning, Claude asks instead of making it.

## Before you start
- The draft, the audience (peer, next shift, end user, executive, client), and the channel (ticket, email, chat).
- Any house style or template.

## Method
1. **Lock the facts.** List the facts in the draft (times, hosts, accounts, actions, status). The edit must preserve all of them exactly.
2. **Edit for the audience:**
   - *Next shift / peer:* status first, what's done, what's pending, what to watch for, where the evidence is.
   - *End user:* plain language, what happened to them, what they need to do (if anything), who to contact. No blame, no alarming jargon.
   - *Executive:* impact, current status, decision or support needed, next update time.
   - *Client (MSSP/MDR):* what we observed, what we did, what we recommend they do, and the confidence level.
3. **Remove ambiguity.** Replace "the server" with its name, "recently" with a time, "resolved" with what was actually done.
4. **Keep certainty honest.** Don't turn "likely" into "confirmed" or the reverse. Point out where the draft overstates or understates.
5. **Show changes.** Return the edited version, followed by a short list of meaning-relevant changes so the author can verify nothing shifted.

## Output format
```
EDITED VERSION
…

FACTS PRESERVED
- …

CHANGES WORTH CHECKING
- <change> — because …

QUESTIONS
- <anything ambiguous I didn't guess at>

YOUR CALL
It's your message — keep, change or discard any edit.
```

## Learning mode
On "coach me": instead of rewriting, mark the three sentences that most need work and say what's wrong with each (vague, overstated, jargon), so the analyst rewrites them.

## Pitfalls
- Polished wording can make a weak finding sound strong. Keep hedges where the evidence is uncertain.
- Don't add reassurance ("there is no risk") the author didn't write.
- Keep the analyst's voice; don't make every note sound the same.

## References
- U.S. Federal Plain Language Guidelines: https://www.plainlanguage.gov/guidelines/
- NIST SP 800-61 Rev. 3, incident response communication and information sharing
