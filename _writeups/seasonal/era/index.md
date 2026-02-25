---
layout: writeup
name: "Era"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/era/
tags: [Linux, Web Exploitation, Binary Analysis]
date: 2026-02-25
pwned: true
---

🕰️ **Era** (HTB Seasonal)

**Status:** 🔒 Private – writeup will be published once the machine retires  
**Difficulty:** Medium  
**Category:** Linux | Web Exploitation | Binary Analysis  
**Date Completed:** 2025-07-27

---

🧠 **Teaser**

What happens when a legacy service meets modern laziness?

A misconfigured file handler, forgotten admin endpoints, and weak password hygiene open the door — but to **root this box**, you'll need to understand how custom binaries are signed and validated in production.

---

🪛 **Tools You'll Want:**

- 🔍 `feroxbuster` or `ffuf` for virtual hosts and hidden paths  
- 🐍 Python + BeautifulSoup for fast endpoint enumeration  
- 🧾 `sqlite3` for user data analysis  
- 🪓 `john` for bcrypt hash cracking  
- ⚙️ `gcc` and `objcopy` for crafting signed ELF binaries  
- 🔏 `openssl asn1parse` to reforge binary integrity  

---

✅ You'll need to:

- 🕵️ Enumerate hidden subdomains and brute force download IDs  
- 🧠 Identify security bypass via SSRF-style payload  
- 📦 Unpack database dumps to harvest real creds  
- 👤 Abuse security question resets to hijack admin accounts  
- 💥 Upload a persistent payload and trigger a monitored executable  
- 🧬 Recompile a binary to preserve its signature check and gain root  

---

📸 **Proof**  
![Era Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/era.png)
