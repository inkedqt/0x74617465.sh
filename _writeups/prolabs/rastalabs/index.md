---
layout: writeup
name: "RastaLabs"
platform: "HackTheBox"
category: "prolabs"
difficulty: "Unknown"
permalink: /writeups/prolabs/rastalabs/
os: "Hack The Box  Pro Lab"
date: 2026-02-24
pwned: true
---
# RastaLabs – HTB Pro Lab (Teaser)

**Status:** ✅ Completed  
**Platform:** Hack The Box – *Pro Lab*  
**Write-up:** Redacted until/unless HTB allows public solutions (Pro Labs stay secret).

---

## Summary
Classic AD: password spray → AS-REP/Kerberoast → BloodHound path → DCSync.

---
## 🧭 Overview
RastaLabs is the AD comfort food—**password spray**, **AS-REP/Kerberoast**, and textbook **BloodHound** edges that land reliably.

---

## 🧪 What I Can Share (No Spoilers)
- Account **discovery** and light **spraying**
- **AS-REP** and **Kerberoast** opportunities
- **Delegation/ACL** edges to DA
- Steady, methodical escalation

---

## 🧠 Takeaways
- Respect account lockouts—**opsec** first
- Build wordlists from **environmental clues**
- Graphs don’t lie—document the path

---

## 🖼️ Proofs
<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/rastalabs.png" alt="RastaLabs proof screen" style="max-width: 800px; border-radius: 8px;">
  <br/><em>RastaLabs: pwned.</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/certs/rastalabs_cert.png" alt="RastaLabs – HTB Pro Lab (Teaser) certificate" style="max-width: 800px; border-radius: 8px;">
  <br/><em>HTB Pro Lab: RastaLabs — Certificate of Completion</em>
</p>

---

## 📌 Notes
No walkthrough here by design. If HTB ever green-lights public write-ups, I’ll publish a full breakdown with proper defensive countermeasures.

**Author:** inkedqt • **Site:** https://inksec.io
