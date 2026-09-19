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
    {"from": "t.reyes@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil",
     "subject": "LEDGER Terminal Access (old creds, deprecated?)",
     "body": ("Whoever's on duty — I still see a stale note floating around for a\n"
              "'svc-relay' account on the LEDGER gateway. I don't think that account\n"
              "exists anymore, or it was never provisioned properly. If someone needs\n"
              "in, use your own duty credentials against the gateway SSH, same as\n"
              "always. Don't go hunting for svc-relay / R3lay!Access9, it's not real.\n"
              "Host: relay.internal, port 22.")},
    {"from": "ops@ocpa.unsc.mil", "to": "sysadmin@ocpa.unsc.mil",
     "subject": "LEDGER sandbox refresh",
     "body": ("Sandbox instance on LEDGER migrated over the weekend.\n"
              "Host: relay.internal\nUser: root\nPass: S3cretDB!2024\n"
              "This is the sandbox copy, not the case-index replica. Don't point\n"
              "anything production-facing at it.")},
    {"from": "records@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil",
     "subject": "New Case Handler Onboarding",
     "body": ("Please provision terminal access for new case handlers.\n"
              "Default temp password: Roster2024!\n\n"
              "Also — a reminder to the floor: the Dependent Status Index still shows\n"
              "leftover reference numbers from the old SPINDLE migration. If a closed\n"
              "case cites a transfer reference that doesn't resolve to anything in the\n"
              "current system, that's expected. It's a decommissioned system, not an\n"
              "active investigation. Please stop opening tickets about it.")},
]


class WebmailHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/login":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""<html><head><title>ROSTER Webmail</title></head><body>
            <h1>OCPA Region 4 - Webmail</h1>
            <form method="POST" action="/login">
            <input name="user" placeholder="Username"><br>
            <input name="pass" type="password" placeholder="Password"><br>
            <button type="submit">Login</button>
            </form></body></html>""")
        elif parsed.path == "/inbox":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = "<html><head><title>Inbox</title></head><body><h1>Inbox</h1>"
            for email in EMAILS:
                html += "<div style='border:1px solid #ccc;padding:10px;margin:5px'>"
                html += f"<b>From:</b> {email['from']}<br>"
                html += f"<b>Subject:</b> {email['subject']}<br>"
                html += f"<pre>{email['body']}</pre></div>"
            html += "</body></html>"
            self.wfile.write(html.encode())
        elif parsed.path == "/debug":
            # Information disclosure: environment variables
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
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
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(f"<html><body><p>Invalid credentials for user: {user}</p><a href='/'>Back</a></body></html>".encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8025), WebmailHandler)
    print("ROSTER webmail running on port 8025")
    server.serve_forever()
