#!/usr/bin/env python3
"""
get_commands.py
Usage: python3 get_commands.py <boxname>
Searches active/, seasonal/, and retired/ for the box, extracts ```bash blocks,
and merges new commands into commands-data.js preserving existing descriptions.
"""

import os
import re
import json
import sys

# ── CONFIG ──────────────────────────────────────────────────────────────────
WRITEUPS_DIR = os.path.expanduser("~/0x74617465.sh/_writeups")
OUTPUT_JS    = os.path.expanduser("~/0x74617465.sh/red-team/commands/commands-data.js")
CATEGORIES   = ["active", "seasonal", "retired"]

# ── TOOL DETECTION ───────────────────────────────────────────────────────────
TOOL_PATTERNS = [
    ("nmap",          [r"\bnmap\b"]),
    ("evil-winrm",    [r"\bevil-winrm\b"]),
    ("netexec",       [r"\bnxc\b", r"\bnetexec\b"]),
    ("crackmapexec",  [r"\bcrackmapexec\b", r"\bcme\b"]),
    ("impacket",      [r"psexec\.py", r"secretsdump\.py", r"wmiexec\.py", r"smbclient\.py",
                       r"getTGT\.py", r"getST\.py", r"GetNPUsers\.py", r"GetUserSPNs\.py",
                       r"impacket-\w+", r"ldapdomaindump"]),
    ("bloodhound",    [r"\bbloodhound\b", r"bloodhound-python"]),
    ("bloodyad",      [r"\bbloodyAD\b", r"\bbloody\b"]),
    ("certipy",       [r"\bcertipy\b"]),
    ("kerbrute",      [r"\bkerbrute\b"]),
    ("hydra",         [r"\bhydra\b"]),
    ("gobuster",      [r"\bgobuster\b"]),
    ("ffuf",          [r"\bffuf\b"]),
    ("feroxbuster",   [r"\bferoxbuster\b"]),
    ("sqlmap",        [r"\bsqlmap\b"]),
    ("metasploit",    [r"\bmsfconsole\b", r"\bmsfvenom\b"]),
    ("hashcat",       [r"\bhashcat\b"]),
    ("john",          [r"\bjohn\b", r"\bpwsafe2john\b", r"\bssh2john\b", r"\bzip2john\b"]),
    ("curl",          [r"^\s*curl\b"]),
    ("python",        [r"^\s*python3?\b"]),
    ("ssh",           [r"^\s*ssh\b", r"^\s*scp\b"]),
    ("dig",           [r"^\s*dig\b"]),
    ("xfreerdp",      [r"\bxfreerdp\b"]),
    ("smbclient",     [r"^\s*smbclient\b"]),
    ("linpeas",       [r"\blinpeas\b", r"\bwinpeas\b"]),
]

def detect_tool(command: str) -> str:
    cmd = command.lower()
    for tool, patterns in TOOL_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, cmd):
                return tool
    return "shell"

def find_lab(box_name: str):
    """Search active/seasonal/retired for the box. Returns (category, full_path) or None."""
    for cat in CATEGORIES:
        cat_path = os.path.join(WRITEUPS_DIR, cat)
        if not os.path.isdir(cat_path):
            continue
        for folder in os.listdir(cat_path):
            if folder.lower() == box_name.lower():
                return cat, os.path.join(cat_path, folder)
    return None, None

def find_index(lab_path: str, box_name: str) -> str:
    """Find the writeup markdown file in the lab folder."""
    for fname in ["index.md", "writeup.md", f"{box_name.lower()}.md"]:
        fpath = os.path.join(lab_path, fname)
        if os.path.exists(fpath):
            return fpath
    return None

def extract_commands(filepath: str, box_name: str, category: str) -> list:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    pattern = re.compile(r"```bash\s*\n(.*?)```", re.DOTALL)
    blocks = pattern.findall(content)
    commands = []
    for block in blocks:
        lines = block.strip().split("\n")
        tool_override = None
        clean_lines = []
        for line in lines:
            tool_match = re.match(r"#\s*tool:\s*(\w+)", line.strip())
            if tool_match:
                tool_override = tool_match.group(1).lower()
            elif line.strip() and not line.strip().startswith("#"):
                clean_lines.append(line)
        if not clean_lines:
            continue
        full_command = " ".join(l.strip() for l in clean_lines)
        tool = tool_override or detect_tool(full_command)
        commands.append({
            "command": full_command,
            "tool": tool,
            "lab": box_name,
            "lab_url": f"/writeups/{category}/{box_name.lower()}/",
            "desc": "",
            "tags": tool,
        })
    return commands

def load_existing(filepath: str):
    if not os.path.exists(filepath):
        print("  No existing commands-data.js — starting fresh.")
        return [], {}
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"const COMMANDS_DATA = (\[.*?\]);", content, re.DOTALL)
    if not match:
        print("  WARNING: Could not parse existing file — starting fresh.")
        return [], {}
    try:
        existing_list = json.loads(match.group(1))
        existing_dict = {e["command"].strip(): e for e in existing_list}
        return existing_list, existing_dict
    except json.JSONDecodeError:
        print("  WARNING: JSON parse error — starting fresh.")
        return [], {}

def write_output(filepath: str, commands: list):
    tool_set = sorted(set(c["tool"] for c in commands))
    lab_set  = sorted(set(c["lab"]  for c in commands))
    meta = {"total": len(commands), "labs": len(lab_set), "tools": tool_set}
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by get_commands.py — do not edit manually\n")
        f.write("// Run: python3 get_commands.py <boxname>\n\n")
        f.write(f"const COMMANDS_DATA = {json.dumps(commands, indent=2)};\n")
        f.write(f"\nconst COMMANDS_META = {json.dumps(meta, indent=2)};\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_commands.py <boxname>")
        print("Example: python3 get_commands.py administrator")
        sys.exit(1)

    box_arg = sys.argv[1].lower()

    category, lab_path = find_lab(box_arg)
    if not lab_path:
        print(f"ERROR: Box '{box_arg}' not found in active/, seasonal/, or retired/")
        sys.exit(1)

    print(f"Found: {lab_path.split('/')[-1]} [{category}]")

    index_path = find_index(lab_path, box_arg)
    if not index_path:
        print(f"ERROR: No index.md / writeup.md found in {lab_path}")
        sys.exit(1)

    new_cmds = extract_commands(index_path, box_arg, category)
    if not new_cmds:
        print("  No ```bash blocks found — nothing to add.")
        sys.exit(0)

    print(f"  Extracted {len(new_cmds)} commands")

    existing_list, existing_dict = load_existing(OUTPUT_JS)
    print(f"  Existing commands-data.js has {len(existing_list)} commands")

    added = 0
    skipped = 0
    for cmd in new_cmds:
        key = cmd["command"].strip()
        if key in existing_dict:
            skipped += 1
            print(f"  skip (exists): {key[:65]}")
        else:
            existing_list.append(cmd)
            existing_dict[key] = cmd
            added += 1
            print(f"  ++ added [{cmd['tool']}]: {key[:65]}")

    write_output(OUTPUT_JS, existing_list)

    print(f"\n── Done ─────────────────────────────")
    print(f"  Added   : {added} new commands")
    print(f"  Skipped : {skipped} duplicates")
    print(f"  Total   : {len(existing_list)} commands in commands-data.js")
    if added > 0:
        print(f"\n  Open commands-data.js and fill in 'desc' for the {added} new entries.")

if __name__ == "__main__":
    main()
