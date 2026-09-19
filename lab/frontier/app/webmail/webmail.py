#!/usr/bin/env python3
"""ROSTER Webmail — OCPA Region 4 internal correspondence gateway."""
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

USERS = {
    "duty.admin": "MailP@ss2024",
    "sysadmin": "admin123",
    "devuser": "devuser2024",
}

EMAILS = [
    {"from": "facilities@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-18 14:02",
     "subject": "Water shutoff - Building 4, Tuesday 0600-0900",
     "body": ("Maintenance is replacing a valve on the third floor. Water will be\n"
              "unavailable in Building 4 (this includes the break room and both\n"
              "restrooms on our floor) from 0600 to approximately 0900 local.\n"
              "Building 2 facilities are unaffected if you need to relocate.")},
    {"from": "t.reyes@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-16 09:47",
     "subject": "re: printer on 2nd floor again",
     "body": ("Yeah I know. It's out of the darker toner cartridge, not the standard\n"
              "one, so it's going to be a few days - vendor doesn't stock it locally.\n"
              "Use the one by the break room until then. Sorry.")},
    {"from": "records@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-10 08:15",
     "subject": "New Case Handler Onboarding",
     "body": ("Please provision terminal access for new case handlers.\n"
              "Default temp password: Roster2024!\n\n"
              "Also — a reminder to the floor: the Dependent Status Index still shows\n"
              "leftover reference numbers from the old SPINDLE migration. If a closed\n"
              "case cites a transfer reference that doesn't resolve to anything in the\n"
              "current system, that's expected. It's a decommissioned system, not an\n"
              "active investigation. Please stop opening tickets about it.")},
    {"from": "ops@ocpa.unsc.mil", "to": "sysadmin@ocpa.unsc.mil", "date": "2547-02-05 21:33",
     "subject": "LEDGER sandbox refresh",
     "body": ("Sandbox instance on LEDGER migrated over the weekend.\n"
              "Host: relay.internal\nUser: root\nPass: S3cretDB!2024\n"
              "This is the sandbox copy, not the case-index replica. Don't point\n"
              "anything production-facing at it.")},
    {"from": "t.reyes@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-01-28 11:04",
     "subject": "LEDGER Terminal Access (old creds, deprecated?)",
     "body": ("Whoever's on duty — I still see a stale note floating around for a\n"
              "'svc-relay' account on the LEDGER gateway. I don't think that account\n"
              "exists anymore, or it was never provisioned properly. If someone needs\n"
              "in, use your own duty credentials against the gateway SSH, same as\n"
              "always. Don't go hunting for svc-relay / R3lay!Access9, it's not real.\n"
              "Host: relay.internal, port 22.")},
]


STYLE = b"""<html><head><title>OCPA Webmail</title>
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {
  --bg: #0a0d11; --surface: #131920; --surface-2: #1a212a; --surface-hover: #1f2731;
  --border: #232c36; --border-soft: #1a2129; --text: #d7dee4; --text-dim: #8a97a3;
  --text-faint: #55616c; --accent: #5fb3d1; --accent-soft: rgba(95,179,209,0.12);
  --danger: #c96560; --danger-bg: #2a1414;
  --sans: 'IBM Plex Sans', -apple-system, 'Segoe UI', Roboto, sans-serif;
  --mono: 'IBM Plex Mono', 'Consolas', monospace;
}
* { box-sizing: border-box; }
html { background: var(--bg); }
body { font-family: var(--sans); margin: 0; background: var(--bg); color: var(--text); font-size: 14px; }
.banner { background: var(--danger-bg); color: var(--danger); text-align: center; padding: 6px 12px; font-size: 11.5px; letter-spacing: 0.4px; border-bottom: 1px solid #3a1d1d; }
.shell { max-width: 900px; margin: 0 auto; border: 1px solid var(--border); border-top: none; display: flex; background: var(--bg); min-height: calc(100vh - 27px); }
.sidebar { width: 170px; background: var(--surface); border-right: 1px solid var(--border); flex-shrink: 0; }
.brand { display: flex; align-items: center; gap: 9px; padding: 16px 14px; border-bottom: 1px solid var(--border-soft); }
.brand img { width: 26px; opacity: 0.92; }
.brand div { font-weight: 600; font-size: 12.5px; }
.folder { padding: 9px 16px; font-size: 13px; color: var(--text-dim); border-left: 2px solid transparent; }
.folder.active { color: var(--accent); background: var(--accent-soft); border-left-color: var(--accent); font-weight: 500; }
.main { flex: 1; padding: 22px 26px; min-width: 0; }
h1 { font-size: 16px; font-weight: 600; color: var(--text); border-bottom: 1px solid var(--border); padding-bottom: 12px; margin: 0 0 16px; }
input { display: block; margin: 10px 0; padding: 8px 10px; width: 260px; background: var(--bg); border: 1px solid var(--border); border-radius: 3px; color: var(--text); font-family: var(--sans); font-size: 13px; }
button { padding: 8px 16px; background: var(--surface-2); color: var(--text); border: 1px solid var(--border); border-radius: 3px; cursor: pointer; font-family: var(--sans); font-size: 13px; }
button:hover { border-color: var(--accent); color: var(--accent); }
.msg { border: 1px solid var(--border); border-radius: 4px; margin: 0 0 10px; background: var(--surface); }
.msg .hdr { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-bottom: 1px solid var(--border-soft); }
.msg .avatar { width: 26px; height: 26px; border-radius: 3px; background: var(--surface-2); color: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; flex-shrink: 0; }
.msg .from { font-weight: 600; color: var(--text); font-size: 13px; }
.msg .subj { color: var(--text-dim); font-size: 13px; }
.msg .date { margin-left: auto; color: var(--text-faint); font-family: var(--mono); font-size: 11.5px; white-space: nowrap; }
pre { font-family: var(--mono); font-size: 12.5px; background: #05070a; color: #9ad0c9; padding: 12px 14px; margin: 0; overflow-x: auto; line-height: 1.6; border-radius: 0 0 4px 4px; }
</style></head><body>"""

def initials(addr):
    name = addr.split("@")[0]
    parts = [p for p in name.replace(".", " ").split(" ") if p]
    return "".join(p[0] for p in parts[:2]).upper() or "?"

FOLDERS = [("Inbox", True), ("Sent", False), ("Drafts", False), ("Trash", False)]

def sidebar_html():
    out = '<div class="sidebar"><div class="brand"><img src="/favicon.png"><div>OCPA Mail</div></div>'
    for name, active in FOLDERS:
        cls = "folder active" if active else "folder"
        out += f'<div class="{cls}">{name}</div>'
    out += "</div>"
    return out


class WebmailHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/login":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = STYLE.decode() + (
                '<div class="banner">OCPA REGION 4 INTERNAL MAIL -- DO NOT FORWARD OFF NETWORK</div>'
                '<div class="shell">' + sidebar_html() +
                '<div class="main">'
                '<h1>OCPA Region 4 :: Webmail</h1>'
                '<form method="POST" action="/login">'
                '<input name="user" placeholder="Username"><br>'
                '<input name="pass" type="password" placeholder="Password"><br>'
                '<button type="submit">Login</button>'
                '</form></div></div>'
            )
            self.wfile.write(html.encode())
        elif parsed.path == "/inbox":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = STYLE.decode() + (
                '<div class="banner">OCPA REGION 4 INTERNAL MAIL -- DO NOT FORWARD OFF NETWORK</div>'
                '<div class="shell">' + sidebar_html() + '<div class="main"><h1>Inbox</h1>'
            )
            for email in EMAILS:
                html += '<div class="msg"><div class="hdr">'
                html += f'<div class="avatar">{initials(email["from"])}</div>'
                html += f'<span class="from">{email["from"]}</span>'
                html += f'<span class="subj">{email["subject"]}</span>'
                html += f'<span class="date">{email.get("date", "")}</span>'
                html += '</div>'
                html += f"<pre>{email['body']}</pre></div>"
            html += "</div></div>"
            self.wfile.write(html.encode())
        elif parsed.path == "/favicon.png":
            try:
                with open("/var/www/html/portal/assets/ocpa_seal.png", "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                self.wfile.write(data)
            except OSError:
                self.send_response(404)
                self.end_headers()
        elif parsed.path == "/debug":
            # Information disclosure: environment variables
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            env_dump = "\n".join(f"{k}={v}" for k, v in os.environ.items())
            self.wfile.write(env_dump.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        if self.path == "/login":
            user = params.get("user", [""])[0]
            pw = params.get("pass", [""])[0]
            # Vulnerable: no rate limiting, no account lockout
            if user in USERS and USERS[user] == pw:
                self.send_response(302)
                self.send_header("Location", "/inbox")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<html><body><p>Invalid credentials for user: {user}</p><a href='/'>Back</a></body></html>".encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8025), WebmailHandler)
    print("ROSTER webmail running on port 8025")
    server.serve_forever()
