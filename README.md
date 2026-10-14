# Opus Orchestrator

**An open-source Claude Code workflow for building software with an Opus lead and specialist agents.**

Plan a task, delegate bounded implementation work, integrate changes, run actual tests, request independent reviews, and deliver a verifiable handoff. Works with existing repositories across programming languages; not tied to any application or framework.

> Community-built and not affiliated with, endorsed by, or maintained by Anthropic. Claude, Claude Code, and Opus are names used to describe compatible tools/models. You need your own Claude Code access.

## What it does

| Phase | Responsibility |
| --- | --- |
| Discover | Inspect repo conventions, existing work, constraints, and test setup |
| Plan | Convert the request into a dependency-aware DAG with exclusive writer ownership |
| Delegate | Assign scoped tasks to Sonnet/Haiku specialists as warranted |
| Implement | Apply minimal compatible patches and integrate in dependency order |
| Verify | Run test commands and use independent code/security review |
| Report | Distinguish completed changes from proposals, missing tests, and risks |

```
                   Claude Code (Opus lead)
                            |
          Discover -> Plan -> Assign -> Integrate
                      /     |      \
            Specialist   Specialist   Reviewer
            (Sonnet)     (Sonnet)     (Sonnet)
                      \     |      /
                     Real test evidence
                            |
                     User handoff / approval
```

**Principles:** agents are real Claude Code subagents, not fictional job titles. A successful agent response is not a passing test. Never allow concurrent writers to own the same file. External and destructive actions require user approval. Use fewer agents when they do not improve the task.

## Quick start (local, before publishing)

Prerequisite: Claude Code CLI installed and authenticated, plus an account/model that can run Opus and your chosen subagent models.

```bash
# From the root of THIS repository:
claude plugin validate ./plugins/opus-orchestrator
claude plugin validate .

# Open a project to be edited and load the local plugin folder:
cd /path/to/your-application
claude --model opus --plugin-dir /path/to/opus-orchestrator/plugins/opus-orchestrator
```

Inside Claude Code, type:

```text
/opus-orchestrator:orchestrate Build an authentication settings page in this repository. Respect existing APIs, add tests, and request independent review.
```

For a small issue:

```text
/opus-orchestrator:orchestrate Fix the flaky pagination test. Investigate root cause, implement a minimal fix, and rerun the relevant tests.
```

The skill is **explicitly user-invoked** and does not silently orchestrate every coding request. The main session's model is selected by `claude --model opus`; the plugin does not force a model switch.

## Install from GitHub

Substitute your actual GitHub account or organization for `YOUR_GITHUB_USERNAME`:

```bash
claude plugin marketplace add YOUR_GITHUB_USERNAME/opus-orchestrator
claude plugin install opus-orchestrator@opus-tools
```

Then, **inside the project you want to work on**, start a Claude Code session with `claude --model opus` and run `/opus-orchestrator:orchestrate ...`.

To update installed plugins later, use the plugin manager in Claude Code. Check the [official plugin installation docs](https://code.claude.com/docs/en/discover-plugins) for up-to-date instructions.

## What's included

```text
.claude-plugin/marketplace.json        # public marketplace catalog
plugins/opus-orchestrator/
  .claude-plugin/plugin.json           # Claude Code plugin manifest
  skills/orchestrate/SKILL.md          # user-triggered orchestration entrypoint
  skills/orchestrate/references/       # plans, delegation, quality, modes
  agents/                              # 9 bounded specialist agents
  scripts/validate_plan.py             # optional read-only JSON plan checker
  examples/plan.example.json
standalone/opus-orchestrator/          # separately installable Skill directory
scripts/validate_repo.py              # static package checks
.github/workflows/validate.yml        # CI
```

### Agent roster

- `scout` (Haiku): read-only repo research
- `architect` (Sonnet): read-only design alternatives
- `implementer` (Sonnet): bounded cross-stack coding
- `frontend-engineer` (Sonnet): UI/UX implementation
- `backend-engineer` (Sonnet): API and database tasks
- `test-engineer` (Sonnet): test authoring and execution
- `code-reviewer` (Sonnet): independent read-only review
- `security-reviewer` (Sonnet): read-only security assessment
- `docs-writer` (Haiku): documentation updates in owned paths

The orchestrator uses a **subset**, based on each task. Workers use aliases rather than pinned release IDs to reduce churn; the running Claude Code configuration and model availability may override preferences.

## Optional Agent Teams

Subagents are the default and do not require experimental features. For collaborative agent sessions that communicate directly, **opt in explicitly**:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude --model opus
```

Teams may improve independent research and reviews but increase token usage and can cause file conflicts in tightly coupled code. The skill prefers subagents unless there is a clear reason to form a team. See [modes](plugins/opus-orchestrator/skills/orchestrate/references/modes.md) and [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams).

## Plan checker

Optional dependency and writer-ownership checker:

```bash
python3 plugins/opus-orchestrator/scripts/validate_plan.py plugins/opus-orchestrator/examples/plan.example.json
```

It checks missing dependencies, cycles, malformed task contracts, risk gates, and overlapping file ownership **within a parallel group**. It does not execute tasks or guarantee that the code is correct. See [plan format](plugins/opus-orchestrator/skills/orchestrate/references/plan-format.md).

## Testing and validation

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 scripts/validate_repo.py

# Authoritative Claude Code plugin validation (requires Claude Code CLI):
claude plugin validate ./plugins/opus-orchestrator
claude plugin validate .
```

The Python checks validate package structure, declarations, sample plan, and overlap/cycle cases. **They are not a live Claude Code multi-agent integration test.** Complete that smoke test locally before declaring a new release ready.

## Security and operational limits

This plugin intentionally ships **no MCP connections, telemetry, automatic shell hooks, permission bypasses, or credentials**. It relies on Claude Code's ordinary tool permission flow. It does not auto-push, auto-deploy, run destructive migrations, or declare test success without evidence. Review third-party plugins before installing them.

Read [SECURITY.md](SECURITY.md) and [documentation](docs/) before using it against production repositories.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local testing, PR requirements, and agent prompt changes. MIT licensed; see [LICENSE](LICENSE).
