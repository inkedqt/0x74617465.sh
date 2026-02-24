---
layout: writeup
name: "Zephyr"
platform: "HackTheBox"
category: "prolabs"
difficulty: "Unknown"
permalink: /writeups/prolabs/zephyr/
os: "Hack The Box  Pro Lab"
date: 2026-02-24
pwned: true
---
Zephyr – HTB Pro Lab (Teaser)
Status: ✅ Completed
Platform: Hack The Box – Pro Lab
Write-up: Redacted until/unless HTB allows public solutions (Pro Labs stay secret).

🧭 Overview
Zephyr blends perimeter mapping with multi-network pivots and mature AD ramp-up. It’s a test of patient mapping, careful trust-abuse, and doing the right small step that opens the next door.

🧪 What I Can Share (No Spoilers)
- Perimeter foothold → methodical internal pivoting  
- Chained web/service footholds that lead to an internal tool you’ll want to inspect  
- AD enumeration and practical escalation paths (service accounts, scheduled tasks, certs/delegation)  
- Defensive reminders: logging, least-privilege, and segmentation checks

🧠 Takeaways
- Map networks first — the environment often points to the shortest safe path  
- Small tooling mistakes (schedules, backup tooling, weak service accounts) compound quickly  
- Validate pivots with minimal noise so you can reproduce and report effectively

## Summary
Perimeter foothold → multi-segment pivots → internal tooling abuse → AD enumeration → domain takeover.

---
## 🖼️ Proofs
<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/zephyr.png" alt="Wanderer proof screen" style="max-width: 800px; border-radius: 8px;">
  <br/><em>Zephyr: pwned.</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/certs/zephyr_cert.png" alt="Wanderer – HTB Pro Lab (Teaser) certificate" style="max-width: 800px; border-radius: 8px;">
  <br/><em>HTB Pro Lab: Zephyr — Certificate of Completion</em>
</p>

📌 Notes
No walkthrough here by design. If HTB flips its policy on Pro Lab write-ups, I’ll publish a full, defense-aware breakdown with mitigation notes.

Author: inkedqt • Site: https://inksec.io
