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


STYLE = b"""<html><head><title>OCPA Webmail</title><link rel="icon" type="image/png" href="/favicon.png"><style>
body { font-family: 'Consolas', 'DejaVu Sans Mono', monospace; margin: 0; background: #0b0f14; color: #c9d6df; }
.banner { background: #2a1010; color: #ff6b5e; text-align: center; padding: 6px; font-size: 0.75em; letter-spacing: 1px; border-bottom: 1px solid #ff6b5e; }
.shell { max-width: 820px; margin: 30px auto; border: 1px solid #1f2b38; display: flex; background: #10161d; min-height: 420px; }
.sidebar { width: 150px; background: #0d1319; border-right: 1px solid #1f2b38; padding: 14px 0; flex-shrink: 0; }
.sidebar .folder { padding: 8px 16px; font-size: 0.82em; color: #7290a3; }
.sidebar .folder.active { color: #7fd1e0; background: #131b23; border-left: 2px solid #7fd1e0; }
.main { flex: 1; padding: 20px 22px; min-width: 0; }
h1 { color: #7fd1e0; font-size: 1.05em; text-transform: uppercase; border-bottom: 1px solid #1f2b38; padding-bottom: 10px; margin-top: 0; }
input { display: block; margin: 10px 0; padding: 8px; width: 240px; background: #0b0f14; border: 1px solid #2a3b4a; color: #c9d6df; font-family: inherit; }
button { padding: 8px 16px; background: #1f2b38; color: #7fd1e0; border: 1px solid #2a3b4a; cursor: pointer; font-family: inherit; }
.msg { border: 1px solid #1f2b38; margin: 10px 0; background: #131b23; }
.msg .hdr { display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-bottom: 1px solid #1a232c; }
.msg .avatar { width: 24px; height: 24px; border-radius: 2px; background: #1f2b38; color: #7fd1e0; display: flex; align-items: center; justify-content: center; font-size: 0.72em; flex-shrink: 0; }
.msg .from { font-weight: bold; color: #c9d6df; font-size: 0.85em; }
.msg .subj { color: #9db3c2; font-size: 0.85em; }
.msg .date { margin-left: auto; color: #4c5a68; font-size: 0.75em; white-space: nowrap; }
pre { background: #05070a; color: #9adfc2; padding: 10px 12px; margin: 0; overflow-x: auto; }
</style></head><body>"""

def initials(addr):
    name = addr.split("@")[0]
    parts = [p for p in name.replace(".", " ").split(" ") if p]
    return "".join(p[0] for p in parts[:2]).upper() or "?"

FOLDERS = [("Inbox", True), ("Sent", False), ("Drafts", False), ("Trash", False)]

def sidebar_html():
    out = '<div class="sidebar">'
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
