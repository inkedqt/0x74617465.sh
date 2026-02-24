#!/usr/bin/env python3
"""
build.py — 0x74617465.sh writeup pipeline
Scans ctf-writeups repo, parses README.md metadata,
copies processed files to _writeups/ with Jekyll front matter,
outputs boxes-data.js for the card grid in index.html.

Usage:
  python build.py
  python build.py --ctf /path/to/ctf-writeups
  python build.py --out /path/to/0x74617465.sh
  python build.py --dry-run

Daily workflow:
  1. Finish writeup in ctf-writeups repo
  2. python build.py
  3. cd ~/0x74617465.sh && git add . && git commit -m "add BoxName" && git push
"""

import re
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────────────────────────
DEFAULT_CTF = Path("/home/tate/INKSEC.IO/ctf-writeups")
DEFAULT_OUT = Path("/home/tate/0x74617465.sh")

# Category scan paths — (ctf-writeups relative path, category label, platform)
SCAN_PATHS = [
    ("HTB/Seasonal",          "seasonal",    "HackTheBox"),
    ("HTB/Active",            "active",      "HackTheBox"),
    ("HTB/Retired",           "retired",     "HackTheBox"),
    ("HTB/Challenges",        "challenges",  "HackTheBox"),
    ("HTB/ProLabs",           "prolabs",     "HackTheBox"),
    ("HTB/StartingPoint",     "starting",    "HackTheBox"),
    ("Other/THM",             "thm",         "TryHackMe"),
    ("Other/PG",              "pg",          "ProvingGrounds"),
    ("Other/HackSmarter",     "hacksmarter", "HackSmarter"),
]

# Difficulty normalisation
DIFF_MAP = {
    "easy": "Easy", "medium": "Medium", "hard": "Hard",
    "insane": "Insane", "medium-hard": "Hard", "varied": "Varied",
    "basic": "Easy", "season": "Varied",
}

# ── SLUG ──────────────────────────────────────────────────────────────────────
def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

# ── METADATA PARSER ───────────────────────────────────────────────────────────
def parse_readme_meta(text):
    """
    Parse metadata from bold markdown lines:
      **Status:** 🔒 Private
      **Difficulty:** Easy
      **Platform:** Linux
      **Category:** Web | IDOR
    Also checks for YAML front matter if present.
    """
    meta = {}

    # YAML front matter first
    fm_match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if ':' in line:
                k, _, v = line.partition(':')
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")

    # Metadata patterns — bold (**Key:**) and plain (Key:) variants
    patterns = {
        'status':     [r'\*\*Status:\*\*\s*(.+)',     r'^Status:\s*(.+)'],
        'difficulty': [r'\*\*Difficulty:\*\*\s*(.+)', r'^Difficulty:\s*(.+)'],
        'platform':   [r'\*\*Platform:\*\*\s*(.+)',   r'^Platform:\s*(.+)'],
        'os':         [r'\*\*(?:OS|Platform):\*\*\s*(.+)', r'^(?:OS|Platform):\s*(.+)'],
        'category':   [r'\*\*Category:\*\*\s*(.+)',   r'^Category:\s*(.+)'],
    }
    for key, plist in patterns.items():
        if key in meta:
            continue
        for pattern in plist:
            m = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if m:
                meta[key] = m.group(1).strip()
                break

    return meta


def extract_teaser(text):
    """Extract the ## 🧠 Teaser section if present."""
    m = re.search(r'##\s*[^\n]*Teaser[^\n]*\n+(.*?)(?=\n##|\Z)', text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ''


def extract_summary_from_existing(name, existing_boxes):
    """Fall back to summary already in hardcoded arrays if no README summary."""
    for box in existing_boxes:
        if box.get('name', '').lower() == name.lower():
            return box.get('summary', '')
    return ''


def extract_diff_from_existing(name, existing_boxes):
    """Fall back to difficulty from hardcoded arrays."""
    for box in existing_boxes:
        if box.get('name', '').lower() == name.lower():
            return box.get('diff', '')
    return ''


def is_private(meta, text):
    """Return True if the writeup is marked private / spoiler policy active."""
    status = meta.get('status', '')
    return '🔒' in status or 'private' in status.lower()

# ── FRONT MATTER WRITER ───────────────────────────────────────────────────────
def build_front_matter(name, meta, category, platform, summary, pwned, date_str, existing_boxes=None):
    diff_raw = meta.get('difficulty', '').strip()
    # Strip dirty trailing content — split on | · – or 2+ spaces or ** or backslash
    diff_raw = re.split(r'[|·\-–\\]|\s{2,}|\*\*', diff_raw)[0].strip()
    # Remove any remaining non-alpha chars except spaces
    diff_raw = re.sub(r'[^\w\s]', '', diff_raw).strip()
    # If it's "Easy Linux" style, just take first word
    diff_raw = diff_raw.split()[0] if diff_raw else ''
    # Fall back to hardcoded arrays if still empty/unknown
    if (not diff_raw or diff_raw.lower() == 'unknown') and existing_boxes:
        diff_raw = extract_diff_from_existing(name, existing_boxes)
    diff = DIFF_MAP.get(diff_raw.lower(), diff_raw.title() if diff_raw else 'Unknown')

    os_val = meta.get('platform', meta.get('os', '')).strip()
    # Clean emoji from os
    os_val = re.sub(r'[^\w\s]', '', os_val).strip()
    # Normalise common values
    if os_val.lower() in ('linux', 'unix', 'freebsd'):
        os_val = 'Linux'
    elif os_val.lower() in ('windows',):
        os_val = 'Windows'

    category_val = meta.get('category', '').strip()
    # Tags from category field — split on | , ;
    tags = [t.strip() for t in re.split(r'[|,;]', category_val) if t.strip()] if category_val else []

    fm = f'---\n'
    fm += f'layout: writeup\n'
    fm += f'name: "{name}"\n'
    fm += f'platform: "{platform}"\n'
    fm += f'category: "{category}"\n'
    fm += f'difficulty: "{diff}"\n'
    fm += f'permalink: /writeups/{category}/{slugify(name)}/\n'
    if os_val:
        fm += f'os: "{os_val}"\n'
    if tags:
        fm += f'tags: [{", ".join(tags)}]\n'
    if date_str:
        fm += f'date: {date_str}\n'
    if pwned:
        fm += f'pwned: true\n'
    fm += f'---\n'
    return fm, diff, os_val, tags


# ── PROCESS ONE BOX ───────────────────────────────────────────────────────────
def process_box(box_dir, category, platform, dest_dir, dry_run, existing_boxes):
    readme = box_dir / 'README.md'
    if not readme.exists():
        return None

    name = box_dir.name
    text = readme.read_text(encoding='utf-8', errors='ignore')
    meta = parse_readme_meta(text)
    private = is_private(meta, text)

    # Date from directory mod time
    date_str = datetime.fromtimestamp(readme.stat().st_mtime).strftime('%Y-%m-%d')

    # Summary: teaser if private, otherwise first paragraph after Overview or full teaser
    teaser = extract_teaser(text)
    existing_summary = extract_summary_from_existing(name, existing_boxes)
    summary = existing_summary or (teaser if private else '')
    # Pwned — assume true unless ⏳ in status
    status_val = meta.get('status', '')
    pwned = '⏳' not in status_val

    fm, diff, os_val, tags = build_front_matter(name, meta, category, platform, summary, pwned, date_str, existing_boxes)

    # Strip existing front matter from content
    content = text
    fm_match = re.match(r'^---\s*\n.*?\n---\s*\n', text, re.DOTALL)
    if fm_match:
        content = text[fm_match.end():]

    # For active/private boxes, replace full content with teaser only
    if private and category == 'active':
        content = f'\n> 🔒 **Spoiler Policy** — Full writeup published on machine retirement.\n\n'
        if teaser:
            content += f'## Teaser\n\n{teaser}\n'

    slug = slugify(name)
    dest_path = dest_dir / category / slug
    dest_path.mkdir(parents=True, exist_ok=True)
    dest_file = dest_path / 'index.md'

    if not dry_run:
        dest_file.write_text(fm + content, encoding='utf-8')

        # Copy images
        for img in box_dir.iterdir():
            if img.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'):
                shutil.copy2(img, dest_path / img.name)

    url = f'/writeups/{category}/{slug}/'

    return {
        'name':     name,
        'diff':     diff,
        'os':       os_val,
        'platform': platform,
        'category': category,
        'status':   '✅' if pwned else '⏳',
        'private':  private,
        'summary':  summary,
        'url':      url,
        'date':     date_str,
    }


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='0x74617465.sh writeup pipeline')
    parser.add_argument('--ctf',     default=str(DEFAULT_CTF), help='Path to ctf-writeups repo')
    parser.add_argument('--out',     default=str(DEFAULT_OUT), help='Path to 0x74617465.sh repo')
    parser.add_argument('--dry-run', action='store_true',      help='Preview without writing')
    args = parser.parse_args()

    ctf_root  = Path(args.ctf)
    out_root  = Path(args.out)
    dest_dir  = out_root / '_writeups'
    js_out    = out_root / 'boxes-data.js'

    if not ctf_root.exists():
        print(f'[ERROR] ctf-writeups not found: {ctf_root}')
        return

    dry_run = args.dry_run
    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)

    # Load existing hardcoded summaries as fallback
    existing_boxes = []
    index_html = out_root / 'red-team' / 'index.html'
    if index_html.exists():
        idx = index_html.read_text(encoding='utf-8', errors='ignore')
        start = idx.find('const SEASONAL_BOXES')
        if start > -1:
            idx = idx[start:]
        names = re.findall(r"name:'([^']+)'", idx)
        diffs = re.findall(r"diff:'([^']+)'", idx)
        summaries = re.findall(r"summary:'(.*?)(?:',|'\s*})", idx, re.DOTALL)
        for name, diff, summary in zip(names, diffs, summaries):
            existing_boxes.append({'name': name, 'diff': diff, 'summary': summary})

    all_boxes   = {}  # category → list of box dicts
    total       = 0
    processed   = 0

    for rel_path, category, platform in SCAN_PATHS:
        scan_dir = ctf_root / rel_path
        if not scan_dir.exists():
            print(f'  [SKIP] not found: {scan_dir}')
            continue

        all_boxes[category] = []

        for box_dir in sorted(scan_dir.iterdir()):
            if not box_dir.is_dir():
                continue
            total += 1
            result = process_box(box_dir, category, platform, dest_dir, args.dry_run, existing_boxes)
            if result:
                processed += 1
                all_boxes[category].append(result)
                flag = '🔒' if result['private'] else '✅'
                print(f'  [{flag}] {category}/{result["name"]} ({result["diff"]})')
            else:
                print(f'  [SKIP] no README: {box_dir.name}')

    # Build boxes-data.js
    js  = f'// AUTO-GENERATED by build.py — do not edit manually\n'
    js += f'// Last built: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
    js += f'// Total writeups: {processed}\n\n'

    for category, boxes in all_boxes.items():
        const_name = f'BOXES_{category.upper()}'
        js += f'const {const_name} = {json.dumps(boxes, indent=2)};\n\n'

    if not args.dry_run:
        js_out.write_text(js, encoding='utf-8')

    print(f'\n{"─"*52}')
    print(f'Scanned: {total}  ·  Processed: {processed}')
    print(f'Output:  {js_out}')
    print(f'Writeups: {dest_dir}')
    if args.dry_run:
        print('Run without --dry-run to write files.')


if __name__ == '__main__':
    main()
