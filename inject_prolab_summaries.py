#!/usr/bin/env python3
"""
inject_prolab_summaries.py
One-off script to backfill ## Summary sections into ProLab READMEs
from the blurb field in prolabs.yml.

After running this, build.py's extract_summary_from_readme() will pick
up summaries natively — the YAML backfill becomes a nice-to-have fallback.

Usage:
  python inject_prolab_summaries.py
  python inject_prolab_summaries.py --dry-run
  python inject_prolab_summaries.py --ctf /path/to/ctf-writeups
  python inject_prolab_summaries.py --yaml /path/to/prolabs.yml
"""

import re
import argparse
from pathlib import Path

import yaml

DEFAULT_CTF      = Path("/home/tate/INKSEC.IO/ctf-writeups")
DEFAULT_YAML     = Path("/home/tate/INKSEC.IO/inkedqt.github.io/_data/prolabs.yml")
PROLABS_REL_PATH = "HTB/ProLabs"


def normalise(name: str) -> str:
    """Strip non-word chars for fuzzy matching."""
    return re.sub(r'[\W_]', '', name.lower())


def has_summary_section(text: str) -> bool:
    return bool(re.search(r'^##\s*(?:📝\s*)?Summary', text, re.MULTILINE | re.IGNORECASE))


def inject_summary(text: str, blurb: str) -> str:
    """
    Insert ## Summary immediately before the first ## section.
    If no ## section exists, append to end of file.
    """
    summary_block = f"## Summary\n{blurb}\n\n---\n"

    # Find the first ## heading (not the # title)
    m = re.search(r'^##\s+', text, re.MULTILINE)
    if m:
        insert_at = m.start()
        return text[:insert_at] + summary_block + text[insert_at:]
    else:
        return text.rstrip('\n') + '\n\n' + summary_block


def main():
    parser = argparse.ArgumentParser(description='Inject prolab summaries into READMEs')
    parser.add_argument('--ctf',     default=str(DEFAULT_CTF),  help='Path to ctf-writeups repo')
    parser.add_argument('--yaml',    default=str(DEFAULT_YAML), help='Path to prolabs.yml')
    parser.add_argument('--dry-run', action='store_true',       help='Preview changes without writing')
    args = parser.parse_args()

    yaml_path   = Path(args.yaml)
    prolabs_dir = Path(args.ctf) / PROLABS_REL_PATH

    if not yaml_path.exists():
        print(f'[ERROR] prolabs.yml not found: {yaml_path}')
        return
    if not prolabs_dir.exists():
        print(f'[ERROR] ProLabs dir not found: {prolabs_dir}')
        return

    prolabs = yaml.safe_load(yaml_path.read_text(encoding='utf-8'))
    if not isinstance(prolabs, list):
        print('[ERROR] prolabs.yml is not a list')
        return

    # Build lookup: normalised name → blurb
    yaml_map = {
        normalise(p['name']): p
        for p in prolabs if isinstance(p, dict) and 'name' in p
    }

    print(f'Loaded {len(yaml_map)} entries from {yaml_path.name}\n')

    updated = 0
    skipped = 0
    missing = 0

    for lab_dir in sorted(prolabs_dir.iterdir()):
        if not lab_dir.is_dir():
            continue

        readme = lab_dir / 'README.md'
        if not readme.exists():
            print(f'  [SKIP] no README: {lab_dir.name}')
            missing += 1
            continue

        key   = normalise(lab_dir.name)
        match = yaml_map.get(key)

        if not match:
            print(f'  [WARN] no YAML match for: {lab_dir.name}')
            missing += 1
            continue

        blurb = match.get('blurb', '').strip()
        if not blurb:
            print(f'  [WARN] empty blurb for: {lab_dir.name}')
            skipped += 1
            continue

        text = readme.read_text(encoding='utf-8', errors='ignore')

        if has_summary_section(text):
            print(f'  [SKIP] already has ## Summary: {lab_dir.name}')
            skipped += 1
            continue

        new_text = inject_summary(text, blurb)

        if args.dry_run:
            # Show a preview of what would be inserted
            m = re.search(r'## Summary\n.*?\n\n---', new_text, re.DOTALL)
            preview = m.group(0) if m else '(preview unavailable)'
            print(f'  [DRY] {lab_dir.name}')
            print(f'        → {preview[:120].strip()}')
        else:
            readme.write_text(new_text, encoding='utf-8')
            print(f'  [OK]  {lab_dir.name}  →  "{blurb[:80]}"')

        updated += 1

    print(f'\n{"─" * 52}')
    if args.dry_run:
        print(f'Would update: {updated}  ·  Skipped: {skipped}  ·  No match: {missing}')
        print('Run without --dry-run to write changes.')
    else:
        print(f'Updated: {updated}  ·  Skipped: {skipped}  ·  No match: {missing}')
        print('\nNext step: python build.py')


if __name__ == '__main__':
    main()
