# Delegation modes

## Default: subagents

- Best for focused bounded tasks. Each worker returns to the Opus lead.
- Choose one or two agents for small features; roughly 2-4 active agents for complex tasks, only if independent work exists.
- Keep file writers isolated and read-only reviewers parallel.

## Optional: Agent Teams (experimental)

Enable only by explicit user choice in their own Claude Code environment:

```
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude --model opus
```

Use when teammates need to exchange findings and challenge each other independently. Avoid for tasks with heavy shared-file edits or strict sequential dependencies. The feature consumes more tokens; do not assume it is enabled merely because an instruction mentions it.

With Agent Teams enabled, use stable teammate names and make each participant's exclusive path ownership explicit. If unsupported/unavailable, fall back to subagents without pretending a team was launched.

## Model routing

- Lead: user-selected Opus model via `claude --model opus`.
- Workers: generally Sonnet for implementation and testing, Haiku for lightweight exploration/docs.
- Escalate architecture/security tradeoffs to the Opus lead.
- Agent definitions express preferred models; environment, availability, and user model settings can override them. Report substitutions if they materially affect decisions.
