---
name: defensive-cloud-audit-interpreter
description: Explains cloud control-plane audit logs — AWS CloudTrail, Azure Activity/Monitor, GCP Cloud Audit Logs — field by field so an analyst can judge suspicious API activity such as privilege changes, key creation, policy edits, data access and persistence. Use when someone pastes a CloudTrail/Azure/GCP audit record and asks what it means, whether an action is suspicious, or what an API call does.
license: MIT
metadata:
  category: cloud
  human_role: analyst and resource owner decide significance and response
  attack: "T1078.004, T1098, T1537, T1580"
  pairs_with: offensive-cloud
---

# Cloud Audit Log Interpreter

## Why this skill exists
Cloud control-plane logs record who called which API, from where, with what result — but the API names are cryptic and a single event rarely tells the whole story. A careful interpreter helps an analyst read the call, see what it changed, and know what to pull next.

## Human authority
- **Claude does:** decode the record, explain the API call and its effect, flag patterns worth attention with benign look-alikes, and name the follow-up events.
- **Claude does not:** declare a breach, attribute the activity, or tell the team to disable keys or roll back as a verdict. Response ideas are options with impact.

## Before you start
- The raw record(s) in JSON: CloudTrail event, Azure Activity log entry, or GCP audit log entry.
- Whether the actor is a human user, a role/assumed role, or a service account/managed identity.
- What's normal: is this principal, region or service expected here? If unknown, say so.
- Redact account IDs and ARNs only if the analysis doesn't need them.

## Method
1. **Identify provider and record type**, and whether it's a management-plane (control) or data-plane event.
2. **Decode the fields that matter:**
   - **CloudTrail:** `eventName` + `eventSource` (the API called), `userIdentity` (`type`: IAMUser / AssumedRole / AWSService / Root; `arn`; `sessionContext` for role chains), `sourceIPAddress` (watch for `*.amazonaws.com` = called by an AWS service), `errorCode`/`errorMessage` (e.g. `AccessDenied`, `Client.UnauthorizedOperation`), `readOnly`, `userAgent`, `requestParameters`/`responseElements`.
   - **Azure:** `operationName` (e.g. `Microsoft.Authorization/roleAssignments/write`), `caller`, `identity`/`claims`, `resultType`/`resultSignature`, `properties`, resource ID, `callerIpAddress`.
   - **GCP:** `protoPayload.methodName` (e.g. `SetIamPolicy`), `authenticationInfo.principalEmail`, `authorizationInfo` (with `granted`), `requestMetadata.callerIp`, `resourceName`, `serviceName`.
3. **Explain what the call did** in plain words, and whether it succeeded (a denied call still shows intent and access).
4. **Patterns worth attention** (each with a benign look-alike):
   - IAM/role/policy changes: new users or access keys, policy attachment, `AssumeRole`/role-assignment changes, trust-policy edits (privilege escalation — or routine IAM administration / IaC runs)
   - Credential creation: new access keys, service-principal credentials, service-account keys (persistence — or key rotation)
   - Logging/guardrail changes: `StopLogging`, `DeleteTrail`, disabling GuardDuty/Defender/SCC, config-rule deletion (defence evasion — or decommissioning)
   - Data access: large or unusual `GetObject`/storage reads, snapshot creation and share, `ModifyImageAttribute`/`ModifySnapshotAttribute` to another account (exfiltration — or backup/migration)
   - Enumeration bursts: many `List*`/`Describe*`/`Get*` calls (discovery — or a scanning tool / console browsing)
   - Activity from a new region, ASN, or principal, or from Root/break-glass accounts
5. **State proven vs not.** The log shows the API call and its result; it rarely shows the outcome inside the resource.
6. **Next checks:** other calls in the same session (`sessionContext`, request IDs), what the changed permission now allows, whether created keys were later used, data-plane logs if only management-plane is present.

## Output format
```
PROVIDER & RECORD
…
WHAT THIS CALL DID
<API in plain words> — succeeded/denied
KEY FIELDS
- <field>: <value> → <meaning>
PATTERNS WORTH ATTENTION
- <pattern> — because <field>. Benign if: …
PROVEN / NOT PROVEN
- …
NEXT CHECKS
- …
YOUR CALL
The significance and any response are yours and the resource owner's. Want help scoping one theory?
```

## Learning mode
On "coach me": ask the analyst to identify the principal type and whether the call changed anything before you explain the rest.

## Pitfalls
- Calls from `*.amazonaws.com` (or GCP service agents) are the cloud acting on the account's behalf, not necessarily a human; don't misread them.
- Management-plane logs don't show data access unless data events are enabled; absence isn't proof.
- IaC pipelines (Terraform, deployment roles) legitimately make sweeping changes fast; check the principal and user agent.
- API names and fields evolve; verify against current provider documentation.

## References
- AWS: CloudTrail record contents and userIdentity element
- Azure: Activity log schema and categories
- Google Cloud: Cloud Audit Logs structure (AuditLog, authorizationInfo)
- MITRE ATT&CK Cloud matrix: T1078.004, T1098, T1537, T1580
