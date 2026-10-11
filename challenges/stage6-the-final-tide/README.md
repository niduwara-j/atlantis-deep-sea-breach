# Stage 6: The Final Tide (Capstone Challenge)

- **Domain:** Linux / System Security (CWE-732: Incorrect Permission Assignment for Critical Resource)
- **Points:** 400 (Hard Capstone)
- **Target Machine:** Ubuntu Server 24.04 LTS (\tlantis-relay-04\) hosted on VirtualBox
- **Network Interface:** Reachable over private Tailscale WireGuard mesh
- **Exposed Services:** TCP 22 (OpenSSH 9.6), TCP 8080 (Nginx Legacy Recovery Portal)
- **Initial Foothold:** Low-privileged account \maint-operator\
- **Root Flag:** \Atlantis{1nc1d3nt_042_r00t_3sc414t10n_v1v4_s3cur3}\

## Vulnerability & Escalation Path
1. **Reconnaissance:** Enumerate services via Nmap (\
map -sC -sV -p- <target_ip>\). Discover HTTP on port 8080 and SSH on port 22.
2. **Foothold:** Discover unprotected backup archive on the recovery portal containing SSH credentials for \maint-operator\.
3. **Internal Enumeration:** Inspect scheduled tasks with \systemctl list-timers\. Identify \incident042-backup.timer\ running as \oot\.
4. **Permission Analysis (CWE-732):** The service calls \/opt/incident042/hooks/pre-backup.sh\. Inspecting permissions with \ls -la\ reveals it is group-writable by \maint-operator\.
5. **Privilege Escalation:** Append a command copying \/root/flag.txt\ to a readable directory (\/tmp/flag_evidence.txt\).
6. **Execution:** Wait for the systemd timer to execute the hook as root, then retrieve the flag.
