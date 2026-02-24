---
layout: writeup
name: "Tier1"
platform: "HackTheBox"
category: "starting"
difficulty: "Unknown"
permalink: /writeups/starting/tier1/
date: 2025-11-12
pwned: true
---
# HTB Starting Point - Tier 1 Summary

-✅ Completed Boxes:
-✅ Appointment
-✅ Sequel
-✅ Crocodile
-✅ Responder
-✅ Three
-✅ Ignition
-✅ Bike
-✅ Funnel
-✅ Pennyworth
-✅ Tactics

---

## Overview

**HTB Starting Point Tier 1** expands on Tier 0 by introducing more web exploitation, privilege escalation, and real-world lateral movement techniques. These boxes are still beginner-friendly but include valuable concepts like exploiting weak credentials, abusing misconfigured services, and extracting secrets from web apps and network traffic.

---

## Box Summaries

### Appointment
- Web enumeration
- Path traversal & sensitive file read  
- Intro to information disclosure via weak web security

### Sequel
- SQL injection exploitation
- Extracting database credentials  
- Using SQLi to gain shell access

### Crocodile
- Weak FTP credentials  
- File discovery via FTP  
- SSH login with found credentials

### Responder
- SMB relay / NBNS spoofing  
- Capturing and cracking NTLM hashes  
- Introduction to Responder tool

### Three
- HTTP Basic Auth brute force  
- Credential reuse across services  
- SSH login → user shell

### Ignition
- Web fuzzing → file upload  
- PHP reverse shell through upload  
- Web shell → user shell

### Bike
- Default web app credentials  
- RCE via command injection in web app  
- Privilege escalation via SUID binaries

### Funnel
- Directory brute force  
- File upload vulnerability  
- Web shell → privilege escalation using weak sudo rights

### Pennyworth
- SMB enumeration  
- Credential reuse  
- Privilege escalation via weak sudo configuration

### Tactics
- Cracking stored Windows hashes  
- Exploiting password reuse  
- Gaining shell via cracked credentials

---

## Key Skills Learned

- SQL injection  
- SMB enumeration & hash cracking  
- RCE via file upload  
- Web fuzzing & dir brute force  
- Privilege escalation via sudo / SUID  
- Responder & network-level attacks  
- Credential reuse exploitation  
- Windows hash cracking basics

---

## Lessons Learned

Tier 1 introduces "real-world" style attacks:
- Password reuse is rampant → always test across services
- SQL injection is still extremely common
- RCE through file upload is a critical threat
- SMB is a treasure trove in internal pentests
- Responder provides a fast path to NTLM hashes
- Privilege escalation relies heavily on enumeration and creativity

Tier 1 boxes are easy but excellent for building **methodical habits** and improving **tool fluency**:
- `nmap`, `gobuster`, `smbclient`, `sqlmap`, `john`, `Responder`, `wfuzz`, `hydra`, `linpeas`

---

*Writeup by inksec*  
*GitHub: [https://github.com/inkedqt](https://github.com/inkedqt)*