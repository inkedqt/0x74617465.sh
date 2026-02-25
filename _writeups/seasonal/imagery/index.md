---
layout: writeup
name: "Imagery"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/imagery/
date: 2026-02-25
pwned: true
---
# Imagery — Teaser (Public)

> **Public teaser** — safe for the public repo. Hints only, no full commands or flags.

Imagery is a fun seasonal box that mixes classic web puzzling with some good old-fashioned sloppy ops. If you like galleries, image uploads, and surprisingly chatty backup tools, this one scratches an itch.

### High-level hints (non-spoiler)
- There's a gallery and an admin log endpoint — don't forget to try reading what the app thinks is a log. (Yep — directory traversal is the friend you didn't know you needed.)
- Image transforms look innocent — numeric fields can be mischievous. Try treating them like text and see what happens.
- Encrypted backups exist on the box; they're readable but they expect a password. Offline wordlists + patience = results.
- The interesting escalation comes from a small, privileged CLI backup tool that includes a shell and scheduling features. Think: "can I make it do the boring job of copying something for me?"
