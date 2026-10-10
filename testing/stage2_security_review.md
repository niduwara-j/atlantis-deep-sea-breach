# Stage 2: Tide-Keeper Hijack - Security Analysis & Testing
- Author: Prabodini M.A.V (IT24102511)
- Category: OWASP A01 (Broken Access Control) & A07 (Identification/Authentication Failures)
- Target: http://127.0.0.1:8092/session-hijack/
- Vulnerability Mechanism: Leaked nh_portal_session cookie in support ticket ATL-042
- Flag: Atlantis{session_hijack_5325bbc991e95799c34448604015782b}
- Remediation: Sanitize diagnostic traces and strip session cookie headers before logging
