# Contributing to claude-blue

Thank you for helping defenders. Contributions are welcome from practitioners at every level.

## What we're looking for

Skills that help a defender **understand, review or improve** their own work. Focused, single-task skills are preferred over broad overviews.

## Requirements for every skill

1. **Follow [PRINCIPLES.md](PRINCIPLES.md).** In particular:
   - A "Human authority" section saying what Claude does and does not do.
   - Output that ends by handing the decision back to the user ("YOUR CALL").
   - No autonomous destructive actions; containment suggestions are options with impact and rollback.
   - A data-handling reminder where personal data or secrets are likely.
   - A learning mode.
2. **Use [templates/SKILL_TEMPLATE.md](templates/SKILL_TEMPLATE.md)** and the `defensive-` name prefix.
3. **Accuracy.** Every event ID, field name, operator behaviour or protocol detail should be checkable against vendor documentation or a standard. Prefer "verify in your version" over a confident guess.
4. **Pitfalls section** covering where models and people commonly go wrong on the task.
5. **No offensive tradecraft.** Explain attacks only as far as a defender needs to recognise and reason about them.

## Automated checks

Run the validator before opening a PR (it also runs on every PR in CI):

```bash
pip install pyyaml
python tools/validate.py
```

It fails the build when a skill is missing frontmatter, its name doesn't match its folder or the `defensive-` convention, its category doesn't match its folder, it lacks `human_role`, a "Human authority" section that says what Claude does not do, a "Learning mode", "Pitfalls", or a "YOUR CALL" hand-back, or when it isn't listed in the README index. Add `--strict` to treat warnings as errors.

### Reference files

Long lookup tables (event IDs, code lists) go in a `references/` folder inside the skill and are linked from `SKILL.md`, so Claude reads them only when needed. Each skill must be self-contained, because only the skill's own folder is installed.

`tools/references/` holds the master copy of each reference table. To change one, edit the master copy, then run `python tools/validate.py --sync-references` to copy it into every skill that uses it. CI fails if a skill's copy has drifted from the master. When adding a reference table, put the master in `tools/references/` and a copy in the skill's `references/` folder.

Frontmatter must use only keys portable to claude.ai uploads (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) and plain-string metadata values.

## Review checklist (for maintainers)

The validator checks structure. Humans check substance:

- [ ] Human authority section is specific to this task, not boilerplate
- [ ] The skill never issues a verdict or takes an action, even in its examples
- [ ] Technical claims verified against vendor documentation or standards
- [ ] No invented sources
- [ ] README badge count updated

## Testing a skill

Before opening a PR, try the skill on at least three prompts:
1. A normal request it should handle well.
2. A request for a verdict ("just tell me if it's malicious"). It should give evidence for and against and hand back the decision.
3. An input with missing information. It should say what's missing rather than fill the gap.

Include the prompts and a short note on the results in your PR.
