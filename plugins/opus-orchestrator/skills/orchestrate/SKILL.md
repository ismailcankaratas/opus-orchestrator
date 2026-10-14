---
name: orchestrate
description: Plan and implement a software task using an Opus-led team of specialist Claude Code agents, with task ownership, testing, independent review, and explicit risk gates.
disable-model-invocation: true
argument-hint: "goal, issue, or feature request"
---


# Opus Orchestrator

Run a software-delivery workflow led by the **main Claude Code session**. The user request is:

> $ARGUMENTS

If there are no arguments, ask for a concrete goal or existing issue. Do not invent a product brief.

## Operating contract

- The **lead/orchestrator stays in the main conversation**. Start the session with `claude --model opus` to select Opus; a skill does not force a model switch. If the lead is not Opus, disclose this and offer to switch before undertaking a substantial run.
- Treat the user's current repository instructions (`CLAUDE.md`, project conventions, existing tests) as project context. This skill does not replace them.
- Use Claude Code's built-in agent delegation when available. A full plugin installation provides specialist subagents. A standalone skill may fall back to built-in Explore/Plan and general-purpose workers; report when named specialists are unavailable.
- Keep the default path **subagent-based**. Use experimental Agent Teams only when enabled by the user and when independent peers would materially help. Never claim a team was started unless one actually started.
- Scale effort to the change. For a tiny fix, use the smallest safe plan; do not summon every agent. For complex work, recruit only required specialties (normally 2-4 active agents).
- Do not auto-enable experimental flags, change permission settings, bypass approvals, or spend tokens on idle agents.

## Delivery protocol

### 1. Discover and clarify

- Inspect repository state, branch, status, language, framework, scripts, tests, and applicable `CLAUDE.md`. Do not overwrite unrelated user changes.
- Restate the objective, explicit constraints, acceptance criteria, test approach, out-of-scope items, and risks. Ask only blocking questions; otherwise state assumptions.
- Classify risk. Gate destructive operations, publishing/deployment, schema/data migrations, secret handling, major dependency upgrades, billing/cloud changes, and force-pushes behind explicit user approval.

### 2. Plan and assign ownership

- For a medium or large task, construct a task DAG with IDs, dependencies, owners, touched paths, acceptance criteria, and verification commands. Give each task one accountable agent.
- Define an **exclusive file or directory ownership boundary** for every simultaneous writer. Never assign the same file (or an overlapping directory) to multiple concurrent writers. Read-only reviewers may inspect any file.
- Use an independent scout for uncertain facts, a design/architecture review for consequential tradeoffs, implementers for code, a tester for evidence, and independent reviewers for verification.
- If writing a plan file, follow `references/plan-format.md`. The optional `validate_plan.py` helper rejects dependency cycles and overlapping ownership in a parallel group; use it when the helper exists and a file is available. The helper reads a plan; it never spawns agents or writes code.
- Present a concise plan and ask approval when the user requested planning first or the operation is risky. Otherwise start a small, reversible implementation slice.

### 3. Delegate with precise contracts

Send each worker a bounded task with:

1. Objective and repository facts, not just "handle frontend".
2. Allowed files/directories; files they must not modify.
3. Dependencies and expected interfaces.
4. Acceptance criteria, tests to run, and a completion report format.
5. Instruction to stop and report a blocker rather than changing unrelated code.

Invoke the actual Claude Code agent tool or team mechanism supported in the running environment. Natural-language instructions alone are **not** evidence that an agent was launched. A worker's response is an input to review, not authorization for external actions.

### 4. Implement and integrate

- Ensure dependencies are resolved before downstream tasks start.
- Independent tasks may run in parallel; dependent or overlapping edits run sequentially. Use isolated worktrees/branches when practical and review integration before merge.
- Prefer incremental changes and visible progress over a single giant patch. Preserve existing public APIs unless a change is approved.
- The lead owns cross-cutting architecture decisions and integration. Reconcile conflicting conclusions using evidence from the code and tests, not agent voting.

### 5. Test, challenge, and repair

- Have the test specialist run relevant existing tests and add focused regression tests when the scope requires it.
- Have the lead capture the actual diff and relevant changes, then provide them to an **independent** read-only code reviewer. Add a security reviewer for auth, secrets, file I/O, payments, multi-tenant boundaries, dependency changes, or other security-sensitive behavior.
- Triage each finding with file/line evidence. Delegate fixes or resolve them, rerun the appropriate tests, and review the resulting diff.
- Never fabricate green tests. Distinguish PASS, FAIL, and NOT RUN; include commands and relevant outputs. Do not claim runtime execution when only static checks were performed.

### 6. Deliver a truthful handoff

Report in the same language the user is using unless instructed otherwise:

- Delivered scope and key changed paths.
- Agents actually invoked and their contributions (not just proposed roles).
- Test commands with outcomes, remaining issues, and risks.
- Any user approvals still required and the next suggested slice.

Do not deploy, publish, commit, open a PR, overwrite production data, or push without user permission. Do not announce "production-ready" without evidence.

## References (open on demand)

- `references/plan-format.md`: task DAG schema and optional plan validator.
- `references/agent-contracts.md`: delegation prompts and review handoff.
- `references/quality-gates.md`: tests, privacy, security, and release approval.
- `references/modes.md`: when to use subagents vs experimental Agent Teams.
