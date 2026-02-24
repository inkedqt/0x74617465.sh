---
layout: writeup
name: "WhiteRabbit"
platform: "HackTheBox"
category: "active"
difficulty: "Insane"
permalink: /writeups/active/whiterabbit/
os: "Hack The Box"
date: 2025-11-12
---
# 🐇 WhiteRabbit — Teaser (inksec.io)

**Platform:** Hack The Box  
**OS:** Linux  
**Difficulty:** Insane  
**Status:** ⏳ Active — Full write-up locked until retirement  
**Machine Page:** https://app.hackthebox.com/machines/whiterabbit  
**Thumbnail:** https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/whiterabbit.png

---

## Overview (No Spoilers)
WhiteRabbit is a beautifully layered Active Directory-adjacent Linux challenge that rewards *methodical recon* and *careful reading*. Expect to follow subtle breadcrumbs from a seemingly quiet surface into a chain that mixes:
- discovery of “hidden” service views,
- crafting correctly signed requests,
- automating a noisy step to prove a point,
- a clever pivot through backup workflows,
- and a finale that hinges on reasoning about time and randomness.

This page is a teaser only to avoid spoilers while the box is active. The full walkthrough will publish automatically after retirement.

## What You’ll Practice
- **Subdomain & service enumeration** that goes beyond standard wordlists
- **Signed webhook flows** (building/verifying request signatures; tamper‑safe testing)
- **Automating manual checks** (light scripting/extension work to eliminate human error)
- **Backup/restore tooling workflows** and safe data handling
- **Time/PRNG intuition** and reproducible verification techniques

## Suggested Prep (General, Non‑spoiler)
- Review HMAC basics and how signature headers are constructed & validated.
- Brush up on **HTTP tooling** (Burp macros/extensions, curl, Python helpers).
- Get comfortable with **repository‑style backup tools** and snapshot restores.
- Revisit PRNG seeding concepts (C `rand` vs. language libraries) and how time is represented (seconds vs. ms/us).

## Publication Policy
Per HTB rules, we do not publish active‑box solutions. This page will unlock the complete write‑up when WhiteRabbit retires. Until then, you can bookmark this link:

**Future full write‑up:** https://github.com/inkedqt/ctf-writeups/tree/main/HTB/Active/WhiteRabbit

If the link 404s while the box is active, that’s expected.
