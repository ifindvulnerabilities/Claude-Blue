# Research Behind Claude-Blue

This file records the evidence used to choose which skills to build and how they behave. Findings are paraphrased; follow the links for the original work.

## How defenders actually use language models

**Field study of a live SOC (Singh et al., 2025).** Researchers analysed 3,090 GPT-4 queries from 45 analysts at an MDR provider over 10 months.
- Command-line understanding was the largest task (31% of queries), followed by text generation and editing (22%) and code/script/regex analysis (11%). Other recurring tasks: tool understanding, file and malware questions, threat intel, query writing, network and IP questions, access control, and email-rule analysis.
- Only about 4% of queries asked for a malicious/benign judgement. Analysts sought explanation and context and kept decision authority.
- Most conversations were two or three turns, used as quick aids between investigative steps.
- The authors recommend surfacing evidence rather than recommendations, and embedding just-in-time explanations into analyst workflows.
- https://arxiv.org/abs/2508.18947

**Incident summarisation (Kramer et al., SOUPS 2025, Google).** 18 analysts, 50 real incidents.
- Autonomous LLM summaries omitted critical details in 35% of cases and introduced factual inaccuracies in 42%.
- Collaborative use reduced analyst effort and improved readability and consistency.
- https://www.usenix.org/conference/soups2025/presentation/kramer

**Practitioner discussions (SOUPS 2026, Arizona State University).** Incident response and investigation support was the most common use case discussed, followed by productivity tasks such as reporting. General-purpose LLMs were mostly discussed for analyst-driven tasks that allow control and easy verification.
- https://sefcom.asu.edu/publications/LLM-SOC-soups2026.pdf

**Threat intelligence mapping.** Studies comparing LLMs on mapping CTI reports to ATT&CK found real potential but also technique confusion and context loss, supporting a "candidate mapping, analyst verifies" design.
- https://arxiv.org/abs/2505.03147
- https://repository.utm.md/handle/5014/35310

**Adoption without structure (SANS 2025 SOC Survey).** 40% of SOCs use AI/ML tools without making them a defined part of operations, and 42% use them out of the box with no customisation.
- https://www.elastic.co/resources/security/report/2025-state-of-the-soc-survey

## Risks to the people doing the work

**Skill erosion and over-reliance (Swimlane survey of 500 security staff).**
- About a quarter said AI had limited their ability to develop security skills.
- Analyst over-reliance on AI recommendations was the most-cited risk of expanding AI.
- Respondents expected a steeper path into the profession and new roles focused on AI oversight and validation.
- https://infosecurity-magazine.com/news/ai-boosts-soc-analyst-capacity

**Gartner** (2025) has warned that complete end-to-end SOC automation is not achievable and that GenAI can become an excuse for deskilling.
- https://securitymea.com/2025/01/27/security-skills-gap-to-leave-one-third-of-senior-roles-vacant-by-2028/

## Moral framework

- *Antiqua et Nova* (Dicastery for the Doctrine of the Faith and Dicastery for Culture and Education, January 2025): AI should complement, not replace, human intelligence; technology should not progressively replace human labour.
  https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_ddf_doc_20250128_antiqua-et-nova_en.html
- *Magnifica Humanitas* (Pope Leo XIV, May 2026): on safeguarding the human person in the time of AI; dignity of work, truth and transparency, clear accountability, education that keeps people asking questions.
  https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html

## From findings to skills

| Finding | Skill |
|---|---|
| Command interpretation is the #1 use | `defensive-command-explainer` |
| Analysts want evidence, not verdicts | `defensive-alert-triage-companion` |
| Telemetry interpretation | `defensive-log-interpreter` |
| Email-rule and phishing questions | `defensive-phishing-review` |
| Regex/query/code checking | `defensive-detection-rule-review` |
| Autonomous summaries omit facts; collaborative ones help | `defensive-incident-summary-review` |
| LLMs miss details over long tasks | `defensive-timeline-review` |
| IR is the most common use case | `defensive-playbook-review`, `defensive-post-incident-review` |
| CTI mapping needs verification | `defensive-threat-intel-review` |
| Defenders review configs written by others | `defensive-config-review` |
| Text editing is the #2 use | `defensive-security-writing-review` |
| Skill erosion and deskilling | `defensive-analyst-coach` |
| Automation bias is the top concern | `defensive-ai-output-check` |
