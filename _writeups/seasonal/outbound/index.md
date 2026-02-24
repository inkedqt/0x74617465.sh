---
layout: writeup
name: "Outbound"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Easy"
permalink: /writeups/seasonal/outbound/
date: 2025-11-12
pwned: true
---
🛰️ Outbound (HTB Seasonal)

**Status**: 🔒 Private – writeup will be published once the machine retires  
**Difficulty**: Easy  
**Category**: Linux | Web | Misconfig | Symlink PrivEsc  
**Date Completed**: 2025-07-14  

🧠 Teaser

A real-world style engagement where you begin with leaked webmail creds, land an RCE in Roundcube, and pivot from container to host...

Can you trace the trail from email to exploitation and escalate using a log file with dangerous permissions?

🧪 Your journey includes:

- 🔍 Creds reuse on Roundcube
- 🚀 Authenticated RCE via CVE-2025-49113
- 🐚 Shell via Metasploit custom module
- 🧬 MySQL session base64 decoding → full access
- 🔑 Password extraction using CyberChef + enc.py
- 🎣 Email hunting and SSH hop
- 🪝 Privesc via symlink overwrite to `/etc/passwd` from `/var/log/below/error_root.log`

📸 Proof  
![Outbound Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/outbound.png)

