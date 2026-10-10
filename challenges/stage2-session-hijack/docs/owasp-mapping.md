# Stage 2: Tide-Keeper Hijack - OWASP Mapping & Remediation Guide

**Stage:** Stage 2 (Tide-Keeper Hijack / Session Hijack)  
**Author:** Prabodini M.A.V (IT24102511) - Member 3 (Web Security Domain)  
**Target:** Atlantis Surface-Liaison Portal  

---

## 1. OWASP Top 10 (2021) Mapping

### A01:2021 - Broken Access Control
- **Observation:** The application relies entirely on bearer session cookies without validating IP binding, client fingerprinting, or user context. When an unprivileged user presents an operator session token, the `/vault` endpoint unconditionally grants administrative access.
- **Root Cause:** Inadequate session-to-identity binding and missing authorization checks at the session validation layer.

### A07:2021 - Identification and Authentication Failures
- **Observation:** High-privilege session tokens (`nh_portal_session`) are leaked in plaintext through diagnostic telemetry attachments (`/support/trace-042.txt`).
- **Root Cause:** Session identifiers treated as unclassified data; diagnostic logging failed to treat session cookies as sensitive credentials during sanitization.

---

## 2. Vulnerability Details & Impact

- **CWE-384:** Session Fixation / Improper Session Management
- **CWE-532:** Insertion of Sensitive Information into Log File
- **Impact:** An authenticated junior liaison (`trainee`) can escalate privileges to `operator` (Tide-Keeper) by replaying the leaked session identifier, bypassing role-based access control.

---

## 3. Recommended Remediation & Countermeasures

1. **Strict Diagnostic Redaction:**
   - Update redaction filters to redact sensitive request headers, specifically `Cookie`, `Set-Cookie`, `Authorization`, and custom authentication headers before exporting traces.
2. **Session Cookie Security Attributes:**
   - Enforce `HttpOnly` to prevent client-side script access.
   - Enforce `Secure` (HTTPS) to ensure tokens are never transmitted in cleartext.
   - Set `SameSite=Strict` to mitigate cross-site request forgery risks.
3. **Short-Lived Tokens & Session Rotation:**
   - Implement short idle timeouts (e.g., 15 minutes) and absolute token expiry.
   - Re-issue session tokens upon privilege level changes or sensitive actions.
