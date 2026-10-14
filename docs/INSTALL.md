# Installation and publication

## Development test without GitHub

```bash
cd opus-orchestrator
claude plugin validate ./plugins/opus-orchestrator
claude plugin validate .
cd /path/to/target-repository
claude --model opus --plugin-dir /absolute/path/to/opus-orchestrator/plugins/opus-orchestrator
```

Inside Claude Code run `/opus-orchestrator:orchestrate Audit the existing checkout flow, identify a small fix, implement it and verify tests.` Confirm that the plugin skill and namespaced agents are visible. The external project is a **test target**; this repository itself is the plugin package, not a sample SaaS application.

## Publish to GitHub

1. Check repository content, license, author attribution and no secrets.
2. Create an empty public repository named `opus-orchestrator` in your own GitHub account (or use `gh`).
3. From this folder, initialize and publish:

```bash
git init
git add .
git commit -m "feat: initial opus orchestrator plugin"
git branch -M main
gh repo create opus-orchestrator --public --source=. --remote=origin --push
```

If `gh` is not available, create the public repo in the GitHub web UI, then add its URL as `origin` and push `main`. You must authenticate GitHub yourself. These commands are intended to be run by the repository owner, not automatically by the skill.

## Install from the published marketplace

```bash
claude plugin marketplace add YOUR_GITHUB_USERNAME/opus-orchestrator
claude plugin install opus-orchestrator@opus-tools
```

If the plugin does not appear after installation, restart the Claude Code session or reload plugins via `/plugin`. Follow the [Claude Code marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces) for changes to the CLI commands.

## Standalone skill variant

A separate distributable `skill.zip` contains one `opus-orchestrator/SKILL.md` and supporting references/scripts. To use it without the plugin, extract the `opus-orchestrator/` directory into:

```text
~/.claude/skills/opus-orchestrator/
```

Run `/opus-orchestrator` in Claude Code. The standalone skill intentionally has **no installed specialist agent files**, so it uses available built-in agents/general-purpose workers as a fallback. For all nine named specialists, install the full plugin instead. Do not install both unless you intentionally want both commands available.

## Manual release checklist

- Run Python tests and the authoritative `claude plugin validate` commands.
- Try a small read-only delegation and a bounded one-file code change in a disposable test repository.
- Verify reviewers are actually read-only, and the user receives an honest test report.
- Test a plan with two writers trying to edit the same file: the plan checker must reject it.
- Validate GitHub marketplace install from a fresh user machine/clean Claude Code configuration.
- Tag the release and update changelog only after runtime smoke tests.
