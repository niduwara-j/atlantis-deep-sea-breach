## The Crystal Briefcase

**Category:** Cryptography
**Difficulty:** Moderate
**Points:** 200

### Scenario

A sealed crystal briefcase was recovered from the Incident 042 breach
site at depth 42 metres. Inside is a single encrypted file. The
encryption is weak — a repeating-key XOR — but the key is short and
the briefcase format is publicly known.

### Your Task

The crystal briefcase format always begins with the header:

    ATLANTIS-CRYSTAL-BRIEFCASE-v1

Use this known plaintext to recover the repeating key, decrypt the
message, and retrieve the flag.

### Files

- briefcase.enc (Base64-encoded ciphertext)

### Flag Format

Atlantis{...}
