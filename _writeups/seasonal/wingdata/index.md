---
layout: writeup
name: "Wingdata"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Easy"
permalink: /writeups/seasonal/wingdata/
os: "Linux  Release HTB Seasonal"
date: 2026-02-21
pwned: true
---
# 🪶 WingData

> **Difficulty:** Easy | **OS:** Linux | **Release:** HTB Seasonal

A Linux box centred around a file transfer server with a known pre-authentication vulnerability. Rooting it requires chaining three distinct skills: web exploitation, offline credential recovery, and abusing a subtle flaw in Python's standard library.

---
## 📸 Proof
![Wingdata Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/wingdata.png)

## 🧠 Concepts Covered

- Virtual host enumeration
- CVE research and exploitation (pre-auth RCE)
- Understanding server-side session storage mechanisms
- Offline hash cracking with custom salt formats
- Python `tarfile` security filtering and its edge cases
- Symlink/hardlink behaviour inside archive extraction
- Linux privilege escalation via `sudo` misuse

---

## 💡 Hints (No Spoilers)

**Foothold**
- The version number is sitting in the login page footer. The developers put it there. Say thank you and go look up CVEs.
- Before you write a single line of exploit code, understand *how* this application stores sessions. The format it chose is unusual and that choice is the entire vulnerability.
- "Pre-authentication" means you don't need an account. Anonymous access exists for a reason — try it.
- Think about what happens when a C string and a file buffer disagree about where a string ends.

**User**
- The server keeps its house in order under `/opt`. Poke around — it's surprisingly talkative about how it hashes passwords.
- The salt isn't random per-user. It's the same for everyone and it's written in a config file you can read. That matters a lot when you're building your Hashcat command.
- Mode `-m 1410` exists for a reason. Read what it does, then look at exactly how this application constructs its hashes. They should match perfectly.
- rockyou will do the job here. Don't overthink it.

**Root**
- `sudo -l`. Always. Do it before anything else.
- Read the entire Python script before you do anything. The input validation is legitimately strict — filenames, directory names, all locked down. But notice what *isn't* validated: the contents of the archive itself.
- `filter="data"` in `tarfile.extractall()` was added specifically to prevent path traversal. It was not a perfect solution. Look up what it relies on and what happens at the edge of that dependency.
- `PATH_MAX` is 4096 bytes. `os.path.realpath()` has to fit its output in that. Think about what "silently truncates" means for a security check.
- Symlinks escape the sandbox. Hardlinks make the escape *writable*. You need both.

---

## 📚 Useful Reading

- Wing FTP Server documentation (understand the data directory structure)
- Hashcat wiki — hash modes, salting formats
- Python `tarfile` module docs — specifically the `filter` parameter and its security guarantees
- [PEP 706](https://peps.python.org/pep-0706/) — the proposal that introduced `tarfile` extraction filters
- `PATH_MAX` and `realpath(3)` man page — what happens at the boundary

---

*This box is part of an active HTB Seasonal rotation. Full writeup will be published after the box retires.*
