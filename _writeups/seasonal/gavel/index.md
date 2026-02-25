---
layout: writeup
name: "Gavel"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/gavel/
os: "Linux"
tags: [Web, Source Disclosure, PHP, Privilege Escalation]
date: 2026-02-25
pwned: true
---
🔨 Gavel – HTB Seasonal (Season 9)

Status: 🔒 Private – writeup will be published once the machine retires
Difficulty: Medium
Platform: Linux
Category: Web | Source Disclosure | PHP | Privilege Escalation

🧠 Teaser

Gavel looks like a straightforward auction platform — until you realise you’ve been handed the blueprint.

A public-facing web app exposes far more than intended, and once the source is in hand, the box becomes a study in how small implementation shortcuts compound into serious risk. Initial access is earned through understanding how applications *think*, not through noisy exploitation.

The second half shifts gears entirely: custom tooling, dynamic code execution, and a privileged service that trusts user input just a little too much. From there, the challenge isn’t finding bugs — it’s understanding how the system was designed to work.

🪛 Tools You’ll Want (High-Level)

    🔍 Source code review and application logic analysis
    🧠 Database behaviour awareness
    🧪 PHP execution model familiarity
    ⚙️ Comfort reasoning about custom binaries and daemons
    🔑 Privilege boundary analysis

Reading beats scanning on this one.

✅ You’ll Need To:

    🕵️ Treat exposed source as an attack surface, not a convenience
    📦 Follow how user input flows through the application
    🧠 Recognise when “safety features” can be redefined at runtime
    🔄 Abuse trusted components rather than breaking isolation
    🔓 Escalate by understanding how privileged helpers are meant to be used

🧠 Takeaways

    • Source disclosure often turns logic flaws into full compromise.
    • Dynamic languages are dangerous when execution rules are mutable.
    • Set-uid helpers are only as safe as the assumptions they make.
    • Sandboxes fail quietly when configuration is user-controlled.

Gavel rewards players who slow down, read carefully, and respect how dangerous “flexibility” can be in production systems.

📸 Proof
![Gavel Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/gavel.png)