---
layout: writeup
name: "Sau"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
permalink: /writeups/retired/sau/
os: "Linux"
date: 2025-11-12
pwned: true
---
# Sau – Hack The Box

**Machine IP:** _Retired Box_  
**Difficulty:** Easy  
**OS:** Linux  
**Date Completed:** 2025-07-31  
**Tags:** SSRF, CVE-2023-27163, Maltrail, OS Command Injection, Sudo Misconfiguration  

---

## 🧭 Overview

Sau is an easy Linux machine featuring an instance of [Request Baskets](https://github.com/darklynx/request-baskets) vulnerable to SSRF (CVE-2023-27163). The vulnerability is exploited to reach an internal `Maltrail` service, which is susceptible to unauthenticated command injection. A reverse shell as `puma` is obtained, followed by privilege escalation via `sudo` misconfiguration.

---

## 🔍 Enumeration



---

## 💥 Exploitation



---

## ⚙️ Privilege Escalation



---

## 🏁 Flags

```
User: 0875193d0242fb5e51be8ece037ef591
Root: 93ef2dd887ed3b5ecd756ba51fac2434
```
