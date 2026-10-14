# Delivery quality gates

## Before implementation

- Understand the target branch and existing dirty changes.
- State the expected user-visible behavior and the no-change invariants.
- Assign exclusive paths to concurrent writers.
- Confirm risk and obtain user approval for destructive or external actions.

## Before claiming success

- Run tests relevant to the changed paths; describe every unavailable test.
- Verify the current diff matches the requested scope and does not contain secrets.
- Ask an independent code reviewer to inspect correctness, security, edge cases, API contracts, and regression risk.
- For security-sensitive code, request targeted adversarial review.
- Check error states and migration/rollback requirements as relevant.
- Verify documentation and minimal handoff instructions.

## Never automate without explicit authorization

- Push, deploy, publish releases, merge PRs, or delete branches.
- Run destructive database operations or modify production data.
- Change credentials, expose secret contents in outputs, or bypass access controls.
- Install or upgrade dependencies that materially alter build/runtime risk without approval.

## Report template

```
Goal:
Completed:
Agents run:
Changed files:
Verification: PASS / FAIL / NOT RUN per command
Review findings addressed:
Known limitations:
Approvals / next step:
```

If any verification was skipped, explain why. An apparently successful subagent report is not evidence that its tests passed.
