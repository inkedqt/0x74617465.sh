---
layout: writeup
name: "Signed"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/signed/
date: 2025-11-12
pwned: true
---
# Signed — Hack The Box (Seasonal) — Teaser

**Difficulty:** Medium  
**Skills:** MSSQL enumeration & extended procedures, NTLM hash capture & cracking, Kerberos silver-ticket forging, `OPENROWSET` / `xp_cmdshell` abuse, SID/RID handling.  
**Box type:** Windows (MS SQL / Kerberos / Active Directory)

---

## Short pitch
An exposed Microsoft SQL Server hides an AD-backed escalation path: trigger an SMB callback from the database, capture and crack the MSSQL service NTLM hash, then forge Kerberos credentials that assert elevated group membership to gain `sysadmin` on the database and abuse SQL features to read sensitive files and pivot to the domain.

---

## What you'll do (high level, non-spoiler)
- Enumerate the MSSQL service and check for extended procedures (e.g. `xp_dirtree`, `xp_cmdshell`).
- Trigger an SMB callback from SQL Server to capture the service NTLMv2 hash and crack it locally.
- Convert hex SID output to `S-1-...` format and collect domain SID + relevant RIDs.
- Forge a Kerberos **silver ticket** for the MSSQL SPN using the cracked service NT hash and claim elevated group membership.
- Use the forged ticket to connect and gain `dbo/sysadmin`, then use `xp_cmdshell` or `OPENROWSET` to retrieve flags and sensitive files.

---

## Why it's fun / what you'll learn
This box ties together core Windows authentication mechanics: SQL extended procedures, NTLM capture and cracking, and Kerberos ticket forging. It’s an excellent hands-on lab for understanding how service account secrets + AD SIDs can be combined to produce powerful forged tickets and domain pivots.

---

## Gentle hints
- Look for available `xp_*` extended procedures and whether your account has `EXECUTE` permission on them.
- An SMB listener (Responder, Impacket's smbserver, or similar) is a reliable way to capture the service NTLMv2.
- SQL often returns SIDs in hex — convert those to `S-1-...` before feeding them into Kerberos tooling.
- If `xp_cmdshell` is disabled, `OPENROWSET(BULK...)` and ad-hoc SQL features can still be useful once elevated.

---

## Starting credentials (CTF)
`scott : Sm230#C5NatH` — useful to begin MSSQL enumeration.

---

> **Reminder:** Only run these steps against machines you own or are authorised to test (CTF/lab environments). Unauthorized testing against production or third-party systems is illegal and unethical.
