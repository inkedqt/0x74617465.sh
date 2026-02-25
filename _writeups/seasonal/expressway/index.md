---
layout: writeup
name: "Expressway"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Easy"
permalink: /writeups/seasonal/expressway/
os: "Hack The Box  Season 9 Easy  Linux"
date: 2026-02-25
pwned: true
---
# Expressway – HTB Seasonal (Teaser)

**Status:** ✅ Completed  
**Platform:** Hack The Box – *Season 9* (Easy • Linux)  
**Write-up:** Redacted until/unless HTB allows public solutions.

---

## 🧭 Overview
VPN-first box with a twist: Aggressive Mode IKE on UDP/500 gives you just enough to move from recon to a real foothold. From there, privilege escalation hinges on reading the environment—not just running an off‑the‑shelf script.

---

## 🧪 What I Can Share (No Spoilers)
- **Recon:** UDP/500 (ISAKMP/IKE) + NAT‑T exposed; Aggressive Mode handshake is capturable.  
- **Foothold:** IKE Aggressive Mode → PSK capture → crack → valid user identified as `ike` → SSH in.  
- **Privesc:** Sudo nuance rather than kernel tricks; a hostname hint in logs unlocks root with a clean, single‑line command.

> If you’re practicing real‑world pace and restraint, this one rewards careful reads over noise.

---

## 🧠 Takeaways
- Don’t skip UDP. IKE on **500/udp** often pays off.
- When enum tools are quiet, scan the **logs** and **config** for environment‑specific breadcrumbs.
- Quote carefully and prefer built‑in tools (`ssh`, `sudo`) for a low‑noise finish.

---

## 🖼️ Proofs
<p align="center">
  <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/expressway.png" alt="Expressway pwned screen" style="max-width: 800px; border-radius: 8px;">
  <br/><em>Expressway: pwned.</em>
</p>

---

## 🔗 Links
- HTB machine page: https://app.hackthebox.com/machines/Expressway

---

## 📌 Notes
No flags or credential values are published here by design. Full write-up lives in a private repo until/unless HTB permits public solutions.
