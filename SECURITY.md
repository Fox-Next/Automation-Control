# Security Policy — Fox Next Automation Control

## Reporting a Vulnerability

If you discover a security vulnerability in **Automation Control** or **Smart Support Bot**, please report it responsibly through the official **Fox Next** portal at [https://foxnext.net/](https://foxnext.net/) rather than opening a public GitHub issue with exploit details.

## Security Architecture Highlights

1. **Zero-LLM Credential Isolation (`Chat-to-Config` & Pre-LLM Masking)**
   - Sensitive tokens (Telegram Bot Tokens, API Keys, SSH secrets) pasted directly in chat are masked as `[REDACTED_SECRET]` before reaching any LLM provider.
   - Secure configuration cards submit credentials directly over HTTPS into the Fernet-encrypted local/tenant Vault without LLM visibility.
2. **Anti-SSRF Fetch Guard**
   - Agent web retrieval blocks private/loopback IP ranges (`127.0.0.1/8`, `10.0.0.0/8`, `169.254.169.254`, RFC-1918 & link-local CIDRs) and rejects unsafe redirects.
3. **Human-in-the-Loop (HITL) Boundaries**
   - Financial verification, service restarts, and public social publishing require explicit human approval cards or authenticated owner policies.
4. **Encrypted Workspace Migration (`.fnbackup`)**
   - Portable workspace exports are encrypted using Fernet symmetric authenticated encryption derived from user credentials/passphrases.
5. **Strict SSH Bridge Guard**
   - Remote infrastructure/SSH actions over the Desktop Bridge are restricted exclusively to the platform/DevOps agent role and audited before execution.
6. **Public Repository Hygiene**
   - Automated scanners enforce zero credentials, zero server IP literals, zero databases/backups, and zero executable binaries across all commits and git history.
