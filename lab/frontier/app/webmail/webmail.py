#!/usr/bin/env python3
"""ROSTER Webmail — OCPA Region 4 internal correspondence gateway."""
import secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from content import EMAILS, UI

USERS = {
    "sysadmin": "admin123",
    "devuser": "devuser2024",
}

# In-memory session store, same pattern as the CAIRN Records Terminal on
# archive. /inbox only renders once /login has actually accepted a
# password - reading it isn't a separate, unauthenticated path.
VALID_SESSIONS = set()


def has_valid_session(handler):
    cookie_header = handler.headers.get("Cookie", "")
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith("roster_session="):
            return part[len("roster_session="):] in VALID_SESSIONS
    return False


STYLE = b"""<html><head><title>OCPA Webmail</title>
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root {
  --bg: #000000; --surface: #060d14; --surface-2: #0a1622; --surface-hover: #0d1c2a;
  --border: #1a3244; --border-soft: #101f2a; --text: #7ec4e8; --text-dim: #4f89ac;
  --text-faint: #2f5870; --accent: #bfe6f7; --accent-soft: rgba(191,230,247,0.06);
  --danger: #d4685c; --danger-bg: #200d0b;
  --mono: 'IBM Plex Mono', 'Consolas', monospace;
}
* { box-sizing: border-box; }
html { background: var(--bg); }
body {
  font-family: var(--mono); margin: 0; color: var(--text); font-size: 15.5px;
  background-color: var(--bg);
  background-image:
    repeating-linear-gradient(180deg, rgba(191,230,247,0.016) 0px, rgba(191,230,247,0.016) 1px, transparent 1px, transparent 3px),
    radial-gradient(ellipse at 50% 40%, rgba(191,230,247,0.02) 0%, rgba(0,0,0,0) 55%),
    radial-gradient(ellipse at 50% 50%, transparent 45%, rgba(0,0,0,0.6) 100%);
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
</style></head><body>""".replace(b"OCPA Webmail", UI["page_title"].encode())

def initials(addr):
    name = addr.split("@")[0]
    parts = [p for p in name.replace(".", " ").split(" ") if p]
    return "".join(p[0] for p in parts[:2]).upper() or "?"

FOLDERS = [(UI["folder_inbox"], True), (UI["folder_sent"], False), (UI["folder_drafts"], False), (UI["folder_trash"], False)]

def sidebar_html():
    out = f'<div class="sidebar"><div class="brand"><img src="/favicon.png"><div>{UI["brand"]}</div></div>'
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
                f'<div class="banner">{UI["banner"]}</div>'
                '<div class="shell">' + sidebar_html() +
                '<div class="main">'
                f'<h1>{UI["login_title"]}</h1>'
                '<form method="POST" action="/login">'
                f'<input name="user" placeholder="{UI["placeholder_user"]}"><br>'
                f'<input name="pass" type="password" placeholder="{UI["placeholder_pass"]}"><br>'
                f'<button type="submit">{UI["login_button"]}</button>'
                '</form></div></div>'
            )
            self.wfile.write(html.encode())
        elif parsed.path == "/inbox":
            if not has_valid_session(self):
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = STYLE.decode() + (
                f'<div class="banner">{UI["banner"]}</div>'
                '<div class="shell">' + sidebar_html() + f'<div class="main"><h1>{UI["inbox_title"]}</h1>'
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
                token = secrets.token_hex(16)
                VALID_SESSIONS.add(token)
                self.send_response(302)
                self.send_header("Location", "/inbox")
                self.send_header("Set-Cookie", f"roster_session={token}; Path=/")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<html><body><p>{UI['invalid_creds']} {user}</p><a href='/'>{UI['back_link']}</a></body></html>".encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8025), WebmailHandler)
    print("ROSTER webmail running on port 8025")
    server.serve_forever()
