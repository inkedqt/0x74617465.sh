---
layout: writeup
name: "Giveback"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/giveback/
os: "Linux"
tags: [Web, Containers, Kubernetes, Privilege Escalation]
date: 2026-02-25
pwned: true
---
🎁 Give Back – HTB Seasonal (Season 9)

Status: 🔒 Private – writeup will be published once the machine retires
Difficulty: Medium
Platform: Linux
Category: Web | Containers | Kubernetes | Privilege Escalation

🧠 Teaser

At first glance, Give Back looks like a typical content-management deployment — friendly, charitable, and unassuming.
But behind the scenes, convenience has quietly replaced security.

A single exposed web component is enough to land you inside a container, where trust boundaries blur and “temporary” decisions start to matter. From there, the real challenge isn’t exploitation — it’s understanding how modern infrastructure stitches itself together, and where those stitches can be pulled apart.

This box rewards players who think like an operator, not just an attacker.

🪛 Tools You’ll Want (High-Level)

    🔍 Web enumeration and plugin awareness
    🧪 Comfort navigating containerised environments
    🧠 Kubernetes concepts and service-to-service trust
    🗝️ Secret handling and credential hygiene awareness
    ⚙️ Binary and runtime behaviour inspection

(No single tool carries this box — observation matters more.)

✅ You’ll Need To:

    🕵️ Identify where convenience has overridden defensive assumptions
    📦 Enumerate your environment once inside a container
    🔑 Recognise where sensitive data leaks through configuration
    🔄 Pivot using legitimate infrastructure mechanisms
    🔓 Escalate privileges by understanding how containers interact with the host

🧠 Takeaways

    • Containers reduce blast radius — until they don’t.
    • Environment variables often say more than configuration files.
    • Modern stacks fail most often at the boundaries between components.
    • Privileged tooling is rarely meant for production exposure.

If you’re preparing for real-world cloud or platform security work, this box offers a very grounded lesson in how small missteps compound.

📸 Proof
![Give Back Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/giveback.png)