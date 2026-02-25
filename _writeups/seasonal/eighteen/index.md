---
layout: writeup
name: "Eighteen"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Easy"
permalink: /writeups/seasonal/eighteen/
os: "Windows"
tags: [Web, Databases, Authentication, Active Directory]
date: 2026-02-25
pwned: true
---
🔢 Eighteen – HTB Seasonal (Season 9)

Status: 🔒 Private – writeup will be published once the machine retires
Difficulty: Easy
Platform: Windows
Category: Web | Databases | Authentication | Active Directory
Date Completed: 2025-XX-XX

🧠 Teaser

Eighteen starts generously.

You’re given working credentials, a clean web application, and a database service that behaves exactly as advertised. It feels almost instructional — until you realise how much trust is being handed out without question.

What follows is less about exploitation and more about pivoting: moving from application logic into identity, from identity into infrastructure, and from infrastructure into full domain control. The difficulty rating reflects the initial access, not the consequences.

This box is a reminder that “low-privileged” often just means “not finished yet”.

🪛 Tools You’ll Want (High-Level)

    🔍 Comfort enumerating Windows services and databases
    🧠 Understanding how applications store and verify credentials
    🔐 Authentication flow awareness
    🧬 Active Directory permission modelling
    ⚙️ Kerberos-centric thinking

Nothing here is hidden — but nothing is labelled either.

✅ You’ll Need To:

    🕵️ Treat valid credentials as a starting point, not a win
    📦 Look beyond the web layer into supporting services
    🔑 Recognise how identity leaks across components
    🔄 Pivot using legitimate access paths
    🔓 Escalate by abusing relationships rather than breaking security controls

🧠 Takeaways

    • Databases often expose more than the application intends.
    • Password reuse quietly connects unrelated systems.
    • “Easy” boxes still teach modern Active Directory lessons.
    • Identity misconfigurations scale faster than exploits.

If you’re learning how real Windows environments fail in practice, Eighteen is a deceptively valuable exercise.

📸 Proof
![Eighteen Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/eighteen.png)