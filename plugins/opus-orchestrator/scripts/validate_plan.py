#!/usr/bin/env python3
"""Validate an Opus Orchestrator task plan (read-only, standard library)."""
import argparse
import json
import posixpath
import sys
from pathlib import Path

AGENTS = {
    'scout', 'architect', 'implementer', 'frontend-engineer', 'backend-engineer',
    'test-engineer', 'code-reviewer', 'security-reviewer', 'docs-writer'
}
RISKS = {'low', 'medium', 'high'}


def check_path(value):
    if not isinstance(value, str) or not value.strip():
        return False
    if '\\' in value or value.startswith('/') or value.startswith('~'):
        return False
    parts = value.rstrip('/').split('/')
    if any(part in ('', '.', '..') for part in parts):
        return False
    if any(c in value for c in '*?[]'):
        return False
    return posixpath.normpath(value.rstrip('/')) != '.'


def overlaps(left, right):
    if left == right:
        return True
    if left.endswith('/') and right.startswith(left):
        return True
    if right.endswith('/') and left.startswith(right):
        return True
    return False


def validate_plan(plan):
    errors = []
    if not isinstance(plan, dict):
        return ['Top-level plan must be an object.']
    if not isinstance(plan.get('goal'), str) or not plan['goal'].strip():
        errors.append('goal must be a non-empty string.')
    tasks = plan.get('tasks')
    if not isinstance(tasks, list) or not tasks:
        return errors + ['tasks must be a non-empty list.']
    ids = {}
    for i, task in enumerate(tasks):
        prefix = f'tasks[{i}]'
        if not isinstance(task, dict):
            errors.append(f'{prefix} must be an object.')
            continue
        tid = task.get('id')
        if not isinstance(tid, str) or not tid.strip():
            errors.append(f'{prefix}.id must be a non-empty string.')
        elif tid in ids:
            errors.append(f'{prefix}.id duplicate: {tid}')
        else:
            ids[tid] = task
        for field in ('title',):
            if not isinstance(task.get(field), str) or not task[field].strip():
                errors.append(f'{prefix}.{field} must be a non-empty string.')
        if not isinstance(task.get('agent'), str) or task.get('agent') not in AGENTS:
            errors.append(f'{prefix}.agent must be one of known agent roles.')
        for field in ('depends_on', 'files_owned'):
            if not isinstance(task.get(field), list):
                errors.append(f'{prefix}.{field} must be a list.')
        for field in ('acceptance_criteria', 'verification'):
            value = task.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(x, str) and x.strip() for x in value):
                errors.append(f'{prefix}.{field} must be a nonempty list of strings.')
        if not isinstance(task.get('risk'), str) or task.get('risk') not in RISKS:
            errors.append(f'{prefix}.risk must be low, medium, or high.')
        if not isinstance(task.get('approval_required'), bool):
            errors.append(f'{prefix}.approval_required must be boolean.')
        if task.get('risk') == 'high' and task.get('approval_required') is not True:
            errors.append(f'{prefix} high-risk task must require approval.')
        group = task.get('parallel_group')
        if group is not None and (not isinstance(group, str) or not group.strip()):
            errors.append(f'{prefix}.parallel_group must be nonempty string or null.')
        for f in (task.get('files_owned') if isinstance(task.get('files_owned'), list) else []):
            if not check_path(f):
                errors.append(f'{prefix}.files_owned invalid path: {f!r}')
        for dep in (task.get('depends_on') if isinstance(task.get('depends_on'), list) else []):
            if not isinstance(dep, str) or not dep.strip():
                errors.append(f'{prefix}.depends_on must contain task ids.')
    for tid, task in ids.items():
        for dep in (task.get('depends_on') if isinstance(task.get('depends_on'), list) else []):
            if not isinstance(dep, str) or dep not in ids:
                errors.append(f'{tid}: missing dependency {dep!r}')
            elif dep == tid:
                errors.append(f'{tid}: cannot depend on itself.')
            elif task.get('parallel_group') is not None and ids[dep].get('parallel_group') == task.get('parallel_group'):
                errors.append(f'{tid}: dependency {dep} is in the same parallel group.')
    colors = {}

    def visit(tid, trail):
        state = colors.get(tid, 0)
        if state == 1:
            errors.append('Dependency cycle: ' + ' -> '.join(trail + [tid]))
            return
        if state == 2:
            return
        colors[tid] = 1
        for dep in (ids[tid].get('depends_on') if isinstance(ids[tid].get('depends_on'), list) else []):
            if isinstance(dep, str) and dep in ids and dep != tid:
                visit(dep, trail + [tid])
        colors[tid] = 2

    for tid in ids:
        if colors.get(tid, 0) == 0:
            visit(tid, [])
    by_group = {}
    for tid, task in ids.items():
        group = task.get('parallel_group')
        if isinstance(group, str) and group.strip():
            by_group.setdefault(group, []).append((tid, task))
    for group, entries in by_group.items():
        for i, (id_a, a) in enumerate(entries):
            for id_b, b in entries[i + 1:]:
                for path_a in (a.get('files_owned') if isinstance(a.get('files_owned'), list) else []):
                    for path_b in (b.get('files_owned') if isinstance(b.get('files_owned'), list) else []):
                        if isinstance(path_a, str) and isinstance(path_b, str) and overlaps(path_a, path_b):
                            errors.append(f'parallel group {group}: {id_a} ({path_a}) overlaps {id_b} ({path_b})')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path, help='JSON task plan path')
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        print(f'INVALID: unable to read plan: {exc}', file=sys.stderr)
        return 2
    problems = validate_plan(plan)
    if problems:
        print(f'INVALID: {len(problems)} problem(s)')
        for problem in problems:
            print('- ' + problem)
        return 1
    print(f'VALID: {len(plan["tasks"])} tasks, dependency and parallel ownership checks passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
