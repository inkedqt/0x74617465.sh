---
layout: writeup
name: "Cybernetics"
platform: "HackTheBox"
category: "prolabs"
difficulty: "Unknown"
permalink: /writeups/prolabs/cybernetics/
os: "Hack The Box  Pro Lab"
date: 2026-02-25
pwned: true
---
# Cybernetics – HTB Pro Lab (Teaser)

**Status:** ✅ Completed  
**Platform:** Hack The Box – *Pro Lab*  
**Write-up:** Redacted until/unless HTB allows public solutions (Pro Labs stay secret).

---

## 🧭 Overview
Cybernetics rewards disciplined web recon feeding into **Kerberos** misconfigs and smart delegation use. Once you stabilize creds, the escalation is surgical.

---

## 🧪 What I Can Share (No Spoilers)
- **Web app** foothold → **AS-REP/Kerberoast** moments
- **Constrained delegation** / ticket abuse for lateral moves
- **BloodHound** to confirm shortest DA route
- Good reps for **opsec** on Windows targets

---

## 🧠 Takeaways
- Wordlists + **context** beat brute force
- Ticket-based attacks shine when **SPNs** are mapped correctly
- Re-run BloodHound after each new cred

---

## 🖼️ Proofs
<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/cybernetics.png" alt="Cybernetics proof screen" style="max-width: 800px; border-radius: 8px;">
  <br/><em>Cybernetics: pwned.</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/certs/cybernetics_cert.png" alt="Cybernetics – HTB Pro Lab (Teaser) certificate" style="max-width: 800px; border-radius: 8px;">
  <br/><em>HTB Pro Lab: Cybernetics — Certificate of Completion</em>
</p>

---

## 📌 Notes
No walkthrough here by design. If HTB ever green-lights public write-ups, I’ll publish a full breakdown with proper defensive countermeasures.

**Author:** inkedqt • **Site:** https://inksec.io
