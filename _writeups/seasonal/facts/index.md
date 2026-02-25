---
layout: writeup
name: "Facts"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Easy"
permalink: /writeups/seasonal/facts/
os: "Linux"
tags: [Web, IDOR, Object Storage, SSH Key Cracking, Sudo Exploitation]
date: 2026-02-25
pwned: true
---
# 📊 Facts – HTB Seasonal

**Status:** 🔒 Private – writeup will be published once the machine retires  
**Difficulty:** Easy  
**Platform:** Linux  
**Category:** Web | IDOR | Object Storage | SSH Key Cracking | Sudo Exploitation

---

## 🧠 Teaser

Facts is a straightforward but well-designed box that demonstrates how seemingly minor access control issues can cascade into full compromise when cloud storage integrations are involved.

The initial foothold centers on a Camaleon CMS instance with a classic vulnerability: an Insecure Direct Object Reference (IDOR) in the user profile management system. What makes this interesting isn't the IDOR itself—it's what it unlocks. Escalating from a low-privilege client account to administrator reveals the real prize: hardcoded S3-compatible storage credentials exposed in the CMS configuration panel.

With those credentials in hand, you gain access to MinIO—an S3-compatible object storage service running on a non-standard port. The challenge shifts from web exploitation to cloud enumeration: navigating buckets, discovering internal data stores, and extracting sensitive files that were never meant to be externally accessible.

The path to root is refreshingly simple once you have initial access, centering on a sudo misconfiguration that permits execution of a fact-gathering utility with arbitrary code execution capabilities. It's a reminder that privilege escalation doesn't always require kernel exploits—sometimes it just requires knowing what your tools can really do.

---

## 🪛 Tools You'll Want (High-Level)

```
🌐 Web application enumeration and directory fuzzing
🔍 Understanding of IDOR vulnerabilities
☁️ AWS CLI familiarity (works with S3-compatible storage)
🔐 SSH key passphrase cracking (John the Ripper)
🧠 Knowledge of Ruby-based fact gathering tools
🔓 Sudo privilege escalation techniques
```

This box rewards systematic enumeration and cloud storage navigation skills.

---

## ✅ You'll Need To:

```
🔎 Enumerate web application for CMS identification and version detection
🔓 Exploit IDOR vulnerability to escalate user privileges within the CMS
🗝️ Extract cloud storage credentials from admin configuration panels
☁️ Enumerate and navigate S3-compatible MinIO buckets using AWS CLI
📥 Download sensitive files from internal object storage buckets
🔑 Crack passphrase-protected SSH private keys
🚀 Exploit sudo permissions on fact-gathering utilities for privilege escalation
```

---

## 🧠 Takeaways

```
- Client-side disabled form controls are not security boundaries—validation must happen server-side
- IDOR vulnerabilities in parameter-based endpoints can often be bypassed through alternate request paths
- CMS configuration panels frequently store cloud storage credentials in plaintext
- S3-compatible storage (MinIO, Minio, etc.) exposes the same API surface as AWS S3
- Internal buckets in object storage often contain sensitive data not intended for public access
- SSH keys stored in cloud object storage should be treated as compromised if credentials leak
- Fact-gathering utilities like Facter can execute arbitrary code through custom fact definitions
- Sudo permissions on scripting-friendly utilities are often unintentional privilege escalation vectors
```

Facts demonstrates a realistic attack chain: web vulnerability → credential disclosure → cloud storage access → SSH foothold → sudo misconfiguration. It's a clean progression that mirrors real-world scenarios where cloud integrations introduce new attack surfaces, and where initial compromises lead to deeper access through chained misconfigurations.

---

## 📸 Proof

![Facts Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/facts.png)