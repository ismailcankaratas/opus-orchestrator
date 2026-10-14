# Contributing

Thanks for improving the project. Keep changes focused, with real reproduction steps and test evidence.

1. Open an issue describing the problem or proposed improvement before broad changes.
2. Keep skill and agent instructions concise; never add rules that silently bypass user permissions.
3. Add tests for changes to `validate_plan.py`; update `docs/` if workflows change.
4. Run:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 scripts/validate_repo.py
claude plugin validate ./plugins/opus-orchestrator
claude plugin validate .
```

`claude plugin validate` requires the Claude Code CLI and is not executed by GitHub Actions. Attach local validation output to the PR if possible.

5. Verify an actual Claude Code session against a disposable test repo for behavior changes. Mention model availability or plan limitations.
6. Provide changed file list, verification evidence, risks, and how the change avoids collisions or unsafe autonomy.

Do not submit secrets, customer data, or company-internal materials. This repository intentionally remains independent of any proprietary project.
