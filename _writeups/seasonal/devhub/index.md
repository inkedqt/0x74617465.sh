---
layout: writeup
name: "Devhub"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/devhub/
os: "HackTheBox"
tags: [seasonal]
date: 2026-05-31
pwned: true
---
# ⚛️ Reactor

> 🤖 ***MCPJam Difficulty: Medium | OS: Linux | Release: HTB Season 11

A Linux box themed around the MCP (Model Context Protocol) ecosystem — very 2025. Getting in requires zero credentials and zero enumeration finesse. Once you're inside, the path forward is a trail of things that shouldn't be left lying around. Root is handed to you by a "secure" admin tool that was a little too helpful.

---

## 📸 Proof
![](devhub.png)


---

🧠 Concepts Covered

- MCP server exploitation (unauthenticated RCE via server config injection)
- Process enumeration for credential discovery
- Chisel reverse port forwarding
- Jupyter Notebook lateral movement
- API key discovery in user home directories
- MCP admin tool abuse for privileged data exfiltration
- SSH private key extraction and root access

💡 Hints (No Spoilers) Foothold

- The box is called MCPJam. The service running on the non-standard port tells you exactly what it is. Read the API spec before you reach for Burp.
- The connect endpoint doesn't validate what you connect. Think about what a "server config" field that accepts a command actually means.
- You don't need to find credentials first. The vulnerability is pre-auth by design — the service is doing exactly what MCP servers are supposed to do.

User

- You landed as a service account. Service accounts run things. Things that are running have arguments. Arguments sometimes contain secrets.
- The port that's listening locally but not externally is the one you want. You'll need a tunnel to get there.
- Once you're through the tunnel, look for the most obvious way a data analyst would interact with a local service. It's not a shell — until it is.

Root

- The analyst left something in their home directory with a name that makes its purpose extremely obvious. Read it.
- There's a local service running that has an admin mode. The key you just found is probably for that. Look at what the admin endpoints expose.
- "Dump" is not a subtle function name. If a tool offers to dump SSH keys and you have the API key to call it — call it.
- You're not exploiting a vulnerability at the root stage. You're using the tool exactly as designed. That's the point.

📚 Useful Reading

- MCP (Model Context Protocol) specification — particularly the server config structure and what `command`/`args` fields actually do
- `ps auxww` — why full argument listing matters and what tokens look like in process tables
- Chisel — reverse tunneling, `R:` port syntax, attacker-side server flags
- Jupyter Notebook terminal access — what it gives you and as whom
- `curl` with API key headers — `-H "X-API-Key:"` and reading JSON responses
- SSH authentication with key files — `chmod 600` and why it matters