---
layout: writeup
name: "DarkCorp"
platform: "HackTheBox"
category: "active"
difficulty: "Insane"
os: "Hack The Box"
date: 2025-11-12
---
# 🕴️ DarkCorp — Teaser (inksec.io)
**Platform:** Hack The Box  
**OS:** Windows  
**Difficulty:** Insane  
**Status:** ⏳ Active — Full write-up locked until retirement  
**Machine Page:** https://app.hackthebox.com/machines/DarkCorp  
**Thumbnail:** https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/darkcorp.png

## Overview (No Spoilers)
DarkCorp feels like a mini‑enterprise: a public‑facing service that leads into a segmented internal environment and, eventually, a mature identity stack. It rewards slow, disciplined recon, reading between the lines of “helpful” features, and confidently moving between web, network, and auth contexts without breaking the chain.

This page is a teaser only to avoid spoilers while the box is active; the full walkthrough will publish after retirement.

## What You’ll Practice
- Careful web recon and safe interaction with user‑facing workflows  
- Turning small information leaks into directional leads  
- Clean, auditable lateral movement across a constrained network segment  
- Identity & ticketing fundamentals (concepts, not tricks) in an AD environment  
- Staying organized across a long, multi‑stage chain

## Suggested Prep (General, Non‑spoiler)
- Refresh HTTP basics (headers, cookies, forms) and common portal behaviors  
- Brush up on SQL fundamentals and reading application config conventions  
- Review Kerberos/AD concepts at a high level (TGT/TGS, SPNs, delegation models)  
- Have a notes‑first workflow for pivoting: hosts file hygiene, tunnels/proxies, and credential handling

## Mindset Hints (Non‑spoiler)
- When a UI says “we’ll contact you,” assume there’s a trail you can observe—ethically.  
- Treat “internal” as “document everything”: names, services, and who talks to whom.  
- Keep certs, tickets, and caches tidy; small operational slips can cost you later.

## Publication Policy
Per HTB rules, no active‑box solutions here. This page will unlock the complete write‑up after DarkCorp retires. Until then, keep your working notes in the private repo path you use for active boxes.
