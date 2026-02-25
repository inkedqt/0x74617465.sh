---
layout: writeup
name: "Down"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/down/
os: "Hack The Box"
date: 2026-02-25
pwned: true
---

# 🚩 Hack The Box - Down

**Platform:** Hack The Box  
**IP Address:** 10.129.234.87  
**Difficulty:** Easy  
**Status:** ✅ Completed

---

## 🧭 Overview

*Down* is a beginner-friendly box involving a vulnerable website status checker. By exploiting an insecure `curl` usage and bypassing input validation, we achieve a reverse shell. Lateral movement to a user-owned encrypted password manager leads to privilege escalation and root access.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- 10.129.234.87 --min-rate 10000
nmap -p 22,80 10.129.234.87 -sCV -oN nmapscan
```

**Open Ports:**  
- 22/tcp: OpenSSH 8.9p1  
- 80/tcp: Apache 2.4.52

---

## 🌐 Web Analysis

- The web service hosts a site called “Is it down or just me?”  
- Subdomain fuzzing reveals no additional vhosts.
- Input to the site is reflected via `curl`, allowing SSRF and LFI (`file:///etc/passwd`).
- Expert mode reveals a hidden form accepting `IP` and `port`.
- Payload: `443+-e+/bin/bash` allows command injection.

---

## ⚙️ Exploitation

- Reverse shell obtained as `www-data`.
- Enumeration reveals a custom password manager output at:  
  `/home/aleks/.local/share/pswm/pswm`

---

## 🔑 Cracking Credentials

- The encrypted secrets are decrypted using a GitHub decryptor.
- Password: `flower`, Final creds: `aleks:1uY3w22uc-Wr{xNHR~+E`

---

## ⬆️ Privilege Escalation

- `aleks` has full sudo rights (`sudo -l` shows ALL).
- Root shell obtained with `sudo su -`.

---

## 🏁 Flags

- **User:** `d4bc94b386ef7c8113698a8c4951cacd`
- **Root:** `87bb9869a311b8abb5fb4d3c7248fdcb`

---

![Down Screenshot](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/down.png)
