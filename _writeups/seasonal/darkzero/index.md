---
layout: writeup
name: "DarkZero"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Hard"
permalink: /writeups/seasonal/darkzero/
os: "Hack The Box  Machine"
date: 2025-11-12
pwned: true
---
DarkZero — HTB Hard (Teaser)
Status: ✅ Completed
Platform: Hack The Box – Machine
Write-up: Redacted until box retires.

🧭 Overview
DarkZero is a layered AD challenge that loves split-horizon DNS, linked SQL servers, and Kerberos surprises. It’s a playground for learning realistic enterprise attacks — if you like DNS puzzles, SQL trust chains, and Kerberos trickery, this one’s for you.

🧪 What I Can Share (No Spoilers)
- The hostname resolves to *two* IPs — try resolving against the target DNS. Multi-homed hosts are a clue.  
- MSSQL linked servers are the tasty pivot — the linked context may let you enable `xp_cmdshell`.  
- Local privesc is flaky: try the suggested exploit but have a hash-dump fallback.  
- Rubeus + a UNC trigger (think `xp_dirtree`) is a reliable way to capture tickets or provoke NTLM fallbacks.  
- Tunnel/pivoting tools (ligolo/lligolo) make internal routing painless once you have a foothold.

🧠 Takeaways
- Map names to *all* IPs, not just the one that answered first.  
- Chaining small wins is the key — linked services, local exploits, and Kerberos flows connect the dots.  
- Practice ticket handling and offline conversions (kirbi ⇄ ccache) — it’s worth it.

🖼️ Proofs
DarkZero proof screen — retained privately.

📌 Notes
No walkthrough here by design. When HTB allows public writeups for this machine, I’ll publish a full, defense-aware walkthrough with mitigations and detection notes.

Author: inkedqt • Site: https://inksec.io