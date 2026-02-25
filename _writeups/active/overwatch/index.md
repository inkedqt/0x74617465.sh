---
layout: writeup
name: "Overwatch"
platform: "HackTheBox"
category: "active"
difficulty: "Medium"
permalink: /writeups/active/overwatch/
os: "Windows"
tags: [Active Directory, MSSQL, DNS Poisoning, WCF Exploitation]
date: 2026-02-25
pwned: true
---

> 🔒 **Spoiler Policy** — Full writeup published on machine retirement.

## Teaser

Overwatch is a Windows domain controller that demonstrates how seemingly isolated components in enterprise infrastructure can be chained together to achieve full system compromise.

The box opens with guest SMB access revealing a .NET monitoring application. What appears to be a simple configuration leak quickly becomes the foundation for a multi-stage attack: hardcoded database credentials lead to MSSQL access, which in turn reveals a broken SQL Server linked server configuration. The real elegance lies in recognizing that the broken link isn't a dead end—it's an opportunity.

With Active Directory DNS write permissions, you can poison name resolution to intercept authentication attempts, capturing credentials that provide initial foothold access. From there, the privilege escalation vector centers on a localhost-bound WCF service running under SYSTEM. The challenge isn't just finding the service—it's understanding how to interact with SOAP-based Windows Communication Foundation endpoints without metadata, and exploiting a PowerShell command injection vulnerability hiding in plain sight.

Overwatch rewards methodical enumeration, understanding of Windows service architectures, and the ability to recognize when "service unavailable" actually means "exploit opportunity."

---
