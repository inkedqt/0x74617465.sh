---
layout: writeup
name: "Interpreter"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Unknown"
permalink: /writeups/seasonal/interpreter/
date: 2026-02-25
pwned: true
---
# 🩸 HTB — Interpreter | Medium | Linux

> No spoilers. Just vibes, nudges, and the occasional raised eyebrow.

---
## 📸 Proof
![Interpreter Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/interpreter.png)
---

## 🖼️ The Vibe

A healthcare integration platform is sitting exposed on the internet, happily telling anyone who asks exactly what version it is.
This box rewards people who read CVE advisories and aren't afraid to poke databases, read source code, and think creatively about what constitutes a "space."

---

## 🗺️ The Path (Spoiler-Free)

### 🔎 Foothold

Start with a thorough nmap. Two web ports, both pointing to the same login page.

> *"What version is this thing running?"*

That's your whole job for the first five minutes. Once you know the version, Google will hand you a present. Nessus can also confirm it if you're feeling fancy.

**Hint:** There's a well-known, well-documented, unauthenticated RCE affecting this application family. It has a CVE number. It has a Metasploit module. You do not need to reinvent the wheel here — but you *might* need to swap your payload when the first one sulks.

---

### 🔑 Lateral Movement

You're in, but you're nobody important. The app has to talk to *something* to store its data.

> *"Where does this application keep its secrets?"*

Applications have config files. Config files have database credentials. Databases have user tables. User tables have password hashes. Password hashes... well, that's what `hashcat` is for.

**Hint:** The hash format here is not your standard MD5/bcrypt fare. Do some reading on how this particular application stores passwords. The salt and hash are bundled together in a way that requires a bit of manual extraction before your cracking tool will accept it. Mode `10900` will ring a bell once you know what you're looking at.

**Hint 2:** The cracked password is something a person from a cold place might use.

---

### 👑 Privilege Escalation

You're a real user now. Time to look around.

> *"What's running on this machine that shouldn't be exposed to regular users?"*

Check your local ports. There's a custom internal service that a developer wrote — and developers, bless them, sometimes do dangerous things with Python's built-in functions when they think a regex will save them.

Read the source code carefully. There are two things to notice:
1. **What** the code is doing with your input (it's very trusting)
2. **What** the developer thought would stop you (it won't)

**Hint:** Spaces are overrated. Python doesn't need them to import things.

**Hint 2:** You can't exploit this remotely. All your work happens from within the box. Script it clean.

---

## 🧠 Skills This Box Will Test

- CVE research and version-based exploitation
- Application configuration file enumeration
- Non-standard hash formatting for password cracking
- Source code auditing (Python)
- Regex filter bypass
- Local service exploitation

---

## 💬 Parting Words

> *"The developer wrote a regex to protect an eval(). Let that sink in."*

If you get stuck on the hash format, don't brute force the problem — read the docs for how the application generates its hashes. Everything you need to format it correctly is in the Base64 string itself.

If you get stuck on privesc, think about what Python lets you do without ever typing a space. The answer is: quite a lot.

Good luck. You've got this. 🖤
