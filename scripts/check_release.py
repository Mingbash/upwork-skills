#!/usr/bin/env python3
"""Validate candidate layout, self-contained links, metadata and shared copies."""
from pathlib import Path
import argparse, ast, json, re

ROOT = Path(__file__).resolve().parents[1]

def check_skill(skill):
    errors=[]
    text=(skill/'SKILL.md').read_text()
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        return [f'{skill.name}: invalid frontmatter']
    fm=text.split('---',2)[1]
    fields=dict(re.findall(r'^([a-z][a-z_-]*):\s*(.+)$',fm,re.M))
    if fields.get('name')!=skill.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',skill.name):
        errors.append(f'{skill.name}: invalid name')
    if not 1<=len(fields.get('description',''))<=1024:errors.append(f'{skill.name}: invalid description')
    for p in skill.rglob('*.md'):
        for ref in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if ref.startswith(('https://','http://','#','mailto:')):continue
            dest=(p.parent/ref.split('#')[0]).resolve()
            if not dest.is_relative_to(skill.resolve()) or not dest.exists():
                errors.append(f'{p.relative_to(skill)}: non-contained or missing reference {ref}')
    for p in skill.rglob('*.py'):
        try:ast.parse(p.read_text())
        except SyntaxError as e:errors.append(f'{p.name}: {e}')
    for p in skill.rglob('*.json'):
        try:json.loads(p.read_text())
        except ValueError as e:errors.append(f'{p.name}: {e}')
    return errors

def check(root=ROOT):
    errors=[]
    skills=list((root/'skills').iterdir())
    for p in skills:errors+=check_skill(p)
    for p in root.rglob('*.md'):
        if any(x in p.parts for x in ('.git','build','__pycache__')):continue
        for ref in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if ref.startswith(('https://','http://','#','mailto:')):continue
            dest=(p.parent/ref.split('#')[0]).resolve()
            if not dest.is_relative_to(root.resolve()) or not dest.exists():errors.append(f'{p.relative_to(root)}: bad link {ref}')
    mapping={'workspace.md':'references/workspace.md','options.md':'references/options.md','options.json':'assets/options.json'}
    if (root/'shared').exists():
        for source,target in mapping.items():
            for skill in skills:
                if (root/'shared'/source).read_bytes()!=(skill/target).read_bytes():errors.append(f'{skill.name}: shared drift {source}')
    # Scan only distributable text; never include private evaluation material.
    forbidden=['/'+'Users/', 'Project'+' X', 'Lead'+'Through', 'sk-'+'proj-','BEGIN '+'PRIVATE KEY','private-'+'audit/']
    for p in root.rglob('*'):
        if not p.is_file() or any(x in p.parts for x in ('.git','build','__pycache__')):continue
        try:text=p.read_text()
        except UnicodeError:errors.append(f'{p.relative_to(root)}: unexpected binary');continue
        for token in forbidden:
            if token in text:errors.append(f'{p.relative_to(root)}: private-content marker')
    return errors

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--public',action='store_true');args=parser.parse_args()
    errors=check()
    if args.public and 'PENDING CONFIRMATION' in (ROOT/'LICENSE').read_text():errors.append('Public release requires a confirmed copyright holder')
    for error in errors:print('FAIL:',error)
    if not errors:print('PASS: links, metadata, Python/JSON syntax, standalone containment, shared contracts and privacy markers')
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())
