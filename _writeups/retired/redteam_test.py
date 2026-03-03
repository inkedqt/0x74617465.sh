#!/usr/bin/env python3
import os, re, json

LABS_DIR = os.path.expanduser("~/0x74617465.sh/_writeups/retired")

TOOL_PATTERNS = [
    ("nmap",          [r"\bnmap\b"]),
    ("evil-winrm",    [r"\bevil-winrm\b"]),
    ("crackmapexec",  [r"\bcrackmapexec\b", r"\bcme\b"]),
    ("impacket",      [r"psexec\.py", r"secretsdump\.py", r"wmiexec\.py", r"smbclient\.py", r"getTGT\.py", r"getST\.py"]),
    ("bloodhound",    [r"\bbloodhound\b", r"\bsharpbound\b", r"bloodhound-python"]),
    ("kerbrute",      [r"\bkerbrute\b"]),
    ("hydra",         [r"\bhydra\b"]),
    ("gobuster",      [r"\bgobuster\b"]),
    ("ffuf",          [r"\bffuf\b"]),
    ("feroxbuster",   [r"\bferoxbuster\b"]),
    ("sqlmap",        [r"\bsqlmap\b"]),
    ("metasploit",    [r"\bmsfconsole\b", r"\bmsfvenom\b"]),
    ("john",          [r"\bjohn\b", r"\bhashcat\b"]),
    ("curl",          [r"^\s*curl\b"]),
    ("python",        [r"^\s*python3?\b"]),
    ("linpeas",       [r"\blinpeas\b", r"\bwinpeas\b"]),
]

def detect_tool(command):
    cmd = command.lower()
    for tool, patterns in TOOL_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, cmd):
                return tool
    return "shell"

all_commands = []
seen = set()

for lab_folder in sorted(os.listdir(LABS_DIR)):
    lab_path = os.path.join(LABS_DIR, lab_folder)
    if not os.path.isdir(lab_path):
        continue
    for fname in ["index.md", "writeup.md", f"{lab_folder}.md"]:
        fpath = os.path.join(lab_path, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            blocks = re.findall(r"```bash\s*\n(.*?)```", content, re.DOTALL)
            cmds = []
            for block in blocks:
                lines = block.strip().split("\n")
                clean = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
                if clean:
                    cmd = " ".join(clean)
                    if cmd not in seen:
                        seen.add(cmd)
                        cmds.append({"command": cmd, "tool": detect_tool(cmd), "lab": lab_folder})
            if cmds:
                print(f"  {lab_folder} ({fname}): {len(cmds)} commands")
                for c in cmds:
                    print(f"    [{c['tool']}] {c['command'][:70]}")
                all_commands.extend(cmds)
            break

print(f"\nTotal: {len(all_commands)} unique commands across {len(set(c['lab'] for c in all_commands))} labs")
tool_counts = {}
for c in all_commands:
    tool_counts[c['tool']] = tool_counts.get(c['tool'], 0) + 1
for t, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
    print(f"  {t}: {count}")
