---
layout: writeup
name: "Mirage"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Hard"
tags: [Active Directory, Windows, Kerberos, Certificates]
date: 2025-11-12
pwned: true
---
🌀 Mirage (HTB Seasonal)

Status: 🔒 Private – writeup will be published once the machine retires  
Difficulty: Hard  
Category: Active Directory | Windows | Kerberos | Certificates  
Date Completed: 2025-07-25

🧠 Teaser

A deceptive illusion hides behind a seemingly quiet domain...

Can you see through the Mirage and trace the attack path from anonymous enumeration to full domain compromise?

🪛 Tools You'll Want:

- 🦊 Impacket (GetNPUsers.py, getST.py, secretsdump.py)
- 📜 Certipy
- 🧠 BloodHound + SharpHound
- 🧾 Mimikatz / Rubeus for ticket insights
- 🗝️ Kerberos ccache for Evil-WinRM

You'll need to:

- 🕵️ Extract TGTs with AS-REP roasting
- 🔓 Crack Kerberos hashes with john/hashcat
- 🔁 Abuse shadow credentials + ESC1 template misconfig
- 📜 Mint forged certs and impersonate DA
- 👑 DCSync or SMB hash retrieval for domain takeover

📸 Proof  
![Mirage Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/mirage.png)
