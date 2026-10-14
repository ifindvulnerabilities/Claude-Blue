# Changelog

## 0.1.0 — 2026-10-14

Initial release: 18 human-in-the-loop defensive skills across 8 categories.

### Skills
- **SOC (6):** `defensive-command-explainer`, `defensive-log-interpreter`, `defensive-alert-triage-companion`, `defensive-phishing-review`, `defensive-web-attack-log-review`, `defensive-ai-output-check`
- **Detection Engineering (1):** `defensive-detection-rule-review`
- **Incident Response (4):** `defensive-incident-summary-review`, `defensive-timeline-review`, `defensive-playbook-review`, `defensive-post-incident-review`
- **Identity (1):** `defensive-signin-log-interpreter`
- **Cloud (1):** `defensive-cloud-audit-interpreter`
- **Threat Intelligence (1):** `defensive-threat-intel-review`
- **Hardening (2):** `defensive-config-review`, `defensive-pentest-report-review`
- **People (2):** `defensive-security-writing-review`, `defensive-analyst-coach`

### Shared references
- `shared/references/windows-security-events.md` (Windows Security, Sysmon, Kerberos, ADCS and PowerShell event reference)
- `shared/references/attention-patterns.md` (command-line patterns with legitimate uses and ATT&CK mappings)
- Skills carry copies, kept in sync with `python tools/validate.py --sync-shared`

### Tooling
- `tools/validate.py`: enforces PRINCIPLES.md on every skill (human authority, learning mode, pitfalls, YOUR CALL hand-back), plus frontmatter portability, folder and category naming, reference links, shared-copy sync and README consistency
- GitHub Actions workflow running the validator and an installer check on every pull request
- `install.sh` for personal or project installs, all skills or one category
- `.gitattributes` to keep LF line endings when committing from Windows

### Docs
- README, PRINCIPLES.md, RESEARCH.md, CONTRIBUTING.md, skill template, MIT license