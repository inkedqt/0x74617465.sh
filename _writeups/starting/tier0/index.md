---
layout: writeup
name: "Tier0"
platform: "HackTheBox"
category: "starting"
difficulty: "Unknown"
permalink: /writeups/starting/tier0/
date: 2026-02-25
pwned: true
---

# HTB Starting Point - Tier 0 Summary

-✅ Completed Boxes:
-✅ Meow
-✅ Fawn
-✅ Dancing
-✅ Redeemer
-✅ Explosion
-✅ Preignition
-✅ Mongod
-✅ Synced

---

## Overview

**HTB Starting Point Tier 0** is the first tier of Hack The Box's beginner learning path. These boxes teach foundational skills needed to enumerate and exploit basic services. The goal is to build fluency with common tools and techniques used in later, harder boxes.

---

## Box Summaries

### Meow
- Telnet enumeration  
- Banner grabbing  
- Simple unauthenticated flag retrieval  

### Fawn
- Anonymous FTP enumeration  
- File retrieval  

### Dancing
- SMB share enumeration  
- `smbclient` usage to download files  

### Redeemer
- Redis enumeration (`redis-cli`)  
- Accessing exposed Redis instance  

### Explosion
- Brute-forcing password-protected zip file (`zip2john`, `john`)  
- Extracting and reading files  

### Preignition
- Web fuzzing (`gobuster`)  
- Discovering hidden directories / pages  

### Mongod
- MongoDB enumeration (`mongo` CLI)  
- Reading unprotected MongoDB collections  

### Synced
- Rsync enumeration (`rsync` CLI)  
- Listing and downloading files from exposed rsync module  

---

## Key Skills Learned

- Service enumeration (Telnet, FTP, SMB, Redis, MongoDB, Rsync)
- Web fuzzing basics
- Password cracking basics (zip files)
- Initial exposure to database enumeration
- Core CLI tools: `nmap`, `gobuster`, `redis-cli`, `mongo`, `smbclient`, `rsync`, `john`

---

## Lessons Learned

Tier 0 provides essential enumeration muscle memory for many real-world services you will continue to encounter in CTFs and pentests:
- Exposed services with no auth
- Poorly configured default installations
- Simple privilege escalation via misconfigurations

These boxes were fast but highly educational. They form a strong base for moving into more challenging boxes.

---

*Writeup by inksec*  
*GitHub: [https://github.com/inkedqt](https://github.com/inkedqt)*
