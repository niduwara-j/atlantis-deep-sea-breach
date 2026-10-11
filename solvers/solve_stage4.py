#!/usr/bin/env python3
"""
Stage 4 — Solution script (Escape Room edition).
Walks the intended path and proves the challenge is solvable.
"""
import os
import re
import subprocess
import tempfile
import zipfile

ZIP = "player/incident-042-evidence.zip"

with zipfile.ZipFile(ZIP) as z:
    pressure = z.read("pressure-gate.log").decode()
    sonar = z.read("sonar-events.log").decode()
    manifest = z.read("relic-vault-manifest.txt").decode()
    fragment = z.read("crystal-fragment.enc")

print("[*] Step 1 — locate the attacker login")
for line in pressure.splitlines():
    if "Accepted passphrase for deep_signal_x" in line:
        print(f"    {line}")

print("[*] Step 2 — recover password piece 1 from pressure-gate.log")
m = re.search(r"hostname lookup for ([a-zA-Z0-9]+)-salvage-node", pressure)
piece1 = m.group(1) if m else None
print(f"    piece 1 = {piece1}")

print("[*] Step 3 — recover password piece 2 from sonar-events.log")
m = re.search(r'salvage run "([^"]+)"', sonar)
piece2 = m.group(1) if m else None
print(f"    piece 2 = {piece2}")

print("[*] Step 4 — recover password piece 3 from the manifest")
m = re.search(r"incident_reference:\s*(\d+)", manifest)
piece3 = m.group(1) if m else None
print(f"    piece 3 = {piece3}")

if None in (piece1, piece2, piece3):
    print("[!] Could not recover all password pieces. Aborting.")
    raise SystemExit(1)

password = f"{piece1}-{piece2}-{piece3}"
print(f"[+] Recovered password: {password}")

print("[*] Step 5 — decrypt crystal-fragment.enc with openssl")
with tempfile.NamedTemporaryFile(delete=False, suffix=".enc") as tmp:
    tmp.write(fragment)
    tmp_path = tmp.name

result = subprocess.run(
    [
        "openssl", "enc", "-d", "-aes-256-cbc",
        "-pbkdf2", "-iter", "100000",
        "-in", tmp_path,
        "-k", password,
    ],
    capture_output=True,
)
os.unlink(tmp_path)

if result.returncode != 0:
    print("[!] openssl failed:")
    print(result.stderr.decode())
    raise SystemExit(1)

print("[+] Decrypted content:")
text = result.stdout.decode(errors="ignore")
# Drop any line that doesn't look like part of the message
lines = [ln for ln in text.splitlines() if "Atlantis" in ln or "Status" in ln or "Flag" in ln]
print("\n".join(lines))
