---
layout: writeup
name: "CodePartTwo"
platform: "HackTheBox"
category: "active"
difficulty: "Medium"
permalink: /writeups/active/codeparttwo/
os: "Hack The Box"
date: 2025-11-12
---
# 🧩 CodeTwo — Teaser (inksec.io)

**Platform:** Hack The Box  
**OS:** Linux  
**Difficulty:** Medium (community consensus may vary)  
**Status:** ⏳ Active — Full write-up locked until retirement  
**Machine Page:** https://app.hackthebox.com/machines/CodeTwo  
**Thumbnail:** https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/codeparttwo.png

---

## Overview (No Spoilers)
**CodeTwo** is a modern web application challenge that rewards careful reading, disciplined testing, and a calm approach to “features” that look helpful but may hide sharp edges. Expect to think like a developer and an operator: understand how components interact, what boundaries are intended, and how small oversights can add up.

This page is a *teaser only* to avoid spoilers while the box is active. The full walkthrough will publish after retirement.

---

## What You’ll Practice
- Targeted web enumeration and request analysis
- Reading application behavior to infer trust boundaries
- Safe handling of credentials/tokens and basic database hygiene
- Post-access discipline: validating assumptions before escalation
- General Linux privesc mindset (services, configs, hooks, and logs)

---

## Suggested Prep (General, Non‑spoiler)
- Refresh HTTP tooling (browser devtools, curl, Burp/ffuf basics)  
- Brush up on Python/web‑app review and common auth/session pitfalls  
- Review a standard Linux privilege‑escalation checklist (services, timers, backups, PATH/use of sudo)  
- Practice keeping notes and reproducing steps cleanly

---

## Publication Policy
Per HTB rules, we don’t publish active‑box solutions. This page will unlock the complete write‑up when **CodeTwo** retires. Until then, you can bookmark this link:

**Future full write‑up:** https://github.com/inkedqt/ctf-writeups/tree/main/HTB/CodePartTwo

> If the link 404s while the box is active, that’s expected.

---

## Credits
Author: **inkedqt** — https://inksec.io
