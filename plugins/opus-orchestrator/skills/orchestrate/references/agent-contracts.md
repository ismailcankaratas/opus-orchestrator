# Delegation contracts

Every worker prompt should follow this compact contract:

```
Role: <specialist agent>
Goal: <concrete outcome>
Repository context: <modules, conventions, links to local files>
Allowed paths: <exclusive list, or read-only>
Do not edit: <paths owned by other tasks>
Dependencies: <what must already exist>
Acceptance: <testable conditions>
Verification: <commands / manual checks>
On blocker: stop, report the problem and lowest-risk options
Return: changed paths, design decisions, test command results, unresolved risks
```

The orchestrator must give filenames and acceptance criteria, not simply role labels.

Code-review agent contract:

```
Inspect the provided actual diff and surrounding code. If the diff is missing, request it from the lead. Stay read-only. Return findings ordered by severity, each with
path:line, concrete failure scenario, and a small suggested fix. Distinguish
observed bugs from speculative risks. State if no material findings were found.
```

Tester contract:

```
Run project-native test commands; if no tests exist, propose and add minimal
focused regression tests only in owned test paths. Report executed command,
exit status, passed/failed/skipped count where available, and failing output.
Do not describe unrun checks as passing.
```

Disagreement: route conflicting recommendations back to the Opus lead; the lead decides after inspecting evidence, and records tradeoffs. No agent can approve permissions on the user's behalf.
