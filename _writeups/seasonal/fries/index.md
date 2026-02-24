---
layout: writeup
name: "Fries"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Hard"
permalink: /writeups/seasonal/fries/
os: "Hack The Box  Seasonal Hard  Hybrid Linux  Windows  AD"
date: 2025-12-23
pwned: true
---
Fries – HTB Seasonal (Teaser)

Status: ✅ Completed
Platform: Hack The Box – Seasonal (Hard • Hybrid Linux + Windows / AD)
Write-up: 🔒 Private – redacted until retirement / HTB allows public solutions.

🧭 Overview

A multi-layer “enterprise lasagna”: Linux web tier, internal containers, a password manager, and a Windows Server 2025 domain behind it all. Every layer you peel back reveals another trust boundary that shouldn’t have been trusted.

🧪 What I Can Share (No Spoilers)

Recon: Public web entrypoint + subdomains; the real action lives on an internal container network.

Foothold: Source/code access is the turning point — configuration and orchestration files tell stories.

Pivot: App-to-service trust leaks credentials in places defenders forget to look.

Escalation: Certificate and identity plumbing becomes the main theme — once you can mint trust, you can mint access.

🧠 Takeaways

Internal service networks are where “secure” apps go to die.

If you can obtain or forge trust material (certs/keys/tickets), everything upstream collapses.

Password managers can become credential extractors if you can edit where they authenticate.

🖼️ Proof
![Fries Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/fries.png)