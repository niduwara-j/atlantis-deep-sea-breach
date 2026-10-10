# Null Horizon CTF — Session Hijack

Complete source package for Stage 2, Web Security, Easy, 100 points.

Players use a supplied junior liaison login, find a live simulated tide-keeper session token in a diagnostic attachment from the Atlantis surface-liaison portal, replace their challenge cookie, and access a protected verification flag in the tide-keeper vault. This is token disclosure and replay, not SQL injection or merely editing a role field. All people, credentials and traces are fictional.

## Start on Windows with Docker Desktop

1. Keep this whole folder together. Start Docker Desktop with Linux containers.
2. Open PowerShell in this folder.
3. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\start.ps1`.
   The execution-policy option applies to that process only.
4. Check `docker compose ps`: wait for `healthy`.
5. Open **http://127.0.0.1:8092/session-hijack/**.

The first build downloads Python dependencies and an Nginx image. The Dockerfiles require no Debian apt downloads. A non-root Nginx gateway publishes only local port 8092 and forwards to the isolated web container. The Compose project is separate from CTFd. Do not run these commands from the CTFd platform folder.

`setup.ps1` generates a random permanent challenge flag once, stores it in `.env`, and writes the same flag to `private/ctfd-flag.txt`. Re-running setup preserves that flag. Do not share `.env`, private files, or this source package with competitors. Only the running application is player-facing.

## Add to CTFd

Open the existing **Session Hijack** challenge. Keep it Standard / Static, Web Security, 100 points, position 2, unlimited attempts, Require Any Flag. Use the player description in `ctfd-description.md`.

- Connection Info for same-laptop testing: `http://127.0.0.1:8092/session-hijack/`.
- Flags: add exactly one Static, case-sensitive flag copied from `private/ctfd-flag.txt`. Do not paste the flag into the public description.
- Files: none; players use the website.
- Requirements: none for independent testing.
- Hints: see `private/stage-specification.md`.
- State: Hidden until your normal-player CTFd submission test passes, then Visible for the lab.

CTFd validation is separate from app authentication. A correct tide-keeper vault flag must be manually registered in CTFd. The portal never needs CTFd's admin credentials, database, secret key or API token.

For another laptop, `localhost` refers to that other laptop. The local URL is NOT a teammate-access URL. Before LAN deployment, explicitly configure the dedicated lab interface, firewall, and target URL. Cookies are not isolated by port; this app uses the unique name `nh_portal_session` and path `/session-hijack`, and does not use the CTFd cookie. Separate hostnames are preferable for a later shared lab.

## Reset, stop and restart

- Reset sessions: `powershell -NoProfile -ExecutionPolicy Bypass -File .\reset.ps1`.
- Stop: `docker compose stop`.
- Start existing build: `docker compose up -d`.
- Logs: `docker compose logs --tail 80 web`.
- Status: `docker compose ps`.

Sessions exist only in memory. Restart generates a new tide-keeper token and clears junior liaison sessions; players must log in and obtain a new trace. The flag in `.env` is unchanged. CTFd points and submissions are not reset by restarting this app.

The tide-keeper is a simulated identity, not a real browser or bot. Its token remains valid for the process lifetime. Tide-keeper sign-out clears only the current browser, so one participant cannot invalidate everybody else's target session. This is an explicit training simplification, not production session management.

## Tests

With the dependencies installed in a Python environment:

```
python -m unittest discover -s tests -v
python verify.py
```

The unit suite checks intended replay, denied access, absence of flag leakage, wrong login, forged identities, independent players, and reset. `verify.py` checks the live local HTTP service on port 8092 and does not print flags or tokens. It does not submit anything to CTFd.

## Native fallback for a local demonstration

Docker is the intended delivery method. If Docker is unavailable, install `requirements.txt` in a Python virtual environment, run setup, set `CHALLENGE_FLAG` from `.env` in that terminal, and run `python app.py`. Waitress binds to loopback by default. This starts the same application but does NOT provide container isolation. Do not describe native testing as Docker isolation testing.

## Resources and boundaries

Proposed web-container limits: 256 MB memory, 0.5 CPU, 64 processes; gateway: 64 MB, 0.25 CPU, 32 processes. Actual suitability needs runtime measurement. Both containers are non-root, read-only, drop Linux capabilities and forbid privilege escalation. The vulnerable web container uses only an internal network with no CTFd attachment or published port. The gateway connects that internal network to a separate frontend bridge and publishes port 8092 on host loopback. Only the gateway has a non-internal network; the claim of no direct external access applies to the web container, not the gateway. The gateway forwards only to the fixed web backend and is not a general forward proxy. Run verify-container.ps1 for runtime checks. Neither service has a persistent database, host filesystem mounts, Docker socket, external fonts, remote scripts or attacker callback server.

The intentionally exposed operator token is the only designed access-control failure. There is no uploaded code execution, command execution, public registration, or real victim involved. Store application source and `.env` privately. Back up this folder and `.env` after validation.

See `private/stage-specification.md`, `private/solution.md`, `private/TEST-RESULTS.md`, and `private/AI-PROMPT-LOG.md` for report and viva material.
