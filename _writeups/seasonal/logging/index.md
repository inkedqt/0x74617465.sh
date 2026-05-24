---
layout: writeup
name: "Logging"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/logging/
os: "HackTheBox"
tags: [seasonal]
date: 2026-05-24
pwned: true
---
# 📋 Logging

> **Difficulty:** Medium | **OS:** Windows | **Release:** HTB Season 10

A Windows AD box that leans into the logging theme — the foothold credential is sitting in a trace log on an SMB share someone left world-readable. The root path is a rogue WSUS attack, which is rare enough in CTF that it's worth doing just for the methodology. In between there's Shadow Credentials, a DLL hijack, and an ADCS template abuse. Busy box with a satisfying finish.

---

## 📸 Proof
![](logging.png)

---

## 🧠 Concepts Covered

- SMB share enumeration and log file credential recovery
- Expired password rotation (year-increment pattern)
- Kerberos-only authentication (NTLM blocked, `getTGT.py` workflow)
- Shadow Credentials attack via `GenericWrite` on an MSA
- PKINIT authentication and NT hash recovery
- DLL hijack via writable `ProgramData` directory
- ADCS ESC17 — Enrollee Supplies Subject + Server Authentication EKU
- ADIDNS record injection (`bloodyAD add dnsRecord`)
- Rogue WSUS server via `wsuks` (WSUS MITM tool)
- Serving a signed binary payload through the rogue update server

---

## 💡 Hints (No Spoilers)

**Foothold**
- Enumerate SMB shares with your initial creds. One share has log files. Read them — application trace logs often contain credentials in cleartext.
- The account you find may have an expired password. The expiry pattern is obvious once you see it.
- NTLM auth will fail on this domain. Use `getTGT.py` and `KRB5CCNAME` for everything.

**User**
- BloodHound will show a `GenericWrite` path to a Managed Service Account. Shadow Credentials is the move.
- The MSA you compromise has WinRM access. From there, look at what binary runs periodically and where it loads DLLs from.
- The `ProgramData` path for that service is writable by your group. Drop a DLL there.

**Root**
- Your new user is in IT. Check `bloodyAD get writable` — you have DNS write access.
- Certipy will find a certificate template with both Enrollee Supplies Subject and Server Authentication EKU enrollable by your group. Request a cert for `wsus.[domain]`.
- Add that DNS record pointing to your IP. Then bring up a rogue WSUS server with `wsuks`. The payload command runs as the account that processes Windows Update.

---

## 📚 Useful Reading

- Shadow Credentials attack — `bloodyAD add shadowCredentials`, `pywhisker`
- ADCS ESC17 — Server Authentication EKU + Enrollee Supplies Subject abuse
- ADIDNS injection — `bloodyAD add dnsRecord` syntax and requirements
- `wsuks` — WSUS MITM tool by NeffIsBack (GitHub)
- Rogue WSUS methodology — how Windows Update clients validate update servers
- DLL hijack via `ProgramData` writable paths
