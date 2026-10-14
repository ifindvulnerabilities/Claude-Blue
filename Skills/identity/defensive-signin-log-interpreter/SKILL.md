---
name: defensive-signin-log-interpreter
description: Explains Entra ID (Azure AD) and Okta sign-in and audit logs field by field — risk state, conditional access results, MFA and authentication methods, legacy auth, token and OAuth consent events — so an analyst can judge a suspicious sign-in. Use when someone pastes an Entra or Okta sign-in or audit record and asks what it means, whether a login is suspicious, or what a consent or conditional-access field indicates.
license: MIT
metadata:
  category: identity
  human_role: analyst decides whether a sign-in is suspicious and what to do
  attack: "T1078.004, T1528, T1621"
  pairs_with: offensive-oauth
---

# Sign-in Log Interpreter

## Why this skill exists
Cloud identity logs have their own vocabulary (conditional access, risk state, authentication requirement, consent grants) that is easy to misread. A field-by-field explainer that is honest about what each value proves helps an analyst judge a sign-in without over- or under-reacting.

## Human authority
- **Claude does:** decode fields, explain risk and conditional-access outcomes, reconstruct the sign-in sequence, and say what is and isn't shown.
- **Claude does not:** declare an account compromised, or tell the analyst to revoke sessions or disable the user as a conclusion. Those are options with impact, for the analyst to choose.

## Before you start
- The raw record(s): Entra sign-in logs, Entra audit logs, or Okta System Log events, in JSON if possible.
- Timezone, and what's normal for this user (home country, usual devices) if known.
- Redact personal data not needed for the analysis; pseudonymise the user if that's enough.

## Method
1. **Identify the record type** (interactive vs non-interactive sign-in, service principal sign-in, audit event, Okta System Log eventType).
2. **Decode the fields that matter:**
   - **Entra sign-ins:** `riskState` / `riskLevelDuringSignIn` / `riskDetail`; `conditionalAccessStatus` (success / failure / notApplied); `authenticationRequirement` (singleFactor / multiFactorAuthentication); `status.errorCode` (e.g. 0 success; 50126 bad credentials; 50074 MFA required; 50140/50097 device or MFA interrupts; 530002/53003 blocked by conditional access); `clientAppUsed` (flag "Other clients" / legacy auth, which bypasses modern controls); `authenticationDetails` (which methods actually satisfied the sign-in); location and `deviceDetail`.
   - **Entra audit:** OAuth app consent grants ("Consent to application", "Add app role assignment"), added credentials to a service principal or app ("Add service principal credentials"), new federation or domain settings, admin role assignments.
   - **Okta System Log:** `eventType` such as `user.session.start`, `user.authentication.sso`, `policy.evaluate_sign_on`, `app.oauth2.*`, `user.mfa.factor.*`, `system.push.send_factor_verify_request`; `outcome.result`; `securityContext` (ASN, isProxy); `debugContext` for policy decisions.
3. **Reconstruct the sequence** in UTC from the records present.
4. **Patterns worth attention** (each with a benign look-alike):
   - Many failures then a success for one account (possible spray or stuffing — or a user who fixed their password)
   - Success with `authenticationRequirement = singleFactor` on a sensitive account (MFA not applied — or a trusted-network policy)
   - Legacy auth / "Other clients" success (bypasses conditional access — or an old mail client)
   - Impossible travel / new ASN (compromise — or VPN and travel)
   - MFA fatigue: repeated push requests then an approval (prompt bombing — or a user retrying)
   - OAuth consent to an unfamiliar app, or new credentials added to a service principal (illicit consent / persistence — or a sanctioned integration)
5. **State what is proven vs not.** A risky sign-in flagged by the provider is a model's score, not a confirmed compromise; a "success" doesn't show what happened in the session.
6. **Next checks:** the user's other recent sign-ins, what the consented app can access, mailbox-rule changes after the sign-in (hand off to `defensive-phishing-review`), audit events for the same actor.

## Output format
```
RECORD TYPE
…
KEY FIELDS
- <field>: <value> → <meaning>
SEQUENCE (UTC)
- …
PATTERNS WORTH ATTENTION
- <pattern> — because <field/value>. Benign if: …
PROVEN / NOT PROVEN
- …
NEXT CHECKS
- …
YOUR CALL
Your read on this sign-in, and any response, is yours. Want help checking one theory?
```

## Learning mode
On "coach me": give the analyst the record and ask them to find the authentication requirement and the conditional-access result first, and say what each implies.

## Pitfalls
- Provider risk scores are probabilistic; don't treat "risky" as proof or "no risk" as safe.
- Non-interactive sign-ins (tokens, service principals) follow different rules than user logins; don't read them as human activity.
- Field names and error codes change over time; verify against current Microsoft/Okta documentation.
- Never follow URLs or app links from the records.

## References
- Microsoft: Entra ID sign-in logs schema and error codes
- Microsoft: Entra ID audit log and OAuth consent events
- Okta: System Log event types reference
- MITRE ATT&CK T1078.004 (Cloud Accounts), T1528 (Steal Application Access Token), T1621 (MFA Request Generation)
