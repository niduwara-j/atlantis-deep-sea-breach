## Deep Signal Pursuit

**Category:** Networking
**Difficulty:** Moderate–Hard
**Points:** 300

### Scenario

Atlantis Deep Security intercepted a suspicious transmission sent from
a surface vessel to an offshore relay. The capture contains two
separate downloads — one carrying a key, the other carrying an
encrypted crystal fragment. Both must be recovered and correlated.

### Your Task

1. Open `deep-signal.pcap` in Wireshark.
2. Filter the traffic to isolate the suspicious relay traffic.
3. Follow each TCP stream and export the two files.
4. Use the key to decrypt the fragment.
5. Recover the flag.

### Files

- `deep-signal.pcap`

### Flag Format

`Atlantis{...}`
