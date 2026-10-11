# Stage 3 — Hints

| Hint | Cost | Text |
|---|---:|---|
| 1 | 15 | XOR is reversible. If you know part of the plaintext, you can recover part of the key. |
| 2 | 30 | XOR the first 30 bytes of ciphertext with the known header. The result repeats every 5 bytes. |
| 3 | 60 | The repeating key is ATL42. Use it to decrypt the rest of the message. |
