#!/usr/bin/env python3
"""Read-only consistency checks for the public Claude Code plugin repository."""
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit('Install PyYAML first: python3 -m pip install -r requirements-dev.txt')

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/opus-orchestrator'
SKILL = PLUGIN / 'skills/orchestrate/SKILL.md'
AGENTS = PLUGIN / 'agents'
STANDALONE = ROOT / 'standalone/opus-orchestrator'


def fm(path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError(f'Missing frontmatter in {path.relative_to(ROOT)}')
    raw = text.split('\n---\n', 1)[0][4:]
    meta = yaml.safe_load(raw)
    if not isinstance(meta, dict):
        raise ValueError(f'Invalid metadata in {path.relative_to(ROOT)}')
    return meta


def check():
    faults = []
    try:
        market = json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
        manifest = json.loads((PLUGIN/'.claude-plugin/plugin.json').read_text())
        entries = market.get('plugins', [])
        assert market['name'] == 'opus-tools'
        assert isinstance(market['owner']['name'], str)
        assert len(entries) == 1
        assert entries[0]['name'] == manifest['name'] == 'opus-orchestrator'
        assert entries[0]['source'] == './plugins/opus-orchestrator'
        assert (ROOT/entries[0]['source']).is_dir()
        assert re.fullmatch(r'\d+\.\d+\.\d+', manifest['version'])
        assert manifest.get('author', {}).get('name')
    except (OSError, KeyError, ValueError, TypeError, AssertionError) as exc:
        faults.append(f'Marketplace/plugin manifest: {exc}')
    try:
        skillmeta = fm(SKILL)
        assert skillmeta['name'] == 'orchestrate'
        assert skillmeta.get('disable-model-invocation') is True
        assert skillmeta.get('description')
    except (OSError, KeyError, ValueError, AssertionError) as exc:
        faults.append(f'Plugin skill: {exc}')
    names = set()
    for agentfile in sorted(AGENTS.glob('*.md')):
        try:
            meta = fm(agentfile)
            assert meta['name'] == agentfile.stem
            assert meta['name'] not in names
            names.add(meta['name'])
            assert meta.get('description')
            assert meta.get('model') in ('sonnet', 'haiku')
            tools = {t.strip() for t in meta.get('tools','').split(',')}
            assert {'Read', 'Grep', 'Glob'}.issubset(tools)
            if meta['name'] in {'scout','architect','code-reviewer','security-reviewer'}:
                assert not tools.intersection({'Edit','Write'})
        except (OSError, ValueError, KeyError, AssertionError) as exc:
            faults.append(f'{agentfile.name}: {exc}')
    if len(names) != 9:
        faults.append(f'Expected 9 agents; found {len(names)}.')
    try:
        smeta = fm(STANDALONE/'SKILL.md')
        assert set(smeta) == {'name','description'}, 'Standalone frontmatter must contain only name/description.'
        assert smeta['name'] == 'opus-orchestrator'
        assert (STANDALONE/'agents/openai.yaml').exists()
        assert len(list((STANDALONE/'references').glob('*.md'))) == 4
        assert (STANDALONE/'scripts/validate_plan.py').exists()
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        faults.append(f'Standalone skill: {exc}')
    for p in ROOT.rglob('*.md'):
        if any(part in ('.git', '__pycache__') for part in p.parts):
            continue
        content = p.read_text(encoding='utf-8')
        if '[TODO:' in content:
            faults.append(f'Unfinished placeholder in {p.relative_to(ROOT)}')
        if any(word in content.lower() for word in ['motiora','proentegre','yerinde teknoloji']):
            faults.append(f'Private project reference in {p.relative_to(ROOT)}')
    sample = PLUGIN/'examples/plan.example.json'
    result = subprocess.run([sys.executable, str(PLUGIN/'scripts/validate_plan.py'), str(sample)], capture_output=True, text=True)
    if result.returncode:
        faults.append('Example plan failed validation: '+result.stdout+result.stderr)
    return faults


if __name__ == '__main__':
    failures = check()
    if failures:
        print('REPO INVALID:')
        for f in failures:
            print(' - '+f)
        sys.exit(1)
    print('REPO VALID: JSON manifests, skill, 9 agents, references, sample plan, and privacy checks passed.')
