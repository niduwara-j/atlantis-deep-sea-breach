# Private author solution — Session Hijack

Do not upload this file as a CTFd challenge attachment.

1. Open `http://127.0.0.1:8092/session-hijack/`.
2. Sign in with the junior liaison credentials displayed on the login page (`trainee` / `HorizonTrainee042!`).
3. Open Tide-keeper vault. It returns HTTP 403: the server recognises a junior liaison, not a tide-keeper.
4. Open Support desk and follow **View diagnostic attachment**.
5. Read the synthetic request associated with the tide-keeper response. The Authorization header was redacted, but the Cookie header exposes a 64-character `nh_portal_session` token. Copy only its value.
6. In Chrome DevTools, use Application → Storage → Cookies → the challenge origin. Find **nh_portal_session**, path **/session-hijack**. Replace its value with the copied tide-keeper value. Edit the existing cookie; do not create a second same-name cookie at another path. An HTTP interception tool can alternatively replay that cookie to the local challenge.
7. Refresh the dashboard. It identifies the visitor as Morgan Vale, operator (tide-keeper).
8. Open Tide-keeper vault. It now returns HTTP 200 with the `Atlantis{...}` flag.
9. Submit that flag to Session Hijack on CTFd using a normal participant account and team. Expected award: 100 points, once per team.

HttpOnly prevents JavaScript reading a cookie; it does not prevent someone who already obtained a token from replaying it through DevTools or an HTTP client. The cookie is not an encoded role or signed JWT. It is a randomly generated bearer token mapped to a server-side identity.

Restarting the app invalidates old tokens. If replay stops working after reset, log in again and fetch the current trace. Merely closing a browser is not a server reset.

## Root cause and remediation

The diagnostic redaction policy omits Cookie headers, and trainees can access an attachment containing an active privileged session. Random token generation and correct role checks cannot compensate for disclosing the bearer credential.

In a real application: redact all session credentials, restrict diagnostic access, revoke exposed sessions, use appropriate expiration and rotation, and require reauthentication for sensitive operations. HTTPS and HttpOnly help with other disclosure paths but do not fix a token deliberately printed in an accessible response. Do not present the intentionally retained operator session as production-grade logout behaviour.
