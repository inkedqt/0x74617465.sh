---
layout: writeup
name: "Editor"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/editor/
tags: [Linux, Web, Reverse Engineering]
date: 2025-11-12
pwned: true
---
🌀 Editor (HTB Seasonal)

Status: 🔒 Private – writeup will be published once the machine retires  
Difficulty: Medium  
Category: Linux | Web | Reverse Engineering  
Date Completed: 2025-08-03

🧠 Teaser

A simple text editor? Or a ticking time bomb of broken logic and hidden payloads...

Are you savvy enough to trace the input validation flaws, disassemble the binary protections, and take full control of the system?

🪛 Tools You'll Want:

🕸️ Burp Suite or ZAP for intercepting funky input  
🔍 Strings, Ghidra or GDB for cracking the binary open  
📦 Python3 + `pickle` for sneaky deserialization  
🐚 Your favorite Linux privesc enumeration tools (linPEAS, pspy, etc.)

You'll need to:

📥 Fuzz inputs and watch for hidden system calls  
💣 Identify and exploit logic bombs in a homebrew interpreter  
🔓 Abuse insecure deserialization to get a shell  
📜 Traverse limited environments to escalate privileges  
🔁 Leverage overlooked system tools to overwrite root

📸 Proof  
![Proof Screenshot](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/editor.png)