---
layout: writeup
name: "Conversor"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Easy"
permalink: /writeups/seasonal/conversor/
date: 2026-02-25
pwned: true
---
# Conversor — HTB Seasonal — Teaser

**Difficulty:** Easy  
**Skills:** Web file/transform parsing, web upload abuse, local file enumeration, basic password reuse, sudo privilege discovery.  
**Box type:** Linux (web app / parsing / local privilege escalation)

## Short pitch
Conversor is a tidy, well-crafted web app that rewards careful reconnaissance and a healthy distrust of uploaded files. If you enjoy poking at server-side parsers and turning file uploads into footholds, this one will scratch that itch.

## What you'll do (high level, non-spoiler)
- Enumerate the web application and its file handling features.  
- Probe the parser/transformer used by the site — uploaded payloads are processed server-side.  
- Look for interesting files and configuration left on disk that can be leveraged.  
- Harvest credentials and reuse them where sensible.  
- Inspect local privileges and sudo rules for a clean privilege escalation path.

## Cheeky hints (no spoilers)
- The app accepts uploaded transformation files — think about how those are executed, not just stored.  
- A small, forgotten database file on disk can hold surprisingly useful secrets.  
- Classic username/password reuse is alive and well; don’t ignore weak hashes or common passwords.  
- When you get a shell, check `sudo -l` and installed maintenance helpers — sometimes the path to root is a single privileged utility.

## Starting creds (CTF)
- Try registering a user via the web app to start exploring (the app supports self-registration).


