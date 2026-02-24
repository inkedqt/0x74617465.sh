---
layout: writeup
name: "Pterodactyl"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Medium"
permalink: /writeups/seasonal/pterodactyl/
os: "Linux  Release HTB Seasonal"
date: 2026-02-21
pwned: true
---
# 🦕 Pterodactyl

> **Difficulty:** Medium | **OS:** Linux | **Release:** HTB Seasonal

A PHP web application box that rewards thorough enumeration before touching an exploit. Getting root requires chaining a lesser-known Polkit quirk with a race condition — patience and two terminals win the day.

---
## 📸 Proof
![Pterodactyl Proof](https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/pterodactyl.png)
---

## 🧠 Concepts Covered

- Subdomain / vhost enumeration
- Web application fingerprinting and CVE research
- Local File Inclusion and chaining LFI → RCE
- PHP-PEAR as an unexpected code execution primitive
- Database credential extraction and lateral movement
- Offline bcrypt cracking
- Linux session model (Polkit, PAM, systemd-logind, seats)
- TOCTOU race conditions in privileged file operations
- XFS filesystem basics and disk image construction

---

## 💡 Hints (No Spoilers)

**Foothold**
- Don't assume the first vhost is the only one. Fuzz broadly before deciding you've seen everything.
- The application is not a custom build — it's a real open-source project. Find the exact version. There's a file on the server that hands it to you for free if you look in the right place.
- Once you know the version, the CVE you need involves a specific API endpoint that transforms user input in a predictable way before passing it to the filesystem. Think about what "transformation" opens up.
- You have file read. Look at what's enabled on the PHP install — `phpinfo.php` is your friend here. One feature being present changes "arbitrary file read" into "code execution" through a well-known technique.
- The technique requires knowing where certain PHP files live on the system. Standard install paths apply.

**User**
- Your web shell runs as the web server user. You're not going to `sudo` your way anywhere from here.
- The application has to talk to a database. Find its config. Read it.
- The database has user accounts with password hashes. Not all of them are worth your time — pick the one that isn't the admin and crack it.
- Bcrypt is slow but rockyou is not that big.

**Root**
- Check your mail. Literally. The system might be trying to tell you something.
- The privesc involves a Linux subsystem that doesn't get much attention in CTFs. Read about how `udisks`, `Polkit`, and session seats interact.
- There are two CVEs here, not one. The first gets you elevated permissions you shouldn't have. The second lets you abuse those permissions to execute code as root — but only for a brief window.
- SUID binaries are blocked on normal mounts. Think about when "normal" rules might not apply during a privileged operation.
- You'll need two terminals open and a tight loop. The race window exists — it's just not very generous.
- Build your payload statically. Dynamic linking assumptions will bite you.

---

## 📚 Useful Reading

- Pterodactyl Panel documentation (understand the locale/translation system)
- PHP-PEAR docs — specifically `pearcmd.php` and how it handles command-line arguments
- [Polkit documentation](https://www.freedesktop.org/software/polkit/docs/latest/) — `allow_active` vs `allow_any`, and what constitutes a "local" session
- `pam_env(8)` man page — what `~/.pam_environment` can and can't do
- udisks2 documentation — loop device setup and filesystem operations
- `mkfs.xfs` and XFS resize behaviour
- hashcat wiki — bcrypt mode

---

*This box is part of an active HTB Seasonal rotation. Full writeup will be published after the box retires.*
