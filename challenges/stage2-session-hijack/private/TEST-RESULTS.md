# Session Hijack — verification record

## Checks executed by the assistant

Environment: Windows, bundled Python 3.12 virtual environment; Flask 3.1.3; Waitress 3.0.2.

- 13 automated application tests passed: intended session replay, anonymous denial, junior liaison denial, invalid login, forged identity denial, cookie properties, flag non-disclosure, private-file protection, reset invalidation, independent players, logout, request-size bound, response headers and absence of remote page resources.
- 9 live HTTP checks passed against Waitress on loopback port 8092: health, anonymous denial, wrong password, junior liaison login, junior liaison vault denial, deliberate trace disclosure, tide-keeper replay, matching private flag, and private-file non-disclosure.
- Browser review: login page renders; junior liaison login reaches dashboard; tide-keeper vault is denied; support page renders with the intended attachment link. Desktop layout inspected visually.
- Docker Compose configuration parses successfully with `docker compose config --quiet`.

## Outstanding runtime checks

- Original web image build/start: confirmed by the user's Docker output. The initial internal-only network did not publish the requested host port; browser access failed. This was a deployment configuration defect, not a passed runtime check.
- Corrected deployment adds a non-root Nginx gateway on a frontend bridge and the internal backend network. Web remains internal-only. On 18 September 2026 the user's screenshot confirmed browser access after deployment, and the assistant reran verify.py against the published port: all 9 live HTTP checks passed, including replay and matching the CTFd handoff flag. Docker configuration/isolation inspection remains pending because assistant access to its control pipe is restricted.
- Actual container isolation/resource limits: not yet verified. Run `verify-container.ps1` after startup.
- CTFd configuration and normal-player flag submission: not yet performed for this challenge. Existing CTFd on port 8000 refused connection during this implementation session.
- Full browser cookie-edit walkthrough and responsive narrow-screen inspection: not yet recorded. HTTP replay was verified programmatically.
- Load testing and remote teammate access: not performed.

The temporary native test service was stopped before handing port 8092 to Docker. Native application checks are not evidence that the Docker deployment has passed. Update this record only after obtaining actual results.
