---
layout: writeup
name: "Browsed"
platform: "HackTheBox"
category: "active"
difficulty: "Medium"
os: "Linux"
tags: [Web, Client-Side Attacks, Code Review, Privilege Escalation]
date: 2026-02-08
pwned: true
---

> 🔒 **Spoiler Policy** — Full writeup published on machine retirement.

## Teaser

Browsed explores what happens when user-generated content isn't just stored—it's _executed_.

The box centers on a web application that allows users to submit Chrome browser extensions for review. But "review" here means something specific: a backend developer actually installs and tests your extension in their own browser. That workflow—where user-controlled code becomes trusted developer context—is the entire threat model.

From there, the box becomes a study in **chained browser-based exploitation**: reaching services that were never meant to be externally accessible, identifying implementation flaws in internal tooling, and finally pivoting from application-level access to full system control through configuration mistakes that seem small but prove critical.

---
