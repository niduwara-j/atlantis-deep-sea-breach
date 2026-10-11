# Stage 4 — Hints

| Hint | Cost | Text |
|---|---:|---|
| 1 | 15 | Start with pressure-gate.log. Look for logins that stand out from the normal pattern. |
| 2 | 30 | The suspicious account is `deep_signal_x`. The file they wrote is `crystal-fragment.enc`. |
| 3 | 60 | Read the hidden dotfile `.kida-warning`. It explains the encryption and where to find the password. |
| 4 | 90 | The password has three pieces. One is a hostname fragment in the gate log, one is a scheduled task name in the sonar log, one is the incident number in the manifest. |
| 5 | 120 | Recover the pieces and join them with hyphens. Then use openssl with `-aes-256-cbc -pbkdf2 -iter 100000`. |
