# Orchestration protocol

## 0. Capture intent

Input can be a feature request, bug, issue, or codebase refactor. The lead inspects existing code before designing a new architecture. Every scope change needs a documented reason. The user's repo-specific instructions take precedence over generic suggested conventions.

## 1. Task decomposition

Represent independent work as a dependency graph. For each work item require an owner, exclusive paths, outcomes, and tests. A worker may inspect any source but can only **write** to paths explicitly owned by that worker. The lead or next sequential task handles shared integration paths.

For parallel code modifications, use branches/worktrees or path isolation. If two writers need the same file, make the tasks sequential or give the shared file to the integrator. Read-only researchers/reviewers may operate concurrently without write ownership.

## 2. Model routing and delegation

The Opus lead decides architecture and boundaries; Sonnet workers handle implementation/review and Haiku workers handle narrow research and docs. Do not open nine agents for every task. If no team support exists, use normal subagents; if no custom agent is available, use built-in exploration and a bounded general worker.

Agent teams are an experimental **opt-in** feature, not a requirement. Peer-to-peer communications may improve research and adversarial review, but introduce cost and conflict risk.

## 3. Verification

The worker executes only relevant checks within the permitted boundary. The integrator reruns tests after merging changes and asks an independent reviewer to inspect the complete diff. Capture command/output evidence in the handoff, especially when tests fail or are unavailable.

## 4. Human gates

Get explicit user approval before publishing, deploying, destructive changes, data migration, credential rotation, privilege or permission changes, broad dependency upgrades, or pushing branches/PRs. Delegate analysis freely; delegate external actions only with actual user authorization and tool permissions.

## 5. Failure recovery

On worker failure: report a blocker, preserve partial results, and retry only if the failure is understood. On conflicting architectural recommendations: inspect relevant code and make an explicit decision. On test failure: reproduce, isolate, implement minimal fix, rerun. Never force success through changed assertion expectations that weaken the specification.
