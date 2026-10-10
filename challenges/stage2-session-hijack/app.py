"""Atlantis Stage 2 — Surface-Liaison Portal. Deliberately vulnerable, isolated training application."""
import logging
import os
import secrets
import threading
from collections import OrderedDict
from datetime import datetime, timezone

from flask import Flask, Response, abort, g, redirect, render_template, request, url_for

BASE = "/session-hijack"
COOKIE = "nh_portal_session"
TRAINEE_PASSWORD = "HorizonTrainee042!"


def create_app(flag=None):
    app = Flask(__name__)
    app.config.update(MAX_CONTENT_LENGTH=8192, DEBUG=False)
    challenge_flag = flag or os.environ.get("CHALLENGE_FLAG")
    if not challenge_flag or not challenge_flag.startswith("Atlantis{") or not challenge_flag.endswith("}"):
        raise RuntimeError("Set CHALLENGE_FLAG to the flag registered in CTFd.")

    # In-memory lab state: one simulated operator and independent trainee sessions.
    # The operator never runs a browser and has no password-login endpoint.
    operator_token = secrets.token_hex(32)
    trainee_sessions = OrderedDict()
    lock = threading.Lock()
    boot_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def identity():
        token = request.cookies.get(COOKIE, "")
        if secrets.compare_digest(token.encode("utf-8"), operator_token.encode("ascii")):
            return {"name": "Morgan Vale", "role": "operator", "display_role": "Tide-Keeper"}
        with lock:
            if token in trainee_sessions:
                return {"name": "Liaison Analyst", "role": "trainee", "display_role": "Junior Liaison"}
        return None

    def require_user():
        if not g.identity:
            abort(401)

    @app.before_request
    def load_identity():
        g.identity = identity()

    @app.after_request
    def headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; style-src 'self'; img-src 'self'; "
            "form-action 'self'; frame-ancestors 'none'; base-uri 'none'"
        )
        # Never write cookies, credentials, the trace body, or the flag to server logs.
        app.logger.info("%s %s %s", request.method, request.path, response.status_code)
        return response

    @app.get("/")
    def root():
        return redirect(BASE + "/")

    @app.get("/healthz")
    def health():
        return {"status": "ok", "challenge": "session-hijack"}

    @app.get(BASE + "/")
    def home():
        return redirect(url_for("dashboard") if g.identity else url_for("login"))

    @app.route(BASE + "/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            if request.form.get("username") == "trainee" and secrets.compare_digest(
                request.form.get("password", "").encode("utf-8"), TRAINEE_PASSWORD.encode("ascii")
            ):
                token = secrets.token_hex(32)
                with lock:
                    trainee_sessions[token] = True
                    # Bound memory use. Oldest trainee must log in again if capacity is reached.
                    if len(trainee_sessions) > 512:
                        trainee_sessions.popitem(last=False)
                response = redirect(url_for("dashboard"))
                response.set_cookie(COOKIE, token, httponly=True, samesite="Strict", path=BASE)
                return response
            error = "Sign-in failed. Check your assigned liaison credentials."
        return render_template("login.html", error=error), 401 if error else 200

    @app.get(BASE + "/dashboard")
    def dashboard():
        if not g.identity:
            return redirect(url_for("login"))
        return render_template("dashboard.html")

    @app.get(BASE + "/support")
    def support():
        require_user()
        return render_template("support.html")

    @app.get(BASE + "/support/trace-042.txt")
    def trace():
        require_user()
        # INTENTIONAL FLAW: trainee-accessible diagnostics expose a live operator bearer token.
        # This trace is synthetic and generated locally; it contains no real captured traffic.
        body = (
            "ATLANTIS SURFACE-LIAISON / REQUEST DIAGNOSTICS\n"
            "Ticket: ATL-042 | Service: surface-portal | Capture: outpost-02 telemetry\n"
            f"Captured at: {boot_time}\n"
            "Redaction policy: Authorization, X-API-Key\n\n"
            "--- REQUEST 01 ---\nGET /session-hijack/dashboard HTTP/1.1\n"
            "Host: surface-liaison.atlantis.internal\nUser-Agent: Atlantis-TideOperations/2.4\n"
            "Authorization: [REDACTED]\n"
            f"Cookie: {COOKIE}={operator_token}\n"
            "X-Request-ID: atl-042-tidekeeper-check\n\n"
            "--- RESPONSE 01 ---\nHTTP/1.1 200 OK\n"
            "X-Portal-Role: tide-keeper\nCache-Control: no-store\n\n"
            "--- REQUEST 02 ---\nGET /healthz HTTP/1.1\n"
            "Host: surface-liaison.atlantis.internal\nX-Request-ID: atl-042-sonar-ping\n\n"
            "--- RESPONSE 02 ---\nHTTP/1.1 200 OK\n\n"
            "End of diagnostic attachment.\n"
        )
        return Response(body, mimetype="text/plain", headers={"Content-Disposition": 'inline; filename="trace-042.txt"'})

    @app.get(BASE + "/vault")
    def vault():
        require_user()
        if g.identity["role"] != "operator":
            return render_template("restricted.html"), 403
        return render_template("vault.html", flag=challenge_flag)

    @app.post(BASE + "/logout")
    def logout():
        with lock:
            trainee_sessions.pop(request.cookies.get(COOKIE, ""), None)
        # Clear this browser only. Preserve the simulated operator so one player cannot
        # invalidate the shared challenge for other participants by clicking Sign out.
        response = redirect(url_for("login"))
        response.delete_cookie(COOKIE, path=BASE, httponly=True, samesite="Strict")
        return response

    @app.errorhandler(401)
    def unauthenticated(_):
        return render_template("error.html", title="Sign-in required", message="Use your assigned liaison account to access this outpost resource."), 401

    @app.errorhandler(404)
    def missing(_):
        return render_template("error.html", title="Resource not found", message="Return to the surface-liaison portal to continue your investigation."), 404

    return app


if __name__ == "__main__":
    from waitress import serve
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    serve(create_app(), host=os.environ.get("BIND_HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "8092")), threads=4)
