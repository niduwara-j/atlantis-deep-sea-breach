#!/usr/bin/env python3
"""
Stage 5 — Solution script.
Reconstructs the player's intended solve path from the pcap.

Player steps:
  1. Open deep-signal.pcap in Wireshark.
  2. Filter to TCP port 8080.
  3. Follow the first stream -> download crystal.key (the XOR key).
  4. Follow the second stream -> download fragment.bin (encrypted flag).
  5. XOR fragment.bin with crystal.key to recover the flag.
"""
import re
from scapy.all import rdpcap, TCP, Raw

PCAP = "player/deep-signal.pcap"

def extract_http_responses(pcap_path):
    """Walk the pcap, reassemble TCP streams, and pull out HTTP responses."""
    packets = rdpcap(pcap_path)

    # Group packets by (src_port, dst_port) so we can reassemble each stream
    streams = {}
    for pkt in packets:
        if not pkt.haslayer(TCP) or not pkt.haslayer(Raw):
            continue
        ip = pkt[0][1] if False else pkt  # noqa
        tcp = pkt[TCP]
        # Response direction: server -> client. Server port is 8080.
        key = (tcp.sport, tcp.dport)
        streams.setdefault(key, b"")
        streams[key] += bytes(tcp.payload)

    return streams

def parse_http_response(data: bytes):
    """Split an HTTP response into headers and body."""
    sep = data.find(b"\r\n\r\n")
    if sep == -1:
        return None, None
    headers = data[:sep].decode(errors="replace")
    body = data[sep + 4:]
    return headers, body

def main():
    streams = extract_http_responses(PCAP)

    key_file = None
    fragment_file = None

    for (sport, dport), blob in streams.items():
        headers, body = parse_http_response(blob)
        if headers is None:
            continue
        if "crystal.key" in headers:
            # Trim to Content-Length to remove trailing TCP junk
            m = re.search(r"Content-Length: (\d+)", headers)
            length = int(m.group(1)) if m else len(body)
            key_file = body[:length]
        elif "fragment.bin" in headers:
            m = re.search(r"Content-Length: (\d+)", headers)
            length = int(m.group(1)) if m else len(body)
            fragment_file = body[:length]

    if not key_file or not fragment_file:
        print("[!] Could not extract both files from the pcap.")
        return

    print(f"[+] Recovered crystal.key:   {key_file!r}")
    print(f"[+] Recovered fragment.bin:  {len(fragment_file)} bytes")

    # XOR-decrypt the fragment using the recovered key
    flag_bytes = bytes(b ^ key_file[i % len(key_file)] for i, b in enumerate(fragment_file))
    print("[+] Decrypted content:")
    print(flag_bytes.decode(errors="replace"))

if __name__ == "__main__":
    main()
