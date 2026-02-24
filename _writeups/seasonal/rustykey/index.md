---
layout: writeup
name: "Rustykey"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Hard"
permalink: /writeups/seasonal/rustykey/
tags: [Active Directory, Windows, Kerberos, RBCD]
date: 2025-11-12
pwned: true
---
# 🗝️ RustyKey (HTB Seasonal)

**Status:** 🔒 Private – writeup will be published once the machine retires  
**Difficulty:** Hard  
**Category:** Active Directory | Windows | Kerberos | RBCD  
**Date Completed:** 2025-06-29

---

## 🧠 Teaser

A domain full of policies, delegation edge cases, and a rusty trust chain...

Can you untangle a messy AD forest where *support is protected*, but *old credentials remain dangerous*?

🪛 Bring your favorite tools:
- 🩸 BloodHound
- 🧪 SharpHound
- 🛠️ RunasCs
- 🗂️ ccache + Kerberos S4U
- ⚙️ Impacket's `getST.py`, `smbexec.py`

You'll need to:
- Identify a misconfigured delegation edge 🕵️
- Abuse **GenericWrite** and **ForceChangePassword** 💥
- Evade *Protected Users* 🤫
- Chain it all for **Domain Admin**

---

## 📸 Proof

![RustyKey Proof] <img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/rustykey.png" />

---

📌 Full writeup will be published [here](https://github.com/inkedqt/ctf-writeups/tree/main/HTB/Seasonal/RustyKey) when the box is retired.
