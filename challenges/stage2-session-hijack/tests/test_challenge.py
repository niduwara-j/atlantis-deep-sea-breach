import re
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import BASE, COOKIE, TRAINEE_PASSWORD, create_app

FLAG = "Atlantis{automated_test_flag_only}"


class ChallengeTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(FLAG)
        self.app.testing = True
        self.player = self.app.test_client()

    def login(self, client=None):
        client = client or self.player
        return client.post(BASE + "/login", data={"username": "trainee", "password": TRAINEE_PASSWORD})

    def operator_token(self, client=None):
        client = client or self.player
        self.login(client)
        trace = client.get(BASE + "/support/trace-042.txt").get_data(as_text=True)
        return re.search(COOKIE + r"=([0-9a-f]{64})", trace).group(1)

    def test_full_intended_solution(self):
        self.login()
        self.assertEqual(self.player.get(BASE + "/vault").status_code, 403)
        token = self.operator_token()
        self.player.set_cookie(COOKIE, token, path=BASE)
        vault = self.player.get(BASE + "/vault")
        self.assertEqual(vault.status_code, 200)
        self.assertIn(FLAG, vault.get_data(as_text=True))

    def test_anonymous_cannot_get_trace_or_flag(self):
        for path in ("/support", "/support/trace-042.txt", "/vault"):
            result = self.player.get(BASE + path)
            self.assertEqual(result.status_code, 401)
            self.assertNotIn(FLAG, result.get_data(as_text=True))

    def test_wrong_password_and_sql_injection_do_not_login(self):
        for username, password in (("trainee", "wrong"), ("trainee", "\u00e9\u00e9"), ("' OR 1=1 --", "anything"), ("operator", TRAINEE_PASSWORD)):
            response = self.player.post(BASE + "/login", data={"username": username, "password": password})
            self.assertEqual(response.status_code, 401)
            self.assertNotIn("Set-Cookie", response.headers)

    def test_forged_role_and_token_do_not_unlock_vault(self):
        self.login()
        self.assertEqual(self.player.get(BASE + "/vault?role=operator", headers={"X-Portal-Role": "operator"}).status_code, 403)
        for token in ("operator", "admin", "1", "a" * 64, "\u00e9\u00e9"):
            self.player.set_cookie(COOKIE, token, path=BASE)
            self.assertEqual(self.player.get(BASE + "/vault").status_code, 401)

    def test_cookie_is_unique_httponly_and_scoped(self):
        first = self.login().headers["Set-Cookie"]
        second = self.login().headers["Set-Cookie"]
        self.assertNotEqual(first, second)
        for attribute in ("HttpOnly", "SameSite=Strict", "Path=" + BASE):
            self.assertIn(attribute, first)

    def test_no_flag_in_trainee_pages_or_static_assets(self):
        self.login()
        for path in ("/", BASE + "/login", BASE + "/dashboard", BASE + "/support", BASE + "/support/trace-042.txt", BASE + "/vault", "/static/portal.css", "/healthz"):
            with self.player.get(path) as response:
                self.assertNotIn(FLAG, response.get_data(as_text=True))

    def test_source_and_private_files_are_not_served(self):
        for path in ("/.env", "/app.py", "/private/ctfd-flag.txt", "/static/../app.py", "/static/../.env"):
            self.assertEqual(self.player.get(path).status_code, 404)

    def test_reset_invalidates_old_operator_token(self):
        token = self.operator_token()
        reset_app = create_app(FLAG)
        after_reset = reset_app.test_client()
        after_reset.set_cookie(COOKIE, token, path=BASE)
        self.assertEqual(after_reset.get(BASE + "/vault").status_code, 401)
        new_token = self.operator_token(after_reset)
        self.assertNotEqual(token, new_token)
        after_reset.set_cookie(COOKIE, new_token, path=BASE)
        self.assertIn(FLAG, after_reset.get(BASE + "/vault").get_data(as_text=True))

    def test_two_players_do_not_invalidate_each_other(self):
        second = self.app.test_client()
        token = self.operator_token()
        self.login(second)
        self.assertEqual(second.get(BASE + "/vault").status_code, 403)
        self.player.set_cookie(COOKIE, token, path=BASE)
        self.player.post(BASE + "/logout")
        second.set_cookie(COOKIE, token, path=BASE)
        self.assertEqual(second.get(BASE + "/vault").status_code, 200)

    def test_trainee_logout_invalidates_session(self):
        self.login()
        token = self.player.get_cookie(COOKIE, path=BASE).value
        self.player.post(BASE + "/logout")
        self.player.set_cookie(COOKIE, token, path=BASE)
        self.assertEqual(self.player.get(BASE + "/support").status_code, 401)

    def test_sensitive_pages_are_not_cached(self):
        self.login()
        response = self.player.get(BASE + "/support/trace-042.txt")
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

    def test_large_request_rejected(self):
        self.assertEqual(self.player.post(BASE + "/login", data={"username": "x" * 9000}).status_code, 413)

    def test_external_resources_not_required(self):
        self.login()
        for path in ("/login", "/dashboard", "/support"):
            html = self.player.get(BASE + path).get_data(as_text=True)
            self.assertNotRegex(html, r'(?:src|href)="https?://')


if __name__ == "__main__":
    unittest.main(verbosity=2)
