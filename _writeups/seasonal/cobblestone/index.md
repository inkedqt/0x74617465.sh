---
layout: writeup
name: "Cobblestone"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Insane"
permalink: /writeups/seasonal/cobblestone/
tags: [Linux, Web Exploitation, XML-RPC Abuse]
date: 2026-02-25
pwned: true
---
# 🏰 Cobblestone (HTB)

**Status:** 🔒 Private – writeup will be published once the machine retires  
**Difficulty:** Insane  
**Category:** Linux | Web Exploitation | XML-RPC Abuse  
**Date Completed:** 2025-08-10  

---

## 🧠 Teaser

What happens when a seemingly harmless game skin site hides an enterprise deployment tool behind closed doors?  
Let’s just say… we found the keys to the castle – and the drawbridge was operated via XML-RPC.

From cracking questionable password choices to tunneling into forgotten services, this box rewards patient enumeration and a willingness to poke at dusty sysadmin tools.

---

## 🪛 Tools You'll Want:

- 🔍 `ffuf` or `feroxbuster` for web content discovery  
- 🐍 `python3` for custom XML-RPC interaction scripts  
- 🪓 `john` for SHA-256 hash cracking  
- 🚇 `ssh -L` for pivoting into internal services  
- 📜 `curl` for quick XML-RPC testing

---

## ✅ You'll Need to:

- 🕵️ Enumerate and find SQL injection points  
- 🗄️ Dump and crack admin hashes  
- 🔐 Use SSH tunneling to expose an internal Cobbler service  
- 📂 Abuse template file fetches to leak sensitive files  
- 👑 Read `/root/root.txt` without ever popping a traditional root shell  

---

📸 **Proof**  
![cobblestone.png](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/cobblestone.png)
