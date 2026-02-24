---
layout: writeup
name: "Offshore"
platform: "HackTheBox"
category: "prolabs"
difficulty: "Medium"
os: "Hack The Box  Pro Lab"
date: 2025-11-12
pwned: true
---
# Offshore – HTB Pro Lab (Teaser)

**Status:** ✅ Completed  
**Platform:** Hack The Box – *Pro Lab*  
**Write-up:** Redacted until/unless HTB allows public solutions (Pro Labs stay secret).

---

## 🧭 Overview
Offshore is a big, realistic network that starts at the external perimeter and steadily pushes you through several pivots into an internal AD estate. Expect multiple web entry points, credential harvesting, careful routing, and a tidy escalation chain once you graph the relationships.

---

## 🧪 What I Can Share (No Spoilers)
- **Perimeter → Web footholds** via disciplined recon and source-reading  
- **Segmentation pivots** with clean tunneling/proxying  
- **Credential discovery/reuse** leading into **AD**  
- **BloodHound validation** to chart a short, reliable path to DA

---

## 🧠 Takeaways
- Treat every small misconfig as a **link in a chain**  
- Keep tunneling light and auditable—**route only what you need**  
- Re-run graphing after each new cred; the **shortest safe path** often appears late

---

## 🖼️ Proofs
<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/offshore.png" alt="Offshore pwned screen" style="max-width: 800px; border-radius: 8px;">
  <br/><em>Offshore: pwned.</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/certs/offshore_cert.png" alt="HTB Pro Lab Offshore certificate" style="max-width: 800px; border-radius: 8px;">
  <br/><em>HTB Pro Lab: Offshore — Certificate of Completion</em>
</p>

---

## 📌 Notes
No spoiler walkthrough here by design. If HTB ever green-lights public write-ups, I’ll publish a full breakdown with defensive guidance.
