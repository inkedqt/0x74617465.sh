---
layout: writeup
name: "Garfield"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Hard"
permalink: /writeups/seasonal/garfield/
os: "HackTheBox"
tags: [seasonal]
date: 2026-05-24
pwned: true
---
# 🐱 Garfield

> **Difficulty:** Hard | **OS:** Windows | **Release:** HTB Season 10

An Active Directory box that takes you through RODC abuse from start to finish. The early chain is straightforward BloodHound enumeration work — the interesting part starts when you land on the RODC and have to understand what makes a Read-Only Domain Controller's krbtgt key different, and how the Key List attack turns RODC-level access into full domain compromise. Not many boxes make you touch this corner of AD.

---

## 📸 Proof
![](garfield.png)

---

## 🧠 Concepts Covered

- BloodHound enumeration and ACL abuse chaining
- SYSVOL logon script deployment via `scriptPath` WRITE permission
- `ForceChangePassword` abuse for lateral movement
- Read-Only Domain Controller (RODC) architecture
- RBCD (Resource-Based Constrained Delegation) S4U exploitation
- RODC-specific `krbtgt_XXXX` account and AES256 key extraction via Mimikatz
- `msDS-RevealOnDemandGroup` and `msDS-NeverRevealGroup` manipulation
- RODC Golden Ticket forging with Rubeus
- Key List attack (`asktgs /keyList`) — using RODC TGT to extract main krbtgt material
- Full domain secrets dump via `secretsdump.py`

---

## 💡 Hints (No Spoilers)

**Foothold**
- You have creds. Run BloodHound. The first interesting edge is a WRITE permission on an AD attribute that controls what runs at logon.
- SYSVOL is writable to you for that share. Place a file there, set the attribute on the target account, and wait for them to "log on."

**User**
- Your new account has a `ForceChangePassword` edge over another account. Use it — that account has WinRM access.

**Root**
- The next target is the RODC. Look at what group membership gives you the delegation path.
- RODC has its own `krbtgt` key (numbered, not the main one). Mimikatz can dump it once you're SYSTEM on the RODC.
- A RODC Golden Ticket isn't a domain Golden Ticket — but it can be used to perform a Key List attack that gets you the real one.
- Read up on `msDS-RevealOnDemandGroup` before you start. You need to add the Administrator account there and clear the never-reveal list.

---

## 📚 Useful Reading

- BloodHound `scriptPath` WRITE abuse — how logon scripts work in AD
- RODC architecture — what `krbtgt_XXXX` is and why it differs from the main krbtgt
- Rubeus `golden /rodcNumber` — RODC Golden Ticket syntax
- Key List attack — `asktgs /enctype:aes256 /keyList` — the Rubeus documentation is the best source
- `msDS-RevealOnDemandGroup` and `msDS-NeverRevealGroup` — RODC attribute documentation
- `secretsdump.py -k` — Kerberos-authenticated secrets dump
