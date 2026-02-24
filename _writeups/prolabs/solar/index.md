---
layout: writeup
name: "Solar"
platform: "HackTheBox"
category: "prolabs"
difficulty: "Intermediate"
permalink: /writeups/prolabs/solar/
os: "Hack The Box  Pro Labs"
date: 2026-02-24
---
# ☀️ Solar — Teaser (inksec.io)

**Platform:** Hack The Box — **Pro Labs**  
**Tier:** Mini Pro Lab  
**Difficulty:** Intermediate–Hard  
**Status:** ⏳ Active — full write-up locked until rotation/retirement  
**Thumbnail:** https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/proofs/solar.png

---

## Summary
Enumeration → situational awareness → FreeBSD exploitation → out-of-band data exfiltration → source code review — tight, chain-heavy lab.

---
## Overview (No Spoilers)

**Solar** is a tight, focused Mini Pro Lab that rewards clean recon and disciplined chaining. Expect a modern web surface backed by BSD-flavored services, light but meaningful source review, and one or two pivots that hinge on *awareness* rather than wordlists. The escalations feel fair: understand the environment, test assumptions safely, and the path opens.

This page is a spoiler-free teaser only. The full walkthrough will publish automatically once the lab rotates/retires.

---

## What You’ll Practice

- **Structured enumeration** across web, service, and host layers without guesswork  
- **BSD basics & service hygiene** (configs, init/rc conventions, users/groups)  
- **Source/code reading** to derive precise inputs instead of fuzzing blindly  
- **Out-of-band thinking** (detecting side effects via collaborator-style checks)  
- **Small-to-big chaining:** turning “minor” findings into meaningful access

---

## Suggested Prep (General, Non-Spoiler)

- Refresh **FreeBSD** fundamentals: `pkg`, `/etc/rc.conf`, service scripts, jails/permissions
- Review common **web hardening** patterns and how to *safely* validate misconfigs
- Have a **local enum checklist** (users, groups, capabilities, scheduled jobs, unusual binaries)
- Be comfortable with **Burp/ffuf/curl** triage and **OAST** (e.g., Collaborator/interactsh) for OOB signals
- Practice converting hints from **code/README/configs** into exact, minimal PoCs

---

## Light-Weight Toolkit

- `nmap` (service/scripts), `curl`/`httpie`, `ffuf`  
- Burp Suite (Intruder/Repeater + Collaborator or interactsh)  
- Grep/awk/jq for quick config & JSON triage  
- A notes template for checklists so you don’t miss pivots

---

## Publication Policy

Per HTB rules, no active-lab solutions are published.  
This page will unlock the full write-up when **Solar** retires. Until then, feel free to bookmark:

**Future full write-up:**  
https://github.com/inkedqt/ctf-writeups/tree/main/HTB/ProLabs/Solar

If the link 404s while the lab is active, that’s expected.

---

## Proofs

- **Completion pop-up:**  
  https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/proofs/solar.png

- **Certificate:**  
  https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/assets/certs/solar_cert.png

---

*No spoilers, just vibes. See you on the other side.* 🛰️
