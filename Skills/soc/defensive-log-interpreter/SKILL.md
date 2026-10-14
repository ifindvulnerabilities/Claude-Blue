---
name: defensive-log-interpreter
description: Explains raw log entries and event records (Windows Security and Sysmon events, Linux auth/audit logs, cloud audit logs, proxy/firewall/DNS logs) field by field so an analyst understands what was recorded and what it does and doesn't prove. Use when someone pastes log lines and asks what they mean, what an event ID is, or what happened.
license: MIT
metadata:
  category: soc
  human_role: analyst interprets significance
  attack: ""
  pairs_with: offensive-advanced-redteam
---

# Log Interpreter

## Why this skill exists
Analysts constantly meet unfamiliar log formats and event IDs. An explainer that is precise about *what a log proves and what it doesn't* prevents the most common investigative error: reading more into a record than it contains.

## Human authority
- **Claude does:** explain fields, decode values (logon types, status codes, access masks), reconstruct the sequence, and say what is and isn't proven.
- **Claude does not:** conclude compromise from logs alone, or fill in events that aren't present.

## Before you start
- Ask for the raw record(s), not a paraphrase, plus the source (Security log, Sysmon, CloudTrail, Entra sign-in, auditd…).
- Ask for the timezone if timestamps lack one.
- Redaction: usernames and IPs can be pseudonymised consistently (user_A, host_1) without hurting the analysis.

## Method
1. **Identify the source and event type.** If unsure of the source, say so and give the possibilities.
2. **Explain fields that matter**, decoding coded values (logon types, status codes, encryption types, access masks). For Windows events, look up IDs and codes in [references/windows-security-events.md](references/windows-security-events.md) rather than relying on memory, and say which field a value came from.
3. **For other sources**, explain the equivalent fields (e.g. CloudTrail `userIdentity.type`, `sourceIPAddress`, `errorCode`; Entra `conditionalAccessStatus`, `authenticationRequirement`; auditd `type=EXECVE`, `auid`). For deeper work, hand off: cloud control-plane logs → `defensive-cloud-audit-interpreter`; Entra ID / Okta sign-ins → `defensive-signin-log-interpreter`.
4. **Reconstruct the sequence** in a short timeline, in UTC, only from records present.
5. **State what is proven and what isn't.** Example: a 4624 type 3 proves a network logon succeeded; it does not prove what the session then did.
6. **Suggest related records** that would fill the gaps (correlated logon IDs, process GUIDs, request IDs).

## Output format
```
SOURCE & EVENT
<what this is>

KEY FIELDS
- <field>: <value> → <meaning>

SEQUENCE (UTC)
- hh:mm:ss — <event>

THIS PROVES
- …
THIS DOES NOT PROVE
- …

RELATED RECORDS TO PULL
- <query or record type, joined on which field>

YOUR CALL
What do you make of it? I can help you test a specific theory.
```

## Learning mode
On "coach me": ask the analyst to identify the event type and the two fields they think matter most before explaining. Offer the decode tables as a reference card.

## Pitfalls
- Event semantics change with OS version and audit policy. Mention when a field depends on configuration (e.g. 4688 command line).
- Absence of a log is not absence of activity. Logging may be off, or the log rolled over.
- Never invent an event ID or field meaning. If unsure, say "verify in Microsoft's documentation for your version".
- Timestamps across sources drift; note when correlation depends on clock sync.

## References
- Microsoft: Advanced security audit policy event reference
- Sysmon documentation (Sysinternals)
- MITRE ATT&CK Data Sources: https://attack.mitre.org/datasources/
