# Example invocation prompts

## New feature (existing repository)

```text
/opus-orchestrator:orchestrate Add organization-level invite emails to this app. Inspect the current authentication flow, propose a minimal plan, assign non-overlapping files, add regression tests, and have another agent review permissions.
```

## Mobile UI

```text
/opus-orchestrator:orchestrate Implement the account settings screen based on existing components. Keep navigation consistent, test empty and error states, and review accessibility. Do not change the design system.
```

## Bugfix

```text
/opus-orchestrator:orchestrate This endpoint sometimes returns duplicate records. Find the root cause, patch it without breaking existing callers, test it, and review the resulting diff.
```

## Planning first

```text
/opus-orchestrator:orchestrate Plan a safe migration from REST to GraphQL. No code changes until I approve the design. Include dependencies, breaking changes, rollback and cost.
```

## Example report (illustrative, not a real run)

```text
Goal: Add pagination to invoices endpoint
Status: IMPLEMENTED IN BRANCH (example)
Agents run: scout, backend-engineer, test-engineer, code-reviewer
Changed paths: src/api/invoices.ts, tests/invoices.test.ts
Verification: npm test -- invoices.test.ts -> PASS (example)
Review: 1 missing input validation check found and fixed (example)
Limitations: full integration suite NOT RUN (example)
Next step: request approval before push
```

Reports from a real run must cite *its actual* commands, errors and files. Do not reuse sample claims as if a task executed.
