---
layout: writeup
name: "VariaType"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/variatype/
os: "HackTheBox"
tags: [seasonal]
date: 2026-05-24
pwned: true
---
# 🔤 VariaType

> **Difficulty:** Medium | **OS:** Linux | **Release:** HTB Season 10

A Linux box themed around typography tooling — the whole kill chain runs through CVEs in font processing libraries. Three separate CVEs, three different users, and every step involving file handling that developers never expected to reach an attacker. If you know your way around font toolchains, the vulnerability surface here will feel very familiar.

---

## 📸 Proof

![](variatype.png)
---

## 🧠 Concepts Covered

- Exposed `.git` repository enumeration and credential recovery from commit history
- Local file inclusion via path traversal (`....//` bypass)
- CVE research across niche font processing libraries
- CVE-2025-66034 — fonttools varLib arbitrary file write via XML injection in `.designspace` files
- CVE-2024-25081 — FontForge command injection via crafted archive filenames
- CVE-2025-47273 — setuptools `PackageIndex.download()` path traversal
- `sudo` abuse via attacker-controlled arguments
- SSH authorized_keys write for persistent root access

---

## 💡 Hints (No Spoilers)

**Foothold**
- There's a subdomain worth finding. Once you're on the portal, look at what the web server is handing out that it shouldn't be.
- The exposed directory you find will have credentials in the diff history — not the current files.
- The portal has a file download endpoint. The filter it uses can be bypassed. Once you can read arbitrary files, figure out what's running on other ports and by whom.
- The internal app processes font files. One specific file type goes through a library that had a CVE this year — the output path is attacker-controlled.

**User**
- You're `www-data`. A cron job runs as another user and processes files from a directory you can write to.
- The processing involves FontForge. Look at how FontForge handles archive filenames — there's a CVE for that. The filename itself is the payload.

**Root**
- `sudo -l`. The command you can run calls a Python script with a wildcard argument.
- The script uses `setuptools` to download a URL you supply. That library had a path traversal CVE this year.
- Think about where you want that "download" to land, and what file at that path would give you root.

---

## 📚 Useful Reading

- CVE-2025-66034 — fonttools varLib `.designspace` XML processing
- CVE-2024-25081 — FontForge archive filename command injection
- CVE-2025-47273 — setuptools PackageIndex path traversal
- Git object storage and recovering credentials from commit diffs
- Python `setuptools` source — `PackageIndex.download()` internals
