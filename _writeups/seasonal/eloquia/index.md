---
layout: writeup
name: "Eloquia"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Insane"
permalink: /writeups/seasonal/eloquia/
os: "Windows"
tags: [Web, Containers, Identity, Privilege Escalation]
date: 2025-12-23
pwned: true
---
🧩 Eloquia – HTB Seasonal (Season 9)

Status: 🔒 Private – writeup will be published once the machine retires
Difficulty: Insane
Platform: Windows
Category: Web | Containers | Identity | Privilege Escalation
Date Completed: 2025-XX-XX

🧠 Teaser

Eloquia is not difficult because of any single vulnerability — it’s difficult because nothing exists in isolation.

What begins as a modest web application slowly unfolds into a layered enterprise environment where trust is repeatedly misplaced. Configuration, identity, containers, and custom Windows services all interact in ways that feel realistic, intentional, and dangerous when misunderstood.

Progress requires switching mindsets constantly: web logic, container boundaries, Windows internals, and operational security all matter. Missing even one link in the chain stalls you completely.

This is a box that rewards patience, context, and deep system literacy.

🪛 Tools You’ll Want (High-Level)

    🔍 Careful web application analysis
    🧠 Strong understanding of Windows service behaviour
    📦 Container orchestration awareness
    🔑 Identity and credential handling intuition
    ⚙️ Comfort reasoning across Linux and Windows boundaries

Automation helps — but comprehension is mandatory.

✅ You’ll Need To:

    🕵️ Treat configuration leaks as architectural failures
    📦 Follow identity and trust relationships across services
    🧠 Recognise when containers are part of the problem, not the solution
    🔄 Pivot through legitimate control paths rather than exploits
    🔓 Escalate by abusing operational assumptions

🧠 Takeaways

    • Loose trust models collapse under real-world complexity.
    • Containers don’t remove risk — they redistribute it.
    • Custom security tooling is often the weakest link.
    • Insane boxes test endurance as much as skill.

Eloquia feels less like a CTF and more like an incident investigation that never quite stops expanding.

📸 Proof
![Eloquia Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/eloquia.png)