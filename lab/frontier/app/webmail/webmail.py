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
    {"from": "hr@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-19 08:03",
     "subject": "Mandatory Annual Compliance Training - Due End of Month",
     "body": ("This is your second reminder. Records show 41% completion for Region 4.\n"
              "The module takes approximately 25 minutes. Access it through the HR\n"
              "portal, not through ROSTER - several people have submitted tickets\n"
              "about this and ROSTER was never going to have it.\n\n"
              "Supervisors: please follow up with staff who have not completed this.")},
    {"from": "facilities@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-18 14:02",
     "subject": "Water shutoff - Building 4, Tuesday 0600-0900",
     "body": ("Maintenance is replacing a valve on the third floor. Water will be\n"
              "unavailable in Building 4 (this includes the break room and both\n"
              "restrooms on our floor) from 0600 to approximately 0900 local.\n"
              "Building 2 facilities are unaffected if you need to relocate.")},
    {"from": "facilities@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-17 16:40",
     "subject": "Elevator B Out of Service",
     "body": ("Elevator B is out of service pending a part that's on backorder.\n"
              "Estimated return to service is unknown. Please use Elevator A or\n"
              "the stairwell by the east entrance. We are aware this is the third\n"
              "time this year.")},
    {"from": "t.reyes@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-16 09:47",
     "subject": "re: printer on 2nd floor again",
     "body": ("Yeah I know. It's out of the darker toner cartridge, not the standard\n"
              "one, so it's going to be a few days - vendor doesn't stock it locally.\n"
              "Use the one by the break room until then. Sorry.")},
    {"from": "d.okonkwo@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-13 10:12",
     "subject": "re: re: re: Thursday lunch order",
     "body": ("Put me down for the same as last time. If they're out of it again\n"
              "just get me whatever, I'm not picky. Are we still doing this at\n"
              "noon or did that move because of the compliance training thing.")},
    {"from": "records@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-10 08:15",
     "subject": "New Case Handler Onboarding",
     "body": ("Please provision terminal access for new case handlers.\n"
              "Default temp password: Roster2024!\n\n"
              "Also — a reminder to the floor: the Dependent Status Index still shows\n"
              "leftover reference numbers from the old SPINDLE migration. If a closed\n"
              "case cites a transfer reference that doesn't resolve to anything in the\n"
              "current system, that's expected. It's a decommissioned system, not an\n"
              "active investigation. Please stop opening tickets about it.")},
    {"from": "systems@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-08 07:55",
     "subject": "Scheduled patch window - terminal reboot required overnight",
     "body": ("ROSTER and Webmail will restart automatically between 0100-0200\n"
              "tonight for routine security patches. Save your work before end\n"
              "of day. No action needed if you're not logged in overnight.")},
    {"from": "ops@ocpa.unsc.mil", "to": "sysadmin@ocpa.unsc.mil", "date": "2547-02-05 21:33",
     "subject": "LEDGER sandbox refresh",
     "body": ("Sandbox instance on LEDGER migrated over the weekend.\n"
              "Host: relay.internal\nUser: root\nPass: S3cretDB!2024\n"
              "This is the sandbox copy, not the case-index replica. Don't point\n"
              "anything production-facing at it.")},
    {"from": "ops@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-03 13:20",
     "subject": "Office supply requisition - toner and staples backordered",
     "body": ("Standard-cartridge toner and box staples are backordered through\n"
              "at least the 20th. Ration what's left at the supply closet. Do not\n"
              "submit duplicate requisition requests, it doesn't make the vendor\n"
              "ship faster.")},
    {"from": "security@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-01-30 09:00",
     "subject": "Building 4 badge access - temporary contractor suspension",
     "body": ("Contractor badge access to Building 4 is suspended pending the\n"
              "annual access review. This does not affect regular staff badges.\n"
              "Contractors needing floor access should be escorted and signed in\n"
              "at the front desk in the interim.")},
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root {
  --bg: #050a12; --surface: #0b1826; --surface-2: #112337; --surface-hover: #162c44;
  --border: #244a63; --border-soft: #1a3348; --text: #7ec4e8; --text-dim: #4f89ac;
  --text-faint: #2f5870; --accent: #bfe6f7; --accent-soft: rgba(191,230,247,0.08);
  --danger: #d4685c; --danger-bg: #2a1310;
  --mono: 'IBM Plex Mono', 'Consolas', monospace;
}
* { box-sizing: border-box; }
html { background: var(--bg); }
body {
  font-family: var(--mono); margin: 0; color: var(--text); font-size: 15.5px;
  background-color: var(--bg);
  background-image:
    repeating-linear-gradient(180deg, rgba(191,230,247,0.022) 0px, rgba(191,230,247,0.022) 1px, transparent 1px, transparent 3px),
    radial-gradient(ellipse at 50% 40%, rgba(191,230,247,0.045) 0%, rgba(0,0,0,0) 55%),
    radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,0.45) 100%);
  background-attachment: fixed;
}
.banner { background: var(--danger-bg); color: var(--danger); text-align: center; padding: 7px 12px; font-size: 12px; letter-spacing: 0.6px; text-transform: uppercase; border-bottom: 1px solid #3a1d1d; }
.shell { max-width: 960px; margin: 0 auto; border: 1px solid var(--border); border-top: none; display: flex; background: var(--bg); min-height: calc(100vh - 30px); }
.sidebar { width: 190px; background: var(--surface); border-right: 1px solid var(--border); flex-shrink: 0; }
.brand { display: flex; align-items: center; gap: 11px; padding: 18px 14px; border-bottom: 1px solid var(--border-soft); }
.brand img { width: 44px; opacity: 0.95; }
.brand div { font-weight: 600; font-size: 13.5px; }
.folder { padding: 10px 16px; font-size: 14px; color: var(--text-dim); border-left: 3px solid transparent; }
.folder.active { color: #051622; background: var(--text); border-left-color: var(--accent); font-weight: 600; }
.main { flex: 1; padding: 24px 26px; min-width: 0; }
h1 { font-size: 17px; font-weight: 600; color: var(--text); border-bottom: 1px solid var(--border); padding-bottom: 12px; margin: 0 0 16px; text-shadow: 0 0 6px rgba(126,196,232,0.35); }
input { display: block; margin: 10px 0; padding: 9px 10px; width: 260px; background: var(--bg); border: 1px solid var(--border); border-radius: 0; color: var(--text); font-family: var(--mono); font-size: 14px; }
button { padding: 9px 18px; background: var(--surface-2); color: var(--text); border: 1px solid var(--border); border-radius: 0; cursor: pointer; font-family: var(--mono); font-size: 13.5px; letter-spacing: 0.4px; text-transform: uppercase; }
button:hover { border-color: var(--text); background: var(--text); color: #051622; }
.msg { border: 1px solid var(--border); border-radius: 0; margin: 0 0 10px; background: var(--surface); }
.msg .hdr { display: flex; align-items: center; gap: 11px; padding: 11px 14px; border-bottom: 1px solid var(--border-soft); }
.msg .avatar { width: 34px; height: 34px; border-radius: 0; background: var(--surface-2); color: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; flex-shrink: 0; border: 1px solid var(--border); }
.msg .from { font-weight: 600; color: var(--text); font-size: 14px; }
.msg .subj { color: var(--text-dim); font-size: 14px; }
.msg .date { margin-left: auto; color: var(--text-faint); font-size: 12px; white-space: nowrap; }
pre { font-family: var(--mono); font-size: 13.5px; background: #030810; color: #8ed0ef; padding: 13px 14px; margin: 0; overflow-x: auto; line-height: 1.6; border-radius: 0; }
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
