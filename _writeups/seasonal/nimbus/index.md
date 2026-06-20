---
layout: writeup
name: "Nimbus"
platform: "HackTheBox"
category: "seasonal"
difficulty: "Hard"
permalink: /writeups/seasonal/nimbus/
os: "HackTheBox"
tags: [seasonal]
date: 2026-06-21
pwned: true
---
# ⚛️ Nimbus

> **Difficulty:** Hard | **OS:** Linux | **Release:** HTB Season 11

Nimbus is a cloud-themed Linux box that simulates a misconfigured AWS-style environment. The path starts with an SSRF vulnerability in a job preview endpoint — bypassing IP restrictions with a decimal-encoded address to reach the instance metadata service and steal IAM role credentials. Those credentials allow injection into an SQS job queue whose worker deserializes untrusted YAML with an unsafe loader, giving RCE and the user flag. From there, an internal LocalStack endpoint exposes a CodeBuild project running in privileged mode. A clever environment variable trick bypasses the container's UID-drop entrypoint, and the resulting root-level container context is used to write a payload into the kernel's `modprobe` usermode-helper — escaping to the real host and reading the root flag.

---

## 📸 Proof
![](nimbus.png)


---

## 🧠 Concepts Covered

- **SSRF with IP obfuscation** — using decimal-encoded IPv4 to bypass SSRF filters and reach `169.254.169.254`
- **IMDSv1 credential theft** — querying the Instance Metadata Service to extract temporary IAM role keys
- **SQS message injection** — writing attacker-controlled job payloads into an AWS SQS queue
- **Unsafe YAML deserialization** — `yaml.Loader` (not `SafeLoader`) executing arbitrary Python objects on the worker side
- **Internal service discovery** — enumerating localhost/internal ports to find a LocalStack endpoint not exposed externally
- **LocalStack with ENFORCE_IAM=false** — unauthenticated access to a full fake-AWS service stack
- **AWS CodeBuild `privilegedMode`** — a build project configured to run its container with elevated Linux capabilities (CAP_SYS_ADMIN)
- **Entrypoint UID-drop bypass via `BASH_FUNC_id%%`** — overriding the shell `id` builtin through environment variable injection so the entrypoint script's root check passes
- **Kernel `modprobe` usermode-helper escape** — writing a malicious script path to `/proc/sys/kernel/modprobe` and triggering kernel execution of an unknown-magic binary to run arbitrary commands as host root

---

## 💡 Hints (No Spoilers)

**Foothold**
- Look for any endpoint that fetches or previews content from a URL you supply. Try pushing that URL toward internal address ranges — but be aware that naive IP blacklists can be bypassed without changing the actual destination.
- Once you can reach the metadata endpoint, look for credentials attached to a named role. That's your ticket into the next layer.

**User**
- With valid cloud credentials, think about what queue-based services might be running. Can you write a message that a backend worker will pick up and process?
- When a worker reads structured data from a queue and deserialises it, the security of that operation depends entirely on *which* deserialiser call is used. Some Python YAML loading functions are dangerous by design — check the docs.

**Root**
- After getting a shell, scan what internal services are listening that aren't exposed externally. A cloud-themed box almost certainly has more fake-AWS infrastructure running locally.
- When you find a build/CI service, look at how its projects are configured — specifically whether any run in privileged mode. Privileged containers have kernel interfaces available that normal containers don't.
- The entrypoint guarding root access inside the container does a runtime identity check that can be spoofed without modifying any binary. Think about how shell builtins can be overridden via the process environment.
- Once you're acting as root inside the privileged container, research which kernel pseudo-file tells the kernel what program to run when it encounters an unknown binary magic number — and whether that file is writable from your context.

---

## 📚 Useful Reading

- [SSRF via IP encoding tricks](https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery) — decimal, octal, and hex IP formats to bypass SSRF filters
- [AWS IMDSv1 credential endpoint](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html) — structure of the metadata service and where role credentials live
- [PyYAML unsafe load](https://pyyaml.org/wiki/PyYAMLDocumentation) — why `yaml.load()` with `Loader=yaml.Loader` allows arbitrary object instantiation
- [LocalStack](https://github.com/localstack/localstack) — local AWS service emulator; `ENFORCE_IAM=false` removes all auth checks
- [Container escape via modprobe path](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation#privileged-escape-abusing-existing-capabilities) — writing `/proc/sys/kernel/modprobe` from a privileged container to execute host-side code
- [BASH_FUNC environment injection](https://www.exploit-db.com/exploits/39044) — overriding shell functions via environment variables (same mechanism as Shellshock)

---

*This box is part of HTB Season 11.*
