# Stage 2 specification — Null Horizon CTF

| Required field | Design / implementation |
|---|---|
| Stage ID & Title | Stage 2 / Session Hijack |
| Domain | Web Technologies / Web Security |
| Difficulty | Easy: supplied login, one linked diagnostic artifact, one cookie replay, one protected page. No brute force, custom exploit code or XSS bot. |
| Scenario | A fictional Atlantis tide-keeper's support trace retained session context in the surface-liaison portal after Incident 042. A junior liaison investigates and accesses the tide-keeper verification record. |
| Learning Objective | Explain bearer sessions, distinguish authentication from authorisation, recognise credential leakage in HTTP diagnostics, and demonstrate session replay. |
| Challenge Environment | Python 3.11 Linux container, Flask 3.1.3, Waitress 3.0.2, one process / four threads; in-memory sessions, no database. Windows native fallback is a separate test mode. |
| Player Task | Use the junior liaison account to investigate the support artifact and retrieve the tide-keeper vault flag. |
| Flag Location / Logic | Flag is supplied through CHALLENGE_FLAG and rendered only by the tide-keeper-authorised vault route. CTFd stores the matching static case-sensitive value. |
| Required Tools | Browser and developer tools; optionally an HTTP interception/replay tool. |
| Dependencies | Reachable challenge service, supplied junior liaison credentials, browser cookie support, CTFd for points. No earlier-stage flag, live victim, internet API, or external callback. |
| Expected Solution Path | Junior liaison login → inspect support trace → recover tide-keeper bearer token → replace challenge cookie → open tide-keeper vault → submit recovered flag. |
| Validation | Automated unit and live HTTP tests, plus a separate normal-player CTFd submission test. See TEST-RESULTS.md for actual status. |
| Hints | Three progressive hints below; proposed costs 0 / 10 / 20 points. CTFd must be configured to enforce these costs. |
| Reset / Recovery | Restart the web service; all sessions regenerate, permanent challenge flag persists through .env. CTFd submissions are managed independently. |

## Proposed hints

1. **0 points:** The support desk has an attachment connected to the tide-keeper's request.
2. **10 points:** Redacting an Authorization header does not remove every form of authentication. Compare the remaining headers with your browser's requests.
3. **20 points:** The portal recognises `nh_portal_session`. Replace your existing challenge cookie with the tide-keeper's value from the trace, then revisit the vault.

## Participant suitability and progression

Designed for beginner-to-intermediate cybersecurity students familiar with browser navigation. Introduces HTTP request inspection after Stage 1 and before cryptographic analysis in Stage 3. Supports module LO1 through information gathering and LO2 through selection of browser inspection/replay techniques. This stage does not independently satisfy LO3's exploitation-code outcome; assess that outcome across the whole project rather than claim it here.

## Architecture

Participant browser → loopback port 8092 → non-root Nginx gateway on frontend and internal networks → isolated Waitress/Flask web container → in-memory session mapping. The web container has no published port or non-internal network; the gateway has a fixed backend destination.

Participant browser → separate CTFd website → CTFd static-flag validation and team scoreboard.

There is no app-to-CTFd API connection. No platform credentials are shared with the vulnerable service. Source package stays with organisers; players receive a URL and briefing only.

## Limitations / risks

- All players share one immutable synthetic tide-keeper (operator) identity and flag. No player can modify the vault or trace through application endpoints, but token/flag sharing remains possible.
- Tide-keeper session has no expiry until restart, and sign-out does not globally revoke it. These are deliberate repeatability simplifications.
- At more than 512 active junior liaison logins, the oldest session is removed. This has not been load-tested for a public event.
- A reset interrupts all players. Reset before a demonstration or coordinated test, not during an active solve without notice.
- Local HTTP is for the isolated lab. Shared deployment needs a tested network and transport configuration.
- Container declarations must be verified at runtime before the report claims working container isolation.
- The diagnostic text is synthetic; do not claim a real packet capture, incident or victim session.

## References

- OWASP, Session hijacking attack: https://community.owasp.org/attacks/Session_hijacking_attack
- Flask, Waitress deployment: https://flask.palletsprojects.com/en/stable/deploying/waitress/
- Docker networking overview (frontend plus isolated backend): https://docs.docker.com/engine/network/
- CTFd, Creating challenges: https://docs.ctfd.io/tutorials/challenges/creating-challenges/
- IE3132 Assignment 01 brief supplied in this conversation: stage fields, difficulty progression and isolation requirements.
