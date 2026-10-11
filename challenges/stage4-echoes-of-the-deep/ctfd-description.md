## Echoes of the Deep

**Category:** Digital Forensics
**Difficulty:** Moderate
**Points:** 200

### Scenario

A compromised pressure gate allowed an intruder into the Atlantis
relic vault. Deep Security recovered the access logs, the vault
manifest, and a suspicious encrypted file. Kida needs you to
reconstruct what happened and recover the crystal fragment.

### Your Task

Analyse the evidence bundle. Determine:

1. Which account was compromised
2. What they wrote into the vault
3. How the file was encrypted
4. Where the decryption password is hiding

The fragment is encrypted with **AES-256-CBC**. The password has been
split into three pieces and hidden across the evidence. You will need
to correlate what you find in the logs and the manifest to reconstruct
it.

### Files

- `incident-042-evidence.zip` — contains logs, manifest, and evidence

### Flag Format

`Atlantis{...}`
