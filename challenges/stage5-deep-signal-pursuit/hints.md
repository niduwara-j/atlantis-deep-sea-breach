# Stage 5 — Hints

| Hint | Cost | Text |
|---|---:|---|
| 1 | 20 | Filter to `tcp.port == 8080`. Not all traffic in the capture is relevant. |
| 2 | 40 | There are two separate TCP streams. Follow each one — `Follow > TCP Stream` in Wireshark. |
| 3 | 70 | The first stream carries a file called `crystal.key`. Export its body. |
| 4 | 100 | The second stream carries `fragment.bin`. XOR it with the recovered key. |
