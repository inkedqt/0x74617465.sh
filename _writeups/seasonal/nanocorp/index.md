---
layout: writeup
name: "Nanocorp"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Hard"
permalink: /writeups/seasonal/nanocorp/
os: "Windows"
tags: [Active Directory, Web, Authentication, Privilege Escalation]
date: 2025-12-23
pwned: true
---
🏢 NanoCorp – HTB Seasonal (Season 9)

Status: 🔒 Private – writeup will be published once the machine retires
Difficulty: Hard
Platform: Windows
Category: Active Directory | Web | Authentication | Privilege Escalation

🧠 Teaser

NanoCorp feels like a real corporate environment — because it is one.

A public-facing recruitment portal shares a host with critical domain services, and that design choice quietly sets the tone for the entire machine. Initial access doesn’t rely on flashy exploits or brute force; instead, it rewards careful observation of how Windows services, authentication, and user workflows intersect.

From there, the box becomes a lesson in trust abuse: how service accounts grow powerful over time, how convenience shortcuts weaken identity boundaries, and how “monitoring” software can quietly become the most dangerous component in the room.

This is a box for players who enjoy reading environments, not racing tools.

🪛 Tools You’ll Want (High-Level)

    🔍 Strong Windows service enumeration
    🧠 Active Directory relationship analysis
    🔐 Authentication protocol literacy (NTLM / Kerberos)
    🧬 Privilege path reasoning over exploit chaining
    ⚙️ Comfort operating inside constrained Windows shells

Automation helps — but understanding wins.

✅ You’ll Need To:

    🕵️ Treat the web application as an entry point, not the target
    🔑 Identify how credentials move between services
    🧠 Follow permission relationships rather than exploit scripts
    🔄 Pivot using legitimate enterprise mechanisms
    🔓 Escalate privileges by abusing trust, not breaking systems

🧠 Takeaways

    • Public services and domain controllers should never coexist.
    • Service accounts tend to accumulate far more power than intended.
    • Monitoring agents often run with excessive privileges.
    • Authentication abuse is quieter — and deadlier — than exploitation.

If you’re preparing for real-world AD assessments or internal engagements, NanoCorp is an excellent study in how small operational decisions cascade into full domain compromise.

📸 Proof
![NanoCorp Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/nanocorp.png)