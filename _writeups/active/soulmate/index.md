---
layout: writeup
name: "Soulmate"
platform: "HackTheBox"
category: "active"
difficulty: "Easy"
permalink: /writeups/active/soulmate/
os: "Hack The BoxhttpsapphacktheboxcommachinesSoulmate"
date: 2025-11-12
pwned: true
---
# Soulmate — Hack The Box

![Soulmate Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/soulmate.png)

---

## 📌 Overview

**Machine Name:** Soulmate  
**Difficulty:** Easy  
**OS:** Linux  
**Status:** Active ✅  
**Platform:** [Hack The Box](https://app.hackthebox.com/machines/Soulmate)

---

## 🧩 Summary

Soulmate combined a **CrushFTP exploit** with **custom Erlang components** for an interesting and layered attack path. After discovering **ftp.soulmate.htb**, we leveraged **CVE-2025-31161** to create an **admin user** in CrushFTP and reset existing credentials. With **RCE** achieved via a PHP backdoor, we escalated to **SSH access** and finally abused a **custom Erlang-based login service** to execute system commands as **root**.

---

## 🛠️ Exploit Chain

**Subdomain discovery → CrushFTP admin RCE → password reset → PHP webshell → SSH creds → Erlang shell → root**

---

## 📂 Write-up

🔗 **Full write-up once retired:** [Soulmate on GitHub](https://github.com/inkedqt/ctf-writeups/tree/main/HTB/Retired/Soulmate)

---

**Author:** inkedqt  
**Website:** [https://inksec.io](https://inksec.io)
