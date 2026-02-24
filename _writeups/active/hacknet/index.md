---
layout: writeup
name: "HackNet"
platform: "HackTheBox"
category: "active"
difficulty: "Hard"
permalink: /writeups/active/hacknet/
os: "Hack The Box  Machine"
date: 2025-11-12
pwned: true
---
# HackNet – HTB Box (Teaser)

**Status:** ✅ Completed  
**Platform:** Hack The Box – *Machine*  
**Write-up:** Redacted until/unless HTB allows public solutions.

---

## 🧭 Overview
A slick Django social app with one critical mistake: server-side template data rendered inside a “likes” fragment. That sink, paired with an IDOR, exposes credentials for a real system user; from there, a world-writable Django file cache enables a pickle deserialization hop to the web user. Final escalation comes from encrypted DB backups left with their GPG key—crack the passphrase, decrypt, and you’re holding the route to root.

---

## 🧪 What I Can Share (No Spoilers)
- **Foothold:** Username rendered in a template → **SSTI**; combined with a “likes” endpoint → credential disclosure → SSH as the intended foothold user.  
- **Lateral:** Django **FileBasedCache** under `/var/tmp/django_cache` is world-writable → replace a fresh cache file with a **pickle** payload → code exec as the web app user.  
- **PrivEsc:** Encrypted SQL backups plus the matching **GPG key** are on the box → crack the key’s passphrase, **decrypt**, recover creds, and pivot to **root**.

---

## 🧠 Takeaways
- Template sinks + IDORs are a nasty combo—**rendered user input** in server templates is game over.
- World-writable caches aren’t harmless scratch space; **pickle loads** equals RCE.
- Backups + keys on the same host are an **inevitable** escalation path—separate and lock them down.

---

## 🖼️ Proof
<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/hacknet.png" alt="HackNet machine proof" style="max-width: 800px; border-radius: 8px;">
  <br/><em>HackNet: pwned.</em>
</p>

---

## 🔗 Links
- HTB machine page: https://app.hackthebox.com/machines/HackNet

---

## 📌 Notes
No payloads or credential values are published here by design. If HTB permits public walkthroughs in the future, I’ll release a full write-up with defensive guidance.
