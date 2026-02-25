---
layout: writeup
name: "FortressAWS"
platform: "HackTheBox"
category: "prolabs"
difficulty: "Unknown"
permalink: /writeups/prolabs/fortressaws/
os: "Hack The Box  Pro Lab"
date: 2026-02-25
pwned: true
---
# Fortress AWS – HTB Pro Lab (Teaser)

**Status:** ✅ Completed  
**Platform:** Hack The Box – *Pro Lab*  
**Write-up:** Redacted until/unless HTB allows public solutions (Pro Labs stay secret).

---

## 🧭 Overview
Fortress AWS is a tight cloud-first lab—**IAM** gotchas, **priv-esc** via policies/roles, and real-world **SSM/S3** workflows that mirror production.

---

## 🧪 What I Can Share (No Spoilers)
- **IAM** misconfigs → privilege escalation
- **SSM** pivots, **S3** data handling, and cloud persistence
- Guardrails vs mis-scoped permissions
- Least-privilege mindset in practice

---

## 🧠 Takeaways
- Read every policy—**the diff matters**
- Enumerate via CLI **and** console for full context
- Log trails tell the story; keep artifacts clean

---

## 🖼️ Proofs
<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/hacknet.png" alt="FortressAWS proof screen" style="max-width: 800px; border-radius: 8px;">
  <br/><em>FortressAWS: pwned.</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/certs/fortress_aws.png" alt="Fortress AWS – HTB Pro Lab (Teaser) certificate" style="max-width: 800px; border-radius: 8px;">
  <br/><em>HTB Pro Lab: Fortress AWS — Certificate of Completion</em>
</p>

---

## 📌 Notes
No walkthrough here by design. If HTB ever green-lights public write-ups, I’ll publish a full breakdown with proper defensive countermeasures.

**Author:** inkedqt • **Site:** https://inksec.io
