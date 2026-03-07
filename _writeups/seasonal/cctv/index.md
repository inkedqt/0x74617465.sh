---
layout: writeup
name: "CCTV"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Easy"
permalink: /writeups/seasonal/cctv/
os: "Linux"
date: 2026-03-08
pwned: true
---
## Summary
Default creds on ZoneMinder v1.37.63 → CVE-2024-51482 Boolean SQLi on tid parameter → 
credentials dumped from zm.Users table → SSH as mark → internal motionEye service on 
port 7999 → picture_filename command injection via on_picture_save → root shell.
# HTB — CCTV | Easy | Linux

_No spoilers. Just vibes, nudges, and the occasional raised eyebrow._

---

## 📸 Proof

![Pirate Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/cctv.png)

---

## 🖼️ The Vibe

A surveillance system watching the watchers. This box is a neat little chain — find the software, find the version, break in through a known flaw, read something you shouldn't, and then notice that the box is running something else internally that really shouldn't be trusted with user input. Two CVEs, one user, one root. Clean and punchy.

---

## 🗺️ The Path (Spoiler-Free)

### 🔎 Recon

Standard nmap to start. Web server is front and centre.

> "What software is managing all these cameras?"

Visit the web interface. It'll tell you exactly what it is and roughly what version. Once you know the name of the application, spend sixty seconds checking whether the default credentials work. Security teams forget to change these more than you'd think.

**Hint:** The username and password are both the same word. A very obvious word.

---

### 💉 Foothold — Known CVE

You're authenticated. Now what?

> "This version is recent enough to feel safe, and old enough to be vulnerable."

Look up the CVE for this application version. There's a well-documented SQL injection vulnerability affecting a specific parameter in the API. It's Boolean-based, which means it's a bit slow — but that's what `sqlmap` is for.

**Hint:** The vulnerable parameter is in a request you can observe while clicking around the interface. Intercept your traffic, find it, and hand it to your injection tool of choice.

**Hint 2:** You're looking for credentials stored in the application's user table. Once you have them, think about where else those credentials might work on this machine.

---

### 🔑 User

SSH is open. You have a username from the database dump. You have something that looks like a credential.

> "People reuse passwords. Application users are people too."

---

### 👑 Root — Internal Service

You're in as a low-privilege user. Time to look around.

> "What's listening that the outside world can't see?"

Check your local network ports. There's a service running internally that isn't exposed externally — which means you'll need to bring it to you. Port forwarding exists for exactly this reason.

Once you can reach the service, identify what it is and look up its CVE history. There's a known authenticated RCE affecting this software. You'll need credentials to use it — and you already have something that might fit.

**Hint:** The exploit requires authentication. The password you need isn't plaintext — check what format the application stores it in. Your SSH session can tell you where the config lives.

**Hint 2:** The vulnerability is in how the software handles a filename field. It gets passed somewhere it really shouldn't be passed. If you've ever seen command injection before, the mechanic will feel familiar.

**Hint 3:** Metasploit has a module for this. Set your `RHOSTS` to localhost, not the box IP — you tunnelled it for a reason.

---

## 🧠 Skills This Box Will Test

- Web application fingerprinting and version identification
- Default credential testing
- Boolean-based SQL injection (tooling-assisted)
- Database credential extraction
- SSH local port forwarding / tunnelling
- CVE research and Metasploit module usage
- Authenticated command injection via filename parameter

---

## 💬 Parting Words

> _"A CCTV system with default creds, a SQLi, and a command injection. Someone really should have patched this."_

The box rewards methodical enumeration over brute force thinking. Each step hands you what you need for the next one — the trick is recognising it when you see it.

If you're stuck on the SQL injection, let your tools do the heavy lifting and point them at the right parameter. If you're stuck on root, remember that "internal only" just means you need a tunnel — not that you can't reach it.

Good luck. Stay nosy. 🖤