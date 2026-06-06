---
layout: writeup
name: "Connected"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Easy"
permalink: /writeups/seasonal/connected/
os: "HackTheBox"
tags: [seasonal]
date: 2026-06-07
pwned: true
---
#  Connected

> **Difficulty:** Easy | **OS:** Linux | **Release:** HTB Season 11

Connected is an Easy Linux box centred on a publicly exposed FreePBX instance vulnerable to CVE-2025-57819. Initial access is achieved through unauthenticated remote code execution, dropping into a low-privilege shell. Privilege escalation abuses a writable configuration file that is sourced by a root-owned init script, triggered automatically via an incron file-watch rule — no interaction required once the payload is in place.

---

## 📸 Proof
![](connected.png)

---

## 🧠 Concepts Covered

- CVE-2025-57819 (FreePBX unauthenticated RCE)
- Incron file-watch event abuse
- Init script configuration injection

---

## 💡 Hints (No Spoilers)

**Foothold**
The web-facing service has a known critical CVE from 2025 — there's a public PoC. Check what it gives you and how to turn it into a shell.

**User**
Your RCE lands you close to the user flag. Standard enumeration gets you there.

**Root**
Look for files you can write to that get executed by a privileged process. Something is watching a directory and reacting to it — figure out what that triggers and where it leads.

---

## 📚 Useful Reading