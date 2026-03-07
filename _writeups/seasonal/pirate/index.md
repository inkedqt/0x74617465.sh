---
layout: writeup
name: "Pirate"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Hard"
permalink: /writeups/seasonal/pirate/
os: "Windows"
date: 2026-03-08
pwned: true
---
## Summary
Pre2k misconfiguration → default machine account creds → ReadGMSAPassword → gMSA hash → ligolo-ng pivot → NTLM coercion + SMB→LDAP relay → Shadow Credentials → RBCD → LSA dump → ForceChangePassword → WriteSPN + KCD protocol transition → SPN hijack → S4U2Proxy → Domain Admin.
# 🩸 HTB — Pirate | Hard | Windows (Active Directory)

_No spoilers. Just vibes, nudges, and the occasional raised eyebrow._

---

## 📸 Proof

![Pirate Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/pirate.png)

---

## 🖼️ The Vibe

A fully exposed Active Directory domain controller is waiting for you — and it's been around long enough to carry some legacy baggage. This box is a love letter to real-world AD pentesting: no exotic CVEs, no magic tricks. Just methodical enumeration, credential chains, and a finale that requires you to actually understand how Kerberos delegation works under the hood. Every step follows naturally from the last. If you're lost, you haven't enumerated hard enough.

---

## 🗺️ The Path (Spoiler-Free)

### 🔎 Recon

You're handed initial credentials. Use them.

Start with a port scan and let the results sink in — you'll see the full picture of a Windows domain immediately. Take note of what's _signing_ and what isn't. That gap matters later.

> "LDAP and SMB are not the same. One of them has its guard up."

Add the domain and DC hostname to `/etc/hosts`. Then run your standard AD enumeration toolkit: users, SPNs, group memberships. You'll find a suspiciously familiar naming pattern among some accounts.

**Hint:** Two users share a surname. One of them has an `_adm` suffix. File that away.

**Hint 2:** Kerberoasting will yield hashes. Don't spend too long on them — a locked door isn't always the right door.

---

### 🔑 Foothold — Pre-Windows 2000 Compatible Access

This is where the box earns its name.

> "What happens when a domain still trusts computers like it's 1999?"

There's a legacy group that grants broad directory read permissions. In modern domains it's usually harmless. Here, it's been applied with a very generous hand. Use a modern tool that has a dedicated module for finding exactly this class of misconfiguration — and look at what accounts are affected.

**Hint:** Pre-created computer accounts have a very predictable default password. The clue is literally in the account name.

**Hint 2:** Once you have machine account access, think about what privileged service accounts that machine might be allowed to read. Group Managed Service Accounts exist for a reason.

---

### 🏃 Lateral Movement — Into the Intranet

You now have a foothold on the DC. But there's more network here than meets the eye.

> "One NIC is never the whole story."

Run an internal scan. There's a second host hiding on an internal subnet. Set up a tunnel to reach it, then start fresh recon against that new target.

Check which machines have SMB signing enforced — and which ones don't. That asymmetry is the entire premise of your next move.

**Hint:** NTLM authentication can be intercepted and redirected. SMB auth from an unsigned host can be relayed somewhere useful. You'll need a listener, a coercion trigger, and patience.

**Hint 2:** Once you have an LDAP shell, think about what attributes you can write to computer objects. Shadow credentials are a thing.

---

### 🧗 User Flag

You've climbed high enough to dump secrets from your beachhead machine. The user flag isn't where you'd expect it.

> "Administrators don't always get the good stuff. Sometimes you have to look in a colleague's bedroom."

Check what plaintext credentials came out of your secrets dump. One of them opens a door that BloodHound already told you about.

---

### 👑 Root — AD ACL Abuse + Delegation Gymnastics

This is the payoff. Everything you've built leads here.

You have a privileged user with a very interesting delegation setting. Not RBCD — the other kind. The dangerous kind, where protocol transition means you don't need a victim's Kerberos ticket to impersonate them.

> "She's allowed to act on behalf of anyone, to a specific service. The question is: _whose_ service is that, exactly?"

The HTTP SPN is registered on the wrong machine for your purposes. AD is a database. Databases can be edited. You have write permissions.

Move the SPN. Then ask the KDC very nicely for a service ticket to somewhere else entirely.

**Hint:** `getST.py` has an `-altservice` flag. Read what it does carefully. This is the trick that turns a ticket for one thing into a ticket for another — as long as the encryption key lines up.

**Hint 2:** The entire attack chain is: WriteSPN → SPN migration → S4U2Self + S4U2Proxy → altservice rewrite → DC compromise. Each link connects logically to the next.

---

## 🧠 Skills This Box Will Test

- Pre-Windows 2000 misconfiguration enumeration and exploitation
- Group Managed Service Account (gMSA) password retrieval
- Kerberos time skew handling in real engagements
- NTLM coercion and cross-protocol relay (SMB → LDAP)
- Shadow Credentials / Pass-the-Certificate
- RBCD self-delegation via machine account
- Active Directory ACL abuse (ForceChangePassword, WriteSPN)
- Kerberos Constrained Delegation with Protocol Transition
- SPN hijacking for cross-host privilege escalation

---

## 💬 Parting Words

> _"She has constrained delegation with protocol transition. He moved the SPN. The KDC didn't notice. Domain Admin arrived quietly."_

If you're stuck at the relay step — check your MIC. If you're stuck at delegation — check whether protocol transition is in play. If you're stuck at the SPN step — remember that SPNs must be unique, and uniqueness means ownership can be transferred.

This box is a masterclass in chaining AD primitives. Each step is well-documented in the wild. The skill isn't knowing one technique — it's recognising which ones connect.

Good luck. Stay methodical. 🖤