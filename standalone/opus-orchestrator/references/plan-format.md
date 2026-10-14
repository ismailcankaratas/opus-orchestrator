# Task plan JSON format

For nontrivial deliveries, optionally save a task plan as JSON in a location the user approves. A plan describes **intent**, not proof of execution.

Required top-level keys: `goal` (string), `tasks` (non-empty array).

Task keys:

- `id`: stable string such as `T01`
- `title`: short descriptive string
- `agent`: `scout`, `architect`, `implementer`, `frontend-engineer`, `backend-engineer`, `test-engineer`, `code-reviewer`, `security-reviewer`, or `docs-writer`
- `depends_on`: list of preceding task IDs
- `files_owned`: list of project-relative file paths or directories ending in `/`; `[]` for read-only tasks
- `acceptance_criteria`: non-empty array of measurable conditions
- `verification`: non-empty array of commands or manual inspection steps
- `parallel_group`: optional group label; tasks in the same group are intended to be executed concurrently
- `risk`: `low`, `medium`, or `high`
- `approval_required`: boolean; must be true for `high` risk tasks

Validation rules: dependencies must exist, have no cycles, and cannot be in the same `parallel_group`; concurrent writers must not claim identical/overlapping paths. Paths must be relative and cannot traverse `..`. A directory owner ends in `/`, e.g. `src/auth/`. Avoid wildcard file ownership; use explicit paths or directory boundaries. Include review and tests as real tasks when relevant.

Call `python3 scripts/validate_plan.py path/to/plan.json` if you are in the source repository, or use the version installed with the plugin or standalone skill. The helper is optional and cannot replace judgment about implicit file ownership.
