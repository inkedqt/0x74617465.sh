---
layout: writeup
name: "Hercules"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Insane"
date: 2025-11-12
pwned: true
---
# Hercules — HTB Seasonal (Windows) — Teaser

**Difficulty:** Insane  
**Skills:** AD ACL abuse, PowerShell / PowerView, PKI & AD CS, Cert enrollment (on-behalf-of), Kerberos (PKINIT, ccaches, S4U/S4U2Proxy), Impacket/Impacket-style tooling, WinRM lateral movement.  
**Box type:** Windows (Active Directory / PKI / Kerberos / WinRM)

## Short pitch
Hercules is a brutal, identity-first Active Directory puzzle that rewards careful enumeration and creative abuse of AD permissions and certificates. You’ll weave ACL modifications, certificate enrollment, and Kerberos trickery into an identity choreography that turns low-privilege access into domain control.

## What you'll do (high level, non-spoiler)
- Start from a foothold and enumerate AD object ACLs, SPNs and certificate templates.  
- Exploit delegated rights on an OU to enable/modify accounts and reset credentials.  
- Use certificate enrollment (including on-behalf-of flows) to obtain PFXs for other users; convert certs into Kerberos material (PKINIT / ccache).  
- Request and inspect TGTs/service tickets, then abuse those tickets to authenticate to WinRM (Kerberos or client-cert) and gain shell.  
- Use impersonation/S4U/S4U2Proxy and service account manipulation to escalate to domain privileges and own the box.

## Why it’s fun / what you'll learn
This box is a deep dive into modern AD identity mechanics. You’ll practice:
- Reading and abusing AD ACLs to create practical escalation pivots.  
- Working with AD CS: templates, DCOM/RPC enrollment, and on-behalf-of request flows.  
- Turning certificates into Kerberos auth (PKINIT, ccaches) and using them for lateral movement.  
- Realistic post-exploitation where the important asset is *who* you are, not just what binary you run.

## Gentle hints
- Inspect ACLs thoroughly — one WriteProperty/GenericAll on the right object is worth far more than a dozen host exploits.  
- Certificate templates and CA permissions are first-class attack surfaces; “on-behalf-of” enrollment can be abused when ACLs are too permissive.  
- Converting a PFX into a usable auth artifact (PEM → PKINIT → ccache) is a core skill here — practice the workflow.  
- Watch Kerberos error messages (AP_REQ failures, “server not found in Kerberos database”, revoked credentials) — they reveal exactly what’s wrong.  
- WinRM on HTTPS often accepts either Kerberos/SPNEGO or client-cert auth — try both if one fails.

## Path outline (non-spoilery sequence)
1. Enumerate AD, SPNs and certificate infrastructure; find where delegated rights exist.  
2. Use delegated rights to enable or reset an account and obtain a fresh TGT/ccache.  
3. Request a certificate (possibly on-behalf-of another user) and export it to a PFX.  
4. Convert PFX → PEM → PKINIT to get a usable ccache / TGT, or use the PFX to auth direct to WinRM.  
5. Use the ticket/cert to access WinRM, pivot, then abuse S4U or service account flows to impersonate higher-privilege principals and get the domain flag.

## Starting hints (CTF)
- PowerView / PowerShell enumeration is valuable for ACL discovery (the box responds well to `Get-AD*` and `dsacls` style probes).  
- Certipy / Impacket are useful in the PKI + Kerberos phases — learn the `req`, `shadow`, `auth` and `getTGT` patterns.  
- Expect to create and consume ccaches (TGT files) and PFXs during the exploit chain.

## Example tooling you’ll probably use
PowerView / PowerShell, Certipy, Impacket (GetTGT/GetST/changepasswd), `kinit` / `klist`, `evil-winrm` (cert or Kerberos), and small PowerShell helpers for ACL changes.

## Final note
Hercules is designed for players who enjoy thinking in identities and permissions. If you like AD puzzles where the exploit surface is permission/attribute choreography (not just CVEs), this box will reward patient, methodical play. Bring your Kerberos and PKI playbooks — you’ll need them.
