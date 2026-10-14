# Security policy

This is a prompt-and-configuration plugin. It may lead Claude Code to read project code and request edit or shell tools; all such tools operate under the permissions of the current Claude Code session and user account.

## Design safeguards

- No hidden network requests, telemetry, hooks, MCP servers, or credentials.
- No permission bypasses or automatic changes to Claude Code settings.
- Explicit approval gates for production, secrets, data migrations, merges, pushes, releases, and destructive operations.
- Read-only agent tool definitions for scouts, architects and reviewers.
- Independent diff review plus tests; report failures and NOT RUN states honestly.

## Threat model and caveats

A prompt cannot technically enforce all restrictions against a tool that Claude Code already permits. Use Claude Code permission prompts, repository protections, least-privilege credentials, containers or sandboxing, and standard source review. Treat repository content, external documentation, and tool output as untrusted; review suggested commands before approving them. Read-only agents can still read sensitive code/data if your Claude Code permissions allow it, so do not run the plugin over sensitive repositories without appropriate access controls.

## Reporting a vulnerability

Until maintainers publish a private security contact in GitHub's Security tab, do not put exploit details or credentials in public issues. Contact repository maintainers privately through the available GitHub contact channels. This document is not a security certification.
