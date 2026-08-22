# Security Policy

## Supported Versions
Only the latest major release (`v2.x.x`) receives active security patches.

## Reporting a Vulnerability
PRISM-Edge handles sensitive clinical and demographic data. If you discover a vulnerability, **do NOT open a public issue**.
Please email the Lead Architect directly at: `rudrasarker130@gmail.com`.

## Threat Model & Defenses
1. **Device Seizure**: Mitigated via PBKDF2-HMAC-SHA256 encrypted vaults and the Duress PIN protocol.
2. **Database Reconstruction Attack**: Mitigated via Laplace Differential Privacy ($\epsilon = 0.5$).
3. **Man-in-the-Middle (Mesh)**: All gossip payloads are authenticated using AEAD (AES-256-GCM) before Base91 encoding.
