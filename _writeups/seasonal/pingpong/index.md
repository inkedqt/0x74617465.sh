---
layout: writeup
name: "PingPong"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Insane"
permalink: /writeups/seasonal/pingpong/
os: "HackTheBox"
tags: [seasonal]
date: 2026-05-24
pwned: true
---
# 🏓 PingPong

> **Difficulty:** Insane | **OS:** Windows | **Release:** HTB Season 10

A two-forest Active Directory box that lives up to the Insane rating. The core mechanic is a bidirectional trust between `PING.HTB` and `PONG.HTB` — every major step involves crossing or exploiting that trust. You'll touch ESC13, JEA jail-breaking, cross-domain gMSA abuse, RBCD to MSSQL, GodPotato, DCSync, and finally ESC4 into ESC1 to close the forest loop. A lot of distinct techniques stacked end to end — none of the individual steps are especially obscure, but you need all of them.

---

## 📸 Proof
![](pingpong.png)

---

## 🧠 Concepts Covered

- ADCS ESC13 — issuance policy OID linked to a security group granting WinRM
- Cross-domain gMSA abuse via group type coercion (Global → Universal → DomainLocal)
- Foreign security principal group membership across a bidirectional forest trust
- JEA (Just Enough Administration) `RestrictedRemoteServer` endpoint enumeration
- PowerShell call operator `&` to escape constrained JEA command surface
- `pypsrp` — Python PSRP client for named WinRM session configurations
- PSReadLine `ConsoleHost_history.txt` credential recovery
- RBCD (Resource-Based Constrained Delegation) against a service account
- S4U2Proxy impersonation to MSSQL with `mssqlclient.py`
- `xp_cmdshell` + `SeImpersonatePrivilege` + GodPotato for local privilege escalation
- DCSync via Impacket `secretsdump.py`
- ADCS ESC4 — abusing template write control to reconfigure a safe template
- ESC1 abuse post-ESC4 modification for cross-domain Administrator certificate

---

## 💡 Hints (No Spoilers)

**Foothold**
- Your initial creds are Kerberos-only. NTLM won't work anywhere.
- Certipy will find a certificate template with an issuance policy. Look up what ESC13 is — the OID links to a group, and that group grants something useful.
- You're not enrolling a cert to get a shell — you're enrolling to get added to a group.

**User (PING → PONG)**
- BloodHound on both domains. You have an Owns edge that crosses the trust. The target is a group, and group types matter when it comes to foreign principal membership.
- Global groups can't have foreign members. DomainLocal groups can. There's a conversion path.
- Once you have the gMSA hash, evil-winrm alone won't work — the WinRM endpoint is a restricted JEA session. You need `pypsrp` and the configuration name.
- The JEA endpoint has almost no commands. The call operator `&` is not a command — it's an operator, and it still works.
- As Pong_gMSA$, check the PSReadLine history. Someone typed a password in plaintext.

**Root (PONG → PING)**
- c.carlssen has GenericWrite on service accounts. Only one of them has SQL Admin Rights. RBCD lets you impersonate a DA-group member against that service.
- SeImpersonatePrivilege in the SQL shell means local admin via potato. Add yourself to Administrators, then DCSync.
- The DCSync output has R.Martinelli's AES256 key. That user is the cross-domain link you need back to PING.
- R.Martinelli is in CA Managers@PING.HTB, which has write control over a certificate template. Modify it to be ESC1-vulnerable, then enroll as Administrator@ping.htb.

---

## 📚 Useful Reading

- ADCS ESC13 — issuance policy OID to group mapping
- ADCS ESC4 — certificate template write control abuse
- Cross-domain group type coercion — Global/Universal/DomainLocal and foreign principals
- JEA architecture — `.pssc` files, `RestrictedRemoteServer`, `ConstrainedLanguage`
- `pypsrp` — Python PSRP client, `RunspacePool(configuration_name=...)`
- RBCD with existing machine accounts — reusing a gMSA when `MachineAccountQuota = 0`
- GodPotato — `SeImpersonatePrivilege` exploitation on modern Windows
- Rubeus / Impacket `getST.py` — S4U2self + S4U2proxy workflow
