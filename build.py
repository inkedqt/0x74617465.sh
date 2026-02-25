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
  2. Add a ## Summary section to README.md (one or two lines, arrow-chain style)
  3. python build.py
  4. cd ~/0x74617465.sh && git add . && git commit -m "add BoxName" && git push

Summary priority (highest to lowest):
  1. ## Summary section in README.md          <- going-forward standard
  2. YAML _data files in inkedqt.github.io    <- one-time backfill for existing boxes
  3. Teaser section (private/active boxes only)
"""

import re
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ── CONFIG ────────────────────────────────────────────────────────────────────
DEFAULT_CTF      = Path("/home/tate/Documents/Obsidian_vault/Hack Academy's Blue Team Obsidian Notes/CTF")
DEFAULT_OUT      = Path("/home/tate/0x74617465.sh")
DEFAULT_YAML_DIR = Path("/home/tate/INKSEC.IO/inkedqt.github.io/_data")

# Category scan paths — (ctf-writeups relative path, category label, platform)
SCAN_PATHS = [
    ("HTB/Seasonal",      "seasonal",    "HackTheBox"),
    ("HTB/Active",        "active",      "HackTheBox"),
    ("HTB/Retired",       "retired",     "HackTheBox"),
    ("HTB/Challenges",    "challenges",  "HackTheBox"),
    ("HTB/ProLabs",       "prolabs",     "HackTheBox"),
    ("HTB/StartingPoint", "starting",    "HackTheBox"),
    ("Other/THM",         "thm",         "TryHackMe"),
    ("Other/PG",          "pg",          "ProvingGrounds"),
    ("Other/HackSmarter", "hacksmarter", "HackSmarter"),
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
    Parse metadata from YAML front matter, bold (**Key:**) or plain (Key:) lines.
    Handles multiple README styles accumulated over the years.
    """
    meta = {}

    # YAML front matter first
    fm_match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if ':' in line:
                k, _, v = line.partition(':')
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")

    # Bold (**Key:**) and plain (Key:) variants
    patterns = {
        'status':     [r'\*\*Status:\*\*\s*(.+)',          r'^Status:\s*(.+)'],
        'difficulty': [r'\*\*Difficulty:\*\*\s*(.+)',       r'^Difficulty:\s*(.+)'],
        'platform':   [r'\*\*Platform:\*\*\s*(.+)',         r'^Platform:\s*(.+)'],
        'os':         [r'\*\*(?:OS|Platform):\*\*\s*(.+)', r'^(?:OS|Platform):\s*(.+)'],
        'category':   [r'\*\*Category:\*\*\s*(.+)',         r'^Category:\s*(.+)'],
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


def extract_summary_from_readme(text):
    """
    Look for a ## Summary section in README.md.
    This is the going-forward standard for new writeups:

      ## Summary
      Changelog leak → version fingerprint → LFI → pearcmd.php RCE → root.

    Returns the first paragraph under that heading, stripped of markdown.
    """
    m = re.search(
        r'##\s*(?:📝\s*)?Summary\s*\n+(.*?)(?=\n##|\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    if not m:
        return ''
    content = m.group(1).strip()
    # First paragraph only
    first_para = content.split('\n\n')[0].strip()
    # Collapse newlines to space
    first_para = re.sub(r'\s*\n\s*', ' ', first_para)
    # Strip markdown bold/italic
    first_para = re.sub(r'\*+([^*]+)\*+', r'\1', first_para)
    return first_para.strip()


def extract_teaser(text):
    """Extract the ## Teaser section — used for private/active boxes."""
    m = re.search(
        r'##\s*[^\n]*Teaser[^\n]*\n+(.*?)(?=\n##|\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    if m:
        return m.group(1).strip()
    return ''


def extract_summary_from_existing(name, existing_boxes):
    """YAML backfill — fall back to summary from _data YAML files."""
    name_clean = re.sub(r'[\W_]', '', name.lower())
    for box in existing_boxes:
        box_name = box.get('name', '')
        if box_name.lower() == name.lower():
            return box.get('summary', '')
        if re.sub(r'[\W_]', '', box_name.lower()) == name_clean:
            return box.get('summary', '')
    return ''


def extract_diff_from_existing(name, existing_boxes):
    """YAML backfill — fall back to difficulty from _data YAML files."""
    name_clean = re.sub(r'[\W_]', '', name.lower())
    for box in existing_boxes:
        box_name = box.get('name', '')
        if box_name.lower() == name.lower():
            return box.get('diff', '')
        if re.sub(r'[\W_]', '', box_name.lower()) == name_clean:
            return box.get('diff', '')
    return ''


def is_private(meta, text):
    """Return True if the writeup is marked private / spoiler policy active."""
    status = meta.get('status', '')
    return '🔒' in status or 'private' in status.lower()


# ── YAML BACKFILL LOADER ──────────────────────────────────────────────────────
def load_existing_boxes(yaml_dir):
    """
    Load summaries and difficulties from inkedqt.github.io/_data YAML files.
    These are the canonical hand-written summaries for all existing boxes.

    Once a box has ## Summary in its README, this backfill becomes irrelevant
    for that box — README always wins.
    """
    existing = []

    if not yaml_dir.exists():
        print(f'  [WARN] YAML _data dir not found: {yaml_dir}')
        return existing

    if not HAS_YAML:
        print('  [WARN] pyyaml not installed — skipping YAML backfill')
        print('         Run: pip install pyyaml --break-system-packages')
        return existing

    for yaml_file in sorted(yaml_dir.glob('*.yml')):
        try:
            entries = yaml.safe_load(yaml_file.read_text(encoding='utf-8', errors='ignore'))
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, dict) or 'name' not in entry:
                    continue
                # summary → notes → blurb depending on which YAML uses which field
                summary = (
                    entry.get('summary') or
                    entry.get('notes') or
                    entry.get('blurb') or
                    ''
                )
                if isinstance(summary, str):
                    # Normalise multiline YAML strings to single line
                    summary = re.sub(r'\s*\n\s*', ' ', summary).strip()
                existing.append({
                    'name':    entry['name'],
                    'diff':    str(entry.get('difficulty', '')).strip(),
                    'summary': summary,
                })
        except Exception as e:
            print(f'  [WARN] failed to parse {yaml_file.name}: {e}')

    print(f'  [YAML] loaded {len(existing)} entries from {yaml_dir}')
    return existing


# ── FRONT MATTER WRITER ───────────────────────────────────────────────────────
def build_front_matter(name, meta, category, platform, summary, pwned, date_str, existing_boxes=None):
    diff_raw = meta.get('difficulty', '').strip()
    # Strip dirty trailing content — split on | · – or 2+ spaces or ** or backslash
    diff_raw = re.split(r'[|·\-–\\]|\s{2,}|\*\*', diff_raw)[0].strip()
    # Remove non-alpha chars
    diff_raw = re.sub(r'[^\w\s]', '', diff_raw).strip()
    # "Easy Linux" style — take first word only
    diff_raw = diff_raw.split()[0] if diff_raw else ''
    # Fall back to YAML if still empty/unknown
    if (not diff_raw or diff_raw.lower() == 'unknown') and existing_boxes:
        diff_raw = extract_diff_from_existing(name, existing_boxes)
    diff = DIFF_MAP.get(diff_raw.lower(), diff_raw.title() if diff_raw else 'Unknown')

    os_val = meta.get('platform', meta.get('os', '')).strip()
    os_val = re.sub(r'[^\w\s]', '', os_val).strip()
    if os_val.lower() in ('linux', 'unix', 'freebsd'):
        os_val = 'Linux'
    elif os_val.lower() == 'windows':
        os_val = 'Windows'

    category_val = meta.get('category', '').strip()
    tags = [t.strip() for t in re.split(r'[|,;]', category_val) if t.strip()] if category_val else []

    fm  = '---\n'
    fm += 'layout: writeup\n'
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
        fm += 'pwned: true\n'
    fm += '---\n'
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

    # Date from file mod time
    date_str = datetime.fromtimestamp(readme.stat().st_mtime).strftime('%Y-%m-%d')

    # ── Summary priority ──────────────────────────────────────────────────────
    # 1. ## Summary in README  (going-forward standard — add this to new writeups)
    # 2. YAML _data backfill   (existing boxes without ## Summary yet)
    # 3. Teaser                (private/active only, last resort)
    teaser = extract_teaser(text)
    summary = (
        extract_summary_from_readme(text) or
        extract_summary_from_existing(name, existing_boxes) or
        (teaser if private else '')
    )

    # Pwned — assume true unless ⏳ in status
    pwned = '⏳' not in meta.get('status', '')

    fm, diff, os_val, tags = build_front_matter(
        name, meta, category, platform, summary, pwned, date_str, existing_boxes
    )

    # Strip existing YAML front matter from content
    content = text
    fm_match = re.match(r'^---\s*\n.*?\n---\s*\n', text, re.DOTALL)
    if fm_match:
        content = text[fm_match.end():]

    # Private active boxes — replace full content with spoiler notice + teaser
    if private and category == 'active':
        content = '\n> 🔒 **Spoiler Policy** — Full writeup published on machine retirement.\n\n'
        if teaser:
            content += f'## Teaser\n\n{teaser}\n'

    slug = slugify(name)
    dest_path = dest_dir / category / slug
    dest_path.mkdir(parents=True, exist_ok=True)

    if not dry_run:
        (dest_path / 'index.md').write_text(fm + content, encoding='utf-8')
        for img in box_dir.iterdir():
            if img.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'):
                shutil.copy2(img, dest_path / img.name)

    return {
        'name':     name,
        'diff':     diff,
        'os':       os_val,
        'platform': platform,
        'category': category,
        'status':   '✅' if pwned else '⏳',
        'private':  private,
        'summary':  summary,
        'url':      f'/writeups/{category}/{slug}/',
        'date':     date_str,
    }


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='0x74617465.sh writeup pipeline')
    parser.add_argument('--ctf',      default=str(DEFAULT_CTF),      help='Path to ctf-writeups repo')
    parser.add_argument('--out',      default=str(DEFAULT_OUT),      help='Path to 0x74617465.sh repo')
    parser.add_argument('--yaml-dir', default=str(DEFAULT_YAML_DIR), help='Path to inkedqt.github.io/_data')
    parser.add_argument('--dry-run',  action='store_true',           help='Preview without writing files')
    args = parser.parse_args()

    ctf_root = Path(args.ctf)
    out_root = Path(args.out)
    dest_dir = out_root / '_writeups'
    js_out   = out_root / 'boxes-data.js'

    if not ctf_root.exists():
        print(f'[ERROR] ctf-writeups not found: {ctf_root}')
        return

    dry_run = args.dry_run
    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)

    # Load YAML backfill (summaries + diffs for existing boxes)
    existing_boxes = load_existing_boxes(Path(args.yaml_dir))

    all_boxes = {}
    total     = 0
    processed = 0

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
            result = process_box(box_dir, category, platform, dest_dir, dry_run, existing_boxes)
            if result:
                processed += 1
                all_boxes[category].append(result)
                flag    = '🔒' if result['private'] else '✅'
                has_sum = '📝' if result['summary'] else '  '
                print(f'  [{flag}] {has_sum} {category}/{result["name"]} ({result["diff"]})')
            else:
                print(f'  [SKIP] no README: {box_dir.name}')

    # ── Enrich prolabs with tier/blurb/proof_img from prolabs.yml ────────────
    # process_box() outputs generic fields (summary, diff) but renderProlabs()
    # in index.html expects tier, blurb, proof_img — pull those from the YAML.
    prolab_yaml_path = Path(args.yaml_dir) / 'prolabs.yml'
    if prolab_yaml_path.exists() and HAS_YAML:
        try:
            prolab_yaml_data = yaml.safe_load(prolab_yaml_path.read_text(encoding='utf-8'))
            if isinstance(prolab_yaml_data, list):
                # Build a lookup keyed on normalised name for fuzzy matching
                yaml_lookup = {
                    re.sub(r'[\W_]', '', p['name'].lower()): p
                    for p in prolab_yaml_data if isinstance(p, dict) and 'name' in p
                }
                for box in all_boxes.get('prolabs', []):
                    key = re.sub(r'[\W_]', '', box['name'].lower())
                    match = yaml_lookup.get(key)
                    if match:
                        box['tier']      = match.get('tier', 'Pro Lab')
                        box['blurb']     = match.get('blurb', box.get('summary', ''))
                        box['proof_img'] = match.get('proof_img', '')
                        # Keep summary in sync so backfill stays consistent
                        if not box.get('summary'):
                            box['summary'] = box['blurb']
                    else:
                        print(f'  [WARN] prolabs.yml has no match for: {box["name"]}')
                print(f'  [YAML] enriched {len(all_boxes.get("prolabs", []))} prolabs from prolabs.yml')
        except Exception as e:
            print(f'  [WARN] failed to enrich prolabs: {e}')
    else:
        print(f'  [WARN] prolabs.yml not found at {prolab_yaml_path} — tier/blurb will be empty')

    # Write boxes-data.js
    js  = '// AUTO-GENERATED by build.py — do not edit manually\n'
    js += f'// Last built: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
    js += f'// Total writeups: {processed}\n\n'
    for category, boxes in all_boxes.items():
        js += f'const BOXES_{category.upper()} = {json.dumps(boxes, indent=2)};\n\n'

    if not dry_run:
        js_out.write_text(js, encoding='utf-8')

    print(f'\n{"─"*52}')
    print(f'Scanned: {total}  ·  Processed: {processed}')
    print(f'Output:  {js_out}')
    print(f'Writeups: {dest_dir}')
    if dry_run:
        print('Run without --dry-run to write files.')


if __name__ == '__main__':
    main()
