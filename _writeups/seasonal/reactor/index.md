---
layout: writeup
name: "reactor"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/reactor/
os: "HackTheBox"
tags: [seasonal]
date: 2026-05-24
pwned: true
---
# ⚛️ Reactor

> **Difficulty:** Medium | **OS:** Linux | **Release:** HTB Season 11

A Linux box built around a Node.js web application with a recently disclosed pre-authentication vulnerability. Getting a foothold is the easy part — the name of the box is basically a hint. User requires you to notice something the app left lying around. Root is a one-liner once you know what that port does, and why running as the same user as the app was always going to be a problem.

---

## 📸 Proof
![](reactor.png)


---

## 🧠 Concepts Covered

- CVE research and exploitation (pre-auth unauthenticated RCE)
- Node.js application enumeration
- Credential discovery in application config/source
- Linux lateral movement via weak credentials
- Node.js V8 inspector protocol (port 9229)
- Remote code execution via debug inspector REPL
- SUID binary abuse for privilege escalation

---

## 💡 Hints (No Spoilers)

**Foothold**
- The box is called Reactor. The app is a React app. That's not a coincidence — look at what CVEs were disclosed this year for the framework it's running on.
- "Unauth" is in the module name. You don't need an account, you don't need to brute anything, you don't need to find credentials first. The vulnerability hands you execution directly.
- If you prefer doing it manually over Metasploit, understanding what the CVE actually does will get you there. The module name is basically a spoiler for the CVE number.

**User**
- You landed as `node`. That user exists to run the app. The app has to connect to things. Applications that connect to things tend to have credentials written down somewhere.
- Look inside the application directory. Developers leave things in config files, environment files, and source code. Read what's there.
- The password you find probably works for one of the other users you can see on the box. Try the obvious one.

**Root**
- Run `ss -lntp` and actually look at every port. One of them is a well-known Node.js port that has no business being accessible to you — but it is, and you're already a Node.js user.
- Port 9229 is the V8 inspector. Look up what `node inspect` does. Then look up what `exec()` does inside the debug REPL.
- You're not exploiting anything novel here. You're using a legitimate debugging feature as the user that owns the process. Think about why that works.
- One command inside the debugger is enough. You know what SUID does.

---

## 📚 Useful Reading

- CVE-2025-55182 — read the advisory, not just the CVSS score
- Node.js Inspector/Debugger documentation — `node inspect`, the `exec` command, what it can call
- `child_process.execSync()` — what it does and what user it runs as
- SUID binaries and `bash -p` — why copying bash and setting the SUID bit gives you what you want
- `ss -lntp` vs `netstat` — knowing what's listening locally vs externally

---

*This box is part of an active HTB Season 11 rotation. Full writeup published after retirement.*
