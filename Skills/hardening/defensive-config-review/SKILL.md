---
name: defensive-config-review
description: Reviews security configuration that a defender pastes — cloud IAM and bucket policies, firewall and security-group rules, Group Policy and audit-policy settings, conditional access policies, SSH/sshd, web server headers, Kubernetes RBAC — and explains risks, misconfigurations and logging gaps. Use when someone shares a policy, rule set or config export and asks "is this secure", "what's wrong with this" or "review this config".
license: MIT
metadata:
  category: hardening
  human_role: system owner decides changes and accepts risk
  attack: "T1078, T1098, T1562"
  pairs_with: offensive-cloud, offensive-active-directory
---

# Security Configuration Review

## Why this skill exists
Defenders spend much of their time reading configuration written by others. A careful reviewer that explains *what a policy actually permits* — in plain words — helps them find risk quickly and explain it to system owners, who make the final change.

## Human authority
- **Claude does:** explain effective permissions, flag risky patterns, map them to known attack paths, and suggest least-privilege alternatives as options.
- **Claude does not:** apply changes, or declare a configuration "secure". It states what it reviewed and what it couldn't see.
- Every recommendation notes possible business impact, so the owner can weigh it.

## Before you start
- The configuration text (policy JSON, rule export, GPO report, sshd_config…), and the platform and version.
- What the system is for and who should have access.
- **Redact secrets.** Remove keys, passwords, connection strings and tokens before pasting. If any appear, tell the analyst to treat them as exposed and rotate them.

## Method
1. **Restate effective behaviour.** "This policy lets any principal in account X read every object in bucket Y from any network."
2. **Flag risky patterns** with the exact line:
   - Cloud IAM: wildcard `Action`/`Resource`, `iam:PassRole` with broad resources, `sts:AssumeRole` trust to `*` or broad principals, missing `Condition` keys, policy-modification permissions that allow privilege escalation, public bucket/blob access
   - Network: `0.0.0.0/0` (or `::/0`) to management ports (22, 3389, 5985/5986, database ports), any-any rules, rules that shadow later, more specific denies
   - Windows/AD: weak or missing audit policy (logon, process creation, account management, Kerberos), LAN Manager/NTLMv1 allowed, SMB signing not required, LDAP signing/channel binding not enforced, local admin password reuse (no LAPS)
   - Identity: conditional access exclusions that cover admins, legacy authentication allowed, MFA not required for privileged roles
   - SSH: `PermitRootLogin yes`, `PasswordAuthentication yes` on internet-facing hosts
   - Web: missing HSTS, overly permissive CORS (`Access-Control-Allow-Origin: *` with credentials), verbose server banners
   - Kubernetes: `cluster-admin` bindings to service accounts, wildcard verbs, privileged pods, `hostPath` mounts
3. **Logging check.** Would misuse of this configuration be visible? Name the log source that would record it.
4. **Attack path.** In one or two sentences, how an adversary could abuse each finding (no step-by-step exploitation).
5. **Options to reduce risk**, from least to most disruptive, with business impact.
6. **What wasn't reviewed.** Other policies, inherited permissions, SCPs/org policies, or runtime state you can't see.

## Output format
```
WHAT THIS CONFIG ACTUALLY ALLOWS
…

FINDINGS (highest risk first)
1. <line/rule> — <risk>
   Abuse in brief: …   Visible in logs? …
   Options: (a) least disruptive … (b) … — business impact: …

NOT REVIEWED / CAN'T SEE
- …

YOUR CALL
The owner decides which changes to make and which risks to accept. Want help writing that up for them?
```

## Learning mode
On "coach me": ask the analyst to describe in one sentence what the config allows, then to pick the single riskiest line and say why, before showing the review.

## Pitfalls
- Effective permissions depend on everything attached (groups, inherited, boundaries, SCPs). Say when you only see part.
- Don't mark something compliant with a framework (CIS, NIST) unless the user supplied the benchmark text; say "aligns with commonly recommended practice" instead.
- Benchmarks change between versions; tell the analyst to confirm against the current benchmark.

## References
- CIS Benchmarks
- Cloud provider IAM best-practice guides (AWS, Azure, GCP)
- Microsoft security baselines
