---
layout: writeup
name: "POO"
platform: "HackTheBox"
category: "prolabs"
difficulty: "Unknown"
os: "Hack The Box  Pro Lab"
date: 2025-11-12
pwned: true
---
# P.O.O – HTB Pro Lab (Teaser)

**Status:** ✅ Completed  
**Platform:** Hack The Box – *Pro Lab*  
**Write-up:** Redacted until/unless HTB allows public solutions (Pro Labs stay secret).

---

## 🧭 Overview
P.O.O leans into Windows internals: **MSSQL** execution, **token impersonation** (potato family), and no-nonsense AD escalation without over-engineering.

---

## 🧪 What I Can Share (No Spoilers)
- **xp_cmdshell/mssqlexec** for initial code-exec
- **SYSTEM** via COM/RPC token abuse (potato)
- **AD** pathing with minimal touch
- Proof collection without noisy payloads

---

## 🧠 Takeaways
- When in doubt, use **cmd /c** and built-in tools
- **Architecture mismatches** are common—verify binaries
- Least-noise ops → fastest route to objective

---

## 🖼️ Proofs
<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/poo.png" alt="POO proof screen" style="max-width: 800px; border-radius: 8px;">
  <br/><em>POO: pwned.</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/certs/poo_cert.png" alt="P.O.O – HTB Pro Lab (Teaser) certificate" style="max-width: 800px; border-radius: 8px;">
  <br/><em>HTB Pro Lab: P.O.O — Certificate of Completion</em>
</p>

---

## 📌 Notes
No walkthrough here by design. If HTB ever green-lights public write-ups, I’ll publish a full breakdown with proper defensive countermeasures.

**Author:** inkedqt • **Site:** https://inksec.io
