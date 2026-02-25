---
layout: writeup
name: "AirTouch"
platform: "HackTheBox"
category: "active"
difficulty: "Medium"
permalink: /writeups/active/airtouch/
os: "Linux"
tags: [Network Security, Wireless Exploitation, Multi-VLAN Pivoting, Authentication Bypass]
date: 2026-02-25
pwned: true
---

> 🔒 **Spoiler Policy** — Full writeup published on machine retirement.

## Teaser

AirTouch is a masterclass in wireless network exploitation and VLAN pivoting that simulates a realistic corporate WiFi infrastructure.

The box begins with network reconnaissance through an unconventional protocol, leading to initial access on a segmented consultant network. From there, the challenge becomes navigating a multi-tiered wireless architecture: consumer-grade WPA2-PSK networks, enterprise 802.1X authentication, and isolated VLANs that require creative pivoting techniques.

What makes AirTouch particularly engaging is its realistic simulation of corporate wireless security. You'll encounter the same authentication mechanisms, network segmentation, and trust boundaries that exist in real enterprise environments—and exploit the same weaknesses that make wireless networks a persistent attack vector.

The path to root requires chaining together wireless credential harvesting, man-in-the-middle attacks against enterprise authentication, and leveraging misconfigurations in network access control. It's not just about breaking WiFi—it's about understanding how wireless networks integrate with broader infrastructure and where those integration points fail.

---
