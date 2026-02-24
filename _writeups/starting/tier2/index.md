---
layout: writeup
name: "Tier2"
platform: "HackTheBox"
category: "starting"
difficulty: "Unknown"
date: 2025-11-12
pwned: true
---
# HTB Starting Point - Tier 2 Summary

- ✅ Completed Boxes: - ✅ Archetype - ✅ Oopsie - ✅ Vaccine - ✅ Unified - ✅ Included - ✅ Markup - ✅ Base

---

## Overview

HTB Starting Point Tier 2 builds on the skills of Tier 0 and Tier 1 by introducing more complex web vulnerabilities, horizontal privilege escalation, JWT exploitation, advanced LFI and XXE techniques, and privilege escalation via SUID binaries and misconfigurations.

The goal is to expand your ability to exploit real-world web applications and perform effective post-exploitation on Linux systems.

---

## Box Summaries

**Archetype**  
SMB enumeration → credential reuse → WinRM foothold

**Oopsie**  
File upload vulnerability → RCE via uploaded PHP shell

**Vaccine**  
Local File Inclusion (LFI) → Privilege escalation via sudo misconfiguration

**Unified**  
JWT cracking → Admin access → Reverse shell

**Included**  
XXE injection → LFI → RCE via malicious XML payload

**Markup**  
LFI exploitation → Reading sensitive files → SSH access

**Base**  
Privilege escalation via SUID binary → Root shell

---

## Key Skills Learned

- SMB enumeration and attacking Windows targets
- JWT cracking and abuse
- XXE injection
- Advanced LFI exploitation
- File upload exploitation → RCE
- SUID binary privilege escalation
- Horizontal privilege escalation
- Web application post-exploitation techniques

---

## Lessons Learned

Tier 2 represents a jump in difficulty compared to earlier tiers:

- Many boxes require chaining multiple vulnerabilities (LFI → RCE, XXE → LFI → RCE, JWT → privesc)
- Deeper understanding of Linux privilege escalation techniques (SUID, sudo misconfig, PATH hijacking)
- Realistic web attack chains (JWT, file upload RCE, XXE)
- More post-exploitation focus — not just getting the shell but getting **root** consistently

Completing Tier 2 gives a solid foundation for moving into Retired and Academy boxes where you'll encounter these techniques regularly.

---

*Writeup by inksec*  
*GitHub: [https://github.com/inkedqt]*
